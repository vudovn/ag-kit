# Migrating to AG Kit v2

AG Kit v2 replaces the old Antigravity-centered managed-tree CLI with one runtime-neutral lifecycle. This guide is for projects upgrading from the `2026.8.31` generation or earlier.

The important change is structural: there is no second `init/update/rollback/status` lifecycle anymore. Every host, including Antigravity, is installed and verified through `ag-kit runtime ...`.

## What changes in v2

- `shared/` is the canonical runtime-neutral source of truth.
- `packs/` holds cold domain/reference knowledge.
- `runtimes/<runtime>/` contains thin capability-aware adapters.
- Generated host trees such as `.agents/`, `.claude/`, `.gemini/`, managed instruction files, and plugin folders are projections, not canonical implementations.
- The resident surface is **1 core, 18 hot-loaded skills, 4 permanent agents, 1 development spine**.
- Legacy `.agents/workflows/` is gone. QUICK, STANDARD, and DEEP are modes of one flow engine.
- No runtime is the product's primary runtime.

## Before migrating

1. Commit or stash project work.
2. Make an external backup if the project contains important runtime-specific customizations.
3. Install the v2 CLI.
4. Detect the runtimes already present:

```bash
ag-kit runtime detect
```

If the project was an older Antigravity-only AG Kit installation, do **not** run the removed managed-tree commands. Install the Antigravity adapter through the unified lifecycle:

```bash
ag-kit runtime install antigravity
ag-kit runtime doctor antigravity
```

During a pre-release review, use the reviewed branch/ref explicitly:

```bash
ag-kit runtime install antigravity --branch <reviewed-ref>
```

After a release tag exists, omit `--branch`; the published CLI resolves runtime source from its matching `v<CLI_VERSION>` tag.

## Migrate additional runtimes

Install detected runtimes in one pass:

```bash
ag-kit runtime install-present
ag-kit runtime doctor
```

Or install adapters explicitly:

```bash
ag-kit runtime install claude
ag-kit runtime install codex
ag-kit runtime install gemini
```

Each runtime install records ownership/lifecycle state under `.ag-kit/runtime-installs/` and snapshots paths the adapter is about to touch. Project-scoped config is preferred. Integrations that only expose user-global configuration are staged for explicit activation instead of being silently mutated.

## Existing `.agents` customizations

An older project may already contain `.agents/` files that are not owned by AG Kit. Keep them backed up/committed before migration.

The v2 Antigravity adapter treats `.agents/` as a runtime projection. Lifecycle state and backups are used so doctor/uninstall can distinguish AG Kit-managed projection state from later user drift. The release smoke test specifically covers a pre-existing user-owned file under `.agents/` and verifies it survives install/uninstall.

Do not manually copy the Antigravity tree into other runtime folders. Use the matching adapter.

## Memory and continuity

Initialize project memory after or before installing runtime projections:

```bash
ag-kit memory init
ag-kit memory status
ag-kit memory recall "package manager"
ag-kit handoff quick "Paused after verification" --next "Review remaining issues"
ag-kit handoff show
```

Markdown under `.ag-kit/memory/` is canonical. SQLite/FTS5 and the optional local semantic tier are rebuildable acceleration layers only.

For large context artifacts:

```bash
ag-kit compress docs/long-context.md
```

Compression writes a separate compact artifact by default. `--write` is explicit and creates a backup before replacement.

## Workflow migration

Do **not** recreate `.agents/workflows/` or depend on old `/coordinate`, `/orchestrate`, `/plan`, or similar v1 workflow files.

Use natural-language intent or the flow CLI:

```bash
ag-kit flow start "Ship account recovery" --mode standard
ag-kit flow artifact "Compared approaches and selected signed one-time tokens"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

Modes:

- QUICK: FRAME → PLAN → EXECUTE → VERIFY
- STANDARD: FRAME → SHAPE → PLAN → EXECUTE → VERIFY → SHIP
- DEEP: FRAME → RECON → SHAPE → PLAN → WAVES → VERIFY → CROSS_AUDIT → SHIP

User gates do not auto-advance. Verification boundaries require fresh mechanical evidence.

## MCP migration

The v2 MCP bridge is served by the CLI:

```bash
ag-kit mcp serve
```

Verified project-scoped adapters wire the MCP entry where supported. Check actual lifecycle/wiring state with:

```bash
ag-kit runtime doctor
```

## Runtime projection examples

- Antigravity → `.agents/`
- Claude → `.claude/` plus managed `CLAUDE.md`
- Codex → managed `AGENTS.md` plus `.codex-plugin/`
- Gemini → `.gemini/` plus managed `GEMINI.md`

Host-specific hooks/plugins stay inside their adapter boundary. Richer native surfaces do not make a runtime primary.

## Validation after migration

For a consumer project:

```bash
ag-kit runtime doctor
ag-kit memory status
ag-kit preflight
```

For AG Kit repository development:

```bash
npm run check:v2
npm run check:docs
npm run test:v2
npm run benchmark:v2 -- --output dist/evidence/benchmark-v2.json
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

## Rollback / removal in v2

There is no generic managed-tree rollback command in v2.

To remove one runtime adapter:

```bash
ag-kit runtime uninstall <runtime>
```

Uninstall uses lifecycle ownership metadata and pre-install backups. It restores/removes only state whose ownership can be proven, preserves user drift, and keeps `.ag-kit/memory/` by default.

If a migration needs to be reverted beyond adapter-owned state, use the project backup or version-control commit created before migration. This is intentionally clearer than maintaining a second hidden lifecycle alongside runtime adapters.

## Compatibility notes

| Area | v2 behavior |
| --- | --- |
| Canonical source | `shared/` + `packs/` |
| Runtime implementation | `runtimes/<runtime>/` adapters |
| Host trees | generated/managed projections |
| Primary runtime | none |
| Lifecycle | one `runtime install/doctor/uninstall` model |
| Legacy managed-tree CLI | removed |
| Legacy workflow files | removed; one flow engine replaces them |
| Slash-command dependency | removed; natural-language intent is first-class |
| Memory | local Markdown canonical store under `.ag-kit/` |
| Runtime config | project-scoped when verified; global-only changes are explicit |
| Runtime uninstall | ownership-aware; preserves user drift and memory |
| Cross-project memory | opt-in registry only; no automatic `$HOME` crawl |

Historical pre-v2 behavior remains available in Git history and the changelog. New work should not restore the old Antigravity-only CLI, duplicate canonical runtime trees, or silently mutate user-global configuration.
