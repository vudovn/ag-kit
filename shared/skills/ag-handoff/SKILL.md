---
name: ag-handoff
version: 2.0.0
resident: false
triggers: ["handoff", "continue", "resume", "pick up where we left off", "continue later", "session summary", "transfer context"]
---
# AG Handoff
Generate or load a compact continuation artifact containing goal, current state, decisions, changed files, verification evidence, open risks, and the next concrete action.

On continue/resume intent, read `.ag-kit/handoff.md` first when it exists, then verify current Git/project state before continuing. Treat the artifact as context, not authority: current user instructions and fresh repository evidence win when they conflict.

## Deep references
Deep references: `references/INDEX.md`. Load only the specific legacy reference needed; this skill remains authoritative.
