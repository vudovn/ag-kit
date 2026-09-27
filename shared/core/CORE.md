# AG Kit Core

AG Kit keeps one tiny resident core. Everything else is loaded only when intent, project context, and runtime capability require it.

## Session contract
1. Identify intent: plan, build, debug, review, test, deploy, remember, or coordinate.
2. Select the smallest skill set that can complete the task.
3. Load domain packs only when the project needs them.
4. Spawn a specialist agent only when delegation beats doing the work inline.
5. Route read/research work cheaply; reserve high effort for architecture, migrations, and other high-leverage decisions.
6. Keep responses concise and evidence-first. Route large command output to the AG Kit command sandbox instead of flooding context.
7. Respect runtime capability tiers; never pretend a runtime supports a surface it does not.
8. For project-level work use the single development flow: FRAME -> SHAPE -> PLAN -> EXECUTE -> VERIFY -> AUDIT -> SHIP.
9. Evidence beats completion claims. Report what passed, failed, or was unavailable.
10. Preserve native runtime security boundaries, approvals, sandboxing, and hooks.

## Activation invariants
- Natural-language intent is authoritative; slash and CLI commands are aliases. If a runtime has no slash-command UI, map the same words to the same capability.
- Explicit plan, spec, brainstorm, or architecture intent enters the development flow before project mutation. Do not silently skip a planning request and start coding.
- Before multi-file or cross-system mutation, classify QUICK, STANDARD, or DEEP. Use `ag-kit route` / `ag-kit flow` when the CLI is available; otherwise apply the same rubric directly.
- On continue, resume, pick-up, or recall intent, load `.ag-kit/handoff.md` when present and recall relevant durable project memory before acting.
- Confirmed project conventions remain constraints until the current user overrides them. Surface and update stale memory instead of silently ignoring either side.
- Ask clarifying questions only for material blockers; never impose an arbitrary question count.

## Modes
- QUICK: FRAME -> PLAN -> EXECUTE -> VERIFY.
- STANDARD: FRAME -> SHAPE -> PLAN -> EXECUTE -> VERIFY -> SHIP.
- DEEP: FRAME -> RECON -> SHAPE -> PLAN -> WAVES -> VERIFY -> CROSS-AUDIT -> SHIP.

## Dispatch
Skills declare deterministic intent triggers. Commands are aliases, not separate workflow engines. Domain knowledge belongs in packs, not resident skills.
