# Claude Code Skills for Team Sync

以下 `.md` 文件放到 `~/.claude/commands/` 即可注册为 slash command。

**注意：这些 skill 不会自动执行，只在用户主动调用 `/tg-send` `/tg-watch` `/tg-deploy` 时触发。**

## 安装

```bash
cp skills/tg-send.md ~/.claude/commands/
cp skills/tg-watch.md ~/.claude/commands/
cp skills/tg-deploy.md ~/.claude/commands/
```

重启 Claude Code 后可用。

## 用法

```
/tg-send doing 开始做 Issue #34
/tg-watch
/tg-deploy
```
