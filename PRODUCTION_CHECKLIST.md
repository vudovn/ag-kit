# AG Kit v2 Production Checklist

Use this checklist before marking a v2 release PR ready, creating a release tag, or publishing `@vudovn/ag-kit`.

A green CI run is necessary but not sufficient: release metadata, migration guidance, package contents, runtime source pinning, and rollback behavior must agree with the code being shipped.

## 1. Branch and PR state

- [ ] Release work is on a reviewable branch; do not publish from an unreviewed working tree.
- [ ] PR base is the intended release branch (`main` unless intentionally changed).
- [ ] PR description matches the actual architecture and supported runtime matrix.
- [ ] No temporary migration/workflow files remain under `.github/workflows/`.
- [ ] No unresolved review thread or known release-blocking issue is being hidden by a documentation-only workaround.

## 2. Architecture invariants

Run:

```bash
npm run check:v2
npm run test:v2
npm run check:antigravity-projection
npm run build:runtimes
```

Confirm:

- [ ] exactly one resident core skill (`ag-core`);
- [ ] 18 top-level hot-loaded skills stay within the configured budget;
- [ ] four permanent agents remain `scout`, `architect`, `builder`, `reviewer`;
- [ ] one development flow engine remains canonical;
- [ ] `.agents/` is a generated/native Antigravity projection, not a second source of truth;
- [ ] legacy `.agents/workflows/` is absent;
- [ ] `platform-capabilities.json` and runtime adapters do not drift.

## 3. CLI and npm package

Run:

```bash
npm --prefix cli ci
npm --prefix cli test
npm --prefix cli pack --dry-run
npm --prefix cli audit --omit=dev --audit-level=high
```

Confirm:

- [ ] `ag-kit --help` exposes v2, context, runtime, and legacy lifecycle commands;
- [ ] `ag-kit runtime --help` includes `detect`, `install-present`, `install`, `doctor`, and `uninstall`;
- [ ] npm-style symlink execution works for both the public dispatcher and legacy lifecycle entrypoint;
- [ ] `lib/` contains every module referenced by the dispatcher (including help, context, brain, runtime discovery, and source pinning);
- [ ] default runtime downloads resolve to `v<CLI_VERSION>` rather than floating `main`;
- [ ] `--branch` remains an explicit source-ref override for development/testing;
- [ ] production npm audit has no high/critical finding.

## 4. Runtime lifecycle smoke test

In a disposable project, run:

```bash
ag-kit runtime detect
ag-kit runtime install <one-installed-runtime>
ag-kit runtime doctor <one-installed-runtime>
ag-kit runtime uninstall <one-installed-runtime>
```

Confirm:

- [ ] install creates an ownership/lifecycle manifest and pre-install backup when required;
- [ ] doctor reports a meaningful state (`live`, `standing-by`, `degraded`, or `untouched`);
- [ ] uninstall removes/restores only AG Kit-owned state;
- [ ] user drift survives uninstall;
- [ ] `.ag-kit/memory/` survives runtime uninstall;
- [ ] filesystem root and user home are rejected as project targets;
- [ ] user-global runtime configuration is never silently mutated.

## 5. Memory and continuity

In a disposable project, run:

```bash
ag-kit memory init
ag-kit memory add "Use pnpm for this repository" --kind convention --session release-audit
ag-kit memory recall "package manager" --session release-audit-2
ag-kit handoff quick "Release smoke test paused" --next "Resume verification"
ag-kit handoff show
```

Confirm:

- [ ] Markdown remains the canonical memory store;
- [ ] recall works without requiring SQLite;
- [ ] optional index state can be rebuilt from Markdown;
- [ ] handoff is written under `.ag-kit/` and old handoffs archive safely;
- [ ] continue/resume activation loads handoff + relevant durable memory before project mutation;
- [ ] cross-project memory only searches explicitly registered projects and never crawls `$HOME` automatically.

## 6. Context economy and command sandbox

Run a bounded-output smoke test through:

```bash
ag-kit run node -e "for(let i=0;i<100;i++) console.log(i)"
```

