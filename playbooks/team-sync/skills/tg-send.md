Send a status update to the team via Telegram sync bot.

Parse the user's input to extract:
1. **kind** — one of: doing, block, handoff, decision, review_context
2. **text** — the message content

If the user doesn't specify a kind, infer it:
- Talking about what they're working on → doing
- Talking about being stuck/blocked → block
- Handing off work to someone → handoff
- Making an architecture/design decision → decision
- Asking someone to review with specific context → review_context

Execute:
```bash
cd $PROJECT_ROOT/telegram_sync_bot && python3 send_cli_update.py --kind <kind> --text "<text>"
```

If `$PROJECT_ROOT/telegram_sync_bot` doesn't exist, look for `send_cli_update.py` in the current project's `telegram_sync_bot/` directory.

If `send_cli_update.py` is not found anywhere, tell the user to set up the Telegram sync bot first.

If httpx is not installed, run: `pip install httpx`

After sending, confirm what was sent and to which topic.
