---
name: contextual-memory
description: Protocols for maintaining rich context across long sessions and multi-session work — session snapshots, CODEBASE.md maintenance, context anchors, and drift prevention.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# Contextual Memory Skill

> Never lose state. Never drift from established decisions. Work as if you remember everything.

---

## Memory Hierarchy

| Layer | Storage | Persist | Use For |
|-------|---------|---------|---------|
| **Hot** | Context window | This session | Active task context |
| **Warm** | `CODEBASE.md` | Permanent | Architecture, stack, decisions |
| **Cold** | `{task-slug}.md` | Per-task | Task plan, progress, decisions |

---

## CODEBASE.md Protocol

### When to Update

- After any architectural decision
- After adding a new dependency
- After changing a pattern (e.g., switching from REST to GraphQL)
- After defining a new shared abstraction

### Template

```markdown
# CODEBASE.md — Project Memory

## Stack
- Frontend: [framework, version]
- Backend: [framework, version]
- Database: [DB + ORM]
- Auth: [provider]
- Hosting: [platform]

## Architecture Decisions
- [Date]: [Decision] — Reason: [why]
- [Date]: [Decision] — Reason: [why]

## Established Patterns
- API: [REST/GraphQL/tRPC]
- State: [Zustand/Redux/Context]
- Styling: [Tailwind/CSS Modules]
- Testing: [Jest/Vitest + Playwright]

## File Map (Key Files)
- Auth: `src/lib/auth.ts`
- DB Client: `src/lib/db.ts`
- API Routes: `src/app/api/`

## Active Tasks
- [task-slug].md: [status]
```

---

## Session Start Protocol

```
1. Check if CODEBASE.md exists → Read it
2. Check for incomplete {task-slug}.md files → Read them
3. Read ARCHITECTURE.md for agent/skill map
4. Summarize state: "I recall we're using X
   with Y pattern. Shall I continue [task] or start fresh?"
```

---

## Context Anchor Pattern

After any important decision, emit a Context Anchor:

```
🔒 Context Anchor: We decided to use [X] because [Y].
   This affects: [list of files/modules]
   Do NOT change this without explicit user confirmation.
```

---

## Context Drift Prevention

```
IF current action contradicts established context:
  STOP
  SURFACE: "I notice this would change [X] which was decided on [date].
            Should I update the pattern or keep consistency?"
  WAIT for user confirmation
  PROCEED only after confirmation
```
