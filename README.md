# AG Kit

> AI Agent templates with Skills, Agents, and Workflows — now with Coordinator Mode, Persistent Memory, and Context Compression

<div  align="center">
    <a href="https://unikorn.vn/p/ag-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/ag-kit?theme=dark" alt="AG Kit - Nổi bật trên Unikorn.vn" style="width: 210px; height: 54px;" width="210" height="54" /></a>
    <a href="https://unikorn.vn/p/ag-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/ag-kit/rank?theme=dark&type=daily" alt="AG Kit - Hàng ngày" style="width: 250px; height: 64px;" width="250" height="64" /></a>
    <a href="https://launch.j2team.dev/products/ag-kit" target="_blank"><img src="https://launch.j2team.dev/badge/ag-kit/dark" alt="AG Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

## 🚀 What's New in 2026.5.13

AG Kit 2026.5.13 introduces **7 new skills**, **3 new workflows**, and a **major orchestrator upgrade** — informed by studying advanced AI agent architectural patterns. The result: **13-33% fewer tokens per session** through smarter orchestration, persistent memory, and context compression.

### v2 vs 2026.5.13 Comparison

| Feature | v2.0 (Before) | 2026.5.13 (After) | Token Impact |
|---------|---------------|--------------|--------------|
| **Orchestration** | Sequential agent chains | Coordinator mode with parallel workers | –33% fewer retries |
| **Memory** | None — re-discovers every session | Persistent MEMORY.md with 4-type taxonomy | –3,000-10,000/session |
| **Skill Loading** | All skills visible to agent | Conditional via `when_to_use` | –1,200 tokens/session |
| **Context Management** | No compression — degrades in long sessions | Auto-compression, micro-compact | +5,000-15,000 recovered |
| **Verification** | Manual testing only | `/verify` proves code works by running it | Fewer debug cycles |
| **Agent Prompts** | Basic templates, high retry rate | Synthesis protocol ("never delegate understanding") | –2,000-5,000/task |
| **Batch Operations** | One file at a time | Multi-file batch skill | Faster bulk changes |
| **Self-Improvement** | Manual skill creation | `/skillify` auto-creates skills | Self-evolving system |
| **Code Quality** | Standard review | `/simplify` reduces complexity | Cleaner output |
| **Agents** | 20 | 20 (1 major upgrade) | — |
| **Skills** | 37 | 44 (+7 new) | Smarter loading |
| **Workflows** | 11 | 14 (+3 new) | — |

### ✅ Pros of 2026.5.13

- **Token-efficient**: 13-33% fewer tokens per session through memory, compression, and smarter prompts
- **Cross-session memory**: Never re-explain preferences, conventions, or past decisions
- **Smarter orchestration**: Parallel for read-only work, sequential for writes — with synthesis protocol
- **Production-tested patterns**: Distilled from advanced AI agent architectures (512K+ lines analyzed)
- **Backward compatible**: All v2 workflows, agents, and skills still work unchanged
- **Self-improving**: Skillify lets the system create new skills from repetitive tasks
- **Better verification**: `/verify` proves code works through execution, not inspection

### ❌ Cons / Trade-offs

- **Larger `.agent/` folder**: ~40KB additional markdown files
- **MEMORY.md overhead**: ~1,000 tokens per session (but saves 3,000-10,000 by eliminating re-discovery)
- **Coordinator complexity**: Advanced orchestration patterns have a learning curve
- **Frontmatter audit**: All 45 skills now have `when_to_use` — needs periodic review
- **Agent tool required**: Coordinator patterns need model with agent/subagent tool support

### 🔄 Migration from v2

- **Non-breaking**: All existing agents, skills, and workflows unchanged
- **Additive**: New features don't modify existing behavior
- **Optional**: Memory system and coordinator mode are opt-in per project
- **Simple**: `ag-kit update` to upgrade

---

## Quick Install

```bash
npx @vudovn/ag-kit init
```

Or install globally:

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

This installs the `.agent` folder containing all templates into your project.

### 🌍 Global / Shared Setup (Avoid Copying)

If you use AG Kit across many projects and don't want to copy-paste the `.agent/` folder into every single one, you can use **Symbolic Links (Symlinks)** to reference a single global `.agent` folder.

1. Install it somewhere globally, e.g., `~/.ag-kit/`
   ```bash
   mkdir ~/.ag-kit && cd ~/.ag-kit
   ag-kit init
   ```
