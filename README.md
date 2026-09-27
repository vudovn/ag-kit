<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  A lean multi-runtime operating layer for AI coding agents: one shared core, hot-loaded skills, local-first memory, gated execution, context economy, privacy controls, and independent verification.
</p>

<p align="center">
  <a href="./README-VI.md">Tiếng Việt</a> · <a href="./docs/RUNTIMES.md">Runtimes</a> · <a href="./docs/PARITY_IJFW.md">IJFW parity</a> · <a href="./MIGRATION.md">Migration</a> · <a href="./SECURITY.md">Security</a>
</p>

---

## What AG Kit v2 is

AG Kit is runtime-neutral at its core. Reusable behavior lives once under `shared/`; runtime folders translate that behavior into host-native surfaces without becoming independent forks.

- **1 resident core** — small always-on operating rules.
- **18 hot-loaded skills** — behavior enters context only when relevant.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development spine** — QUICK / STANDARD / DEEP modes with explicit gates.
- **16 runtime targets** — capability tiers instead of fake parity.
- **Domain packs** — deep knowledge stays cold until needed.
- **Local-first memory** — Markdown is canonical; FTS and semantic retrieval are optional rebuildable acceleration.
- **Executable evidence** — preflight, runtime doctor, cross-audit, receipts, benchmark artifacts, dependency audits, and CI.

```text
shared/                  # canonical runtime-neutral behavior
├── core/                # tiny always-on core
├── skills/              # hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # one development spine

packs/                   # cold domain/reference knowledge
runtimes/                # thin capability-aware adapters
engine/                  # memory / planning / audit / preflight / observability
cli/                     # lifecycle, MCP, context, memory, audit tools
```

Generated host trees such as `.agents/`, `.claude/`, or `.gemini/` are projections created by adapters. `shared/` remains the source of truth.

## Runtime coverage

| Tier | Runtimes |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

The machine-readable contract is [`platform-capabilities.json`](platform-capabilities.json). No runtime is AG Kit's primary runtime.

## Install

Requirements: Node.js **22+** and Git.

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

Installing the package installs the CLI only. Project files change only after an explicit runtime install.

Install or remove one target:

```bash
ag-kit runtime install claude
ag-kit runtime doctor claude
ag-kit runtime uninstall claude
```

Runtime installs use ownership manifests and pre-install backups. Uninstall removes/restores only AG Kit-owned state where ownership can be proven, preserves user drift, and keeps project memory by default.

### Migrating a pre-v2 Antigravity project

The old Antigravity-only managed-tree CLI is removed. Commit or back up the project, then migrate through the same lifecycle used by every runtime:

```bash
ag-kit runtime install antigravity
ag-kit runtime doctor antigravity
```

See [`MIGRATION.md`](MIGRATION.md) for pre-v2 recovery and migration details.

## Memory and continuity

```bash
ag-kit memory init
ag-kit memory add "Use pnpm in this repo" --kind convention --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory dream
ag-kit memory status

ag-kit memory semantic status
ag-kit memory semantic on
ag-kit memory semantic rebuild

ag-kit brain register .
ag-kit brain search "deployment convention"
```

Markdown under `.ag-kit/memory/` is canonical. SQLite/FTS5 and the local semantic tier are disposable, rebuildable acceleration layers. Semantic retrieval is off by default. Cross-project recall is opt-in and never crawls `$HOME` automatically.

Create continuation artifacts:

```bash
ag-kit handoff create --goal "finish runtime rollout" --state "core is green" --next "run full CI"
ag-kit handoff show
```

## One development spine

```bash
ag-kit prompt-check "update it"
ag-kit route "design a multi-service migration"
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Compared approaches and selected signed one-time tokens"
ag-kit flow waves '[{"id":"foundation","mode":"parallel","tasks":["A","B"],"dependsOn":[]}]'
ag-kit flow ready
ag-kit flow wave-complete foundation "Foundation verified"
ag-kit flow approve "approved"
```

Every gated phase needs an artifact before approval. Verification boundaries require fresh mechanical evidence. DEEP mode uses explicit dependency waves and independent cross-audit before shipping.

Project-specific specialists stay temporary:

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship safely"
```

## Context economy

```bash
ag-kit run npm test
ag-kit run npm run build --max-lines 30
ag-kit compress docs/long-context.md
```

Full command output stays under `.ag-kit/session-sandbox/`; the caller receives a bounded summary. Compression is deterministic and non-destructive by default.

## Independent cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

External reviewer lineages receive bounded snapshot chunks in temporary directories, never a writable source mount. Independent lineages can run in bounded parallelism. Findings remain separated into consensus and contested groups with traceable receipts.

## Observability and privacy

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
```

The local ledger is bounded/rotating, rolls up by runtime and trace, and the dashboard binds to localhost. AG Kit records measured or explicitly supplied values rather than inventing savings multipliers.

Personalization is evidence-backed and opt-in:

```bash
ag-kit personalize status
ag-kit personalize learn "Use compact prose" --evidence "User shortened the report" --session s1
ag-kit personalize inject on
ag-kit personalize forget all
```

`AG_KIT_PROFILE_KILL=1` is a hard kill switch.

## Design and MCP

```bash
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
ag-kit mcp serve
```

`DESIGN.md` carries portable design intent across runtimes. The MCP bridge intentionally keeps a small runtime-neutral tool surface.

## Runtime adapters

Each adapter lives under `runtimes/<runtime>/` and declares its verified capability surface in `platform-capabilities.json`.

Examples:

- Antigravity can project native rules, skills, agents, hooks, MCP, and plugin packaging.
- Claude can project native skills/agents plus project integration.
- Codex receives portable instructions, skills, hooks/plugin surfaces where verified.
- Connected/bridge targets expose only the surfaces AG Kit has independently verified.

Adapter-specific richness never becomes a product-wide primary-runtime contract.

## Repository validation

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

`check:runtimes` enforces repository neutrality. `check:docs` verifies links plus machine-checkable command/gate claims. CI also publishes a deterministic benchmark receipt for memory recall, routing, compression, and runtime lifecycle.

## Principles

1. **Context is a budget.**
2. **Behavior is not knowledge.** Skills act; packs inform.
3. **One source, many runtimes.**
4. **No primary runtime.** Host-specific richness stays behind adapter boundaries.
5. **Capability claims must be machine-checkable.**
6. **Memory stays human-readable and user-owned.**
7. **Judgment stays explicit.** No silent phase approval.
8. **Verification produces evidence.**
9. **Privacy is inspectable and kill-switchable.**
10. **One lifecycle.** Runtime install/doctor/uninstall replaces runtime-specific hidden lifecycle systems.

AG Kit v2 independently implements useful IJFW-class feature categories and multi-runtime discipline while keeping AG Kit's own code, names, lifecycle model, and privacy posture. See [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md).

## Documentation

- [`docs/ARCHITECTURE_V2.md`](docs/ARCHITECTURE_V2.md) — architecture
- [`docs/RUNTIMES.md`](docs/RUNTIMES.md) — runtime tiers/adapters
- [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) — functional parity map
- [`MIGRATION.md`](MIGRATION.md) — migration guidance
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) — release checklist
- [`SECURITY.md`](SECURITY.md) — security model
- [`AGENT_FLOW.md`](AGENT_FLOW.md) — flow architecture
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## License

Released under the [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
