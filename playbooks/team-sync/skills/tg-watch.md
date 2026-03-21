Start watching Telegram sync bot notifications in the terminal.

Execute:
```bash
cd $PROJECT_ROOT/telegram_sync_bot && python3 watch_updates.py
```

If the user specifies a custom URL, pass it:
```bash
python3 watch_updates.py --url <url>
```

If the user specifies a poll interval:
```bash
python3 watch_updates.py --interval <seconds>
```

Default URL: https://lingoteen-telegram-sync-bot.onrender.com
Default interval: 10 seconds

If `watch_updates.py` is not found, tell the user to set up the Telegram sync bot first.

If httpx is not installed, run: `pip install httpx`

This runs continuously until Ctrl+C. Warn the user it will occupy the terminal.
