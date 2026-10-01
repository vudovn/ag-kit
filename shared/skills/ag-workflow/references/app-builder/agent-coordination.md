# Agent Coordination

> How App Builder orchestrates specialist agents.

## Agent Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                   APP BUILDER (Orchestrator)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PROJECT PLANNER                          │
│  • Task breakdown                                            │
│  • Dependency graph                                          │
│  • File structure planning                                   │
│  • Create {task-slug}.md in project root (MANDATORY)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              CHECKPOINT: PLAN VERIFICATION                   │
│  🔴 VERIFY: Does {task-slug}.md exist in project root?       │
│  🔴 If NO → STOP → Create plan file first                    │
│  🔴 If YES → Proceed to specialist agents                    │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ DATABASE        │ │ BACKEND         │ │ DESIGN SOURCE   │
│ ARCHITECT       │ │ SPECIALIST      │ │ OF TRUTH        │
│                 │ │                 │ │                 │
│ • Schema design │ │ • API routes    │ │ • Read design-  │
│ • Migrations    │ │ • Controllers   │ │   spec & refs   │
│ • Seed data     │ │ • Middleware    │ │ • Create        │
│                 │ │                 │ │   DESIGN.md     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          │                   │                   ▼
          │                   │         ┌─────────────────┐
          │                   │         │ FRONTEND        │
          │                   │         │ SPECIALIST      │
          │                   │         │                 │
          │                   │         │ • UI Components │
          │                   │         │ • Pages         │
          │                   │         │ • Strict tokens │
          │                   │         └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 PARALLEL PHASE (Optional)                    │
│  • Security Auditor → Vulnerability check                   │
│  • Test Engineer → Unit tests                               │
│  • Performance Optimizer → Bundle analysis                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     DEVOPS ENGINEER                          │
│  • Environment setup                                         │
│  • Preview deployment (`python .agents/scripts/auto_preview.py`) │
│  • Health check & report URL                                 │
└─────────────────────────────────────────────────────────────┘
```

## Execution Order

| Phase | Agent(s) / Step | Parallel? | Prerequisite | CHECKPOINT |
|-------|-----------------|-----------|--------------|------------|
| 0 | Socratic Gate | ❌ | - | ✅ Ask 3 questions |
| 1 | Project Planner | ❌ | Questions answered | ✅ **{task-slug}.md created** |
| 1.5 | **PLAN VERIFICATION** | ❌ | {task-slug}.md exists | ✅ **File exists in root** |
| 1.8 | **DESIGN SOURCE-OF-TRUTH** | ❌ | Plan verified (UI projects) | ✅ **DESIGN.md created at root** |
| 2 | Database Architect | ❌ | Plan ready | Schema defined |
| 3 | Backend Specialist | ❌ | Schema ready | API routes created |
| 4 | Frontend Specialist | ✅ | DESIGN.md + API ready (partial) | UI components match tokens |
| 5 | Security Auditor, Test Engineer | ✅ | Code ready | Tests & audit pass |
| 6 | DevOps Engineer | ❌ | All code ready | Deployment & preview ready |

> 🔴 **CRITICAL:** Phase 1.5 and Phase 1.8 are MANDATORY gates.
> - Phase 1.5: No specialist agents proceed without `{task-slug}.md` verification.
> - Phase 1.8: For any project with a UI (web, mobile, desktop), **`DESIGN.md` MUST exist at the project root** before writing UI components or pages (per `@[rules/design-rules]` and `@[skills/design-spec]`). Skip only for headless APIs or CLI tools.

