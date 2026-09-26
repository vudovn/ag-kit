---
name: ag-core
version: 2.0.0
resident: true
triggers: ["always"]
---
# AG Core
Route each request to the smallest capability set.

- Classify intent and task size.
- Choose QUICK, STANDARD, or DEEP only for project-level work.
- Load skills lazily; unload them after their phase.
- Load packs only for relevant technology/domain knowledge.
- Prefer inline work over agent spawn unless specialization or parallelism pays off.
- Read `platform-capabilities.json` before using runtime-specific surfaces.
