# Team Sync via Telegram — Playbook

CLI-to-Telegram 双向协同方案。GitHub 自动通知系统事件，CLI 手动通知人的状态，两者不重叠。

## 架构

```
你的 CLI ──────┐
               ├──→ Render Server ──→ Telegram Group Topics
合作人的 CLI ──┘     (FastAPI)          ↑
                                       │
GitHub Webhook ────────────────────────┘
```

## 文件结构

```
telegram_sync_bot/
├── main.py                 # FastAPI server（部署到 Render）
├── send_cli_update.py      # 发送端 CLI（参考实现）
├── watch_updates.py        # 接收端 CLI（参考实现）
├── requirements.txt        # httpx, fastapi, uvicorn, python-dotenv
└── README.md
```

## 通知边界（核心原则）

| 通道 | 职责 | 禁止 |
|------|------|------|
| GitHub Webhook | 系统事件：issue 创建、PR 创建/ready、blocker comment | 不手动重复 |
| CLI 手动 | 人的状态：doing / block / handoff / decision / review_context | 不发系统事件 |

## 部署步骤

### 前置条件

- Telegram Bot Token（@BotFather 创建）
- Telegram Supergroup + Forum Topics（Backlog / Doing / Blockers / PR-Review / Decisions）
- Render 账号
- GitHub 仓库

### 1. 创建 Telegram Bot 和群

```
1. Telegram 搜索 @BotFather → /newbot → 拿到 BOT_TOKEN
2. 创建 Supergroup → 开启 Topics 功能
3. 创建 5 个 topic：00-Backlog, 10-Doing, 20-Blockers, 30-PR-Review, 40-Decisions
4. 把 bot 加入群并设为管理员
5. 获取 Chat ID（群 ID，负数）和每个 topic 的 thread ID
```

获取 Chat ID 方法：
```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/getUpdates" | python3 -m json.tool
# 在 result 里找 chat.id
```

### 2. 复制 bot 代码到你的项目

```bash
# 从参考实现复制
cp -r <source>/telegram_sync_bot/ <your-project>/telegram_sync_bot/
```

或者直接用下面的参考实现文件。

### 3. 部署到 Render

render.yaml 添加：
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

通过 Render Dashboard 或 API 创建服务并设置环境变量。

### 4. 配置 GitHub Webhook

```bash
# 生成 secret
WEBHOOK_SECRET=$(openssl rand -hex 32)

# 创建 webhook
gh api repos/<owner>/<repo>/hooks --method POST \
  -f config[url]="https://<render-domain>/github-webhook" \
  -f config[content_type]="json" \
  -f config[secret]="$WEBHOOK_SECRET" \
  -f "events[]=issues" \
  -f "events[]=issue_comment" \
  -f "events[]=pull_request"
```

确保 Render 环境变量 `GITHUB_WEBHOOK_SECRET` 和这里的 secret 一致。

### 5. 验证

```bash
# 健康检查
curl https://<render-domain>/healthz

# 发测试消息
python3 send_cli_update.py --url https://<render-domain> --kind doing --text "部署验证"

# GitHub ping
gh api repos/<owner>/<repo>/hooks/<hook-id>/pings --method POST

# 创建测试 issue 验证自动通知
gh issue create --repo <owner>/<repo> --title "[test] webhook verification" --body "test"
```

### 6. 更新 send_cli_update.py 的 DEFAULT_URL

```python
DEFAULT_URL = "https://<your-render-domain>"
```

### 7. 合作人设置（零配置）

合作人只需要：
```bash
cd telegram_sync_bot
python3 -m venv .venv && source .venv/bin/activate
pip install httpx
python3 send_cli_update.py --kind doing --text "上线"
python3 watch_updates.py  # 终端看通知
```

不需要 Bot Token，不需要 .env，不需要部署。

## 多项目隔离

每个项目部署独立的 Render 实例，配不同的环境变量：
- 不同的 `CHAT_ID`（不同 Telegram 群）
- 不同的 `TOPIC_*`（不同 topic ID）
- 不同的 `ALLOWED_REPOS`（白名单隔离）
- 不同的 `GITHUB_WEBHOOK_SECRET`

代码完全相同，通过环境变量区分。

## CLI 用法速查

```bash
# 发送
python3 send_cli_update.py --kind doing --text "在做什么"
python3 send_cli_update.py --kind block --text "被什么卡住"
python3 send_cli_update.py --kind handoff --text "交接给谁"
python3 send_cli_update.py --kind decision --text "决策了什么"
python3 send_cli_update.py --kind review_context --text "PR 重点看什么"

# 接收
python3 watch_updates.py                    # 默认 Render URL
python3 watch_updates.py --interval 5       # 5 秒轮询
python3 watch_updates.py --url http://...   # 自定义 URL
```
