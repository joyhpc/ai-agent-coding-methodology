Deploy or set up the Telegram sync bot for a project. This skill handles both new deployments and connecting to existing ones.

## What you need from the user

1. **Telegram Bot Token** — from @BotFather
2. **Telegram Chat ID** — the supergroup ID (negative number)
3. **Topic IDs** — forum topic thread IDs for: Backlog, Doing, Blockers, PR-Review, Decisions
4. **GitHub repo** — which repo to receive webhooks from
5. **GitHub Webhook Secret** — generate with `openssl rand -hex 32` if not existing

## Setup steps

### 1. Check if telegram_sync_bot/ exists in the project

If not, the user needs to either:
- Copy it from a project that has it (e.g., lingoteen-ai)
- Or clone the files: `main.py`, `send_cli_update.py`, `watch_updates.py`, `requirements.txt`

### 2. Local test

```bash
cd telegram_sync_bot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # fill in values
uvicorn main:app --port 8000
# In another terminal: curl http://localhost:8000/healthz
```

### 3. Deploy to Render

Check if render.yaml has the telegram bot service entry. If not, add:

```yaml
  - type: web
    name: <project>-telegram-sync-bot
    runtime: python
    rootDir: telegram_sync_bot
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /healthz
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: CHAT_ID
        sync: false
      - key: TOPIC_BACKLOG
        sync: false
      - key: TOPIC_DOING
        sync: false
      - key: TOPIC_BLOCKERS
        sync: false
      - key: TOPIC_PR_REVIEW
        sync: false
      - key: TOPIC_DECISIONS
        sync: false
      - key: GITHUB_WEBHOOK_SECRET
        sync: false
      - key: ALLOWED_REPOS
        sync: false
```

Then create the service via Render API or Dashboard, set env vars, and wait for deploy.

### 4. Configure GitHub webhook

```bash
gh api repos/<owner>/<repo>/hooks --method POST \
  -f config[url]="https://<render-domain>/github-webhook" \
  -f config[content_type]="json" \
  -f config[secret]="<webhook-secret>" \
  -f "events[]=issues" \
  -f "events[]=issue_comment" \
  -f "events[]=pull_request"
```

### 5. Verify

```bash
# Health check
curl https://<render-domain>/healthz

# Send test
python send_cli_update.py --url https://<render-domain> --kind doing --text "部署验证"

# Watch
python watch_updates.py --url https://<render-domain>
```

### 6. Update send_cli_update.py DEFAULT_URL

Change the `DEFAULT_URL` in `send_cli_update.py` to the new Render domain so users don't need `--url` every time.

Always confirm each step succeeded before moving to the next.
