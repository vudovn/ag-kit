# AG Kit Architecture

> Antigravity-native AI Agent Capability Toolkit — 2026.7.26

---

## 📋 Overview

AG Kit is a modular Antigravity workspace system consisting of:

- **20 Specialist Agents** — role-based AI personas and orchestration roles;
- **48 Skills** — domain knowledge modules with progressive conditional loading;
- **13 Workflows** — slash-command procedures;
- **6 Rules** — workspace routing, coding, design, safety, and quick-reference constraints;
- **Antigravity runtime layer** — contract, native hook, MCP helper, plugin builder, Doctor, schemas, and tests.

---

## 🔐 Managed Component Registry (2026.7.26)

AG Kit uses dual-track versioning:

- Toolkit releases use **CalVer** in `VERSION` (`YYYY.M.D`).
- Agents, skills, workflows, and rules use strict **SemVer** in frontmatter.
- `manifest.json` records component paths, versions, tools, dependencies, and the Antigravity runtime contract.
- `manifest.lock.json` records deterministic SHA-256 hashes for managed components and runtime tooling.
- `DEPENDENCY_GRAPH.md` is generated from the registry and must not be edited manually.

The registry is synchronized by executable checks:

```bash
python .agents/scripts/generate_manifest.py --check
python .agents/scripts/dependency_graph.py --check
python .agents/scripts/validate_kit.py
```

Any managed change without registry regeneration fails validation and CI. Google Antigravity is the primary production runtime; other Markdown-compatible tools are best-effort consumers.

---

## 🏗️ Directory Structure

```plaintext
.agents/
├── README.md                 # Toolkit operating guide
├── ARCHITECTURE.md           # Capability inventory and design
├── VERSION                   # Toolkit CalVer
├── antigravity.json          # Runtime contract and six integration phases
├── hooks.json                # Native Antigravity hook registration
├── mcp_config.json           # Workspace MCP example/source
├── manifest.json             # Generated component registry
├── manifest.lock.json        # Generated integrity lock
├── DEPENDENCY_GRAPH.md       # Generated workflow → agent → skill graph
├── agent/                    # 20 specialist role definitions
├── skills/                   # 48 progressive skills
├── workflows/                # 13 slash-command procedures
├── rules/                    # 6 workspace constraints
├── memory/                   # Persistent project context
├── hooks/                    # Antigravity Doctor, policy, MCP, plugin, schemas, tests
├── schemas/                  # Managed component and memory schemas
└── scripts/                  # Registry, validator, and project verification tools
```

---


## Antigravity runtime architecture

```text
.antigravity.json contract
        ↓
workspace discovery ── rules + skills + workflows + agent roles
        ↓
routing/orchestration ── direct role | /coordinate | /orchestrate
        ↓
Antigravity permissions + .agents/hooks.json PreToolUse gate
        ↓
tool execution, project validation, evidence, memory update
        ↓
optional plugin packaging and production release gates
```

| Phase | Managed files | Production guarantee |
| --- | --- | --- |
| Discovery | `rules/`, `skills/`, `workflows/` | Frontmatter and required paths validated |
| MCP | `mcp_config.json`, `hooks/sync-mcp.mjs` | No implicit home-directory write; placeholder and conflict protection |
| Hooks | `hooks.json`, `hooks/validate-tool-call.mjs` | Narrow destructive-command gate; native permissions retained |
| Orchestration | workflows, agents, routing skills | Antigravity `/agents` and `/tasks` remain runtime state |
| Plugin | `hooks/build-plugin.mjs`, `hooks/plugin/` | Reviewable local bundle with SHA-256 inventory |
| Validation | Doctor, tests, CI, production checklist | Automated checks plus mandatory hands-on smoke test |

The Antigravity runtime files are included in the managed integrity lock beginning with `2026.7.26`.

---

## 🤖 Agents (20)

Specialist AI personas for different domains.

