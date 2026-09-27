# Agent Flow Architecture

AG Kit v2 uses one execution spine instead of many unrelated workflow engines.

## Core model

```text
USER REQUEST
    ↓
TINY RESIDENT CORE
    ↓
REQUEST CLASSIFICATION
    ├── QUICK
    ├── STANDARD
    └── DEEP
    ↓
HOT-LOAD RELEVANT SKILLS + PACKS
    ↓
CORE AGENT ROUTING
    ├── scout
    ├── architect
    ├── builder
    └── reviewer
    ↓
OPTIONAL PROJECT TEAM
    ↓
EXECUTE IN DEPENDENCY WAVES
    ↓
VERIFY / CROSS-AUDIT / PREFLIGHT
    ↓
WRITE RECEIPTS + DURABLE MEMORY + HANDOFF
    ↓
DELIVER RESULT
```

## Activation invariants

Natural-language intent is first-class. CLI and slash commands are aliases, not a requirement for the runtime to expose a particular command UI.

- `plan`, `spec`, `brainstorm`, and architecture intent enter the development flow before multi-file project mutation.
- `continue`, `resume`, and “pick up where we left off” load the latest handoff plus relevant durable memory before mutation.
- Before multi-file or cross-system changes, classify QUICK, STANDARD, or DEEP.
- Confirmed project conventions remain constraints until the current user overrides them; stale memory conflicts should be surfaced and corrected.
- Runtime capability tiers define which native surfaces may be used; missing surfaces are not invented.

## The four permanent agents

| Agent | Responsibility |
| --- | --- |
| `scout` | Inspect the project, gather evidence, map constraints, and reduce uncertainty before changes |
| `architect` | Decide structure, interfaces, dependencies, sequencing, and acceptance criteria |
| `builder` | Implement the approved change and produce runnable artifacts |
| `reviewer` | Verify behavior, test evidence, security, regressions, and acceptance criteria independently |

Project-specific specialists are generated only when needed under `.ag-kit/agents/`. They do not become permanent framework context.

## Three depth modes

### QUICK

Use when the change is narrow, reversible, and well understood.

```text
FRAME → PLAN → EXECUTE → VERIFY
```

### STANDARD

Default mode for normal feature work.

```text
FRAME → SHAPE → PLAN → EXECUTE → VERIFY → SHIP
```

STANDARD requires explicit acceptance criteria and evidence from the project's own checks.

### DEEP

Use for architecture changes, migrations, multi-system work, security-sensitive changes, or broad refactors.

```text
FRAME
  ↓
RECON + risk map
  ↓
SHAPE
  ↓
PLAN
  ↓
WAVES
  ├── wave 1: independent work may run in parallel
  └── wave 2: dependent work waits for prerequisites
  ↓
VERIFY
  ↓
CROSS-AUDIT
  ↓
SHIP
```

Parallel work is allowed only when tasks are truly independent. Dependency order wins over artificial concurrency.

## Skill loading

Skills are not permanently resident.

1. The core classifies the request.
2. The runtime loads only relevant `shared/skills/<name>/SKILL.md` contracts.
3. Domain reference material is pulled from `packs/` only when needed.
4. Runtime-specific adapters translate shared behavior without creating a new canonical copy.

The architecture budget currently targets one resident skill and no more than 22 top-level skills; the committed v2 surface contains 18.

## Memory and continuity flow

```text
accepted durable fact
    ↓
Markdown entry in .ag-kit/memory/
    ↓
canonical source of truth
    ↓
optional SQLite/FTS5 warm index
    ↓
ranked recall
```

The index is disposable. If SQLite is unavailable or the index is stale, recall falls back to scanning Markdown.

Only durable project information belongs in memory: decisions, conventions, recurring constraints, accepted learnings, and handoff context. Temporary hidden reasoning or speculative notes do not.

Session continuity uses a compact `.ag-kit/handoff.md` artifact containing the goal, current state, decisions, changed files, verification evidence, open risks, and next concrete action. Previous handoffs archive under `.ag-kit/` rather than being silently destroyed.

Cross-project brain search is opt-in: only explicitly registered projects participate, searched projects are read-only from the search operation, and AG Kit never recursively crawls `$HOME` looking for context.

## Context economy

Large tool/command output should not flood the model context.

