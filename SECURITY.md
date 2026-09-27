# Security policy

## Supported versions

AG Kit uses calendar versioning. Security fixes are provided for the latest published release. Upgrade the CLI and toolkit before reporting an issue already fixed in a newer release.

## Reporting a vulnerability

Use GitHub private vulnerability reporting or the repository Security Advisory flow. Do not publish suspected secrets, exploitable command payloads, private paths, prompt contents, source code, or proof-of-concept data in a public issue.

Include only sanitized information:

- affected AG Kit, CLI, web, and runtime-projection versions;
- runtime/build/channel and operating system;
- Node.js and relevant tool/runtime versions;
- affected hook, MCP surface, plugin file, runtime adapter, memory/context artifact, CLI command, CI job, or deployment path;
- minimal reproduction steps with credentials and private data removed;
- expected impact, observed behavior, and known mitigations.

## V2 threat model

AG Kit assumes prompts, repository content, tool arguments, MCP responses, external reviewer output, third-party dependencies, and runtime configuration may be untrusted.

Primary risks include:

- prompt/repository instructions inducing unsafe tool use;
- destructive shell commands reaching a trusted host;
- secrets or private content leaking through MCP, logs, observability, handoffs, or cross-project memory;
- malicious or compromised MCP servers and reviewer CLIs;
- generated runtime projections drifting from canonical `shared/` behavior;
- user files being overwritten during install/update/uninstall;
- path traversal or symlink escape from project-local state/artifacts;
- stale or contradictory memory changing agent behavior unexpectedly;
- upstream hook-payload changes causing false blocks or a stuck tool loop;
- dependency, release-source, npm, or GitHub Actions supply-chain compromise.

AG Kit reduces these risks but is not an operating-system sandbox. Keep runtime permissions, workspace trust, least-privilege credentials, code review, and human approval enabled.

## Project containment

AG Kit v2 prefers project-local state under `.ag-kit/` and project-scoped runtime configuration.

Security invariants:

- filesystem root and the user's home directory are rejected as AG Kit project roots;
- context artifact writes are contained by realpath-aware ancestor checks so a symlinked parent cannot escape the project;
- runtime install records ownership and pre-install state before mutation;
- runtime uninstall restores/removes only state AG Kit can prove it owns and preserves later user drift;
- project memory is preserved by runtime uninstall;
- integrations that only expose global configuration are staged for explicit activation rather than silently changed.

## Native Antigravity hook boundary

`.agents/hooks.json` registers a narrow `PreToolUse` safety gate for command execution and a privacy-minimal `PostToolUse` observability hook.

The safety policy reads at most 1 MiB of JSON from stdin, performs no network request, and blocks only high-confidence patterns:

- recursive deletion of a Unix filesystem root;
- filesystem formatting commands;
- raw-disk overwrite with `dd`;
- Windows drive formatting;
- recursive forced deletion of a Windows drive root.

Normal project cleanup such as deleting `dist/` or `node_modules/` is intentionally allowed.

Hook outcomes follow the Antigravity decision contract:

- recognized destructive command → JSON `deny` decision;
- ordinary recognized command → JSON `allow` decision;
- invalid/oversized hook input → JSON `force_ask` decision so a human/runtime permission boundary remains in control;
- an unrecognized payload with no command field → `allow` with an explicit compatibility reason rather than inventing a command.

Direct-run detection resolves the executed file through realpath + file-URL conversion so npm-style symlinks and Windows path syntax cannot silently skip the hook body.

The `PostToolUse` observability hook is fail-open by design. It records only bounded metadata such as sanitized tool name, status, runtime/session identifier, and workspace destination. It must not record prompt bodies, command arguments, file contents, secrets, or become a dependency of the agent loop; it always emits `{}` back to the runtime.

Keep Antigravity's native permission/workspace-trust controls enabled even when AG Kit hooks are active.

## MCP security boundary

The v2 MCP server is local stdio:

```bash
ag-kit mcp serve
```

