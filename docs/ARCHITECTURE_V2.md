# AG Kit v2 — Lean Multi-Runtime Architecture

AG Kit v2 is a small runtime-neutral operating layer. `shared/` is canonical; native runtime folders are projections.

## Canonical model
- `shared/core/CORE.md` — the only always-resident policy surface.
- `shared/skills/` — 18 behavior skills, hot-loaded by intent.
- `packs/` — domain knowledge, loaded only when relevant.
- `shared/agents/` — four permanent roles: scout, architect, builder, reviewer.
- `shared/flows/development.json` — one workflow engine with QUICK, STANDARD, and DEEP modes.
- `engine/` / `cli/lib/v2-engine.js` — memory, team assembly, audit probing, preflight, and runtime installation.
- `runtimes/*/adapter.json` — honest capability projections.

## Antigravity
`.agents/` is generated from `shared/` because Antigravity requires native workspace discovery paths. It contains 18 projected skills, 4 projected agents, one always-on core rule, hooks, MCP, and native plugin metadata. Legacy `.agents/agent`, `.agents/workflows`, `.agents/memory`, manifest registries, and dependency graphs were removed in v2.

Run `npm run sync:antigravity` after editing shared skills/agents/core, and CI enforces `npm run check:antigravity-projection`.

## Context budget
- 1 resident skill (`ag-core`)
- 18 top-level shared skills (budget <=22)
- 4 permanent agents
- 1 workflow engine
- project-generated specialists live under local `.ag-kit/` and are not framework residents

## Runtime tiers
First-class: Antigravity, Claude, Codex, Gemini.
Connected/bridge: Cursor, Windsurf, GitHub Copilot, OpenCode.
Capability parity is deliberately not claimed where a runtime lacks native surfaces.

## Shared brain
`ag-kit mcp serve` exposes a small project-local MCP bridge for memory/team/runtime state. Markdown remains memory source-of-truth; indexes are disposable acceleration layers.
