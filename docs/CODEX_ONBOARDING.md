# Codex 学生上手指南

面向第一次在 Codex 里使用 Canvas Pilot 的学生。

## 安装与首次运行

把 <https://canvas-pilot-rho.vercel.app/install> 上的安装提示词粘贴给 Codex。Agent 会：

1. 下载仓库，先询问你的学校，再解析学校官方 Canvas 地址。
2. 运行 `canvas-setup`：打开 Canvas 浏览器窗口，由你本人在浏览器里完成登录（SSO / 2FA）。密码、2FA、cookie 不粘贴到聊天或终端。
3. 鉴权通过后运行 `canvas-skill-opportunity`：读取有代表性的作业规格，写出只保存在本地的长期 Skill 机会榜单，然后停在编号选择前，等你选号。
4. 你选号之后才运行 `canvas-bootstrap` 生成课程技能；再之后才是 `canvas-scan → 看计划 → 批准 → canvas-execute`。

会话过期时，重新运行 `python -m src.canvas_login`，在弹出的 Canvas 浏览器里重新登录。

## 安全默认值

- 只出草稿、不提交：批准计划只授权在本地起草。
- 自动提交要单独的显式授权，并且必须通过验证闸：只有整条消息恰好是 `submit N` 时，`canvas-submit` 才签发一次性收据，`src/authorization.py` 拒绝任何没有收据的 Canvas 写操作。
- live quiz 动作 fail-closed：`take quiz N` / `retake quiz N` 同样需要精确命令和收据；遇到 New Quizzes、锁定或缺少来源时直接停止。
- 私有的课程 ID、作业 ID、私人链接、姓名和邮箱放在本地配置（`SECRETS.md`、`courses.yaml`、`_private/`），不写进受跟踪的文档。
