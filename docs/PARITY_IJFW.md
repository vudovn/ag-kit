# AG Kit v2 vs IJFW — Functional Parity Map

This tracks architectural/functionality convergence without copying IJFW source code.

| Capability | IJFW pattern | AG Kit v2 |
|---|---|---|
| Tiny resident core | one small always-on core | done: `ag-core` + `shared/core` |
| Hot-loaded skills | trigger-driven capabilities | done: 18 shared skills |
| Shared portable source | shared rules/skills/lib | done: `shared/` + `packs/` |
| Lean native runtime projection | per-platform deployment | done for Antigravity: 18 skills / 4 agents / 0 workflows |
| Runtime tiers | honest platform capability matrix | done for 12 runtimes |
| One workflow spine | plan-before-build phases | done: QUICK/STANDARD/DEEP |
| Wave execution contract | explicit dependency waves | encoded in DEEP mode |
| Local-first memory | human-readable canonical store | done: Markdown canonical store + receipts |
| Warm memory index | rebuildable search acceleration | done: optional SQLite/FTS5 with Markdown fail-open |
| Project team assembly | generated local specialist bench | done: stack-aware archetype generator |
| Cross-model audit | independent lineages + receipts | done: read-only snapshot execution for reachable headless reviewers |
| Preflight | blocking ship gates | done: AG Kit-native gates; ecosystem-specific advisory gates can remain runtime/project-owned |
| MCP bridge | shared brain for thin runtimes | done: MCP SDK v2 stdio server |
| Runtime installer | project projections | done for 12 targets; user-global registries are intentionally never mutated silently |
| Native Antigravity | IJFW currently thinner | AG Kit stronger: native rules/skills/agents/hooks/plugin |

“100% like IJFW” here means matching useful feature classes and discipline while keeping AG Kit’s own implementation, naming, stronger Antigravity integration, and independently verified platform contracts. It does not mean copying IJFW source or reproducing stale/unsupported platform claims.
