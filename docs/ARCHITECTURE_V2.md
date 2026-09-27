# AG Kit v2 — Lean Multi-Runtime Architecture

AG Kit v2 is a runtime-neutral operating layer. `shared/` is canonical; runtime folders translate that source into host-specific projections.

## Canonical model

- `shared/core/CORE.md` — the only always-resident policy surface.
- `shared/skills/` — 18 behavior skills, hot-loaded by intent.
- `packs/` — domain knowledge, loaded only when relevant.
- `shared/agents/` — four permanent roles: scout, architect, builder, reviewer.
- `shared/flows/development.json` — one workflow engine with QUICK, STANDARD, and DEEP modes.
- `engine/` and `cli/lib/` — memory, team assembly, audit, preflight, observability, context, and runtime lifecycle.
- `runtimes/*/adapter.json` — capability-aware runtime adapters.
- `platform-capabilities.json` — machine-readable support matrix.

No runtime is the canonical implementation or the product's primary runtime.

## Projection model

Generated host trees are outputs of adapters. Examples include:

- Antigravity → `.agents/`
- Claude → `.claude/` + managed `CLAUDE.md`
- Codex → managed `AGENTS.md` + `.codex-plugin/`
- Gemini → `.gemini/` + managed `GEMINI.md`

These trees may contain host-native hooks, MCP files, plugin metadata, skills, agents, or rules when the host supports them. Adapter-specific implementation remains under `runtimes/<runtime>/`; reusable behavior remains under `shared/`.

Use the generic repository commands after shared or adapter changes:

```bash
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
```

## Context budget

- 1 resident skill (`ag-core`)
- 18 top-level shared skills (budget <=22)
- 4 permanent agents
- 1 workflow engine
- project-generated specialists live under local `.ag-kit/` and are not framework residents

## Runtime tiers

First-class: Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline.

Connected: Cursor, Windsurf, GitHub Copilot.

Bridge: OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi.

Capability parity is deliberately not claimed where a runtime lacks native surfaces. Tier and capability claims come from `platform-capabilities.json`, not marketing copy.

## Shared brain

`ag-kit mcp serve` exposes a small project-local MCP bridge for memory, team, runtime state, and audit probing. Markdown remains memory source-of-truth; indexes are disposable acceleration layers.

## Repository invariants

`check:runtimes` enforces the architecture boundary:

- `shared/` stays the source of truth;
- no `primaryRuntime`/`primary_runtime` contract is allowed;
- root scripts and GitHub workflow gates stay runtime-neutral;
- removed Antigravity-era source tooling does not return inside generated `.agents/`;
- adapter capability declarations match `platform-capabilities.json`.
