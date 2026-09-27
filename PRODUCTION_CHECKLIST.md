# AG Kit v2 Production Checklist

Use this checklist before marking a v2 release PR ready, creating a release tag, or publishing `@vudovn/ag-kit`.

A green CI run is necessary but not sufficient: release metadata, migration guidance, package contents, runtime source pinning, ownership behavior, and reproducible evidence must agree with the code being shipped.

## 1. Branch and PR state

- [ ] Release work is on a reviewable branch.
- [ ] PR base is the intended release branch (`main` unless intentionally changed).
- [ ] PR description matches the actual architecture and supported runtime matrix.
- [ ] No temporary migration/workflow files remain under `.github/workflows/`.
- [ ] No unresolved release-blocking review is hidden by a docs-only workaround.

## 2. Architecture and evidence invariants

Run:

```bash
npm run check:v2
npm run check:docs
npm run test:v2
npm run benchmark:v2 -- --output dist/evidence/benchmark-v2.json
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
```

Confirm:

- [ ] exactly one resident core skill (`ag-core`);
- [ ] 18 top-level hot-loaded skills stay within the configured budget;
- [ ] four permanent agents remain `scout`, `architect`, `builder`, `reviewer`;
- [ ] one development flow engine remains canonical;
- [ ] `shared/` remains canonical and runtime projections do not become source-of-truth forks;
- [ ] no runtime is declared primary in repository contracts or public docs;
- [ ] root package scripts and GitHub workflow gates remain runtime-neutral;
- [ ] legacy `.agents/workflows/` is absent;
- [ ] the old Antigravity-only `init/update/rollback/status` lifecycle source is absent;
- [ ] `platform-capabilities.json` and runtime adapters do not drift;
- [ ] deterministic benchmark fixtures pass for memory recall, routing, compression, and runtime lifecycle;
- [ ] CI uploads the benchmark receipt and fails if the receipt is missing.

## 3. CLI and npm package

Run:

```bash
npm --prefix cli ci
npm --prefix cli test
npm --prefix cli pack --dry-run
npm --prefix cli audit --omit=dev --audit-level=high
```

Confirm:

- [ ] global npm installation installs the CLI only;
- [ ] `ag-kit --help` exposes only the runtime-neutral v2 command surface;
- [ ] `ag-kit --version` works directly and through an npm-style symlink;
- [ ] unknown commands fail instead of falling back to a second lifecycle;
- [ ] `ag-kit runtime --help` exposes discovery, install, doctor, and uninstall commands;
- [ ] machine-readable project-relative paths use stable `/` separators across Linux and Windows;
- [ ] default runtime downloads resolve to `v<CLI_VERSION>` rather than floating `main`;
- [ ] `--branch` remains an explicit source-ref override for development/testing;
- [ ] MCP runtime status reports all lifecycle manifests in multi-runtime projects;
- [ ] production npm audit has no high/critical finding.

## 4. Multi-runtime lifecycle smoke

CI must install the real packed npm artifact and exercise multiple ownership/projection shapes. The representative set currently covers Antigravity, Claude, and Codex.

For each representative runtime, verify:

```bash
ag-kit runtime install <runtime> --branch <reviewed-ref>
ag-kit runtime doctor <runtime>
ag-kit runtime uninstall <runtime>
ag-kit runtime doctor <runtime>
```

Confirm:

- [ ] install creates an ownership/lifecycle manifest and backup when required;
- [ ] doctor reports a meaningful state (`live`, `standing-by`, `degraded`, or `untouched`);
- [ ] uninstall removes/restores only AG Kit-owned state;
- [ ] user drift survives uninstall;
- [ ] `.ag-kit/memory/` survives runtime uninstall;
- [ ] filesystem root and user home are rejected as project targets;
- [ ] user-global runtime configuration is never silently mutated.