| Agent                    | Focus                      | Skills Used                                              |
| ------------------------ | -------------------------- | -------------------------------------------------------- |
| `orchestrator`           | Multi-agent coordination   | parallel-agents, coordinator-mode, memory-system, context-compression, verify-changes |
| `project-planner`        | Discovery, task planning   | brainstorming, plan-writing, architecture                |
| `frontend-specialist`    | Web UI/UX                  | frontend-design, nextjs-react-expert, tailwind-patterns |
| `backend-specialist`     | API, business logic        | api-patterns, nodejs-best-practices, database-design     |
| `database-architect`     | Schema, SQL                | database-design                                          |
| `mobile-developer`       | iOS, Android, RN           | mobile-design                                            |
| `game-developer`         | Game logic, mechanics      | game-development                                         |
| `devops-engineer`        | CI/CD, Docker              | deployment-procedures, server-management                 |
| `security-auditor`       | Security compliance        | vulnerability-scanner, red-team-tactics                  |
| `penetration-tester`     | Offensive security         | red-team-tactics                                         |
| `test-engineer`          | Testing strategies         | testing-patterns, tdd-workflow, webapp-testing           |
| `debugger`               | Root cause analysis        | systematic-debugging                                     |
| `performance-optimizer`  | Speed, Web Vitals          | performance-profiling                                    |
| `seo-specialist`         | Ranking, visibility        | seo-fundamentals, geo-fundamentals                       |
| `documentation-writer`   | Manuals, docs              | documentation-templates                                  |
| `product-manager`        | Requirements, user stories | plan-writing, brainstorming                              |
| `product-owner`          | Strategy, backlog, MVP     | plan-writing, brainstorming                              |
| `qa-automation-engineer` | E2E testing, CI pipelines  | webapp-testing, testing-patterns                         |
| `code-archaeologist`     | Legacy code, refactoring   | clean-code, code-review-checklist                        |
| `explorer-agent`         | Codebase and source analysis | architecture, deep-research, systematic-debugging      |

---

## 🧩 Skills (48)

Modular knowledge domains that agents can load on-demand based on task context. Each skill has a `when_to_use` frontmatter field for conditional/intelligent loading.

### Frontend & UI

| Skill                   | Description                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `design-spec`           | DESIGN.md token format — required design source-of-truth before UI    |
| `nextjs-react-expert`   | React & Next.js performance optimization (Vercel - 58 rules)          |
| `frontend-architecture` | Frontend code organization — layers, state tiers, services (React/Vue) |
| `web-design-guidelines` | Web UI audit - 100+ rules for accessibility, UX, performance (Vercel) |
| `tailwind-patterns`     | Tailwind CSS v4 utilities                                             |
| `frontend-design`       | UI/UX patterns, design systems                                        |

### Backend & API

| Skill                   | Description                    |
| ----------------------- | ------------------------------ |
| `api-patterns`          | REST, GraphQL, tRPC            |
| `nodejs-best-practices` | Node.js async, modules         |
| `python-patterns`       | Python standards, FastAPI      |
| `rust-pro`              | Rust async, systems, type system |

### Database

| Skill             | Description                 |
| ----------------- | --------------------------- |
| `database-design` | Schema design, optimization |

### Cloud & Infrastructure

| Skill                   | Description               |
| ----------------------- | ------------------------- |
| `deployment-procedures` | CI/CD, deploy workflows   |
| `server-management`     | Infrastructure management |

### Testing & Quality

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `testing-patterns`      | Jest, Vitest, strategies |
| `webapp-testing`        | E2E, Playwright          |
| `tdd-workflow`          | Test-driven development  |
| `code-review-checklist` | Code review standards    |
| `lint-and-validate`     | Linting, validation      |

### Security

| Skill                   | Description              |
| ----------------------- | ------------------------ |
| `vulnerability-scanner` | Security auditing, OWASP |
| `red-team-tactics`      | Offensive security       |

### Architecture & Planning

