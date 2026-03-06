## v6.9.0 - Multi-Tool & Agent Infrastructure

> **Agent capabilities expand with email infrastructure, video intelligence, and multi-tool installer support.**

### 🚀 New Skills

**📧 AgentMail** — Email infrastructure for AI agents
- Create email accounts with karma-based rate limiting
- Send/receive emails with attachments
- Webhook signature verification for secure notifications
- Full SDK examples and API reference

**📹 VideoDB** — Video and audio perception, indexing, and editing
- Ingest from files, URLs, RTSP/live feeds, or desktop capture
- Semantic, visual, and spoken word indexes with timestamp search
- Timeline editing with subtitles, overlays, transcoding
- AI generation for images, video, music, voiceovers

### 📦 Improvements

- **Multi-Tool Install Support**: Install skills for multiple tools simultaneously (e.g., `npx antigravity-awesome-skills --claude --codex`). Fixes #182.
- **Web-App Sync Optimization**: Hybrid sync strategy using git fetch (5+ min → < 2 sec). Includes sort by "Most Stars".
- **Registry**: 970 skills (+2 new)

### 👥 Contributors

- @zinzied — Web-app sync optimization (PR #180)
- @0xrohitgarg — VideoDB skill (PR #181)
- @uriva — AgentMail skill (PR #183)

---

_Upgrade: `npx antigravity-awesome-skills` or `git pull origin main`_