Runtime installers wire the `ag-kit` MCP entry only for project-scoped formats that AG Kit has verified. The lifecycle manifest lets `runtime doctor` and `runtime uninstall` reason about ownership without treating arbitrary user configuration as AG Kit state.

Review any MCP server source, permissions, network destinations, and data-retention policy before enabling it. Prefer environment-based secret injection where supported. Rotate any credential that appears in a commit, log, artifact, issue, or chat transcript.

AG Kit does not require copying repository MCP configuration into the user home directory.

## Memory, brain, and personalization privacy

Project memory is local-first and human-readable Markdown. Optional indexes are disposable acceleration layers rather than a hidden canonical database.

Cross-project brain behavior is explicitly opt-in:

- projects must be registered explicitly;
- AG Kit does not recursively crawl `$HOME` looking for projects;
- cross-project search is read-only with respect to the searched projects;
- kill switches can disable cross-project behavior.

Personalization separates local learning from disclosure:

- injection is off by default;
- a preference requires verbatim evidence and cross-session confirmation before becoming durable;
- confirmed disclosures can be logged to a local egress ledger;
- `AG_KIT_PROFILE_KILL=1` overrides stored injection settings;
- `personalize forget` removes the preference and related egress rows.

Current user instructions override stale stored preferences/memory. Conflicts should be surfaced and corrected rather than silently resolved in favor of old state.

## Cross-audit boundary

External reviewer CLIs receive snapshot/diff material in temporary workspaces. They do not receive a writable mount of the source project.

Treat reviewer findings as untrusted analysis:

- calling-model lineage can be excluded;
- findings are classified as consensus or contested rather than automatically applied;
- no reviewer result authorizes a write by itself;
- temporary material should contain only the project scope required for the review.

## Context artifacts and command sandbox

`ag-kit run` executes without shell interpolation by default, stores full command output under project-local sandbox state, and returns only a bounded summary to context.

Bare `python` / `python3` may resolve to a usable project virtual environment (`.venv`, `venv`, then `env`). Explicit interpreter paths are not rewritten.

`ag-kit compress` writes a separate artifact by default. `--write` is explicit and creates a timestamped backup before source replacement. Handoff artifacts are project-local and should contain compact continuation facts, not raw conversation dumps or secrets.

## Plugin and generated-artifact security

The Antigravity plugin builder reads repository files only. It does not copy environment variables or home-directory configuration. Review generated plugin contents before installation.

Do not install or publish generated artifacts when:

- their release/version metadata disagrees with the intended tag;
- expected content inventory is missing or unexpected;
- they contain a real credential or private configuration;
- they were generated from an unreviewed branch;
- projection drift, CI, Dependency Review, or production audit is failing.

## Update, runtime install, and rollback safety

Legacy `ag-kit update` keeps the managed-tree merge strategy by default. Local modifications are not silently overwritten; conflicts receive an incoming copy/report and pre-update backups support `ag-kit rollback`.

V2 runtime lifecycle is separate:

```bash
ag-kit runtime install <runtime>
ag-kit runtime doctor <runtime>
ag-kit runtime uninstall <runtime>
```

Published CLI runtime installs default to the repository tag matching the CLI package version (`v<CLI_VERSION>`) instead of floating `main`. `--branch` is an explicit development/source-ref override.

## Repository and release baseline

The repository expects:

- immutable commit-SHA references for GitHub Actions;
- least-privilege `GITHUB_TOKEN` permissions;
- protected `main`, `production`, and `npm` environments where applicable;
- npm Trusted Publishing through OIDC instead of a long-lived npm token;
- private vulnerability reporting, Dependabot, secret scanning, and push protection where available;
- `V2 core validation`, `CLI tests and package validation`, `Web lint, typecheck, build, and audit`, `Antigravity Compatibility`, and `Dependency Review` before release;
- production dependency audits and documentation-link integrity checks;
- hands-on runtime smoke testing appropriate to the release before leaving Draft.

See [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) and [.github/RELEASE_SETUP.md](.github/RELEASE_SETUP.md).
