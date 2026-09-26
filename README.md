<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  A lean multi-runtime operating layer for AI coding agents: tiny resident core, hot-loaded skills, project memory, specialist teams, MCP, preflight gates, and read-only cross-audit.
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
- **18 hot-loaded top-level skills** — behavior is loaded when relevant instead of living permanently in context.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development flow** — QUICK, STANDARD, or DEEP mode instead of many unrelated workflow engines.
- **Domain packs** — reference knowledge lives in `packs/`, not inside giant skills.
- **Shared source of truth** — portable behavior lives in `shared/`; runtime folders are projections/adapters.
- **Local-first memory** — Markdown is canonical; SQLite FTS5 is an optional rebuildable warm index when available.
- **Project-local MCP bridge** — runtimes can share memory/team/audit capabilities without pretending to have native feature parity.
- **Read-only cross-audit** — independent reviewer CLIs receive a snapshot/diff in a temporary directory, never the writable project tree.

## Architecture

```text
shared/                  # canonical runtime-neutral behavior
├── core/                # tiny always-on core
├── skills/              # 18 hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # one development flow, 3 depth modes

packs/                   # domain knowledge, loaded only when needed
runtimes/                # thin capability-aware adapters
engine/                  # memory, team, audit, preflight wrappers/tests
cli/                     # published @vudovn/ag-kit CLI + MCP server
.agents/                 # generated lean Antigravity projection
```

`shared/` is the source of truth. `.agents/` is no longer a second toolkit implementation; it is the native Antigravity projection of the shared core.

## Runtime coverage

AG Kit currently declares **12 verified targets** with honest capability tiers.

| Tier | Runtimes |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider |

The exact capability matrix lives in [`platform-capabilities.json`](platform-capabilities.json). AG Kit does not claim native agents, hooks, plugins, or skills on runtimes where those surfaces are not verified.

## Requirements

- Node.js **22+**.
- Git for reviewable updates and rollback.
- Optional reviewer CLIs such as Codex, Gemini, Qwen, or OpenCode for cross-audit execution.
- Optional SQLite support from the Node runtime for the warm memory index; Markdown recall remains the fallback.

## Quick start

### Install the CLI

```bash
npm install -g @vudovn/ag-kit
```

Or run it directly:

```bash
npx @vudovn/ag-kit --help
```

### Install a runtime adapter

```bash
ag-kit runtime list
ag-kit runtime install antigravity
ag-kit runtime install claude
ag-kit runtime install qwen
```

The installer writes only project-scoped runtime files that AG Kit has a verified contract for. It does not silently modify unrelated user-global configuration.

### Project memory

```bash
ag-kit memory init
ag-kit memory add "Use pnpm for this repository" --kind convention --title "Package manager"
ag-kit memory recall "package manager"
ag-kit memory reindex
ag-kit memory status
```

Memory is stored under `.ag-kit/memory/`. Markdown files are canonical. The SQLite/FTS5 index is disposable acceleration and can always be rebuilt.

### Assemble a project team

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship the next release safely"
```

Generated project-specific roles live under `.ag-kit/agents/`; the framework itself keeps only four permanent core agents.

### Run cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 2
ag-kit cross-audit src/auth.ts --reviewers 3
```

Cross-audit probes available independent reviewer lineages, snapshots the requested target or git diff, runs reviewers in temporary directories, and stores receipts/reports under `.ag-kit/`.

### Run release gates

```bash
ag-kit preflight
```

The current repository gates cover the v2 architecture budget, engine tests, Antigravity projection drift, runtime projection build, Antigravity doctor/tests/plugin build, CLI tests, and web checks in CI.

## MCP bridge

Run the shared project-local bridge over stdio:

```bash
ag-kit mcp serve
```

The bridge intentionally exposes a small surface around project memory, team assembly/status, runtime status, and audit probing. Runtime installers wire project-scoped MCP configuration where the runtime contract has been verified.

## Antigravity native projection

Antigravity remains the richest native target. The committed `.agents/` projection contains the lean v2 surface:

- **18 skills**
- **4 permanent agents**
- **0 legacy workflow files**
- native safety hook
- project MCP configuration
- native plugin packaging

Keep the projection synchronized with:

```bash
npm run sync:antigravity
npm run check:antigravity-projection
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

The projection is generated from `shared/`; reusable behavior should be edited in `shared/`, not duplicated inside `.agents/`.

## Legacy lifecycle compatibility

The published CLI still keeps the safe managed-tree lifecycle for existing AG Kit installations:

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit update --strategy replace
ag-kit rollback
ag-kit status
```

Updates remain backup-aware and merge-aware so existing users have a migration path while v2 becomes the canonical architecture.

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

CI also runs dependency review and production dependency audits.

## Design principles

1. **Context is a budget.** Resident instructions must stay small.
2. **Behavior and knowledge are different.** Skills define behavior; packs hold domain reference material.
3. **One source, many runtimes.** Adapters translate the shared core instead of forking it.
4. **Capability claims must be machine-checkable.** Runtime parity is a matrix, not marketing copy.
5. **Memory stays human-readable.** Indexes accelerate retrieval; they never become the only copy.
6. **Verification is executable.** Preflight, CI, doctor, and cross-audit produce evidence and receipts.
7. **Dangerous automation is narrow.** Safety hooks block high-confidence destructive actions without replacing runtime permissions or human review.

## IJFW parity work

AG Kit v2 borrows architectural ideas such as a tiny resident core, hot-loaded skills, portable shared behavior, tiered runtime adapters, local-first memory, and independent audit lines. The implementation is original and AG Kit-specific; the goal is functional/architectural parity where useful, not source-code duplication.

See [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) for the tracked capability map.

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

<p align="center">
  <img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Buy me coffee" width="200" />
</p>

<p align="center">
  <code>CA: Gjpatn3d24dCRhUng7F37K6xJba4R8SDBC18xs1Apump</code>
</p>

## License

Released under the [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