2. Symlink it into your local projects:
   - **Mac/Linux:** `ln -s ~/.ag-kit/.agent .agent`
   - **Windows (Command Prompt as Admin):** `mklink /D .agent C:\Users\YourUser\.ag-kit\.agent`
   - **Windows (PowerShell as Admin):** `New-Item -ItemType SymbolicLink -Path ".agent" -Target "C:\Users\YourUser\.ag-kit\.agent"`

This way, updating your global `.agent` folder instantly applies the updates to all your projects.

### ⚠️ Important Note on `.gitignore`
If you are using AI-powered editors like **Cursor** or **Windsurf**, adding the `.agent/` folder to your `.gitignore` may prevent the IDE from indexing the workflows. This results in slash commands (like `/plan`, `/debug`) not appearing in the chat suggestion dropdown.

**Recommended Solution:**
To keep the `.agent/` folder local (not tracked by Git) while maintaining AI functionality:
1. Ensure `.agent/` is **NOT** in your project's `.gitignore`.
2. Instead, add it to your local exclude file: `.git/info/exclude`

### 🌍 Global Usage (Avoid Copy-Pasting)

If you work on many projects and don't want to duplicate the `.agent` folder for each one, you can keep a single `.agent` folder somewhere on your system and use **Symlinks** (Symbolic Links). This lets you update the kit in one place, and all your projects will automatically use the latest version.

**1. Create a central folder:**
Install the Kit to a common location (e.g., `~/global-tools/.agent` or `C:\tools\.agent`).

**2. Link it to your project:**
Navigate to your project directory in the terminal and run:

**Windows (Command Prompt as Admin):**
```cmd
mklink /D .agent "C:\path\to\global\.agent"
```

**macOS / Linux:**
```bash
ln -s /path/to/global/.agent .agent
```

This creates a lightweight folder shortcut. Your IDE and AI assistants will treat it as if the `.agent` folder is right inside your project!

## What's Included

| Component     | Count | Description                                                        |
| ------------- | ----- | ------------------------------------------------------------------ |
| **Agents**    | 20    | Specialist AI personas (frontend, backend, security, PM, QA, etc.) |
| **Skills**    | 45    | Domain-specific knowledge modules with conditional loading         |
| **Workflows** | 14    | Slash command procedures                                           |
| **Modern ES** | 2026+ | **Next.js 16 & React 19 Native** (Cache Components, PPR, Proxy)   |

### New in 2026.5.13

| Component | Name | Description |
|-----------|------|-------------|
| **Skill** | `coordinator-mode` | Multi-agent orchestration with parallel workers and synthesis |
| **Skill** | `memory-system` | Persistent cross-session memory with MEMORY.md index |
| **Skill** | `context-compression` | Auto-compress context in long sessions |
| **Skill** | `verify-changes` | Prove code works by running it |
| **Skill** | `batch-operations` | Multi-file batch modifications |
| **Skill** | `simplify-code` | Reduce over-engineered complexity |
| **Skill** | `skillify` | Auto-create skills from repetitive workflows |
| **Skill** | `code-review-graph` | Token-efficient code review via Tree-sitter AST graphs + MCP (6.8–49x savings) |
| **Workflow** | `/coordinate` | Advanced multi-agent coordination |
| **Workflow** | `/remember` | Save to persistent memory |
| **Workflow** | `/verify` | Verify code through execution |

#### 📊 49x Token Optimization Details (Code-Review-Graph)
The `code-review-graph` skill automates blast-radius mapping for your codebase (via Tree-sitter & SQLite).
If it is installed globally via Pip/Pipx, AG Kit Agents will now intelligently auto-query it, dropping token usage massively on large projects:

| Codebase Type | Scenario Tested | Token Cost (Standard) | Token Cost (With Graph) | Token Savings | Impact & Outcome |
|---|---|---|---|---|---|
| **Large API** (FastAPI) | Modified 1 endpoint | 138,585 tokens | 37,217 tokens | **3.7x fewer** | Reads only affected endpoints instead of all middleware. |
| **Mid-level Lib** (httpx) | Breaking change | 64,666 tokens | 14,090 tokens | **4.6x fewer** | Successfully skips disconnected source files. |
| **Massive Monorepo** | Cross-package update | 739,352 tokens | 15,049 tokens | **49.1x fewer** | Excludes exactly ~26,500 unrelated files instantly. |

