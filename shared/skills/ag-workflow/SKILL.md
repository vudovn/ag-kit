---
name: ag-workflow
version: 2.0.0
resident: false
triggers: ["plan", "plan this", "spec", "spec this", "brainstorm", "architect", "architecture", "build this", "new project", "major refactor", "launch", "launch this"]
---
# AG Workflow
Run the single project workflow engine.

QUICK: FRAME -> PLAN -> EXECUTE -> VERIFY.
STANDARD: FRAME -> SHAPE -> PLAN -> EXECUTE -> VERIFY -> SHIP.
DEEP: FRAME -> RECON -> SHAPE -> PLAN -> WAVES -> VERIFY -> CROSS-AUDIT -> SHIP.

Explicit planning, spec, brainstorm, or architecture intent is a gate: produce and confirm the plan artifact before implementation. Natural-language intent must activate this skill even when the runtime has no slash-command UI.

Plans must be explicit before destructive or multi-file implementation. Wave execution labels work PARALLEL or SEQUENTIAL with a dependency reason.
