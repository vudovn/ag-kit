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
WRITE RECEIPTS + DURABLE MEMORY
    ↓
DELIVER RESULT
```

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
classify → load minimal skill → build → targeted verification → result
```

Typical examples: a small bug fix, one-file refactor, copy change, or deterministic config edit.

### STANDARD

Default mode for normal feature work.

```text
scout → architect → build → review → verify → result
```

STANDARD requires explicit acceptance criteria and evidence from the project's own checks.

### DEEP

Use for architecture changes, migrations, multi-system work, security-sensitive changes, or broad refactors.

```text
scout
  ↓
architecture + risk map
  ↓
dependency graph
  ↓
wave 1 ─┬─ task A
         └─ task B
  ↓
wave 2 ─┬─ task C
         └─ task D
  ↓
independent review
  ↓
cross-audit when useful
  ↓
preflight
  ↓
result + receipts + memory
```

Parallel work is allowed only when tasks are truly independent. Dependency order wins over artificial concurrency.

## Skill loading

Skills are not permanently resident.

1. The core classifies the request.
2. The runtime loads only relevant `shared/skills/<name>/SKILL.md` contracts.
3. Domain reference material is pulled from `packs/` only when needed.
4. Runtime-specific adapters translate the shared behavior without creating new canonical copies.

The architecture budget currently targets one resident skill and no more than 22 top-level skills; the committed v2 surface contains 18.

## Memory flow

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

Only durable project information belongs in memory: decisions, conventions, recurring constraints, accepted learnings, and handoff context. Temporary chain-of-thought or speculative notes do not.

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

Reviewer CLIs do not receive a writable mount of the source project. AG Kit prefers multiple independent lineages rather than several reviewers backed by the same model family.

## Preflight flow

`ag-kit preflight` runs blocking repository gates before a release-quality result is accepted.

Current gates include:

- v2 architecture budget;
- v2 engine tests;
- Antigravity projection drift check;
- runtime projection build;
- Antigravity doctor;
- Antigravity regression tests;
- native plugin build.

CI additionally runs CLI tests, web lint/typecheck/build, production dependency audits, and dependency review.

## Runtime boundary

`shared/` is canonical. Runtime folders are adapters.

```text
shared/
   ↓
capability matrix
   ↓
┌───────────────┬───────────────┬───────────────┐
│ first-class   │ connected     │ bridge        │
├───────────────┼───────────────┼───────────────┤
│ Antigravity   │ Cursor        │ OpenCode      │
│ Claude        │ Windsurf      │ OpenClaw      │
│ Codex         │ Copilot       │ Aider         │
│ Gemini        │               │               │
│ Qwen          │               │               │
│ Kimi          │               │               │
└───────────────┴───────────────┴───────────────┘
```

A runtime gets only the surfaces AG Kit has actually verified. Missing native agents/hooks/plugins are not simulated in the capability matrix.

## Antigravity projection

Antigravity receives a generated `.agents/` projection containing:

- 18 skills;
- 4 permanent agents;
- zero legacy workflow files;
- one always-on core rule;
- safety hook;
- project MCP config;
- plugin packaging support.

The projection must match `shared/` exactly. CI rejects drift.

## Safety boundary

1. Runtime permissions and workspace trust remain enabled.
2. AG Kit safety hooks supplement runtime controls; they do not replace sandboxing or human approval.
3. High-confidence destructive command patterns are denied at the tool boundary.
4. Cross-audit is read-only and runs outside the writable source tree.
5. Project-global or user-global configuration is not silently overwritten when a project-scoped adapter is sufficient.
6. Release-quality work requires executable verification, not inspection-only claims.

## Completion rule

A task is complete only when the requested artifact exists, acceptance criteria are met, relevant checks pass, unresolved risks are surfaced, and durable outcomes are written to receipts/memory where appropriate.
