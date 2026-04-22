---
description: Create project plan using project-planner agent. No code writing - only plan file generation.
---

# /plan - Project Planning Mode

$ARGUMENTS

---

## Rules

1. Planning only. Do not write implementation code.
2. Use the `project-planner` agent.
3. Output must be `docs/PLAN-{task-slug}.md`.
4. Report the exact file path created.

## Task

Use the `project-planner` agent with this context:

```text
CONTEXT:
- User Request: $ARGUMENTS
- Mode: planning only
- Output contract: docs/PLAN-{task-slug}.md

RULES:
1. Read repository context that exists (`README.md`, `AGENT_FLOW.md`, `.agent/ARCHITECTURE.md`, relevant plan files)
2. Ask concise clarifying questions only if material information is missing
3. Use only real agents, skills, and scripts from this repository
4. Create a plan with executable tasks and explicit verification steps
5. Do not create code files
6. Report the exact plan path created
```

## Expected Output

- `docs/PLAN-{task-slug}.md`
- task breakdown with owners and verification
- `Phase X` verification checklist
