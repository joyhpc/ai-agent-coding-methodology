#!/usr/bin/env python3
"""Watch Telegram sync bot notifications in your terminal.

Polls the bot's /recent endpoint and prints new messages as they arrive.

Usage:
    python watch_updates.py
    python watch_updates.py --url https://lingoteen-telegram-sync-bot.onrender.com
    python watch_updates.py --interval 5
"""

import argparse
import sys
import time
from datetime import datetime

import httpx

TOPIC_LABELS = {
    "backlog": "00-Backlog",
    "doing": "10-Doing",
    "blockers": "20-Blockers",
    "pr_review": "30-PR-Review",
    "decisions": "40-Decisions",
}


def strip_markdown_v2(text: str) -> str:
    """Remove MarkdownV2 escape backslashes for terminal display."""
    return text.replace("\\", "")


def format_message(msg: dict) -> str:
    ts = datetime.fromtimestamp(msg["ts"]).strftime("%H:%M:%S")
    topic = TOPIC_LABELS.get(msg["topic"], msg["topic"])
    text = strip_markdown_v2(msg["text"])
    # Truncate long messages for terminal readability
    lines = text.split("\n")
    preview = "\n    ".join(lines[:5])
    if len(lines) > 5:
        preview += "\n    ..."
    return f"  [{ts}] [{topic}]\n    {preview}"


def watch(base_url: str, interval: int) -> None:
    since = time.time()
    print(f"Watching {base_url}/recent (poll every {interval}s)")
    print(f"Press Ctrl+C to stop\n{'─' * 50}")

    while True:
        try:
            resp = httpx.get(f"{base_url}/recent", params={"since": since}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for msg in data.get("messages", []):
                    print(format_message(msg))
                    since = max(since, msg["ts"])
            else:
                print(f"  [warn] HTTP {resp.status_code}", file=sys.stderr)
        except httpx.ConnectError:
            print(f"  [warn] Cannot reach {base_url}", file=sys.stderr)
        except Exception as e:
            print(f"  [error] {e}", file=sys.stderr)

        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Watch Telegram sync bot updates")
    parser.add_argument("--url", default="https://lingoteen-telegram-sync-bot.onrender.com")
    parser.add_argument("--interval", type=int, default=10, help="Poll interval in seconds")
    args = parser.parse_args()
    try:
        watch(args.url, args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