| Skill           | Description                |
| --------------- | -------------------------- |
| `app-builder`   | Full-stack app scaffolding |
| `architecture`  | System design patterns     |
| `plan-writing`  | Task planning, breakdown   |
| `brainstorming` | Socratic questioning       |

### Mobile

| Skill           | Description           |
| --------------- | --------------------- |
| `mobile-design` | Mobile UI/UX patterns |

### Game Development

| Skill              | Description           |
| ------------------ | --------------------- |
| `game-development` | Game logic, mechanics |

### SEO & Growth

| Skill              | Description                   |
| ------------------ | ----------------------------- |
| `seo-fundamentals` | SEO, E-E-A-T, Core Web Vitals |
| `geo-fundamentals` | GenAI optimization            |

### Research

| Skill           | Description                                            |
| --------------- | ------------------------------------------------------ |
| `deep-research` | Multi-source research, citations, and live X evidence |

### Shell/CLI

| Skill                | Description               |
| -------------------- | ------------------------- |
| `bash-linux`         | Linux commands, scripting |
| `powershell-windows` | Windows PowerShell        |

### Orchestration & Memory (2026.5.13)

| Skill                     | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| `coordinator-mode`        | Multi-agent orchestration with parallel workers & synthesis  |
| `memory-system`           | Persistent cross-session memory with MEMORY.md index        |
| `context-compression`     | Auto-compress context in long sessions                      |
| `verify-changes`          | Prove code works by running it, not just inspecting         |
| `batch-operations`        | Multi-file pattern-based modifications                      |
| `simplify-code`           | Reduce over-engineered complexity                           |
| `skillify`                | Auto-create skills from repetitive workflows                |
| `code-review-graph`       | Token-efficient code review via Tree-sitter AST + MCP       |

### Other

| Skill                     | Description               |
| ------------------------- | ------------------------- |
| `clean-code`              | Coding standards (Global) |
| `behavioral-modes`        | Agent personas            |
| `parallel-agents`         | Multi-agent patterns      |
| `mcp-builder`             | Model Context Protocol    |
| `documentation-templates` | Doc formats               |
| `i18n-localization`       | Internationalization      |
| `performance-profiling`   | Web Vitals, optimization  |
| `systematic-debugging`    | Troubleshooting           |
| `intelligent-routing`     | Request → agent routing   |

---

## 🔄 Workflows (13)

Slash command procedures. Invoke with `/command`.

| Command          | Description                                    |
| ---------------- | ---------------------------------------------- |
| `/brainstorm`    | Socratic discovery                             |
| `/coordinate`    | **NEW** Advanced multi-agent coordination      |
| `/create`        | Create new features                            |
| `/debug`         | Debug issues                                   |
| `/deploy`        | Deploy application                             |
| `/enhance`       | Improve existing code                          |
| `/orchestrate`   | Multi-agent coordination                       |
| `/plan`          | Task breakdown                                 |
| `/preview`       | Preview changes                                |
| `/remember`      | **NEW** Save to persistent memory              |
| `/status`        | Check project status                           |
| `/test`          | Run tests                                      |
| `/verify`        | **NEW** Prove code works by running it         |

---

## 🎯 Skill Loading Protocol (Conditional)

```plaintext
User Request → Check `when_to_use` frontmatter → Match? → Load full SKILL.md
                                                    ↓ No match
                                                 Skip (save tokens)
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata, when_to_use & instructions
├── scripts/           # (Optional) Python/Bash scripts
├── references/        # (Optional) Templates, docs
└── assets/            # (Optional) Images, logos
```

### Required Frontmatter Fields

```yaml
---
name: skill-name
description: What this skill does
when_to_use: "When to activate. NOT for X."  # 2026.5.13
allowed-tools: Read, Grep, Glob
---
```

### Enhanced Skills (with scripts/references)

| Skill               | Files | Coverage                            |
| ------------------- | ----- | ----------------------------------- |
| `app-builder`       | 20    | Full-stack scaffolding              |

---

## 🛠️ Runtime Scripts

