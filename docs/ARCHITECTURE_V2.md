# AG Kit v2 — Lean Multi-Runtime Architecture

## Goal
Keep AG Kit smaller in context while supporting more runtimes. The shared layer is runtime-neutral; adapters project only capabilities that a runtime genuinely supports.

## Canonical model
- `shared/core/CORE.md`: the only always-resident policy surface.
- `shared/skills/`: behavior, hot-loaded by deterministic intent triggers.
- `packs/`: reusable domain knowledge, loaded only when relevant.
- `shared/agents/`: four permanent roles: scout, architect, builder, reviewer.
- `shared/flows/development.json`: one workflow engine with QUICK, STANDARD, and DEEP modes.
- `runtimes/*/adapter.json`: thin capability projections.

## Compatibility migration
The historical `.agents/` tree remains temporarily as the Antigravity compatibility/runtime output while v2 becomes canonical. New reusable behavior belongs in `shared/`; new domain reference material belongs in `packs/`. Legacy workflows must not gain new features.

## Size budget
- 1 resident skill (`ag-core`).
- <=22 top-level shared skills.
- 4 permanent agents.
- 1 workflow engine.
- Unlimited project-generated specialists, but they are local project artifacts rather than framework residents.

## Runtime rule
Capability parity is not a goal. Honest support tiers are. Antigravity, Claude, Codex, and Gemini are first-class targets; Cursor, Windsurf, Copilot, and OpenCode use thinner adapters.
