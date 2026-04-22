---
description: Coordinate multiple agents for complex tasks. Use for multi-perspective analysis, comprehensive reviews, or tasks requiring different domain expertise.
---

# Multi-Agent Orchestration

You are now in **ORCHESTRATION MODE**. Coordinate the right specialists to solve this problem:

$ARGUMENTS

---

## Rules

1. Use orchestration only when the task actually spans multiple domains or stages.
2. Use the minimum specialist set that fits the task.
3. Use only agents that exist in this repository.
4. Start with planning if no approved plan exists.

## 2-Phase Flow

### Phase 1: Planning

| Step | Agent | Action |
|------|-------|--------|
| 1 | `project-planner` | Create `docs/PLAN-{task-slug}.md` |
| 2 | `explorer-agent` | Optional discovery if the codebase shape is still unclear |

After planning, report the exact file path and ask whether to proceed with implementation.

### Phase 2: Implementation

Select the specialists that match the approved plan. Typical patterns:
- web delivery: `frontend-specialist`, `backend-specialist`, `test-engineer`
- backend/API: `backend-specialist`, `security-auditor`, `test-engineer`
- debugging: `debugger`, `explorer-agent`, `test-engineer`
- release flow: domain specialist, `test-engineer`, `devops-engineer`

## Available Agents

| Agent | Domain | Use When |
|-------|--------|----------|
| `project-planner` | Planning | task breakdown, milestones |
| `explorer-agent` | Discovery | codebase mapping |
| `frontend-specialist` | Frontend | React, Next.js, UI systems |
| `backend-specialist` | Backend | API, server, services |
| `database-architect` | Database | schema, migrations, queries |
| `security-auditor` | Security | auth, review, vulnerabilities |
| `penetration-tester` | Security Testing | active testing |
| `test-engineer` | Testing | unit, integration, E2E |
| `qa-automation-engineer` | QA Automation | browser and QA flows |
| `devops-engineer` | Ops | CI/CD, deploy, infra |
| `mobile-developer` | Mobile | React Native, Flutter, mobile UX |
| `performance-optimizer` | Performance | profiling and optimization |
| `seo-specialist` | SEO | search visibility |
| `documentation-writer` | Documentation | docs when needed |
| `debugger` | Debug | root-cause analysis |
| `code-archaeologist` | Legacy | brownfield analysis |
| `product-manager` | Product | requirements framing |
| `product-owner` | Product | scope and backlog decisions |
| `game-developer` | Games | game-specific work |

## Execution Protocol

1. Detect whether an approved `docs/PLAN-*.md` exists for the task.
2. If not, go to Phase 1 and stop after the plan is created.
3. If yes, invoke only the specialists required by that plan.
4. Pass full context into every specialist handoff:
   - original user request
   - decisions already made
   - current plan state
   - relevant files and constraints
5. Run the project-local verification that fits the task:

```bash
python .agent/scripts/checklist.py .
python .agent/scripts/verify_all.py . --url http://localhost:3000
```

If runtime prerequisites are missing, record the blocked validation explicitly.

## Output Format

```markdown
## Orchestration Report

### Task
[summary]

### Plan
[docs/PLAN-{task-slug}.md or existing approved plan]

### Agents Invoked
| Agent | Focus | Status |
|-------|-------|--------|
| frontend-specialist | UI implementation | ✅ |

### Validation
- checklist.py: pass/fail
- verify_all.py: pass/fail or blocked reason

### Key Findings
- finding 1
- finding 2

### Remaining Risks
- risk 1
```
