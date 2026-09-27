# Release setup

The workflow files provide a secure baseline, but maintainers must configure repository and environment settings before production use.

## Branch protection

Protect `main` and require pull requests. Require these checks before merge:

- `V2 core validation`
- `CLI tests and package validation`
- `CLI Windows compatibility`
- `Web lint, typecheck, build, and audit`
- `Runtime contracts`
- `Dependency Review`

Dismiss stale approvals after new commits. Block force pushes and branch deletion. Keep release PRs in Draft until the hands-on smoke tests in `PRODUCTION_CHECKLIST.md` are complete and recorded in the PR.

The core job runs documentation-link integrity and generic runtime contract checks. The Linux CLI job packs the real npm artifact and exercises legacy migration plus representative multi-runtime lifecycle paths through the npm-created binary. The Windows CLI job runs the full CLI test suite and package dry-run so path, entrypoint, MCP, lifecycle, and package assumptions are exercised on Windows as well as Linux.

## npm Trusted Publishing

1. In npm package settings for `@vudovn/ag-kit`, configure GitHub Actions as a trusted publisher.
2. Set the repository and workflow to `.github/workflows/publish.yml`.
3. Create a GitHub Environment named `npm` and require approval when appropriate.
4. Remove any legacy `NPM_TOKEN` secret after a successful OIDC release.

The publish workflow requires `id-token: write` and must not consume a long-lived npm token. Tag releases as `v<version>`; the workflow verifies that the tag without `v` equals `cli/package.json` exactly.

## Versioned runtime source integrity

Published v2 CLI runtime installs download their projection source from `v<CLI_VERSION>` by default rather than floating `main`.

Before tagging:

- ensure the intended tag contains the same `shared/`, `packs/`, and runtime adapters tested by CI;
- verify `runtimeSourceSpec()` resolves to that release tag;
- use `--branch` only as an explicit development/beta override;
- do not publish a package version whose matching repository tag will not exist.

## Production deployment

Create a protected GitHub Environment named `production`. Store deployment values as environment secrets/variables using placeholders appropriate to the selected platform, for example:

- `DOKPLOY_TOKEN`
- `DOKPLOY_URL`
- `DOKPLOY_APPLICATION_ID`

Never place token samples, internal addresses, application IDs, or private certificate material in repository documentation.

Require an approval gate and a rollback plan before the deployment job can access production credentials. Deployment/preview integrations are operational concerns and must not weaken repository CI, dependency, or package-release gates.

## Multi-runtime release evidence

The runtime matrix is a capability claim, not a marketing list. Before marking a release PR ready:

1. run the full automated command set in `PRODUCTION_CHECKLIST.md`;
2. run `ag-kit runtime detect` in representative staging projects;
3. verify at least two different first-class runtimes from their actual host applications where practical;
4. verify a plugin/instruction-style target whose ownership shape differs from directory-based hosts;
5. verify global-only targets are staged rather than silently modifying home configuration;
6. verify runtime doctor reports lifecycle state that matches files on disk;
7. verify uninstall preserves user drift and project memory;
8. after the release tag exists, confirm default install without `--branch` resolves to the matching release tag;
9. record platform-specific caveats in `platform-capabilities.json`/docs rather than pretending parity.

Adapter-specific evidence belongs with the adapter. For example, a runtime that supports native hooks should test hook payload/decision behavior; a runtime that packages plugins should build and inspect that artifact. These are adapter checks, not primary-runtime requirements for the whole product.

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
- root, CLI, web, package locks, generated runtime metadata, and release docs use the intended version consistently;
- the Git tag is exactly `v<cli-package-version>`;
- `shared/` is canonical and no runtime is treated as product source-of-truth;
- runtime adapters build from the same source being tagged;
- `platform-capabilities.json` matches adapter declarations;
- generic runtime checks pass without relying on a runtime-specific root command or workflow gate;
- npm `pack --dry-run` contains every required CLI module and no unexpected secret/private file;
- Linux packaged lifecycle smoke and Windows CLI compatibility are green on the final release commit;
- `CHANGELOG.md` `[Unreleased]` entries are moved into the dated release section;
- `MIGRATION.md`, `SECURITY.md`, README files, and `PRODUCTION_CHECKLIST.md` match commands that actually ship;
- release notes match `CHANGELOG.md`;
- no package, release, or production deployment action starts before the PR is intentionally approved and merged;
- rollback commands and prior artifacts are available.
