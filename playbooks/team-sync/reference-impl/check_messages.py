#!/usr/bin/env python3
"""One-shot check for new messages. Designed to be called by coding agents.

Unlike watch_updates.py (continuous), this runs once and exits.
Returns nothing if no new messages, prints and exits if there are.

Usage:
    python3 check_messages.py                    # check since last run
    python3 check_messages.py --since 0          # show all messages
    python3 check_messages.py --url http://...   # custom server
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import httpx

DEFAULT_URL = "https://lingoteen-telegram-sync-bot.onrender.com"
STATE_FILE = Path.home() / ".tg_sync_last_check"

TOPIC_LABELS = {
    "backlog": "00-Backlog",
    "doing": "10-Doing",
    "blockers": "20-Blockers",
    "pr_review": "30-PR-Review",
    "decisions": "40-Decisions",
}


def load_since() -> float:
    if STATE_FILE.exists():
        try:
            return float(STATE_FILE.read_text().strip())
        except ValueError:
            pass
    return time.time() - 3600  # default: last hour


def save_since(ts: float) -> None:
    STATE_FILE.write_text(str(ts))


def strip_md2(text: str) -> str:
    return text.replace("\\", "")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--since", type=float, default=None)
    args = parser.parse_args()

    since = args.since if args.since is not None else load_since()

    try:
        resp = httpx.get(f"{args.url}/recent", params={"since": since}, timeout=10)
    except httpx.ConnectError:
        print("Bot server unreachable", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        print(f"HTTP {resp.status_code}", file=sys.stderr)
        sys.exit(1)

    messages = resp.json().get("messages", [])
    if not messages:
        sys.exit(0)  # no output = no new messages

    for msg in messages:
        ts = datetime.fromtimestamp(msg["ts"]).strftime("%H:%M")
        topic = TOPIC_LABELS.get(msg["topic"], msg["topic"])
        text = strip_md2(msg["text"]).split("\n")[0][:80]
        print(f"[{ts}] [{topic}] {text}")
        since = max(since, msg["ts"])

    save_since(since)


if __name__ == "__main__":
    main()
