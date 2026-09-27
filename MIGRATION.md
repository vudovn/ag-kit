# Migrating to AG Kit v2

AG Kit v2 replaces the old prompt-heavy Antigravity-only layout with a lean multi-runtime operating layer. This guide is for projects upgrading from the `2026.8.31` generation or earlier.

The migration is intentionally non-destructive: existing user files and locally modified managed files are preserved by the default merge strategy, runtime lifecycle writes are project-scoped where possible, and AG Kit-owned state lives under `.ag-kit/`.

## What changes in v2

### Architecture

- `shared/` is the canonical runtime-neutral source of truth.
- `packs/` holds domain reference knowledge that loads only when relevant.
- `.agents/` is the native Antigravity projection, not a second canonical implementation.
- The resident surface is deliberately small: **1 core, 18 hot-loaded skills, 4 permanent agents, 1 development spine**.
- Legacy `.agents/workflows/` files are removed. QUICK, STANDARD, and DEEP are modes of one flow engine rather than separate slash-command workflows.

### Activation model

Natural-language intent is authoritative. Slash commands and CLI commands are aliases, not a requirement for the runtime to support a slash-command UI.

Examples:

- `plan this`, `spec this`, `brainstorm`, or `architecture` enters the development flow before multi-file implementation;
- `continue`, `resume`, or `pick up where we left off` loads the latest handoff and relevant durable project memory before mutation;
- a current user instruction overrides stale memory, and AG Kit should surface/update the conflict rather than silently choosing one side.

### Runtime model

AG Kit declares 16 runtime targets across first-class, connected, and bridge tiers. Installation is capability-aware rather than pretending every tool has identical native surfaces.

```bash
ag-kit runtime list
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

Use a single-runtime install when you want explicit control:

```bash
ag-kit runtime install antigravity
ag-kit runtime install claude
ag-kit runtime install codex
```

AG Kit refuses filesystem root and the user home directory as project targets. Integrations that only expose user-global configuration are staged for explicit activation instead of being silently mutated.

## Before upgrading

1. Commit or stash project work.
2. Install the current CLI build/release.
3. Preview the legacy managed-tree update:

```bash
ag-kit update --dry-run
```

4. Review local modifications and any reported conflicts.

The default `merge` strategy preserves user-owned files and locally modified managed files. Use `--strategy replace` only when you intentionally want the upstream `.agents/` tree and have reviewed the backup behavior.

## Upgrade an existing Antigravity project

Apply the safe managed-tree migration:

```bash
ag-kit update
```

Then inspect and activate the runtimes already present on the machine/project:

```bash
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

`runtime install-present` only operates on detected targets. Lifecycle manifests and pre-install backups are written under `.ag-kit/` so doctor/uninstall can distinguish AG Kit-owned state from later user drift.

## Project memory and continuity

Initialize the v2 project memory store:

```bash
ag-kit memory init
ag-kit memory status
```

Markdown under `.ag-kit/memory/` is canonical. The optional SQLite/FTS5 index is rebuildable acceleration only.

Useful continuity commands:

```bash
ag-kit memory recall "package manager"
ag-kit handoff create --goal "Continue the release" --state "Core implementation complete" --next "Run final preflight"
ag-kit handoff show
ag-kit handoff quick "Paused after verification" --next "Review remaining issues"
```

The current handoff lives at `.ag-kit/handoff.md`; older handoffs are archived. Resume intent should read the handoff, then verify current Git/project state before acting.

For large Markdown/context artifacts:

```bash
ag-kit compress docs/long-context.md
```

Compression writes a separate compact artifact by default. `--write` is explicit and creates a timestamped backup before replacing the source.

## Workflow migration

Do **not** recreate the old workflow directory or depend on `/coordinate`, `/orchestrate`, `/plan`, or similar slash files being discoverable.

Use natural-language intent or the v2 CLI flow:

```bash
ag-kit flow start "Ship account recovery" --mode standard
ag-kit flow artifact "Compared approaches and selected signed one-time tokens"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

The modes are:

- QUICK: FRAME → PLAN → EXECUTE → VERIFY
- STANDARD: FRAME → SHAPE → PLAN → EXECUTE → VERIFY → SHIP
- DEEP: FRAME → RECON → SHAPE → PLAN → WAVES → VERIFY → CROSS-AUDIT → SHIP

User gates do not auto-advance. DEEP mode requires an explicit dependency-wave table before execution convergence.

## MCP migration

The v2 MCP bridge is served by the CLI:

```bash
ag-kit mcp serve
```

Verified project-scoped runtime adapters wire the AG Kit MCP entry where their configuration format supports it. There is no migration step that blindly copies MCP configuration into the user home directory.

Check actual wiring with:

```bash
ag-kit runtime doctor
```

## Antigravity migration

The v2 Antigravity projection contains:

- `.agents/rules/ag-kit-v2.md` — always-on lean core;
- `.agents/skills/` — 18 hot-loaded skills;
- `.agents/agents/` — scout, architect, builder, reviewer;
- `.agents/hooks.json` plus native hook scripts;
- `.agents/mcp_config.json`;
- native plugin packaging support;
- **no legacy `.agents/workflows/` directory**.

The `PreToolUse` safety hook blocks only high-confidence destructive root/disk operations. The `PostToolUse` observability hook records bounded metadata and must never block the agent loop.

Smoke-test the safety hook with a mocked payload, never a real destructive command:

```bash
printf '%s' '{"toolCall":{"name":"run_command","args":{"CommandLine":"rm -rf /"}}}' \
  | node .agents/hooks/validate-tool-call.mjs
```

Expected output is a JSON deny decision.

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
npm run test:v2
npm run check:antigravity-projection
npm run build:runtimes
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

## Rollback and uninstall

To restore a pre-update `.agents` backup:

```bash
ag-kit rollback
```

To remove one v2 runtime projection:

```bash
ag-kit runtime uninstall <runtime>
```

Runtime uninstall removes or restores only AG Kit-owned projection state where ownership can be proven. User drift is preserved, and `.ag-kit/memory/` is preserved by default.

## Compatibility notes

| Area | v2 behavior |
| --- | --- |
| Canonical source | `shared/` + `packs/` |
| Antigravity runtime tree | generated/native `.agents/` projection |
| Legacy workflow files | removed; one flow engine replaces them |
| Slash-command dependency | removed; natural-language intent is first-class |
| Memory | local Markdown canonical store under `.ag-kit/` |
| Existing `.agents` user files | preserved by default merge strategy |
| Runtime config | project-scoped when verified; global-only changes are explicit |
| Runtime uninstall | preserves user drift and memory |
| Cross-project memory | opt-in registry only; no automatic `$HOME` crawl |

Historical migration details for pre-v2 releases remain available in Git history and the changelog. New v2 work should not restore legacy workflow trees, duplicate canonical runtime trees, or silently mutate user-global configuration.
