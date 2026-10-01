# AG Kit v2 vs IJFW — Functional Parity Map

This tracks feature-class and architectural convergence without copying IJFW source code. **Done** means AG Kit has an independently implemented and testable equivalent contract; it does not imply identical internals or identical configuration behavior.

| Capability | IJFW pattern | AG Kit v2 |
|---|---|---|
| Tiny resident core | one small always-on core | **done** — `ag-core` + `shared/core`, machine-capped |
| Hot-loaded skills | trigger-driven capability tree | **done** — 18 shared top-level skills |
| Shared portable source | shared rules/skills/lib | **done** — `shared/` + `packs/` |
| Lean runtime projections | generated per-platform deployment | **done** — capability-aware adapters under `runtimes/`; generated host trees are outputs |
| Runtime tiers | honest capability matrix | **done** — 16 targets across first-class / connected / bridge tiers |
| No primary runtime | shared core independent of one host | **done** — repository contract rejects primary-runtime declarations and runtime-specific root gates |
| One-install discovery | detect tools already present | **done** — `runtime detect` + `runtime install-present`; no `gh == Copilot` false-positive |
| Verified injection states | live / standing-by / untouched | **done** — lifecycle manifests + digest/marker/MCP doctor checks |
| Safe uninstall | remove only framework-owned state | **done** — restores backups, strips owned blocks/MCP keys, preserves drift and memory |
| Prompt quality gate | deterministic ambiguity check before subjective work | **portable core done** — `prompt-check` + MCP `ag_prompt_check`; verified automatic interception is wired for Claude, Gemini, and Qwen, with raw-prompt provenance rules and no raw-prompt persistence |
| Plan-before-build workflow | explicit phases and sign-off | **done** — QUICK/STANDARD/DEEP session engine; artifact required before approval |
| Deep convergence | dependency waves | **done** — DEEP convergence requires an explicit wave table |
| Local-first memory | human-readable canonical store | **done** — Markdown canonical entries + receipts |
| Warm memory index | rebuildable ranked search | **done** — optional SQLite/FTS5, Markdown fail-open |
| Semantic cold retrieval | optional local vector retrieval behind canonical memory | **done, opt-in** — project-local Transformers.js provider install, explicit model-download approval, rebuildable vector index, no raw memory stored in the index |
| Memory evolution | candidate → durable / supersede / prune | **done** — repeated cross-session references promote candidates; dream archives/deduplicates |
| Temporal facts | valid-at-time recall | **done** — `validFrom` / `validTo` filtering and supersession metadata |
| Cross-project brain | one brain across projects/tools | **done** — explicit opt-in registry + strictly read-only cross-project Markdown search |
| Dream cycle | periodic consolidation | **done** — explicit `memory dream`; scheduling remains host/runtime-owned |
| Project team assembly | local specialist bench | **done** — stack-aware archetype generator under `.ag-kit/agents` |
| Cross-model audit | multiple independent model families | **done** — read-only snapshot execution with calling-lineage exclusion and bounded parallel lineages |
| Audit convergence | consensus vs contested | **done** — structured finding parser/clustering + receipts |
| Preflight | blocking ship gates | **done** — runtime-neutral architecture/docs/engine/runtime/CLI gates |
| MCP bridge | one local brain for thin runtimes | **done** — MCP SDK v2 stdio server; project and opt-in cross-project recall |
| Smart routing | cheap reads / strong high-leverage work | **done** — runtime-neutral role + effort + flow routing, without vendor model lock-in |
| Command sandbox | keep large output off-context | **done** — full output on disk, bounded summary in context, no shell interpolation |
| Compression | shrink context artifacts | **done** — deterministic Markdown compaction with measured byte reduction; non-destructive by default |
| Session handoff | compact continuity artifact | **done** — goal/state/decisions/changed files/evidence/risks/next action + archives |
| Observability | local token/cost dashboard | **done** — bounded rotating JSONL ledger + localhost dashboard + measured-only methodology + trace rollups |
| Native event ingestion | runtime hooks feed observability | **done by verified surface** — bounded metadata-only normalizer; adapters project automatic ingestion only where a stable hook/event contract is independently verified and tested |
| Benchmark receipts | reproducible evidence instead of marketing claims | **done as blocking CI evidence** — deterministic memory, routing, lifecycle, and compression fixtures emit a head-addressed JSON receipt that CI uploads as an immutable artifact; provider/model arms remain optional and separate |
| Personalization | learn repeated user preferences | **done** — verbatim evidence + two-session confirmation |
| Privacy controls | disclosure log / forget / kill switch | **done** — opt-in injection, egress JSONL, purge-on-forget, `AG_KIT_PROFILE_KILL` |
| Design contract | cross-agent `DESIGN.md` | **done** — 12 templates + nine-section validator |
| Host-native extensions | exploit richer runtime surfaces without coupling the core | **done by adapter** — e.g. Antigravity hooks/plugin packaging, Claude agents/hooks, Codex plugin/MCP where declared by the capability matrix |
| Security dependency gate | fail release on vulnerable prod deps | **done** — CI audit remains blocking |

## Intentional differences

- **No silent user-global writes.** AG Kit prefers project-scoped adapters and stages explicit snippets when a runtime only exposes global configuration.
- **No fabricated token savings.** Observability records measured/supplied values and reports byte reduction for compression; it does not invent a “without AG Kit” multiplier.
- **No writable cross-audit mount.** External reviewers receive only a snapshot/diff in a temporary directory.
- **No automatic home-directory memory crawl.** Cross-project memory is opt-in per project, realpath-contained, bounded, and can be disabled with `AG_KIT_MINIMAL` or `AG_KIT_NO_CROSS_PROJECT`.
- **No duplicate canonical runtime trees.** Runtime-specific copies are generated projections; reusable behavior remains in `shared/`.
- **No primary runtime.** Rich host-native surfaces stay behind adapter boundaries instead of defining the product architecture.
- **No capability-by-badge.** Detection, lifecycle manifests, adapter contracts, and doctor checks distinguish installed/live, staged/standing-by, and untouched states.
- **No raw-prompt telemetry from prompt quality checks.** The checker returns only bounded structural metadata, signals, and clarification questions.
- **No implicit semantic-provider or model download.** The CLI stays lean; project-local provider install and model download require separate explicit network approvals.
- **No paid-provider benchmark in the default release gate.** Core benchmark evidence is deterministic and local; provider/model experiments must stay explicit, cost-capped, and non-blocking unless a future release contract deliberately changes that policy.

## Remaining convergence work

These are strengthening areas, not reasons to inflate the resident core:

1. expand automatic prompt-quality interception beyond Claude, Gemini, and Qwen only when another runtime’s user-prompt hook/event contract is current, project-safe, provenance-safe, and independently tested;
2. optionally extend deterministic benchmark receipts into an explicit cost-capped multi-arm provider benchmark without turning provider spend into a default requirement;
3. keep runtime schemas current and promote bridge targets only when their native contracts justify it;
4. add more adapter-specific artifact builders only when a host has a real package/plugin artifact worth building, rather than manufacturing parity.

“100% like IJFW” here means matching useful feature classes and multi-runtime operational discipline while preserving AG Kit's own implementation, names, privacy posture, and capability-aware adapter model. It does **not** mean copying IJFW source or forcing vendor-specific behavior onto runtimes that cannot independently support it.