*(Note: The integration automatically ignores parsing small projects under 200 files since naive file-reading is cheaper at that size).*

## Usage

### Using Agents

**No need to mention agents explicitly!** The system automatically detects and applies the right specialist(s):

```
You: "Add JWT authentication"
Agent: Applying @security-auditor + @backend-specialist...

You: "Fix the dark mode button"
Agent: Using @frontend-specialist...

You: "Login returns 500 error"
Agent: Using @debugger for systematic analysis...
```

**How it works:**

- Analyzes your request silently

- Detects domain(s) automatically (frontend, backend, security, etc.)
- Selects the best specialist(s)
- Informs you which expertise is being applied
- You get specialist-level responses without needing to know the system architecture

**Benefits:**

- ✅ Zero learning curve - just describe what you need
- ✅ Always get expert responses
- ✅ Transparent - shows which agent is being used
- ✅ Can still override by mentioning agent explicitly

### Using Workflows

Invoke workflows with slash commands:

| Command          | Description                           |
| ---------------- | ------------------------------------- |
| `/brainstorm`    | Explore options before implementation |
| `/coordinate`    | **NEW** Advanced multi-agent coordination |
| `/create`        | Create new features or apps           |
| `/debug`         | Systematic debugging                  |
| `/deploy`        | Deploy application                    |
| `/enhance`       | Improve existing code                 |
| `/orchestrate`   | Multi-agent coordination              |
| `/plan`          | Create task breakdown                 |
| `/preview`       | Preview changes locally               |
| `/remember`      | **NEW** Save to persistent memory     |
| `/status`        | Check project status                  |
| `/test`          | Generate and run tests                |
| `/ui-ux-pro-max` | Design with 50 styles                 |
| `/verify`        | **NEW** Prove code works by running it |

Example:

```
/coordinate comprehensive security + performance review
/remember I prefer bun over npm
/verify the login endpoint handles expired tokens
```

### Using Skills

Skills are loaded automatically based on task context. Each skill has a `when_to_use` field that helps the AI determine relevance — loading only what's needed instead of browsing all 45 skills.

### Using Memory

Memory persists across sessions. The AI remembers your preferences, project conventions, and past decisions:

```
You: "/remember Always use TypeScript strict mode"
AI: ✅ Saved to memory: [project] TypeScript strict mode required

--- Next session ---
You: "Create a new util function"
AI: (silently applies strict mode, no need to re-tell)
```

## CLI Tool

| Command         | Description                               |
| --------------- | ----------------------------------------- |
| `ag-kit init`   | Install `.agent` folder into your project |
| `ag-kit update` | Update to the latest version              |
| `ag-kit status` | Check installation status                 |

### Options

```bash
ag-kit init --force        # Overwrite existing .agent folder
ag-kit init --path ./myapp # Install in specific directory
ag-kit init --branch dev   # Use specific branch
ag-kit init --quiet        # Suppress output (for CI/CD)
ag-kit init --dry-run      # Preview actions without executing
```

## Attribution

AG Kit 2026.5.13 was informed by studying advanced AI agent source code architectures, including patterns observed in production AI coding assistants. Architectural patterns and prompt engineering insights were analyzed and rewritten as **original markdown-based skill templates**. **No external code was copied** — all skills are original implementations.

Key patterns distilled:
- **Coordinator mode**: Multi-agent orchestration with parallel workers and synthesis protocol
- **Persistent memory**: MEMORY.md index with topic files and 4-type taxonomy
- **Context compression**: Auto-compact, micro-compact, and phase summarization
- **Conditional skill loading**: `when_to_use` frontmatter for intelligent skill activation
- **Worker prompt synthesis**: "Never delegate understanding" protocol

## Documentation

- **[Web App Example](https://ag-kit.unikorn.vn/docs/guide/examples/brainstorm)** - Step-by-step guide to creating a web application
- **[Online Docs](https://ag-kit.unikorn.vn/docs)** - Browse all documentation online

## Buy me coffee

<p align="center">
  <a href="https://buymeacoffee.com/vudovn">
    <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" />
  </a>
</p>

<p align="center"> - or - </p>

<p align="center">
  <img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Buy me coffee" width="200" />
</p>

## License

MIT © Vudovn
