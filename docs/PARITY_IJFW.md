# AG Kit v2 vs IJFW — Functional Parity Map

This tracks feature-class and architectural convergence without copying IJFW source code. A row marked **done** means AG Kit has an independently implemented equivalent contract; it does not mean identical internals or identical global configuration behavior.

| Capability | IJFW pattern | AG Kit v2 |
|---|---|---|
| Tiny resident core | one small always-on core | **done** — `ag-core` + `shared/core`, machine-capped |
| Hot-loaded skills | trigger-driven capability tree | **done** — 18 shared top-level skills |
| Shared portable source | shared rules/skills/lib | **done** — `shared/` + `packs/` |
| Lean native projection | generated per-platform deployment | **done** — Antigravity is 18 skills / 4 agents / 0 legacy workflows |
| Runtime tiers | honest capability matrix | **done** — 16 targets across first-class / connected / bridge tiers |
| Plan-before-build workflow | explicit phases and sign-off | **done** — QUICK/STANDARD/DEEP session engine; artifact required before approval |
| Deep convergence | dependency waves | **done** — DEEP CONVERGE requires an explicit wave table |
| Local-first memory | human-readable canonical store | **done** — Markdown canonical entries + receipts |
| Warm memory index | rebuildable ranked search | **done** — optional SQLite/FTS5, Markdown fail-open |
| Memory evolution | candidate → durable / supersede / prune | **done** — repeated cross-session references promote candidates; dream archives/deduplicates |
| Temporal facts | valid-at-time recall | **done** — `validFrom` / `validTo` filtering and supersession metadata |
| Dream cycle | periodic consolidation | **done** — explicit `memory dream` lifecycle; scheduling remains host/runtime-owned |
| Project team assembly | local specialist bench | **done** — stack-aware archetype generator under `.ag-kit/agents` |
| Cross-model audit | multiple independent model families | **done** — read-only snapshot execution with calling-lineage exclusion |
| Audit convergence | consensus vs contested | **done** — structured finding parser/clustering + schema-v2 receipts |
| Preflight | blocking ship gates | **done** — AG Kit-native architecture/runtime/CLI/Antigravity gates |
| MCP bridge | one local brain for thin runtimes | **done** — MCP SDK v2 stdio server with deliberately small tool surface |
| Observability | local token/cost dashboard | **done** — explicit JSONL ledger + localhost summary/dashboard |
| Personalization | learn repeated user preferences | **done** — verbatim evidence + two-session confirmation |
| Privacy controls | disclosure log / forget / kill switch | **done** — opt-in injection, egress JSONL, executable forget, `AG_KIT_PROFILE_KILL` |
| Design contract | cross-agent `DESIGN.md` | **done** — 12 templates + nine-section validator |
| Runtime installer | per-runtime projection | **done** — 16 targets; project scope preferred; global-only integrations are staged, not silently mutated |
| Native Antigravity | richer IDE-specific integration | **done / AG Kit strength** — native rules, skills, agents, safety hook, MCP and plugin build |

## Intentional differences

- **No silent user-global writes.** IJFW's one-shot installer mutates several home-directory registries. AG Kit prefers project-scoped adapters and stages explicit snippets when the runtime only exposes a global config.
- **No fabricated token savings.** AG Kit's observability records explicit usage/cache/saved/cost values supplied by an integration; it does not infer savings without evidence.
- **No writable cross-audit mount.** External reviewers receive only a snapshot/diff in a temporary directory.
- **No duplicate canonical runtime trees.** Runtime-specific copies are generated projections; reusable behavior remains in `shared/`.

## Remaining convergence work

These are not required for the current feature-class parity claim, but they are useful follow-ups where AG Kit can become stronger:

1. verified live-injection doctor states (`live`, `standing-by`, `untouched`) for every runtime;
2. v2 runtime uninstall that removes only AG Kit-owned projections while preserving memory by default;
3. optional semantic/cold retrieval provider behind the Markdown + FTS tiers;
4. automatic observability ingestion adapters for runtimes that expose stable usage events;
5. more runtime-specific native projections only when their schemas are stable enough to verify in CI.

“100% like IJFW” in this project means matching useful feature classes and operational discipline while preserving AG Kit's own implementation, names, privacy posture, and stronger Antigravity integration. It does **not** mean copying IJFW source or reproducing unsupported/stale platform claims.
