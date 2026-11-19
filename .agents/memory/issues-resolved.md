---
type: reference
created: 2026-08-31
updated: 2026-08-31
---

# Issues Resolved

> Cross-session tracking of resolved technical issues and root causes. Consult this log first to avoid repeating past debugging cycles or re-introducing solved bugs.

## Format
Each resolved issue follows this standard structure:
- **Symptom:** Observed error message, failing test, or broken behavior.
- **Root Cause:** Underlying technical cause.
- **Fix:** Changes applied to solve the problem.
- **Prevention Rule:** Rule or check to prevent recurrence.

---

## Issue 1: Windows CRLF Line Endings in Manifest SHA-256 Lockfile
- **Symptom:** GitHub Actions Linux runner fails with `Stale generated registry files: manifest.lock.json` when checked with `python .agents/scripts/generate_manifest.py .agents --check`.
- **Root Cause:** `component_registry.py` reads component files in raw binary mode (`open("rb")`). On Windows, default git configurations checkout text files with CRLF (`\r\n`), causing Windows-computed SHA-256 hashes to mismatch Linux runners that clone with LF (`\n`).
- **Fix:** Enforce `core.autocrlf false` and `core.eol lf` in git configuration and save all `.agents/` assets with pure Unix LF line endings.
- **Prevention Rule:** Never commit CRLF line endings in `.agents/`; always verify with `python .agents/scripts/generate_manifest.py .agents --check`.

## Issue 2: Next.js and Sharp Production Dependency Audit Vulnerabilities
- **Symptom:** CI fails on the `web` job during `npm audit --omit=dev --audit-level=high` with critical/high security advisories.
- **Root Cause:** Upstream dependencies in `web/package.json` had outdated versions of `next` and `sharp` subject to published CVE advisories.
- **Fix:** Upgraded `next` to `^16.4.6` and defined package overrides for `"sharp": "0.35.5"` and `"source-map-js": "^1.2.4"`.
- **Prevention Rule:** Run `npm audit --omit=dev --audit-level=high` before pushing any PR branch.

## Issue 3: Strict `npm ci` Lockfile Mismatch for Next.js Transitive Packages
- **Symptom:** `npm ci` fails with `lock file's @next/mdx does not satisfy @next/mdx@16.2.10`.
- **Root Cause:** Pinned dependencies (`@next/mdx: 16.2.10`) conflicted with updated `next` package version (`16.4.6`) in `package-lock.json`.
- **Fix:** Aligned `@next/mdx` and `eslint-config-next` to `^16.4.6` in `web/package.json` and synchronized `package-lock.json`.
- **Prevention Rule:** Always verify `npm ci` locally in `web/` after updating any npm package.
