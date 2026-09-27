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
- **Local-first memory** — Markdown is canonical; SQLite/FTS5 is optional acceleration.
- **Executable evidence** — preflight, runtime doctor, cross-audit, receipts, dependency audits, and CI.

```text
shared/                  # canonical runtime-neutral behavior
├── core/                # tiny always-on core
├── skills/              # hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # one development spine

packs/                   # domain knowledge
runtimes/                # thin capability-aware adapters
engine/                  # memory / planning / audit / preflight / observability
cli/                     # lifecycle, MCP, context, memory, audit tools
```

Generated host trees such as `.agents/`, `.claude/`, or `.gemini/` are projections created by their adapters. `shared/` remains the source of truth.

## Runtime coverage

| Tier | Runtimes |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

The machine-readable contract is [`platform-capabilities.json`](platform-capabilities.json). A capability is claimed only when the corresponding adapter declares and verifies it.

No runtime is AG Kit's primary runtime. Richer hosts may expose more native surfaces than others, but product behavior must remain portable through the shared core.

## Install

Requirements: Node.js **22+** and Git.

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

Install one target explicitly when needed:

```bash
ag-kit runtime install claude
ag-kit runtime install codex
ag-kit runtime uninstall claude
```

Runtime installs use ownership manifests and pre-install backups. Uninstall removes only AG Kit-owned state where ownership can be proven, preserves user drift, and keeps project memory by default.

## Local-first memory

```bash
ag-kit memory init
ag-kit memory add "Use pnpm in this repo" --kind convention --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory dream
ag-kit memory status
```

Markdown under `.ag-kit/memory/` is canonical. Candidates can become durable after repeated cross-session evidence, carry validity windows, supersede older facts, and be archived by the dream cycle. SQLite FTS5 is a disposable warm index.

Cross-project recall is opt-in:

```bash
ag-kit brain register .
ag-kit brain list
ag-kit brain search "deployment convention"
```

AG Kit does not crawl the user home directory automatically. Root/home registration is rejected, and global-only runtime configuration is staged for explicit activation rather than silently modified.

## One development spine

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Compared approaches and selected signed one-time tokens"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

Every gated phase needs an artifact before approval. DEEP mode additionally requires an explicit dependency-wave table before execution convergence.

Project-specific specialists stay temporary:

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship safely"
```

Generated project roles live under `.ag-kit/agents/`; the framework itself keeps four permanent agents.

## Context economy

Route work without hard-coding a vendor model:

```bash
ag-kit route "read the auth module and explain the flow"
ag-kit route "design a multi-service migration"
```

Bound large command output:

```bash
ag-kit run npm test
ag-kit run npm run build --max-lines 30
```

Full stdout/stderr stays under `.ag-kit/session-sandbox/`; the caller receives a bounded summary.

Create continuation artifacts:

```bash
ag-kit handoff create \
  --goal "finish runtime rollout" \
  --state "core and CLI are green" \
  --evidence "npm test passed" \
  --risk "web audit still pending" \
  --next "run full CI"

ag-kit handoff show
```

## Independent cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

External reviewer lineages receive a snapshot/diff in temporary directories, never a writable source mount. Findings remain separated into consensus and contested groups with receipts.

## Observability and privacy

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
```

The local ledger is bounded/rotating and the dashboard binds to localhost. AG Kit records measured or explicitly supplied values rather than inventing savings multipliers.

Adapters may use host-native observability hooks when supported. Those hooks are runtime-specific implementation details and must remain privacy-minimal and fail-open.

## Design contract

```bash
ag-kit design list
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
```

`DESIGN.md` carries brand intent, colors, typography, layout, components, imagery, motion, accessibility, and constraints across runtimes without adding another resident prompt.

## MCP bridge

```bash
ag-kit mcp serve
```

The MCP surface intentionally stays small: project memory, opt-in cross-project search/status, team initialization, runtime status, and audit probing. Runtime adapters wire or stage the MCP bridge only where their verified configuration model supports it.

## Runtime adapters

Each adapter lives under `runtimes/<runtime>/` and declares its capability surface in `platform-capabilities.json`.

Examples:

- Antigravity can project native rules, skills, agents, hooks, MCP, and plugin packaging.
- Claude can project native skills/agents plus project MCP integration.
- Codex receives portable instructions, skills, and a plugin/MCP projection.
- Connected/bridge targets expose only the surfaces AG Kit has verified.

Adapter-specific implementation and tests stay inside the adapter boundary. Root-level validation stays runtime-neutral.

## Repository validation

```bash
npm run check:v2
npm run check:docs
npm run test:v2
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

`check:runtimes` also enforces repository neutrality: no primary runtime declaration, no runtime-specific root scripts/workflow gates, and no return of removed Antigravity-era tooling into the generated `.agents/` surface.

## Legacy lifecycle compatibility

Existing AG Kit installations still have a safe migration path:

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit rollback
ag-kit status
```

Legacy updates remain merge-aware and backup-aware while v2 is canonical.

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

AG Kit v2 independently implements the useful feature classes behind the IJFW-style tiny-core multi-runtime model while keeping AG Kit's own code, names, lifecycle model, and privacy posture. See [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) for the capability map and intentional differences.

## Documentation

- [`docs/ARCHITECTURE_V2.md`](docs/ARCHITECTURE_V2.md) — v2 architecture
- [`docs/RUNTIMES.md`](docs/RUNTIMES.md) — runtime tiers and adapters
- [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) — functional parity map
- [`MIGRATION.md`](MIGRATION.md) — migration guidance
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) — release checklist
- [`SECURITY.md`](SECURITY.md) — security model
- [`AGENT_FLOW.md`](AGENT_FLOW.md) — flow architecture
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## License

Released under the [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