For migration from a pre-v2 Antigravity project, keep a committed/external backup and run the same `runtime install antigravity` lifecycle. There is no separate managed-tree release path.

After the matching `v<CLI_VERSION>` tag exists, repeat a default install without `--branch` and verify source resolution uses the release tag.

## 5. Memory and continuity

```bash
ag-kit memory init
ag-kit memory add "Use pnpm for this repository" --kind convention --session release-audit
ag-kit memory recall "package manager" --session release-audit-2
ag-kit handoff quick "Release smoke test paused" --next "Resume verification"
ag-kit handoff show
```

Confirm Markdown remains canonical, optional FTS/semantic indexes are rebuildable, semantic retrieval stays opt-in/local, handoffs archive safely, and cross-project search never crawls `$HOME` automatically.

## 6. Context economy and command sandbox

```bash
ag-kit run node -e "for(let i=0;i<100;i++) console.log(i)"
```

Confirm full output is stored on disk while returned context stays bounded, shell interpolation is not used by default, project virtualenv preference is safe, explicit interpreter paths are preserved, and context artifact writes cannot escape the project through symlink parents.

## 7. Runtime adapter validation

Root validation is runtime-neutral. Adapter-specific evidence belongs inside `runtimes/<runtime>/` and is invoked through the generic runners:

```bash
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
```

For adapters that expose native hooks/plugins, additionally confirm payload shape, deterministic artifact output, privacy boundaries, and failure behavior.

Antigravity-specific destructive-command tests must use mocked stdin only; this remains adapter evidence, not a product-wide primary-runtime gate.

## 8. Cross-audit and privacy

Confirm external reviewer CLIs receive read-only snapshot/diff material, lineage exclusion works, reviewer lineages execute with bounded parallelism, consensus/contested findings stay distinguishable, trace IDs connect evidence to the active flow, personalization injection defaults off, kill switches override stored settings, forget semantics purge related egress state, and no fabricated token-savings multiplier is reported.

## 9. Web/docs quality gate

```bash
npm run check:docs
npm --prefix web ci
npm --prefix web run lint
npm --prefix web run typecheck
npm --prefix web run build
npm --prefix web audit --omit=dev --audit-level=high
```

Confirm docs describe **1 core / 18 skills / 4 permanent agents / 1 flow / 16 runtimes**, package-level docs match shipped commands, Node.js 22+ remains the requirement, local links/claims pass, and public copy does not present one runtime as the product identity.

## 10. Release metadata

Only when the code is actually ready to release:

- [ ] choose the calendar version (`YYYY.M.D`);
- [ ] move `[Unreleased]` changelog entries into that dated release section;
- [ ] update root, CLI, web, lockfile, and committed runtime/version metadata consistently;
- [ ] ensure `cli/package.json` version equals the intended Git tag without the leading `v`;
- [ ] run the full CI matrix again after the version bump;
- [ ] create tag `v<version>` only from the reviewed release commit.

Do not bump the version early just to make a branch appear release-ready.

## 11. Migration and removal readiness

Before tagging:

- [ ] `MIGRATION.md` describes only commands that actually ship;
- [ ] pre-v2 Antigravity migration uses `runtime install antigravity`, not a hidden second lifecycle;
- [ ] runtime uninstall restores/removes only adapter-owned state and preserves user drift/memory;
- [ ] project backup/version control is documented as the recovery path for pre-v2 state that is not adapter-owned;
- [ ] the PR can remain Draft until maintainers intentionally choose review/merge timing.

## Required GitHub gates

For the final release commit, require:

- [ ] **CI / V2 core validation**;
- [ ] **CI / CLI tests and package validation**;
- [ ] **CI / CLI Windows compatibility**;
- [ ] **CI / Web lint, typecheck, build, and audit**;
- [ ] **Runtime Compatibility / Runtime contracts**;
- [ ] **Dependency Review**.

External preview/deployment integrations are operational concerns and must not weaken or bypass repository gates.
