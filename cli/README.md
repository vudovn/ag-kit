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

Installing the package installs the CLI only. A project changes only after an explicit runtime install.

## Runtime lifecycle

```bash
ag-kit runtime list
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime install claude
ag-kit runtime doctor
ag-kit runtime doctor claude
ag-kit runtime uninstall claude
```

AG Kit declares 16 runtime targets across first-class, connected, and bridge tiers. `install-present` downloads the source once and installs only detected targets. Project-scoped config is preferred; global-only integrations are staged rather than silently written into user-global registries.

No runtime is the product's primary runtime. Runtime-specific hooks, plugins, and projection formats remain implementation details of their adapters.

Runtime lifecycle uses pre-install backups, ownership manifests, drift-aware doctor checks, and surgical uninstall. Filesystem root and user home are rejected as project targets.

### Migrating a pre-v2 Antigravity project

Do not use the removed `init/update/rollback/status` managed-tree lifecycle. Commit or back up the project, then install the Antigravity adapter through the same lifecycle used by every other runtime:

```bash
ag-kit runtime install antigravity
ag-kit runtime doctor antigravity
```

The adapter snapshots touched paths before installation and tracks AG Kit-owned state. `runtime uninstall antigravity` restores/removes only state whose ownership can be proven and preserves project memory by default.

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

ag-kit memory semantic status
ag-kit memory semantic on
ag-kit memory semantic rebuild

ag-kit brain register .
ag-kit brain list
ag-kit brain search "deployment convention"
ag-kit brain unregister .
```

Markdown is canonical. SQLite/FTS5 and the local semantic tier are optional, rebuildable acceleration layers. Semantic retrieval is off by default and does not make its index canonical. Cross-project search only sees explicitly registered projects, does not crawl `$HOME`, and is disabled by `AG_KIT_MINIMAL=1` or `AG_KIT_NO_CROSS_PROJECT=1`.

## Flow and teams

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Compared approaches"
ag-kit flow waves '[{"id":"foundation","mode":"parallel","tasks":["A","B"],"dependsOn":[]}]'
ag-kit flow ready
ag-kit flow wave-complete foundation "Foundation verified"
ag-kit flow approve "approved"
ag-kit flow status

ag-kit team --archetype auto --name product --brief "Ship safely"
```

QUICK, STANDARD, and DEEP share one development spine. User gates require artifacts; DEEP execution uses explicit dependency waves and mechanical verification evidence.

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

## Prompt quality and audit

```bash
ag-kit prompt-check "update it"
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
ag-kit preflight
```

Prompt quality checks return bounded structural signals without persisting raw prompts. Cross-audit reviewers receive read-only snapshot chunks in temporary directories, never a writable source mount. Independent lineages can run in bounded parallelism; findings are clustered into consensus/contested groups and recorded with traceable receipts.

## Observability

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
ag-kit dashboard status
ag-kit dashboard stop
```

The ledger is bounded and rotating; the dashboard binds to localhost and rolls events up by runtime and trace. AG Kit reports explicit/measured values rather than inventing a counterfactual savings multiplier.

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

The MCP surface intentionally stays small and runtime-neutral: project/shared memory, team initialization, runtime status, audit probing, and prompt-quality assistance.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Success or no changes required |
| `1` | Unknown command or validation/filesystem/configuration/preflight/runtime/audit failure |
| `130` | Interrupted by the user |

## License

MIT
