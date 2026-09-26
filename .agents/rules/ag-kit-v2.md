---
trigger: always_on
priority: P0
version: 2.0.0
---
# AG Kit Core

AG Kit keeps one tiny resident core. Everything else is loaded only when intent, project context, and runtime capability require it.

## Session contract
1. Identify intent: plan, build, debug, review, test, deploy, remember, or coordinate.
2. Select the smallest skill set that can complete the task.
3. Load domain packs only when the project needs them.
4. Spawn a specialist agent only when delegation beats doing the work inline.
5. Respect runtime capability tiers; never pretend a runtime supports a surface it does not.
6. For project-level work use the single development flow: FRAME -> SHAPE -> PLAN -> EXECUTE -> VERIFY -> AUDIT -> SHIP.
7. Evidence beats completion claims. Report what passed, failed, or was unavailable.
8. Preserve native runtime security boundaries, approvals, sandboxing, and hooks.

## Modes
- QUICK: FRAME -> PLAN -> EXECUTE -> VERIFY.
- STANDARD: FRAME -> SHAPE -> PLAN -> EXECUTE -> VERIFY -> SHIP.
- DEEP: FRAME -> RECON -> SHAPE -> PLAN -> WAVES -> VERIFY -> CROSS-AUDIT -> SHIP.

## Dispatch
Skills declare deterministic intent triggers. Commands are aliases, not separate workflow engines. Domain knowledge belongs in packs, not resident skills.
