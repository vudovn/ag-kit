---
ag_kit_schema: 2
source_of_truth: shared
primary_runtime: antigravity
---

# AG Kit Repository Instructions

The canonical AG Kit v2 behavior lives in `shared/`. Runtime folders and `.agents/` are capability-aware adapters/projections, not places to fork reusable behavior.

Start with `shared/core/CORE.md`. Load only the skill(s) required for the current intent and load `packs/*` only for relevant domain knowledge. The permanent framework agents are `scout`, `architect`, `builder`, and `reviewer`; generate project-specific specialists only when needed.

For project work use the single development spine in `shared/flows/development.json`. Natural-language intent is authoritative: planning/spec/architecture requests enter the flow before multi-file mutation, and continue/resume requests load handoff + relevant durable memory first.

Before claiming cross-runtime support, verify `platform-capabilities.json` and the matching runtime adapter. Do not restore legacy `.agents/workflows/`, duplicate canonical runtime trees, or silently write user-global configuration.

Validation from repository root:

```bash
npm run check:v2
npm run check:docs
npm run test:v2
npm run check:antigravity-projection
npm run build:runtimes
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

For release work also follow `PRODUCTION_CHECKLIST.md`, `MIGRATION.md`, and `SECURITY.md`. Do not bump the CalVer version until the reviewed artifact is actually ready to tag.
