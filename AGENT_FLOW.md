# Agent Flow Architecture

> Antigravity Kit request lifecycle and routing contracts

## 1. Request Entry Points

The kit supports two primary entry paths:

| Entry Path | Use When | Result |
|------------|----------|--------|
| Direct request | User asks for implementation, review, debugging, or explanation | Route to the best matching agent |
| Slash command | User invokes `/plan`, `/orchestrate`, `/debug`, and related workflows | Follow the workflow contract first |

## 2. Planning Contract

All non-trivial planning surfaces use one canonical output:

- `docs/PLAN-{task-slug}.md`

The system must not require:
- `docs/PLAN.md`
- `./{task-slug}.md`

If a complex task has no approved plan, create one first and stop for approval before implementation.

## 3. Agent Routing

Use only agents that exist in `.agent/agents/`.

| Domain | Primary Agent | Common Supporting Agents |
|--------|---------------|--------------------------|
| Web UI | `frontend-specialist` | `backend-specialist`, `test-engineer`, `performance-optimizer` |
| Backend/API | `backend-specialist` | `database-architect`, `security-auditor`, `test-engineer` |
| Mobile | `mobile-developer` | `test-engineer`, `security-auditor`, `devops-engineer` |
| Security | `security-auditor` | `penetration-tester`, `backend-specialist` |
| Testing | `test-engineer` | `qa-automation-engineer` |
| Debugging | `debugger` | `explorer-agent`, `code-archaeologist` |
| Discovery | `explorer-agent` | `project-planner`, `code-archaeologist` |
| Planning | `project-planner` | `product-manager`, `product-owner`, `orchestrator` |
| Release / Infra | `devops-engineer` | `test-engineer`, `security-auditor` |
| SEO | `seo-specialist` | `frontend-specialist`, `performance-optimizer` |
| Games | `game-developer` | `test-engineer`, `performance-optimizer` |

## 4. Workflow Commands

| Command | Purpose |
|---------|---------|
| `/brainstorm` | explore options before implementation |
| `/create` | start a new feature or app flow |
| `/debug` | run debugging-oriented analysis |
| `/deploy` | prepare deployment work |
| `/enhance` | improve an existing implementation |
| `/orchestrate` | coordinate multi-agent work |
| `/plan` | create an executable plan |
| `/preview` | preview or expose local output |
| `/status` | inspect current project status |
| `/test` | generate and run tests |
| `/ui-ux-pro-max` | run the design-system workflow backed by shared UI assets |

## 5. Skill Loading

Agents load skills from their own frontmatter. The authoritative source for agent-to-skill mapping is the file in `.agent/agents/`, not this document.

Common examples:
- `frontend-specialist` -> `nextjs-react-expert`, `web-design-guidelines`, `tailwind-patterns`, `frontend-design`
- `backend-specialist` -> `nodejs-best-practices`, `python-patterns`, `api-patterns`, `database-design`
- `test-engineer` -> `testing-patterns`, `tdd-workflow`, `webapp-testing`
- `security-auditor` -> `vulnerability-scanner`, `red-team-tactics`, `api-patterns`
- `orchestrator` -> `parallel-agents`, `behavioral-modes`, `plan-writing`, `architecture`

## 6. Validation Layer

Project-local scripts live in `.agent/scripts/`.

| Script | Purpose |
|--------|---------|
| `auto_preview.py` | start or manage preview exposure |
| `checklist.py` | incremental project validation |
| `session_manager.py` | session/runtime helper |
| `verify_all.py` | full verification suite |

Preferred validation commands:

```bash
python .agent/scripts/checklist.py .
python .agent/scripts/verify_all.py . --url http://localhost:3000
```

If a runtime prerequisite such as a preview URL does not exist, the blocked validation must be reported explicitly.

## 7. Typical Lifecycle

1. Classify the request.
2. Route to the right agent or workflow.
3. Create `docs/PLAN-{task-slug}.md` first for non-trivial work.
4. Execute with the smallest useful specialist set.
5. Run validation.
6. Report changes, evidence, and remaining risks.
