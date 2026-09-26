# AG Kit CLI

CLI for AG Kit v2, a lean multi-runtime operating layer for AI coding agents.

## Requirements

- Node.js 22+

## Installation

```bash
npm install -g @vudovn/ag-kit
```

Or run without installing globally:

```bash
npx @vudovn/ag-kit --help
```

## V2 commands

| Command | Description |
|---|---|
| `ag-kit runtime list` | List supported runtime targets |
| `ag-kit runtime install <runtime>` | Install the shared core/runtime projection and wire verified project MCP config |
| `ag-kit memory init` | Create local-first project memory |
| `ag-kit memory add <text...>` | Add a durable Markdown memory entry |
| `ag-kit memory recall <query...>` | Recall project memory using the warm index or Markdown fallback |
| `ag-kit memory reindex` | Rebuild the optional SQLite/FTS5 warm index |
| `ag-kit memory status` | Show canonical/index memory state |
| `ag-kit team` | Generate a project-specific specialist team |
| `ag-kit cross-audit [target]` | Run independent read-only reviewer lineages against a snapshot/diff |
| `ag-kit preflight` | Run blocking AG Kit release gates |
| `ag-kit mcp serve` | Serve the project-local AG Kit MCP bridge over stdio |

### Runtime adapters

```bash
ag-kit runtime list
ag-kit runtime install antigravity
ag-kit runtime install claude
ag-kit runtime install qwen --path ./my-project
```

AG Kit currently declares 12 targets across first-class, connected, and bridge tiers. Capability claims are tracked in the repository's `platform-capabilities.json` instead of assuming every runtime supports the same surfaces.

### Memory

```bash
ag-kit memory init
ag-kit memory add "Use pnpm in this repository" --kind convention --title "Package manager"
ag-kit memory recall "package manager" --limit 5
ag-kit memory reindex
ag-kit memory status
```

Markdown under `.ag-kit/memory/` is canonical. When the Node runtime provides SQLite/FTS5, AG Kit uses a rebuildable warm index. Recall falls back to Markdown if the index is unavailable.

### Team assembly

```bash
ag-kit team --archetype auto --name product --brief "Ship the release safely"
```

Supported archetypes include software, web, research, content, game, operations, and auto detection.

### Cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 2
ag-kit cross-audit src/auth.ts --reviewers 3
```

Reviewers run against a snapshot or git diff in temporary directories. They do not receive a writable mount of the project tree. Reports and receipts are written under `.ag-kit/`.

### MCP

```bash
ag-kit mcp serve
```

Runtime installers wire project-scoped MCP files only where the runtime format has been verified.

## Legacy lifecycle compatibility

The CLI keeps the managed-tree lifecycle for existing AG Kit installations:

| Command | Description |
|---|---|
| `ag-kit init` | Install the legacy managed Antigravity tree or safely merge into an existing installation |
| `ag-kit update` | Update managed files while preserving local changes |
| `ag-kit rollback` | Restore the newest or a selected pre-update backup |
| `ag-kit status` | Show installation, version, backups, and CLI status |

```bash
ag-kit update --dry-run
ag-kit update --strategy merge
ag-kit update --strategy replace
ag-kit rollback
```

`merge` remains the default update strategy. `replace` is explicit and still creates a pre-update backup unless `--no-backup` is supplied.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Success or no changes required |
| `1` | Validation, filesystem, configuration, preflight, or runtime failure |
| `2` | Legacy update completed with conflicts requiring manual review |
| `130` | Interrupted by the user |

## License

MIT
