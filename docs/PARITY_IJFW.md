# AG Kit v2 vs IJFW — Functional Parity Map

This tracks architectural/functionality convergence without copying IJFW source code.

| Capability | IJFW pattern | AG Kit v2 |
|---|---|---|
| Tiny resident core | one small always-on core | done: `ag-core` + `shared/core` |
| Hot-loaded skills | trigger-driven capabilities | done: 18 shared skills |
| Shared portable source | shared rules/skills/lib | done: `shared/` + `packs/` |
| Lean native runtime projection | per-platform deployment | done for Antigravity: 18 skills / 4 agents / 0 workflows |
| Runtime tiers | honest platform capability matrix | done for 8 runtimes |
| One workflow spine | plan-before-build phases | done: QUICK/STANDARD/DEEP |
| Wave execution contract | explicit dependency waves | encoded in DEEP mode |
| Local-first memory | human-readable canonical store | done: Markdown canonical store + receipts |
| Warm memory index | rebuildable search acceleration | pending: SQLite FTS optional layer |
| Project team assembly | generated local specialist bench | done: archetype-based team generator |
| Cross-model audit | independent lineages + receipts | partial: roster probe/receipts; execution adapters pending |
| Preflight | blocking ship gates | done: AG Kit-native gates; broader ecosystem gates pending |
| MCP bridge | shared brain for thin runtimes | done: MCP SDK v2 stdio server |
| Runtime installer | project projections | done for 8 targets; MCP config auto-wiring still expanding |
| Native Antigravity | IJFW currently thinner | AG Kit stronger: native rules/skills/agents/hooks/plugin |

## Definition of parity
“100% like IJFW” means matching useful feature classes and discipline while keeping AG Kit’s implementation, naming, stronger Antigravity integration, and independently verified platform contracts. It does not mean copying IJFW source or reproducing unsupported claims.
