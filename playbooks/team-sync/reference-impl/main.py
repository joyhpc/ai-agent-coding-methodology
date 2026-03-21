import hashlib
import hmac
import os
import re
import time
from collections import deque
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse


load_dotenv()

app = FastAPI(title="LingoTeen Telegram Sync Bot")

TELEGRAM_API_BASE = "https://api.telegram.org"
MARKDOWN_V2_SPECIALS = r"_*[]()~`>#+-=|{}.!"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


BOT_TOKEN = require_env("BOT_TOKEN")
CHAT_ID = require_env("CHAT_ID")
TOPIC_IDS = {
    "backlog": int(require_env("TOPIC_BACKLOG")),
    "doing": int(require_env("TOPIC_DOING")),
    "blockers": int(require_env("TOPIC_BLOCKERS")),
    "pr_review": int(require_env("TOPIC_PR_REVIEW")),
    "decisions": int(require_env("TOPIC_DECISIONS")),
}
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
ALLOWED_REPOS = set(filter(None, os.getenv("ALLOWED_REPOS", "joyhpc/lingoteen-ai").split(",")))

# In-memory message log for CLI polling (last 100, lost on restart — intentional)
MESSAGE_LOG: deque[dict[str, Any]] = deque(maxlen=100)
TOPIC_NAMES = {v: k for k, v in TOPIC_IDS.items()}


def escape_markdown_v2(text: str) -> str:
    return re.sub(f"([{re.escape(MARKDOWN_V2_SPECIALS)}])", r"\\\1", text)


def issue_has_label(issue: dict[str, Any], label_name: str) -> bool:
    labels = issue.get("labels", [])
    return any(label.get("name") == label_name for label in labels if isinstance(label, dict))


def verify_github_signature(raw_body: bytes, signature_header: str | None) -> None:
    if not GITHUB_WEBHOOK_SECRET:
        return

    if not signature_header:
        raise HTTPException(status_code=401, detail="Missing GitHub signature header")

    expected = "sha256=" + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature_header):
        raise HTTPException(status_code=401, detail="Invalid GitHub signature")


def build_issue_opened_message(payload: dict[str, Any]) -> str:
    issue = payload["issue"]
    repo = payload["repository"]["full_name"]
    return (
        f"*New issue opened*\n"
        f"Repo: `{escape_markdown_v2(repo)}`\n"
        f"Issue: `\\#{issue['number']}` {escape_markdown_v2(issue['title'])}\n"
        f"URL: {escape_markdown_v2(issue['html_url'])}\n"
        f"By: `{escape_markdown_v2(issue['user']['login'])}`"
    )


def build_blocker_comment_message(payload: dict[str, Any]) -> str:
    issue = payload["issue"]
    comment = payload["comment"]
    repo = payload["repository"]["full_name"]
    snippet = comment["body"].strip() or "(empty comment)"
    if len(snippet) > 300:
        snippet = snippet[:297] + "..."
    return (
        f"*Blocked issue updated*\n"
        f"Repo: `{escape_markdown_v2(repo)}`\n"
        f"Issue: `\\#{issue['number']}` {escape_markdown_v2(issue['title'])}\n"
        f"URL: {escape_markdown_v2(issue['html_url'])}\n"
        f"Comment by `{escape_markdown_v2(comment['user']['login'])}`:\n"
        f"{escape_markdown_v2(snippet)}"
    )


def build_pr_message(payload: dict[str, Any]) -> str:
    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]
    action = payload["action"]
    label = "PR opened" if action == "opened" else "PR ready for review"
    return (
        f"*{label}*\n"
        f"Repo: `{escape_markdown_v2(repo)}`\n"
        f"PR: `\\#{pr['number']}` {escape_markdown_v2(pr['title'])}\n"
        f"URL: {escape_markdown_v2(pr['html_url'])}\n"
        f"By: `{escape_markdown_v2(pr['user']['login'])}`"
    )


def route_github_event(event_name: str, payload: dict[str, Any]) -> tuple[int, str] | None:
    action = payload.get("action")

    if event_name == "issues" and action == "opened" and "issue" in payload:
        return TOPIC_IDS["backlog"], build_issue_opened_message(payload)

    if event_name == "issue_comment" and action == "created" and "issue" in payload:
        issue = payload["issue"]
        if "pull_request" in issue:
            return None
        if issue_has_label(issue, "block"):
            return TOPIC_IDS["blockers"], build_blocker_comment_message(payload)
        return None

    if event_name == "pull_request" and action in {"opened", "ready_for_review"} and "pull_request" in payload:
        return TOPIC_IDS["pr_review"], build_pr_message(payload)

    return None


async def send_telegram_message(topic_id: int, text: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(
            f"{TELEGRAM_API_BASE}/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "message_thread_id": topic_id,
                "text": text,
                "parse_mode": "MarkdownV2",
                "disable_web_page_preview": True,
            },
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=f"Telegram returned non-JSON response: {exc}") from exc

    if response.status_code >= 400 or not payload.get("ok"):
        raise HTTPException(status_code=502, detail=f"Telegram sendMessage failed: {payload}")

    MESSAGE_LOG.append({
        "ts": time.time(),
        "topic": TOPIC_NAMES.get(topic_id, str(topic_id)),
        "text": text,
    })

    return payload


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/recent")
async def recent(since: float = Query(0.0)) -> JSONResponse:
    msgs = [m for m in MESSAGE_LOG if m["ts"] > since]
    return JSONResponse({"messages": msgs})


CLI_KIND_MAP = {
    "doing":          ("doing",      "[doing]"),
    "block":          ("blockers",   "[block]"),
    "handoff":        ("doing",      "[handoff]"),
    "decision":       ("decisions",  "[decision]"),
    "review_context": ("pr_review",  "[review-context]"),
}


@app.post("/cli-update")
async def cli_update(request: Request) -> JSONResponse:
    body = await request.json()
    kind = body.get("kind", "")
    text = body.get("text", "")
    if kind not in CLI_KIND_MAP:
        raise HTTPException(status_code=400, detail=f"Unknown kind: {kind}. Allowed: {list(CLI_KIND_MAP)}")
    if not text:
        raise HTTPException(status_code=400, detail="Missing text")

    topic_key, prefix = CLI_KIND_MAP[kind]
    topic_id = TOPIC_IDS[topic_key]
    message = f"*{escape_markdown_v2(prefix)}* {escape_markdown_v2(text)}"
    await send_telegram_message(topic_id, message)
    return JSONResponse({"status": "sent", "kind": kind, "topic": topic_key})


@app.post("/github-webhook")
async def github_webhook(request: Request) -> JSONResponse:
    raw_body = await request.body()
    verify_github_signature(raw_body, request.headers.get("X-Hub-Signature-256"))

    event_name = request.headers.get("X-GitHub-Event")
    if not event_name:
        raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")

    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {exc}") from exc

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload must be a JSON object")

    repo = payload.get("repository", {}).get("full_name", "")
    if repo and repo not in ALLOWED_REPOS:
        return JSONResponse({"status": "rejected", "reason": f"repo {repo} not in allowlist"})

    routed = route_github_event(event_name, payload)
    if routed is None:
        return JSONResponse({"status": "ignored", "event": event_name})

    topic_id, text = routed
    telegram_response = await send_telegram_message(topic_id, text)
    return JSONResponse(
        {
            "status": "sent",
            "event": event_name,
            "topic_id": topic_id,
            "telegram_message_id": telegram_response["result"]["message_id"],
        }
    )
