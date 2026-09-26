<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  A lean multi-runtime operating layer for AI coding agents: tiny resident core, hot-loaded skills, evolving project memory, gated execution, MCP, observability, privacy controls, and independent cross-audit.
</p>

<div align="center">
  <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="AG Kit on Unikorn.vn" width="210" height="54" /></a>
  <a href="https://trendshift.io/repositories/21490" target="_blank"><img src="https://trendshift.io/api/badge/repositories/21490" alt="AG Kit on Trendshift" width="250" height="55" /></a>
  <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="AG Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

<p align="center">
  <a href="./README-VI.md">Tiếng Việt</a> · <a href="./docs/PARITY_IJFW.md">Parity map</a> · <a href="./MIGRATION.md">Migration</a> · <a href="./SECURITY.md">Security</a>
</p>

---

## Why AG Kit v2

Large agent kits usually fail in the same way: too many always-loaded roles, duplicated instructions, runtime-specific forks, and multiple workflow engines competing for context.

AG Kit v2 takes the opposite approach:

- **1 tiny resident core** — always-on operating rules only.
- **18 hot-loaded top-level skills** — behavior loads only when relevant.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development spine** — QUICK, STANDARD, or DEEP with explicit phase gates.
- **Domain packs** — reference knowledge lives in `packs/`, not inside giant skills.
- **Shared source of truth** — portable behavior lives in `shared/`; runtime folders are projections/adapters.
- **Evolving local-first memory** — Markdown stays canonical; SQLite FTS5 is optional acceleration; candidates can become durable, expire, supersede older facts, or be archived by the dream cycle.
- **Project-local MCP bridge** — runtimes can share memory/team/audit capabilities without fake native parity.
- **Independent cross-audit** — reviewer lineages inspect read-only snapshots and classify findings as consensus or contested.
- **Local observability + privacy controls** — explicit token/cost events, localhost dashboard, evidence-backed personalization, disclosure log, forget, and a hard kill switch.
- **Design contract** — a portable `DESIGN.md` contract with 12 starting templates and validation.

## Architecture

```text
shared/                  # canonical runtime-neutral behavior
├── core/                # tiny always-on core
├── skills/              # 18 hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # one development spine

packs/                   # domain knowledge, loaded only when needed
runtimes/                # thin capability-aware adapters
engine/                  # small runtime-neutral wrappers/tests
cli/                     # @vudovn/ag-kit CLI + MCP + local engines
.agents/                 # generated lean Antigravity projection
```

`shared/` is the source of truth. `.agents/` is not a second toolkit implementation; it is the native Antigravity projection of the shared core.

## Runtime coverage

AG Kit declares **16 runtime targets** with honest capability tiers.

| Tier | Runtimes |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

The exact matrix lives in [`platform-capabilities.json`](platform-capabilities.json). Project-scoped activation is preferred. If a runtime only exposes user-global configuration, AG Kit stages guidance/snippets instead of silently editing the user's home directory.

## Requirements

- Node.js **22+**.
- Git for reviewable updates and rollback.
- Optional reviewer CLIs such as Codex, Gemini, Qwen, or OpenCode for cross-audit execution.
- Optional SQLite support from Node for the warm memory index; Markdown recall remains the fallback.

## Quick start

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime list
ag-kit runtime install antigravity
```

Or run directly:

```bash
npx @vudovn/ag-kit --help
```

### Gated development flow

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Compared three approaches; selected signed one-time tokens"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

Every phase needs an artifact summary before approval. DEEP mode also requires an explicit dependency-wave table at CONVERGE. AG Kit never auto-approves a user gate.

### Evolving project memory

```bash
ag-kit memory init
ag-kit memory add "Use pnpm for this repository" --kind convention --title "Package manager" --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory touch <memory-id> --session s3
ag-kit memory dream
ag-kit memory reindex
ag-kit memory status
```

Markdown under `.ag-kit/memory/` is canonical. Repeated evidence across sessions can promote candidates to durable memory. Temporal validity windows and supersession keep historical facts queryable without pretending old facts are current.

### Project specialist team

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship the next release safely"
```

Generated project roles live under `.ag-kit/agents/`; the framework itself keeps only four permanent core agents.

### Independent cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

Reviewers run in temporary directories against a snapshot or git diff, never a writable source mount. Findings are clustered into **consensus** (multiple independent lineages agree) and **contested** findings, with duration/count receipts saved under `.ag-kit/`.