```text
command
    ↓
no-shell-interpolation spawn
    ↓
full output → .ag-kit/session-sandbox/
    ↓
bounded summary → active context
```

Bare `python` / `python3` commands may resolve to a usable project virtual environment in `.venv`, `venv`, or `env`. Explicit interpreter paths are preserved.

`ag-kit compress` performs deterministic Markdown compaction and reports measured byte reduction. It writes a separate output by default; explicit in-place writes create a backup and remain project-contained through realpath-aware path checks.

## Team assembly

`ag-kit team` creates project-specific roles from archetypes such as software, web, research, content, game, or operations.

Generated roles:

- live under `.ag-kit/agents/`;
- receive the shared core, relevant skills, packs, and project brief;
- return explicit evidence and handoff notes;
- do not claim another role's verification as their own.

## Cross-audit flow

Cross-audit is independent and read-only by construction.

```text
project target / git diff
    ↓
snapshot
    ↓
temporary reviewer workspace
    ├── Codex lineage
    ├── Gemini lineage
    ├── Qwen lineage
    └── other available independent CLI
    ↓
stdout findings only
    ↓
.ag-kit audit report + receipt
```

Reviewer CLIs do not receive a writable mount of the source project. AG Kit prefers multiple independent lineages rather than several reviewers backed by the same model family. Consensus findings are evidence, not automatic authorization to modify source.

## Preflight flow

`ag-kit preflight` runs the local blocking gates that can be executed from the repository checkout before a release-quality result is accepted.

Local preflight gates include:

- v2 architecture budget;
- documentation-link integrity;
- v2 engine tests;
- runtime contract + committed projection drift checks;
- runtime adapter regression tests;
- runtime projection build;
- native runtime artifact build;
- CLI tests.

Those gates are invoked through runtime-neutral root commands. Adapter-specific doctor/hook/plugin checks are discovered through the generic runtime runners rather than promoted to product-wide gates.

Full GitHub CI additionally enforces CLI package dry-run and production audit, representative multi-runtime lifecycle smoke, Windows compatibility, web lint/typecheck/build/audit, and Dependency Review.

## Runtime boundary

`shared/` is canonical. Runtime folders are adapters, and runtime installs default to the repository release tag matching the CLI version rather than floating `main`.

The current capability matrix exposes 16 runtime targets across first-class, connected, and bridge tiers.

| Tier | Runtimes |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

A runtime gets only the surfaces AG Kit has actually verified. Missing native agents/hooks/plugins are not simulated in the capability matrix. Project-scoped activation is preferred; global-only integrations are staged for explicit activation rather than silently mutating home configuration.

No runtime is primary. Runtime-specific richness belongs behind `runtimes/<runtime>/`.

## Runtime lifecycle

```text
detect
  ↓
prepare backup + ownership manifest
  ↓
install projection + verified MCP wiring/staging
  ↓
doctor: live / standing-by / degraded / untouched
  ↓
uninstall only AG Kit-owned state
```

User drift and project memory are preserved. Filesystem root and the user's home directory are rejected as project targets.

## Adapter projections

Different hosts receive different projections according to verified capabilities:

- Antigravity: `.agents/` with rules, skills, agents, hooks, MCP, and plugin metadata.
- Claude: `.claude/` skills/agents plus managed `CLAUDE.md` and project MCP.
- Codex: managed `AGENTS.md`, shared skills, and `.codex-plugin/` MCP/plugin projection.
- Gemini/Qwen/Kimi/Cline and lower tiers receive only the native/portable surfaces declared in `platform-capabilities.json`.

Generated host trees are outputs. Shared behavior must not be authored separately inside them.

## Safety boundary

1. Runtime permissions and workspace trust remain enabled.
2. AG Kit adapter hooks supplement runtime controls; they do not replace sandboxing or human approval.
3. High-confidence destructive command patterns may be denied at a verified host tool boundary.
4. Cross-audit is read-only and runs outside the writable source tree.
5. Project-global or user-global configuration is not silently overwritten when a project-scoped adapter is sufficient.
6. Context artifacts cannot escape the project through symlinked parent paths.
7. Release-quality work requires executable verification, not inspection-only claims.
8. Product-wide CI uses runtime-neutral gates; host-specific checks remain adapter evidence.
