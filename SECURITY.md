# Security policy

## Supported versions

AG Kit uses calendar versioning. Security fixes are provided for the latest published release. Upgrade the CLI and runtime projections before reporting an issue already fixed in a newer release.

## Reporting a vulnerability

Use GitHub private vulnerability reporting or the repository Security Advisory flow. Do not publish suspected secrets, exploitable command payloads, private paths, prompt contents, source code, or proof-of-concept data in a public issue.

Include only sanitized information: affected version/runtime, OS/tool versions, affected hook/MCP/adapter/CLI path, minimal reproduction steps, expected impact, observed behavior, and known mitigations.

## Threat model

AG Kit assumes prompts, repository content, tool arguments, MCP responses, reviewer output, dependencies, and runtime configuration may be untrusted.

Primary risks include unsafe tool use, destructive commands, secret leakage, compromised MCP/reviewer tools, adapter drift, accidental overwrite of user files, path/symlink escape, stale memory, host hook/config changes, and supply-chain compromise.

AG Kit reduces these risks but is not an operating-system sandbox. Keep host permissions, workspace trust, least-privilege credentials, code review, and human approval enabled.

## Runtime-neutral architecture boundary

`shared/` is canonical. Runtime-specific code belongs under `runtimes/<runtime>/`; generated host trees are projections.

Security invariants:

- no runtime is the product's primary runtime or canonical source;
- adapter capability claims must match `platform-capabilities.json`;
- root validation/workflow gates remain runtime-neutral;
- host-native hooks/plugins are adapter evidence, not global assumptions;
- generated projections may not silently fork reusable policy from `shared/`.

## One lifecycle, explicit ownership

AG Kit v2 has one lifecycle for every runtime:

```bash
ag-kit runtime install <runtime>
ag-kit runtime doctor <runtime>
ag-kit runtime uninstall <runtime>
```

The old Antigravity-only managed-tree lifecycle is removed.

Security properties:

- runtime install records pre-install state and ownership before mutation;
- runtime uninstall restores/removes only state AG Kit can prove it owns;
- later user drift is preserved;
- `.ag-kit/memory/` is preserved by runtime uninstall;
- filesystem root and the user home directory are rejected as project roots;
- user-global-only integrations are staged for explicit activation rather than silently mutated;
- published CLI runtime installs resolve to `v<CLI_VERSION>` by default; `--branch` is an explicit reviewed-ref override.

For migration from pre-v2 Antigravity projects, commit or externally back up the project first, then install the Antigravity adapter through this same lifecycle. Version control/external backup is the recovery boundary for pre-v2 state not owned by a v2 adapter.

## Project containment

Project-local state lives under `.ag-kit/` where possible. Context artifact writes use realpath-aware containment so symlink parents cannot escape the project. Machine-readable project paths are normalized for portability without weakening filesystem checks.

## Host-native hook boundaries

Native hooks supplement host permissions; they never replace runtime trust controls, sandboxing, or human review.

For Antigravity, the adapter may project narrow command-safety and privacy-minimal observability hooks. Safety rules block only high-confidence destructive root/disk patterns; invalid/oversized payloads fail toward the host/human permission boundary rather than inventing a command.

Prompt-quality hooks are fail-open and must not persist raw prompts in telemetry. Automatic prompt interception is enabled only where the adapter has a current, verified hook contract and lifecycle/trust semantics are understood.

Observability hooks may record bounded metadata such as sanitized tool name, status, runtime/session identifiers, and trace IDs. They must not record prompt bodies, command arguments, file contents, or secrets.

## MCP security boundary

The MCP server is local stdio:

```bash
ag-kit mcp serve
```

Runtime adapters wire the `ag-kit` MCP entry only for project-scoped formats AG Kit has verified. Global-only integrations are staged for explicit activation. Lifecycle manifests let doctor/uninstall reason about ownership without treating arbitrary user configuration as AG Kit state.

Review any MCP server source, permissions, network destinations, and data-retention policy before enabling it. Prefer environment-based secret injection where supported.

## Memory, semantic retrieval, brain, and personalization

Project memory is local-first and human-readable Markdown. SQLite/FTS5, graph, and semantic indexes are disposable acceleration layers rather than hidden canonical stores.

The local semantic tier is opt-in. Model download is not implicit; index rebuilds must not turn raw memory into a second canonical store.

Cross-project brain behavior is opt-in:

- projects must be explicitly registered;
- AG Kit does not recursively crawl `$HOME`;
- cross-project search is read-only with respect to searched projects;
- kill switches can disable cross-project behavior.

Personalization injection is off by default, preferences require evidence and cross-session confirmation, disclosures can be logged locally, `AG_KIT_PROFILE_KILL=1` overrides stored settings, and forget removes related egress state.

Current user instructions override stale stored memory/preferences. Conflicts should be surfaced rather than silently resolved in favor of old state.

## Cross-audit boundary

External reviewer CLIs receive bounded snapshot chunks in temporary workspaces. They do not receive a writable source-project mount.

- calling-model lineage can be excluded;
- independent lineages run with bounded concurrency and timeout handling;
- findings are consensus/contested rather than auto-applied;
- reviewer output is untrusted analysis;
- trace IDs correlate evidence without granting write authority;
- no reviewer result authorizes a mutation by itself.

## Context artifacts and command sandbox

`ag-kit run` executes without shell interpolation by default, stores full command output under project-local sandbox state, and returns a bounded summary.

Bare `python` / `python3` may resolve to a project virtualenv. Explicit interpreter paths are not rewritten.

`ag-kit compress` is non-destructive by default. Explicit overwrite creates a backup. Handoff artifacts should contain compact continuation facts, not raw conversation dumps or secrets.

## Generated artifacts and release evidence

Runtime artifact builders must consume reviewed repository input only and must not copy environment variables or user-home configuration.

Do not install/publish generated artifacts when version metadata disagrees, expected inventory is missing, secrets/private config appear, source is unreviewed, runtime drift/CI/Dependency Review/audit is failing, or deterministic benchmark evidence is missing.

The benchmark receipt is local/deterministic evidence for memory recall, routing, compression, and runtime lifecycle. It does not fabricate a no-AG-Kit baseline or require paid providers.

## Repository and release baseline

The repository expects:

- immutable commit-SHA references for GitHub Actions;
- least-privilege workflow permissions;
- npm Trusted Publishing through OIDC rather than long-lived npm tokens;
- private vulnerability reporting, Dependabot, secret scanning, and push protection where available;
- `V2 core validation`, `CLI tests and package validation`, `CLI Windows compatibility`, `Web lint, typecheck, build, and audit`, `Runtime contracts`, and `Dependency Review` before release;
- production dependency audits plus documentation link/claim integrity;
- representative multi-runtime packaged lifecycle smoke before leaving Draft.

See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) and [.github/RELEASE_SETUP.md](.github/RELEASE_SETUP.md).
