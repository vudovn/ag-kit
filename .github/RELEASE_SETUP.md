# Release setup

The workflow files provide a secure baseline, but maintainers must configure repository and environment settings before production use.

## Branch protection

Protect `main` and require pull requests. Require these checks before merge:

- `V2 core validation`
- `CLI tests and package validation`
- `CLI Windows compatibility`
- `Web lint, typecheck, build, and audit`
- `Antigravity Compatibility`
- `Dependency Review`

Dismiss stale approvals after new commits. Block force pushes and branch deletion. Keep release PRs in Draft until the hands-on smoke tests in `PRODUCTION_CHECKLIST.md` are complete and recorded in the PR.

The v2 core job also runs documentation-link integrity checks so public migration/security/readme links cannot silently drift to deleted repository paths. The Linux CLI job packs the real npm artifact and runs branch-backed managed-tree plus Antigravity lifecycle smoke tests through the npm-created binary. The Windows CLI job runs the full CLI test suite and package dry-run so path, symlink/entrypoint, MCP, lifecycle, and package assumptions are exercised on Windows as well as Linux.

## npm Trusted Publishing

1. In npm package settings for `@vudovn/ag-kit`, configure GitHub Actions as a trusted publisher.
2. Set the repository and workflow to `.github/workflows/publish.yml`.
3. Create a GitHub Environment named `npm` and require approval when appropriate.
4. Remove any legacy `NPM_TOKEN` secret after a successful OIDC release.

The publish workflow requires `id-token: write` and must not consume a long-lived npm token. Tag releases as `v<version>`; the workflow verifies that the tag without `v` equals `cli/package.json` exactly.

## Versioned runtime source integrity

Published v2 CLI runtime installs download their projection source from `v<CLI_VERSION>` by default rather than floating `main`.

Before tagging:

- ensure the intended tag will contain the same runtime projection tested by CI;
- verify `runtimeSourceSpec()` resolves to that release tag;
- use `--branch` only as an explicit development/beta override;
- do not publish a package version whose matching repository tag will not exist.

## Production deployment

Create a protected GitHub Environment named `production`. Store deployment values as environment secrets/variables using placeholders appropriate to the selected platform, for example:

- `DOKPLOY_TOKEN`
- `DOKPLOY_URL`
- `DOKPLOY_APPLICATION_ID`

Never place token samples, internal addresses, application IDs, or private certificate material in repository documentation.

Require an approval gate and a rollback plan before the deployment job can access production credentials. Deployment/preview integrations are operational concerns and must not be used to weaken repository CI, dependency, or package-release gates.

## Antigravity release evidence

Before marking a release PR ready:

1. run the full automated command set in `PRODUCTION_CHECKLIST.md`;
2. open the release branch in a trusted Antigravity staging workspace;
3. verify `.agents/rules/`, `.agents/skills/`, and `.agents/agents/` are discovered and `.agents/workflows/` is absent;
4. verify natural-language planning intent enters the gated workflow without relying on legacy slash-command files;
5. verify continue/resume intent reads the current handoff and relevant project memory before mutation;
6. test the destructive-command policy with mocked stdin only;
7. verify the PostToolUse observability hook returns `{}` and does not block a normal command;
8. verify the project MCP entry with `ag-kit runtime doctor antigravity` / the relevant staging runtime;
9. build and inspect the local plugin bundle;
10. record Antigravity build/channel, operating system, results, and unresolved warnings in the PR.

## Multi-runtime release evidence

The runtime matrix is a capability claim, not a marketing list. CI automatically smoke-tests the packed CLI against the current reviewed ref for legacy managed-tree init/update and for Antigravity install → doctor → uninstall, including user-file and memory preservation. Before release, still perform hands-on checks where runtime-owned UI or external configuration is involved:

- run `ag-kit runtime detect` in at least one representative staging project;
- verify a first-class runtime is usable from its actual host application, not only from lifecycle state;
- verify global-only targets are staged rather than silently modifying home configuration;
- after the release tag exists, confirm a default install without `--branch` resolves to the matching release tag;
- record any platform-specific caveat in `platform-capabilities.json`/docs rather than pretending parity.

## GitHub security settings

Enable:

- private vulnerability reporting;
- Dependabot alerts, security updates, and version updates;
- dependency graph and Dependency Review;
- secret scanning and push protection when available;
- CodeQL default setup for JavaScript/TypeScript and any other actively shipped language surface;
- protected `npm` and `production` environments;
- branch rules that prevent required checks from being bypassed.

## Release operator checklist

The release operator must confirm:

- the calendar version is chosen only when the artifact is actually ready to tag;
- root, CLI, web, package locks, `.agents/VERSION`, and committed release metadata use the intended version consistently;
- the Git tag is exactly `v<cli-package-version>`;
- `shared/` is canonical and the committed Antigravity projection passes the drift gate;
- runtime adapters build from the same source being tagged;
- npm `pack --dry-run` contains every required CLI module and no unexpected secret/private file;
- Linux packaged lifecycle smoke and Windows CLI compatibility are green on the final release commit;
- `CHANGELOG.md` `[Unreleased]` entries are moved into the dated release section;
- `MIGRATION.md`, `SECURITY.md`, README files, and `PRODUCTION_CHECKLIST.md` match commands that actually ship;
- release notes match `CHANGELOG.md`;
- no package, release, or production deployment action starts before the PR is intentionally approved and merged;
- rollback commands and prior artifacts are available.
