#!/usr/bin/env python3
"""CLI 主动发信到 Telegram topic（通过 Render server 转发）。

只允许发送"人的状态"，不允许重复 GitHub webhook 已自动播报的系统事件。

用法:
    python send_cli_update.py --kind doing --text "开始做 Issue #34 session schema"
    python send_cli_update.py --kind block --text "Groq API 限流，等恢复"
    python send_cli_update.py --kind handoff --text "PCP 微调完成，交给合作人 review"
    python send_cli_update.py --kind decision --text "Director 判定保持 Groq，不换 OpenAI"
    python send_cli_update.py --kind review_context --text "PR #30 重点看 agent.py L319 路径修复"

    # 自定义 server URL（默认 Render）
    python send_cli_update.py --url http://localhost:8000 --kind doing --text "本地测试"
"""

import argparse
import sys

import httpx

DEFAULT_URL = "https://lingoteen-telegram-sync-bot.onrender.com"
KINDS = ["doing", "block", "handoff", "decision", "review_context"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a status update to Telegram")
    parser.add_argument("--kind", required=True, choices=KINDS)
    parser.add_argument("--text", required=True)
    parser.add_argument("--url", default=DEFAULT_URL, help="Bot server URL")
    args = parser.parse_args()

    resp = httpx.post(
        f"{args.url}/cli-update",
        json={"kind": args.kind, "text": args.text},
        timeout=20,
    )

    if resp.status_code >= 400:
        print(f"Error: {resp.text}", file=sys.stderr)
        sys.exit(1)

    data = resp.json()
    print(f"Sent [{data.get('kind')}] -> {data.get('topic')}")


if __name__ == "__main__":
    main()