Confirm:

- [ ] full output is stored on disk while returned context remains bounded;
- [ ] command execution does not use shell interpolation by default;
- [ ] bare `python` / `python3` prefers `.venv`, then `venv`, then `env` when a usable project interpreter exists;
- [ ] explicit interpreter paths are never silently replaced;
- [ ] `ag-kit compress <file>` writes a separate compact file by default;
- [ ] `compress --write` creates a backup and cannot escape the project through symlink parents.

## 7. Antigravity-native validation

Run:

```bash
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

Confirm:

- [ ] native projection contains 18 skills and four permanent agents;
- [ ] `PreToolUse` safety hook emits valid decision JSON for ordinary and denied payloads;
- [ ] safety hook direct-run detection works through symlinked paths;
- [ ] `PostToolUse` observability always returns `{}` and never blocks the agent loop;
- [ ] plugin output is deterministic;
- [ ] no secret, home-directory configuration, prompt body, command arguments, or file contents are captured by observability telemetry.

Mock destructive payload test only — never execute the destructive command:

```bash
printf '%s' '{"toolCall":{"name":"run_command","args":{"CommandLine":"rm -rf /"}}}' \
  | node .agents/hooks/validate-tool-call.mjs
```

## 8. Cross-audit and privacy

Confirm:

- [ ] external reviewer CLIs receive read-only snapshot/diff material, not a writable project mount;
- [ ] calling-model lineage exclusion works when requested;
- [ ] consensus and contested findings remain distinguishable;
- [ ] personalization injection defaults off;
- [ ] `AG_KIT_PROFILE_KILL=1` overrides stored profile settings;
- [ ] `personalize forget` removes both the inference and related egress rows;
- [ ] no fabricated token-savings multiplier is reported.

## 9. Web/docs quality gate

Run:

```bash
npm --prefix web ci
npm --prefix web run lint
npm --prefix web run typecheck
npm --prefix web run build
npm --prefix web audit --omit=dev --audit-level=high
```

Confirm:

- [ ] docs describe **1 core / 18 skills / 4 permanent agents / 1 flow / 16 runtimes**;
- [ ] EN/VI/ZH/JA install copy no longer claims the legacy 47-skill / 20-agent / 13-workflow inventory;
- [ ] current docs require Node.js 22+;
- [ ] `README.md`, `README-VI.md`, `MIGRATION.md`, `CHANGELOG.md`, `SECURITY.md`, and this checklist have no known broken top-level links;
- [ ] production dependency audit passes.

## 10. Release metadata

Only when the code is actually ready to release:

- [ ] choose the calendar version (`YYYY.M.D`);
- [ ] move the `CHANGELOG.md` `[Unreleased]` entries into that dated release section;
- [ ] update root, CLI, web, lockfile, and committed runtime/version metadata consistently;
- [ ] ensure `cli/package.json` version equals the intended Git tag without the leading `v`;
- [ ] run the full CI matrix again after the version bump;
- [ ] create tag `v<version>` only from the reviewed release commit.

Do **not** bump the version early just to make a branch look release-ready; the version should identify the artifact that will actually be tagged and published.

## 11. Publish and rollback readiness

The npm publish workflow verifies the Git tag against `cli/package.json` and uses Trusted Publishing.

Before tagging:

- [ ] `ag-kit update --dry-run` still produces a non-destructive migration plan for legacy managed trees;
- [ ] `ag-kit rollback` can restore a pre-update `.agents` backup;
- [ ] runtime uninstall behavior is documented separately from legacy tree rollback;
- [ ] `MIGRATION.md` reflects the commands that actually ship in the package;
- [ ] the PR can remain Draft until maintainers intentionally choose review/merge timing.

## Required GitHub gates

For the final release commit, require:

- [ ] **CI** — v2/core, CLI/package, web build, and production audits;
- [ ] **Antigravity Compatibility** — projection/doctor/tests/plugin build;
- [ ] **Dependency Review**.

External preview/deployment integrations are operational concerns and should not be used to weaken or bypass these repository gates.
