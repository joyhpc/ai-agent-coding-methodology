Check for new team messages from the Telegram sync bot. Run this when the user asks "any new messages?", "check messages", "看下消息", etc.

This is a ONE-SHOT check, not continuous polling. It prints new messages since last check and exits.

Execute:
```bash
cd $PROJECT_ROOT/telegram_sync_bot && python3 check_messages.py
```

If no output, tell the user "no new messages".
If there is output, display it formatted.

Do NOT run this automatically or on a schedule. Only run when the user explicitly asks.
