# AG Kit CLI

CLI for installing and safely updating [AG Kit](https://github.com/vudovn/ag-kit), a collection of agents, skills, workflows, rules, memory conventions, and validation tools for Google Antigravity.

## Installation

```bash
npx @vudovn/ag-kit init
```

Or install globally:

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

## Commands

| Command | Description |
|---|---|
| `ag-kit init` | Install `.agents`; safely merges when an installation already exists |
| `ag-kit update` | Update managed files while preserving local changes |
| `ag-kit rollback` | Restore the newest or a selected pre-update backup |
| `ag-kit status` | Show installation, manifest, toolkit version, backups, and CLI status |

## Safe update model

AG Kit records SHA-256 baselines in `.agents/.ag-kit/manifest.json`. During an update it compares the previous upstream version, the current local file, and the new upstream file.

- Clean managed files are updated automatically.
- Files changed only locally are preserved.
- User-created files are preserved.
- Files changed both locally and upstream are reported as conflicts.
- Incoming conflict copies are written under `.agents/.ag-kit/conflicts/`.
- A full pre-update backup is stored under `.ag-kit-backups/` by default.

```bash
ag-kit update --dry-run
ag-kit update --strategy merge
ag-kit update --strategy replace
ag-kit rollback
ag-kit rollback --backup 20260712-090000-000
```

`merge` is the default strategy. `replace` is intentionally explicit and still creates a backup unless `--no-backup` is supplied.

## Common options

```bash
ag-kit init --path ./myapp
ag-kit init --branch dev
ag-kit update --force
ag-kit update --quiet --force
ag-kit update --conflict-report ./ag-kit-update.json
ag-kit rollback --dry-run
```

When `--quiet` is used against an existing installation, `--force` is required because the CLI cannot safely ask for confirmation.

## Included toolkit

- **20 specialist agents**
- **48 skills**
- **13 workflows**
- Shared rules, persistent memory conventions, MCP configuration, and validation scripts

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Success or no changes required |
| `1` | Download, validation, filesystem, or configuration failure |
| `2` | Update completed, but one or more conflicts require manual review |
| `130` | Interrupted by the user |

## License

MIT