### Local observability

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start --port 4737
```

The dashboard binds to `127.0.0.1`. AG Kit records only explicit metrics supplied by the runtime/integration; it does not invent token savings.

### Personalization and privacy

```bash
ag-kit personalize learn "Use compact prose" --evidence "User requested a shorter release note" --session s1
ag-kit personalize learn "Use compact prose" --evidence "User shortened the next report again" --session s2
ag-kit personalize inject on
ag-kit personalize preview --host claude
ag-kit personalize egress
ag-kit personalize forget all
```

Preferences need verbatim evidence and repeat evidence across sessions before confirmation. Injection is off by default. `AG_KIT_PROFILE_KILL=1` disables profile injection regardless of stored settings. Disclosures are logged locally and `forget` removes both the preference and matching disclosure rows.

### Design contract

```bash
ag-kit design list
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
```

`DESIGN.md` captures brand intent, colors, typography, layout, components, imagery, motion, accessibility, and do/don't constraints so visual behavior travels across runtimes without another resident prompt.

### Release gates

```bash
ag-kit preflight
```

Preflight covers the v2 architecture budget, engine tests, Antigravity projection drift, runtime projections, Antigravity doctor/tests/plugin build, and CLI tests. CI also runs web lint/typecheck/build, dependency audits, and dependency review.

## MCP bridge

```bash
ag-kit mcp serve
```

The stdio MCP bridge intentionally stays small: evolving memory recall/status/add, team initialization, runtime status, and audit probing. Richer local capabilities remain CLI/state modules instead of inflating the MCP tool surface.

## Antigravity native projection

Antigravity remains the richest native target. The committed `.agents/` projection contains:

- **18 skills**
- **4 permanent agents**
- **0 legacy workflow files**
- native safety hook
- project MCP configuration
- native plugin packaging

```bash
npm run sync:antigravity
npm run check:antigravity-projection
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

Reusable behavior belongs in `shared/`, never as a new canonical copy inside `.agents/`.

## Legacy lifecycle compatibility

Existing AG Kit installations keep a safe migration path:

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit update --strategy replace
ag-kit rollback
ag-kit status
```

Legacy updates remain merge-aware and backup-aware while v2 becomes canonical.

## Repository validation

```bash
npm run check:v2
npm run test:v2
npm run check:antigravity-projection
npm run build:runtimes
npm run check:antigravity
npm run test:antigravity
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

## Design principles

1. **Context is a budget.** Resident instructions stay small.
2. **Behavior and knowledge are different.** Skills define behavior; packs hold reference knowledge.
3. **One source, many runtimes.** Adapters translate the shared core instead of forking it.
4. **Capability claims must be machine-checkable.** Runtime parity is a matrix, not marketing copy.
5. **Memory stays human-readable.** Indexes accelerate retrieval; they never become the only copy.
6. **Judgment stays explicit.** Phase gates require artifacts and user approval; automation does not silently advance.
7. **Verification is executable.** Preflight, CI, doctor, and cross-audit create evidence and receipts.
8. **Privacy is inspectable.** Profile injection is opt-in, local disclosures are logged, and forgetting is executable.
9. **Dangerous automation stays narrow.** Safety hooks supplement runtime permissions and human review.

## IJFW parity work

AG Kit v2 implements the useful feature classes behind IJFW-style tiny-core architecture—hot-loaded skills, tiered runtime adapters, evolving local memory, gated workflow phases, specialist assembly, independent audit, observability, personalization/privacy, and design contracts—using AG Kit's own code and runtime model.

See [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) for the tracked capability map and intentional differences.

## Documentation

- [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) — functional parity map
- [`MIGRATION.md`](MIGRATION.md) — migration guidance
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) — release checklist
- [`SECURITY.md`](SECURITY.md) — security model
- [`AGENT_FLOW.md`](AGENT_FLOW.md) — flow architecture
- [`.agents/hooks/README.md`](.agents/hooks/README.md) — Antigravity native integration
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## Support the project

<p align="center">
  <a href="https://buymeacoffee.com/vudovn" target="_blank"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" /></a>
</p>

<p align="center"> - or - </p>

<p align="center"><img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Buy me coffee" width="200" /></p>
<p align="center"><code>CA: Gjpatn3d24dCRhUng7F37K6xJba4R8SDBC18xs1Apump</code></p>

## License

Released under the [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
