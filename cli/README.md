# AG Kit CLI

CLI for AG Kit v2, a lean multi-runtime operating layer for AI coding agents.

## Requirements

- Node.js 22+
- Git for lifecycle/verification features

## Install

```bash
npm install -g @vudovn/ag-kit
# or
npx @vudovn/ag-kit --help
```

## Runtime lifecycle

```bash
ag-kit runtime list
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime install antigravity
ag-kit runtime doctor
ag-kit runtime doctor antigravity
ag-kit runtime uninstall antigravity
```

AG Kit declares 16 runtime targets across first-class, connected, and bridge tiers. `install-present` downloads the source once and installs only detected targets. Project-scoped config is preferred; global-only integrations are staged rather than silently written into user-global registries.

Runtime lifecycle uses pre-install backups, ownership manifests, drift-aware doctor checks, and surgical uninstall. Filesystem root and user home are rejected as v2 project targets.

## Memory and shared brain

```bash
ag-kit memory init
ag-kit memory add "Use pnpm" --kind convention --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory touch <id> --session s3
ag-kit memory supersede <id> "Use bun" --session s4
ag-kit memory dream
ag-kit memory reindex
ag-kit memory status

ag-kit brain register .
ag-kit brain list
ag-kit brain search "deployment convention"
ag-kit brain unregister .
```

Markdown is canonical. SQLite/FTS5 is optional acceleration. Cross-project search only sees explicitly registered projects, does not crawl `$HOME`, and is disabled by `AG_KIT_MINIMAL=1` or `AG_KIT_NO_CROSS_PROJECT=1`.

## Flow and teams

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Compared approaches"
ag-kit flow waves '[{"name":"foundation","parallel":false}]'
ag-kit flow approve "approved"
ag-kit flow status

ag-kit team --archetype auto --name product --brief "Ship safely"
```

QUICK, STANDARD, and DEEP share one development spine. User gates require artifacts; DEEP convergence requires an explicit wave table.

## Context economy

```bash
ag-kit route "read the auth module"
ag-kit run npm test --max-lines 30
ag-kit compress notes.md
ag-kit compress notes.md --write
ag-kit handoff create --goal "finish rollout" --next "run CI"
ag-kit handoff show
```

`run` keeps full command output under `.ag-kit/session-sandbox/` and returns a bounded summary. `compress` is deterministic and non-destructive by default. `handoff` produces a structured continuation artifact and archives the previous one.

## Audit and release gates

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
ag-kit preflight
```

Cross-audit reviewers receive a read-only snapshot/diff in temporary directories, never a writable source mount. Findings are clustered into consensus/contested groups and recorded with receipts.

## Observability

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
ag-kit dashboard status
ag-kit dashboard stop
```

The ledger is bounded and rotating; the dashboard binds to localhost. AG Kit reports explicit/measured values rather than inventing a counterfactual savings multiplier. Antigravity can feed privacy-minimal tool events automatically via `PostToolUse`.

## Personalization and design

```bash
ag-kit personalize status
ag-kit personalize learn "Use compact prose" --evidence "User shortened the report" --session s1
ag-kit personalize inject on
ag-kit personalize preview --host claude
ag-kit personalize egress
ag-kit personalize forget all

ag-kit design list
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
```

Personalization requires verbatim evidence and cross-session confirmation. Injection is opt-in and `AG_KIT_PROFILE_KILL=1` is a hard kill switch.

## MCP

```bash
ag-kit mcp serve
```

The MCP surface intentionally stays small: project memory, opt-in cross-project search/status, team initialization, runtime status, and audit probing.

## Legacy lifecycle compatibility

Existing AG Kit installations still have the managed-tree migration path:

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update --strategy merge
ag-kit update --strategy replace
ag-kit rollback
ag-kit status
```

`merge` remains the default. `replace` is explicit and still creates a backup unless `--no-backup` is supplied.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Success or no changes required |
| `1` | Validation, filesystem, configuration, preflight, runtime, or audit failure |
| `2` | Legacy update completed with conflicts requiring review |
| `130` | Interrupted by the user |

## License

MIT
