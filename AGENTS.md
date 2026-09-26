---
ag_kit_schema: 2
source_of_truth: shared
primary_runtime: antigravity
---

# AG Kit

The canonical AG Kit v2 source lives in `shared/`. Runtime folders and the historical `.agents/` tree are projections/compatibility surfaces, not places to fork reusable behavior.

Start with `shared/core/CORE.md`. Load only the skill(s) required for the current intent. Load `packs/*` only for relevant domain knowledge. Use the four permanent agents in `shared/agents/` and generate project-specific specialists only when needed.

For project work use `shared/flows/development.json`. Before claiming cross-runtime support, verify `platform-capabilities.json` and the matching `runtimes/<name>/adapter.json`.

Validation:

```bash
npm run check:v2
npm run build:runtimes
npm run check:agents
npm run test:toolkit
npm run check:antigravity
npm run test:antigravity
```
