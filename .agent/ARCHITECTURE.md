# Antigravity Kit Architecture

> Repository-local agent, skill, workflow, and validation surface

## Overview

Antigravity Kit currently contains:

- **20 agents** in `.agent/agents/`
- **37 top-level skills** in `.agent/skills/`
- **11 workflows** in `.agent/workflows/`
- **4 project-local scripts** in `.agent/scripts/`

The live filesystem is the source of truth for names and counts.

## Directory Structure

```text
.agent/
├── ARCHITECTURE.md
├── agents/
├── rules/
├── scripts/
├── skills/
└── workflows/
```

## Agents

| Agent | Focus | Primary Skills |
|-------|-------|----------------|
| `backend-specialist` | backend and API delivery | `nodejs-best-practices`, `python-patterns`, `api-patterns`, `database-design` |
| `code-archaeologist` | brownfield analysis | `clean-code`, `code-review-checklist` |
| `database-architect` | schema and data design | `database-design` |
| `debugger` | root-cause analysis | `systematic-debugging` |
| `devops-engineer` | deployment and infrastructure | `deployment-procedures`, `server-management` |
| `documentation-writer` | documentation authoring | `documentation-templates` |
| `explorer-agent` | discovery and mapping | `architecture`, `plan-writing`, `brainstorming`, `systematic-debugging` |
| `frontend-specialist` | web UI systems | `nextjs-react-expert`, `web-design-guidelines`, `tailwind-patterns`, `frontend-design` |
| `game-developer` | game development | `game-development` plus its nested genre/gameplay subskills |
| `mobile-developer` | mobile apps | `mobile-design` |
| `orchestrator` | multi-agent coordination | `parallel-agents`, `behavioral-modes`, `plan-writing`, `architecture` |
| `penetration-tester` | active security testing | `vulnerability-scanner`, `red-team-tactics`, `api-patterns` |
| `performance-optimizer` | performance | `performance-profiling` |
| `product-manager` | requirements and planning | `plan-writing`, `brainstorming` |
| `product-owner` | prioritization and scope | `plan-writing`, `brainstorming` |
| `project-planner` | executable planning | `app-builder`, `plan-writing`, `brainstorming` |
| `qa-automation-engineer` | QA automation | `webapp-testing`, `testing-patterns`, `web-design-guidelines` |
| `security-auditor` | security review | `vulnerability-scanner`, `red-team-tactics`, `api-patterns` |
| `seo-specialist` | SEO and GEO | `seo-fundamentals`, `geo-fundamentals` |
| `test-engineer` | testing strategy and execution | `testing-patterns`, `tdd-workflow`, `webapp-testing`, `lint-and-validate` |

## Skills

### Core Engineering

- `clean-code`
- `code-review-checklist`
- `lint-and-validate`
- `plan-writing`
- `brainstorming`
- `architecture`

### Frontend and UI

- `frontend-design`
- `nextjs-react-expert`
- `tailwind-patterns`
- `web-design-guidelines`

### Backend and Data

- `api-patterns`
- `database-design`
- `mcp-builder`
- `nodejs-best-practices`
- `python-patterns`
- `rust-pro`

### Testing and Quality

- `testing-patterns`
- `tdd-workflow`
- `webapp-testing`
- `performance-profiling`

### Security

- `vulnerability-scanner`
- `red-team-tactics`

### Platform and Ops

- `deployment-procedures`
- `server-management`
- `powershell-windows`
- `bash-linux`

### Product and Routing

- `app-builder`
- `behavioral-modes`
- `intelligent-routing`
- `parallel-agents`

### Domain Packs

- `mobile-design`
- `game-development`
- `seo-fundamentals`
- `geo-fundamentals`
- `documentation-templates`
- `i18n-localization`

## Workflows

| Workflow | Purpose |
|----------|---------|
| `brainstorm` | discovery and idea shaping |
| `create` | new feature or app flow |
| `debug` | debugging workflow |
| `deploy` | deployment workflow |
| `enhance` | improvement workflow |
| `orchestrate` | multi-agent coordination |
| `plan` | planning-only workflow |
| `preview` | preview management |
| `status` | project status |
| `test` | test generation and execution |
| `ui-ux-pro-max` | shared design-system workflow |

## Scripts

| Script | Purpose |
|--------|---------|
| `auto_preview.py` | preview/startup helper |
| `checklist.py` | incremental validation |
| `session_manager.py` | session helper |
| `verify_all.py` | full verification |

## Execution Contracts

### Planning

- canonical plan path: `docs/PLAN-{task-slug}.md`
- do not rely on `docs/PLAN.md`
- do not write plan files to project root as the default contract

### Validation

Preferred commands:

```bash
python .agent/scripts/checklist.py .
python .agent/scripts/verify_all.py . --url http://localhost:3000
```

If the URL or runtime prerequisites are unavailable, record the blocked validation instead of assuming a pass.