AG Kit includes **7 user-facing top-level utilities**, **2 internal registry/runner modules**, **4 Antigravity runtime utilities**, and **18 skill-level scripts**.

### Toolkit utilities

| Script | Purpose | Typical use |
|---|---|---|
| `scripts/checklist.py` | Fast, priority-ordered validation | During development and pre-commit |
| `scripts/verify_all.py` | Complete verification suite | Before release or deployment |
| `scripts/validate_kit.py` | Self-check versions, registry, memory, links, and references | After editing `.agents/` |
| `scripts/generate_manifest.py` | Generate/check component registry and lock | After changing managed metadata or runtime files |
| `scripts/dependency_graph.py` | Generate/check workflow-agent-skill graph | After changing dependencies |
| `scripts/session_manager.py` | Summarize project/session context | At session start or status checks |
| `scripts/auto_preview.py` | Start, stop, and inspect local preview servers | UI development |
| `scripts/validation_runner.py` | Shared process runner used by checklist/verify | Internal module |
| `scripts/component_registry.py` | Registry parser, SemVer resolver, runtime metadata, and hasher | Internal module |

### Antigravity runtime utilities

| Script | Purpose |
|---|---|
| `hooks/antigravity-doctor.mjs` | Read-only six-phase compatibility and release diagnostics |
| `hooks/validate-tool-call.mjs` | Native destructive-command safety gate |
| `hooks/sync-mcp.mjs` | Review and explicitly synchronize MCP configuration |
| `hooks/build-plugin.mjs` | Build a reviewable Antigravity plugin bundle |

### Usage

```bash
# Regenerate managed metadata after component/runtime edits
python .agents/scripts/generate_manifest.py
python .agents/scripts/dependency_graph.py

# Validate toolkit and Antigravity integration
npm run check:agents
npm run check:antigravity
npm run test:antigravity

# Fast project checks
python .agents/scripts/checklist.py .

# Full verification with a running app
python .agents/scripts/verify_all.py . \
  --url http://localhost:3000 \
  --report .agents/reports/verification.json
```

### Verification coverage

- Component SemVer, registry, lock, dependency graph, memory, links, and references
- Antigravity discovery, MCP shape/placeholders, native hook registration, orchestration inputs, plugin inputs, and version synchronization
- Security and secret scanning with blocking exit codes
- Offline dependency/lock-file hygiene
- Linting, type coverage, schema validation, and tests
- UX, accessibility, SEO, GEO, API, mobile, and i18n audits
- Build asset/bundle sizing
- Lighthouse and Playwright runtime checks when a URL is available

For command details and prerequisites, see [scripts/README.md](scripts/README.md) and [hooks/README.md](hooks/README.md).

---

## 📊 Statistics

| Metric              | Value                             |
| ------------------- | --------------------------------- |
| **Total Agents**    | 20 (1 major upgrade in 2026.5.13) |
| **Total Skills**    | 48                                |
| **Total Workflows** | 13 (+2 new in 2026.5.13)          |
| **Toolkit Utilities** | 7 user-facing + 2 internal modules |
| **Antigravity Utilities** | 4 runtime utilities              |
| **Total Skill Scripts** | 18                              |
| **Coverage**        | Web, API, mobile, security, quality, runtime, orchestration |
| **Token Efficiency**| Reduced via conditional skill loading |

---

## 🔗 Quick Reference

| Need     | Agent                 | Skills                                |
| -------- | --------------------- | ------------------------------------- |
| Web App  | `frontend-specialist` | nextjs-react-expert, frontend-design |
| API      | `backend-specialist`  | api-patterns, nodejs-best-practices   |
| Mobile   | `mobile-developer`    | mobile-design                         |
| Database | `database-architect`  | database-design                       |
| Security | `security-auditor`    | vulnerability-scanner                 |
| Testing  | `test-engineer`       | testing-patterns, webapp-testing      |
| Debug    | `debugger`            | systematic-debugging                  |
| Plan     | `project-planner`     | brainstorming, plan-writing           |
