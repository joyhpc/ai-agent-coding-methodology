When the user says things like "告诉合作人", "同步下进度", "通知合作人", "现在需要告诉合作人什么", or any intent to communicate status to their partner:

1. **Analyze current context** — look at what was just done in this conversation:
   - Recent git commits/pushes
   - PRs created/merged
   - Issues opened/closed
   - Code changes made
   - Blockers encountered
   - Decisions made

2. **Compose a concise message** summarizing the key update. Keep it under 2 sentences.

3. **Infer the kind** based on context:
   - Just finished work or made progress → `doing`
   - Hit a problem that needs the partner → `block`
   - Work is ready for partner to take over → `handoff`
   - Made an architecture/design choice → `decision`
   - Created a PR that needs review → `review_context`

4. **Show the user what you'll send** before sending. Example:
   ```
   准备发送:
   [handoff] PR #30 已合并，路径修复 + PCP 微调完成。Day 1-7 通过率 96%，剩余 Day 4/6 偶发 FAIL 是 Groq 推理问题。

   发送？
   ```

5. **After user confirms**, execute:
   ```bash
   python3 telegram_sync_bot/send_cli_update.py --kind <kind> --text "<message>"
   ```

6. If `send_cli_update.py` is not in the current project, try the project's `telegram_sync_bot/` subdirectory.

7. If the user says "不用了" or "算了", do not send.

Do NOT auto-send without showing the user first. Always confirm.
