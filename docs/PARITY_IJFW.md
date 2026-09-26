# AG Kit v2 vs IJFW — Functional Parity Map

This document tracks architectural/functionality convergence without copying IJFW source code.

| Capability | IJFW pattern | AG Kit v2 status |
|---|---|---|
| Tiny resident core | one small always-on core | implemented (`shared/core`, `ag-core`) |
| Hot-loaded skills | trigger-driven capabilities | implemented in shared skill contracts |
| Shared portable source | shared rules/skills/lib | implemented (`shared/`, `packs/`) |
| Thin runtime adapters | per-platform tiered surfaces | implemented for 8 runtimes |
| Capability drift gate | machine-readable platform matrix | implemented (`check:v2`) |
| One workflow spine | plan-before-build phases | implemented with QUICK/STANDARD/DEEP |
| Wave execution contract | explicit dependency waves | encoded in DEEP flow contract |
| Local-first memory | human-readable canonical store + rebuildable index | implemented markdown canonical store; indexed acceleration remains optional |
| Project team assembly | generated local specialist bench | implemented deterministic archetype generator |
| Cross-model audit | probe independent reviewer lineages + receipts | implemented roster probing/receipts; execution adapters are intentionally separate |
| Preflight | blocking ship gates | implemented AG Kit-native gate runner |
| Runtime projection build | generate runtime-specific outputs | implemented (`build:runtimes`) |
| Native Antigravity | IJFW currently thin | AG Kit stronger: native rules/skills/agents/hooks/plugins |

## Non-goal
`100% identical` means feature-class parity where it benefits AG Kit, not copying IJFW files, wording, private conventions, or platform claims that AG Kit cannot verify.
