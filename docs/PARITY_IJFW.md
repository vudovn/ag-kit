# AG Kit v2 vs IJFW — Functional Parity Map

This tracks feature-class and architectural convergence without copying IJFW source code. **Done** means AG Kit has an independently implemented and testable equivalent contract; it does not imply identical internals or identical configuration behavior.

| Capability | IJFW pattern | AG Kit v2 |
|---|---|---|
| Tiny resident core | one small always-on core | **done** — `ag-core` + `shared/core`, machine-capped |
| Hot-loaded skills | trigger-driven capability tree | **done** — 18 shared top-level skills |
| Shared portable source | shared rules/skills/lib | **done** — `shared/` + `packs/` |
| Lean native projection | generated per-platform deployment | **done** — Antigravity is 18 skills / 4 agents / 0 legacy workflows |
| Runtime tiers | honest capability matrix | **done** — 16 targets across first-class / connected / bridge tiers |
| One-install discovery | detect tools already present | **done** — `runtime detect` + `runtime install-present`; no `gh == Copilot` false-positive |
| Verified injection states | live / standing-by / untouched | **done** — lifecycle manifests + digest/marker/MCP doctor checks |
| Safe uninstall | remove only framework-owned state | **done** — restores backups, strips owned blocks/MCP keys, preserves drift and memory |
| Plan-before-build workflow | explicit phases and sign-off | **done** — QUICK/STANDARD/DEEP session engine; artifact required before approval |
| Deep convergence | dependency waves | **done** — DEEP convergence requires an explicit wave table |
| Local-first memory | human-readable canonical store | **done** — Markdown canonical entries + receipts |
| Warm memory index | rebuildable ranked search | **done** — optional SQLite/FTS5, Markdown fail-open |
| Memory evolution | candidate → durable / supersede / prune | **done** — repeated cross-session references promote candidates; dream archives/deduplicates |
| Temporal facts | valid-at-time recall | **done** — `validFrom` / `validTo` filtering and supersession metadata |
| Cross-project brain | one brain across projects/tools | **done** — explicit opt-in registry + strictly read-only cross-project Markdown search |
| Dream cycle | periodic consolidation | **done** — explicit `memory dream`; scheduling remains host/runtime-owned |
| Project team assembly | local specialist bench | **done** — stack-aware archetype generator under `.ag-kit/agents` |
| Cross-model audit | multiple independent model families | **done** — read-only snapshot execution with calling-lineage exclusion |
| Audit convergence | consensus vs contested | **done** — structured finding parser/clustering + receipts |
| Preflight | blocking ship gates | **done** — AG Kit-native architecture/runtime/CLI/Antigravity gates |
| MCP bridge | one local brain for thin runtimes | **done** — MCP SDK v2 stdio server; project and opt-in cross-project recall |
| Smart routing | cheap reads / strong high-leverage work | **done** — runtime-neutral role + effort + flow routing, without vendor model lock-in |
| Command sandbox | keep large output off-context | **done** — full output on disk, bounded summary in context, no shell interpolation |
| Compression | shrink context artifacts | **done** — deterministic Markdown compaction with measured byte reduction; non-destructive by default |
| Session handoff | compact continuity artifact | **done** — goal/state/decisions/changed files/evidence/risks/next action + archives |
| Observability | local token/cost dashboard | **done** — bounded rotating JSONL ledger + localhost dashboard + measured-only methodology |
| Native event ingestion | runtime hooks feed observability | **partial by verified surface** — Antigravity `PostToolUse` auto-ingestion is privacy-minimal/fail-open; other runtimes remain adapter-owned until stable contracts are verified |
| Personalization | learn repeated user preferences | **done** — verbatim evidence + two-session confirmation |
| Privacy controls | disclosure log / forget / kill switch | **done** — opt-in injection, egress JSONL, purge-on-forget, `AG_KIT_PROFILE_KILL` |
| Design contract | cross-agent `DESIGN.md` | **done** — 12 templates + nine-section validator |
| Native Antigravity | richer IDE-specific integration | **done / AG Kit strength** — native rules, skills, agents, safety + observability hooks, MCP and plugin build |
| Security dependency gate | fail release on vulnerable prod deps | **done** — CI audit kept blocking; Next.js moved to the patched 16.3.3 security release |

## Intentional differences

- **No silent user-global writes.** AG Kit prefers project-scoped adapters and stages explicit snippets when a runtime only exposes global configuration.
- **No fabricated token savings.** Observability records measured/supplied values and reports byte reduction for compression; it does not invent a “without AG Kit” multiplier.
- **No writable cross-audit mount.** External reviewers receive only a snapshot/diff in a temporary directory.
- **No automatic home-directory memory crawl.** Cross-project memory is opt-in per project, realpath-contained, bounded, and can be disabled with `AG_KIT_MINIMAL` or `AG_KIT_NO_CROSS_PROJECT`.
- **No duplicate canonical runtime trees.** Runtime-specific copies are generated projections; reusable behavior remains in `shared/`.
- **No capability-by-badge.** Detection, lifecycle manifests and doctor checks distinguish installed/live, staged/standing-by and untouched states.

## Remaining convergence work

These are optional strengthening areas, not reasons to inflate the resident core:

1. add automatic observability adapters only for runtimes whose hook/event contracts can be verified and tested;
2. optionally add a local semantic/cold retrieval provider behind Markdown + FTS without making it canonical or mandatory;
3. expand benchmark/field-test coverage so memory, routing and context-reduction claims have reproducible project-level receipts;
4. keep runtime schemas current and promote bridge targets only when their native contracts justify it.

“100% like IJFW” here means matching useful feature classes and operational discipline while preserving AG Kit's own implementation, names, privacy posture, and stronger Antigravity integration. It does **not** mean copying IJFW source or reproducing vendor-specific behavior that cannot be independently verified.
