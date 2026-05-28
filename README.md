<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AGKIT">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
    AI Agent templates with Skills, Agents, and Workflows — featuring Coordinator Mode, Persistent Memory, and Context Compression.
</p>

<div align="center">
    <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="AG Kit - Nổi bật trên Unikorn.vn" style="width: 210px; height: 54px;" width="210" height="54" /></a>
    <a href="https://trendshift.io/repositories/21490" target="_blank"><img src="https://trendshift.io/api/badge/repositories/21490" alt="vudovn%2Fantigravity-kit | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
    <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="AG Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

<p align="center">
  <strong>🇻🇳 <a href="./README-VI.md">Tiếng Việt (Vietnamese Version)</a></strong>
</p>

---

## ⚡ Quick Start

Install and initialize AG Kit to inject the `.agent/` configuration folder directly into your local project.

### Method 1: On-demand Execution (Recommended)

```bash
npx @vudovn/ag-kit init
```

### Method 2: Global Installation

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

---

## 🌍 Global Shared Setup (Symlinks)

If you work across multiple repositories and want to avoid duplicating the `.agent/` folder in every single project, you can centralize AG Kit and use symbolic links.

1. **Install centrally** (e.g., to a global folder like `~/.ag-kit`):
   ```bash
   mkdir -p ~/.ag-kit && cd ~/.ag-kit
   npx @vudovn/ag-kit init
   ```

2. **Link it locally** from inside your project root:
   - **macOS / Linux:**
     ```bash
     ln -s ~/.ag-kit/.agent .agent
     ```
   - **Windows (CMD - Run as Administrator):**
     ```cmd
     mklink /D .agent "%USERPROFILE%\.ag-kit\.agent"
     ```
   - **Windows (PowerShell - Run as Administrator):**
     ```powershell
     New-Item -ItemType SymbolicLink -Path ".agent" -Target "$env:USERPROFILE\.ag-kit\.agent"
     ```

---

## ⚠️ Important Note on `.gitignore`

If you are using AI-native code editors (like **Cursor** or **Windsurf**), adding the `.agent/` directory to `.gitignore` will prevent the editor's language server from indexing the workflows, which disables autocomplete for slash commands (e.g. `/plan`, `/debug`).

### Recommended Solution:
To keep `.agent/` out of your remote repository without losing editor integration:
1. Ensure `.agent/` is **NOT** listed in your project's `.gitignore`.
2. Add `.agent/` to your local Git exclude file: `.git/info/exclude` instead.

---

## 📦 What's Included

AG Kit packages domain-specific knowledge, specialized agent personas, and automated workflows optimized for modern AI coding tools.

| Component | Count | Description |
| :--- | :--- | :--- |
| **Agents** | 20 | Specialist AI personas (Frontend, Backend, Security, PM, QA, etc.) |
| **Skills** | 45 | Domain-specific context modules with conditional loading rules |
| **Workflows** | 13 | Pre-configured interactive developer procedures (slash commands) |

---

## 🛠️ Usage

### 1. Zero-Setup Agent Auto-Routing

You don't need to manually orchestrate agents. The system silently classifies your request, auto-routes to the best domain experts, and applies their rules instantly:

```
You: "Add JWT authentication to the login API"
Agent: Applying @security-auditor + @backend-specialist...

You: "Align the checkout button to the center and fix dark mode"
Agent: Using @frontend-specialist...
```

### 2. Interactive Workflows (Slash Commands)

Execute structured development workflows by typing slash commands in your AI agent chat:

| Command | Description |
| :--- | :--- |
| `/brainstorm` | Structured exploration of options and architecture before coding |
| `/coordinate` | Orchestrate multiple agents in parallel for complex reviews |
| `/create` | Create new features or full applications from scratch |
| `/debug` | Activate evidence-based systematic debugging |
| `/deploy` | Execute pre-flight checks and deploy to production |
| `/enhance` | Safely add or update features in an existing codebase |
| `/plan` | Generate a structured implementation plan and checklist |
| `/preview` | Start, stop, or check status of local preview servers |
| `/remember` | Save custom project conventions to persistent memory |
| `/status` | Generate a clear status report of the agent's progress |
| `/test` | Generate and execute comprehensive tests |
| `/verify` | Prove code works via execution rather than simple inspection |

---

## 🧠 Core Architectural Concepts

AG Kit is built on production-tested agentic design patterns designed to reduce token usage by **13% to 33%** while yielding higher output quality:

*   **Coordinator Mode:** Multi-agent orchestration with parallel workers and synthesis, avoiding expensive sequential retries.
*   **Persistent Memory:** A 4-type taxonomy memory engine index (`MEMORY.md`) to prevent re-explaining project guidelines across sessions.
*   **Context Compression:** Automated summarization and micro-compaction routines to prevent context degradation in long-lived sessions.
*   **Conditional Skill Loading:** Context-aware loading of rules via custom frontmatter, preventing your context window from bloating with idle instructions.

---

## 📚 References & Attribution

AG Kit represents an original implementation of markdown-based prompt and rules engineering. It was built by analyzing production agent patterns to distill core agentic behaviors:
*   *No proprietary code or files were copied.*
*   All templates, rules, and scripts are rewritten as original, open-source implementations under the MIT license.

---

## ☕ Support the Project

If AG Kit has made your AI programming sessions more productive, consider supporting the project:

| ☕ Support & Donations | 🚀 Support |
| :---: | :---: |
| <a href="https://buymeacoffee.com/vudovn" target="_blank"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" /></a><br/><br/>**Vietnamese Bank (MBBank QR):**<br/><img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Donate QR" width="140" style="border-radius: 8px; margin-top: 10px;" /> | **donation donation info (CA):**<br/><br/>`Gjpatn3d24dCRhUng7F37K6xJba4R8SDBC18xs1Apump`<br/><br/>*Copy the donation info (CA) above to trade on Raydium, Jupiter, or your favorite DEX.* |

---

## 📄 License

Released under the [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
