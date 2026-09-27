# CLAUDE.md

This file provides repository guidance to Claude Code when working on AG Kit.

## What this repository is

AG Kit v2 is a lean multi-runtime operating layer for AI coding agents.

Canonical behavior lives in `shared/`:

- `shared/core/` — one tiny always-on operating contract;
- `shared/skills/` — 18 top-level hot-loaded behavior skills;
- `shared/agents/` — four permanent roles: `scout`, `architect`, `builder`, `reviewer`;
- `shared/flows/` — one development spine with QUICK / STANDARD / DEEP modes;
- `packs/` — domain reference knowledge loaded only when relevant.

Runtime surfaces are adapters/projections:

- `.agents/` — native Antigravity projection (18 skills, 4 agents, rules, hooks, MCP, plugin support, **no legacy workflow files**);
- `runtimes/` — capability-aware projections for the rest of the supported runtime matrix;
- `platform-capabilities.json` — machine-readable capability claims.

The other major deliverables are:

- `cli/` — npm package `@vudovn/ag-kit`, Node.js 22+, ESM;
- `web/` — Next.js 16 docs/marketing site;
- `.ag-kit/` — project-local runtime state produced in consumer projects (memory, receipts, lifecycle manifests, audits, handoffs, etc.), not a canonical source folder in this repository.

## Operating rules

1. Treat `shared/` as source of truth. Do not add reusable behavior directly to runtime projections.
2. Keep the resident core small. New capability belongs in a hot-loaded skill or pack unless it is truly universal.
3. Natural-language intent is authoritative; do not depend on a slash-command UI.
4. Explicit plan/spec/brainstorm/architecture requests enter the development flow before multi-file mutation.
5. Continue/resume requests load the latest handoff and relevant durable memory before mutation.
6. Verify `platform-capabilities.json` before claiming a runtime supports hooks, agents, MCP, plugins, or another native surface.
7. Do not recreate `.agents/workflows/`; QUICK/STANDARD/DEEP are modes of one flow engine.
8. Do not silently mutate user-global runtime configuration. Prefer project scope; stage global-only activation explicitly.
9. Preserve user drift during runtime uninstall/update unless ownership can be proven.
10. Evidence beats completion claims: run the relevant gates and report failures rather than weakening them.

## Commands

Run from repository root unless noted.

```bash
# V2 architecture + docs
npm run check:v2
npm run check:docs
npm run test:v2
npm run check:antigravity-projection
npm run build:runtimes

# Antigravity native projection
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin

# CLI
npm run test:cli
# or:
npm --prefix cli test
npm --prefix cli pack --dry-run
npm --prefix cli audit --omit=dev --audit-level=high

# Web
npm run lint:web
npm run typecheck:web
npm run build:web
npm --prefix web audit --omit=dev --audit-level=high
```

There is no Python-based canonical toolkit validator in v2. Do not restore removed `generate:agents`, `check:agents`, `test:toolkit`, manifest-lock, dependency-graph, or legacy workflow regeneration steps.

## CLI architecture

`cli/bin/ag-kit.js` is the public dispatcher.

Key surfaces include:

- `runtime detect/install-present/list/install/doctor/uninstall`;
- evolving `memory` plus opt-in cross-project `brain`;
- `flow`, `team`, and `cross-audit`;
- `route` and bounded `run` command sandbox;
- `compress` and `handoff` continuity tools;
- local `observe` / `dashboard`;
- `personalize` privacy controls;
- `design` contract tools;
- `mcp serve`;
- legacy managed-tree `init/update/rollback/status` for safe migration compatibility.

Published runtime installs default to the repository tag matching the CLI version (`v<CLI_VERSION>`), not floating `main`. `--branch` is an explicit source-ref override for development/testing.

## Memory and privacy

- Project memory is Markdown-first under `.ag-kit/memory/` in consumer projects.
- SQLite/FTS5 is optional, rebuildable acceleration only.
- Cross-project brain search is opt-in and never automatically crawls `$HOME`.
- External cross-audit reviewers receive read-only snapshot/diff workspaces, not a writable source mount.
- Personalization injection defaults off; `AG_KIT_PROFILE_KILL=1` is the hard kill switch.
- Observability must not record prompt bodies, command arguments, file contents, or secrets.

## Antigravity hooks

The native safety hook is intentionally narrow: it blocks high-confidence root/disk destructive operations and supplements, rather than replaces, Antigravity permissions/workspace trust.

Hook entrypoint detection must remain cross-platform and symlink-safe. `PostToolUse` observability must always fail open and return `{}` so telemetry can never block the agent loop.

## Release

AG Kit uses CalVer `YYYY.M.D`. Do not bump versions while a large branch is still being polished.

When the artifact is ready:

1. follow `PRODUCTION_CHECKLIST.md`;
2. move `CHANGELOG.md` `[Unreleased]` entries into the dated release section;
3. synchronize root/CLI/web/lock/runtime version metadata;
4. rerun every required GitHub gate;
5. create tag `v<version>` only from the reviewed release commit.

The npm publish workflow uses Trusted Publishing and verifies the tag against `cli/package.json`.

## Web notes

`next build --webpack` is intentional. Keep web copy consistent with the v2 inventory: 1 core, 18 hot-loaded skills, 4 permanent agents, one development spine, and 16 runtime targets.
