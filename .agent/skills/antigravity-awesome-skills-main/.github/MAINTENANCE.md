# 🛠️ Repository Maintenance Guide (V5)

> **"If it's not documented, it's broken."**

This guide details the exact procedures for maintaining `antigravity-awesome-skills`.
It covers the **Quality Bar**, **Documentation Consistency**, and **Release Workflows**.

**Maintainer shortcuts:** [Merge a PR](#b-when-you-merge-a-pr-step-by-step) · [Post-merge & contributors](#c-post-merge-routine-must-do-before-a-release) · [Close issues](#when-to-close-an-issue) · [Create a release](#4-release-workflow)

---

## 0. 🤖 Agent Protocol (THE BIBLE)

**AGENTS MUST READ AND FOLLOW THIS SECTION BEFORE MARKING ANY TASK AS COMPLETE.**

There are 3 things that usually fail/get forgotten. **DO NOT FORGET THEM:**

### 1. 📤 ALWAYS PUSH (Non-Negotiable)

Committing is NOT enough. You must PUSH to the remote.

- **BAD**: `git commit -m "feat: new skill"` (User sees nothing)
- **GOOD**: `git commit -m "..." && git push origin main`

### 2. 🔄 SYNC GENERATED FILES (Avoid CI Drift)

If you touch **any of these**:

- `skills/` (add/remove/modify skills)
- the **Full Skill Registry** section of `README.md`
- **counts/claims** about the number of skills (`560+ Agentic Skills...`, `(560/560)`, etc.)

…then you **MUST** run the Validation Chain **BEFORE** committing.

- Running `npm run chain` is **NOT optional**.
- Running `npm run catalog` is **NOT optional**.

If CI fails with:

> `❌ Detected uncommitted changes produced by registry/readme/catalog scripts.`

it means you **did not run or commit** the Validation Chain correctly.

### 3. 📝 EVIDENCE OF WORK

- You must create/update `walkthrough.md` or `CHANGELOG.md` to document what changed.
- If you made something new, **link it** in the artifacts.

### 4. 🚫 NO BRANCHES

- **ALWAYS use the `main` branch.**
- NEVER create feature branches (e.g., `feat/new-skill`).
- We commit directly to `main` to keep history linear and simple.

---

## 1. 🚦 Daily Maintenance Routine

### A. Validation Chain

Before ANY commit that adds/modifies skills, run the chain:

1.  **Validate, index, and update readme**:

    ```bash
    npm run chain
    ```

    _Must return 0 errors for new skills._

2.  **Build catalog**:

    ```bash
    npm run catalog
    ```

3.  **COMMIT GENERATED FILES**:
    ```bash
    git add README.md skills_index.json data/catalog.json data/bundles.json data/aliases.json CATALOG.md
    git commit -m "chore: sync generated files"
    ```
    > 🔴 **CRITICAL**: If you skip this, CI will fail with "Detected uncommitted changes".
    > See [docs/CI_DRIFT_FIX.md](../docs/CI_DRIFT_FIX.md) for details.

### B. When You Merge a PR (Step-by-Step)

**Before merging:**

1.  **CI is green** — All Validation Chain and catalog steps passed (see [workflows/ci.yml](workflows/ci.yml)).
2.  **No drift** — PR does not introduce uncommitted generated-file changes; if the "Check for Uncommitted Drift" step failed, ask the author to run `npm run chain` and `npm run catalog` and commit the result.
3.  **Quality Bar** — PR description confirms the [Quality Bar Checklist](.github/PULL_REQUEST_TEMPLATE.md) (metadata, risk label, credits if applicable).
4.  **Issue link** — If the PR fixes an issue, the PR description should contain `Closes #N` or `Fixes #N` so GitHub auto-closes the issue on merge.

**Right after merging:**

1.  **If the PR had `Closes #N`** — The issue is closed automatically; no extra action.
2.  **If an issue was fixed but not linked** — Close it manually and add a comment, e.g.:
    ```text
    Fixed in #<PR_NUMBER>. Shipped in release vX.Y.Z.
    ```
3.  **Single PR or small batch** — Optionally run the full Post-Merge Routine below. For a single, trivial PR you can defer it to the next release prep.

### C. Post-Merge Routine (Must Do Before a Release)

After you have merged several PRs or before cutting a release:

1.  **Sync Contributors List**:
    - Run: `git shortlog -sn --all`
    - Update `## Repo Contributors` in README.md.

2.  **Verify Table of Contents**:
    - Ensure all new headers have clean anchors.
    - **NO EMOJIS** in H2 headers.

3.  **Prepare for release** — Draft the release and tag when ready (see [§4 Release Workflow](#4-release-workflow) below).

---

## 2. 📝 Documentation "Pixel Perfect" Rules

We discovered several consistency issues during V4 development. Follow these rules STRICTLY.

### A. Table of Contents (TOC) Anchors

GitHub's anchor generation breaks if headers have emojis.

- **BAD**: `## 🚀 New Here?` -> Anchor: `#--new-here` (Broken)
- **GOOD**: `## New Here?` -> Anchor: `#new-here` (Clean)

**Rule**: **NEVER put emojis in H2 (`##`) headers.** Put them in the text below if needed.

### B. The "Trinity" of Docs

If you update installation instructions or tool compatibility, you MUST update all 3 files:

1.  `README.md` (Source of Truth)
2.  `docs/GETTING_STARTED.md` (Beginner Guide)
3.  `docs/FAQ.md` (Troubleshooting)

_Common pitfall: Updating the clone URL in README but leaving an old one in FAQ._

### C. Statistics Consistency (CRITICAL)

If you add/remove skills, you **MUST** ensure the total count is identical in ALL locations.
**Do not allow drift** (e.g., 560 in title, 558 in header).

Locations to check:

1.  **Title of `README.md`**: "560+ Agentic Skills..."
2.  **`## Full Skill Registry (560/560)` header**.
3.  **`docs/GETTING_STARTED.md` intro**.

### D. Credits Policy (Who goes where?)

- **Credits & Sources**: Use this for **External Repos**.
  - _Rule_: "I extracted skills from this link you sent me." -> Add to `## Credits & Sources`.
- **Repo Contributors**: Use this for **Pull Requests**.
  - _Rule_: "This user sent a PR." -> Add to `## Repo Contributors`.

### E. Badges & Links

- **Antigravity Badge**: Must point to `https://github.com/sickn33/antigravity-awesome-skills`, NOT `anthropics/antigravity`.
- **License**: Ensure the link points to `LICENSE` file.

### F. Workflows Consistency (NEW in V5)

If you touch any Workflows-related artifact, keep all workflow surfaces in sync:

1. `docs/WORKFLOWS.md` (human-readable playbooks)
2. `data/workflows.json` (machine-readable schema)
3. `skills/antigravity-workflows/SKILL.md` (orchestration entrypoint)

Rules:

- Every workflow id referenced in docs must exist in `data/workflows.json`.
- If you add/remove a workflow step category, update prompt examples accordingly.
- If a workflow references optional skills not yet merged (example: `go-playwright`), mark them explicitly as **optional** in docs.
- If workflow onboarding text is changed, update the docs trinity:
  - `README.md`
  - `docs/GETTING_STARTED.md`
  - `docs/FAQ.md`

---

## 3. 🛡️ Governance & Quality Bar

### A. The 5-Point Quality Check

Reject any PR that fails this:

1.  **Metadata**: Has `name`, `description`?
2.  **Safety**: `risk: offensive` used for red-team tools?
3.  **Clarity**: Does it say _when_ to use it?
4.  **Examples**: Copy-pasteable code blocks?
5.  **Actions**: "Run this command" vs "Think about this".

### B. Risk Labels (V4)

- ⚪ **Safe**: Default.
- 🔴 **Risk**: Destructive/Security tools. MUST have `[Authorized Use Only]` warning.
- 🟣 **Official**: Vendor mirrors only.

---

## 4. 🚀 Release Workflow

When cutting a new version (e.g., v4.1.0):

**Release checklist (order matters):**  
Validate → Changelog → Bump `package.json` (and README if needed) → Commit & push → Create GitHub Release with tag **matching** `package.json` (e.g. `v4.1.0` ↔ `"version": "4.1.0"`) → npm publish (manual or via CI) → Close any remaining linked issues.

---

1.  **Run Full Validation**: `python3 scripts/validate_skills.py --strict`
2.  **Update Changelog**: Add the new release section to `CHANGELOG.md`.
3.  **Bump Version**:
    - Update `package.json` → `"version": "X.Y.Z"` (source of truth for npm).
    - Update version header in `README.md` if it displays the number.
    - One-liner: `npm version patch` (or `minor`/`major`) — bumps `package.json` and creates a git tag; then amend if you need to tag after release.
4.  **Create GitHub Release** (REQUIRED):

    > ⚠️ **CRITICAL**: Pushing a tag (`git push --tags`) is NOT enough. You must create a **GitHub Release Object** for it to appear in the sidebar and trigger the NPM publish workflow.

    Use the GitHub CLI:

    ```bash
    # Prepare release notes (copy the new section from CHANGELOG.md into release_notes.md, or use CHANGELOG excerpt)
    # Then create the tag AND the release page (tag must match package.json version, e.g. v4.1.0)
    gh release create v4.0.0 --title "v4.0.0 - [Theme Name]" --notes-file release_notes.md
    ```

    **Important:** The release tag (e.g. `v4.1.0`) must match `package.json`'s `"version": "4.1.0"`. The [Publish to npm](workflows/publish-npm.yml) workflow runs on **Release published** and will run `npm publish`; npm rejects republishing the same version.

    _Or create the release manually via GitHub UI > Releases > Draft a new release, then publish._

5.  **Publish to npm** (so `npx antigravity-awesome-skills` works):
    - **Option A (manual):** From repo root, with npm logged in and 2FA/token set up:
      ```bash
      npm publish
      ```
      You cannot republish the same version; always bump `package.json` before publishing.
    - **Option B (CI):** On GitHub, create a **Release** (tag e.g. `v4.6.1`). The workflow [Publish to npm](.github/workflows/publish-npm.yml) runs on **Release published** and runs `npm publish` if the repo secret `NPM_TOKEN` is set (npm → Access Tokens → Granular token with Publish, then add as repo secret `NPM_TOKEN`).

6.  **Close linked issue(s)**:
    - Issues that had `Closes #N` / `Fixes #N` in a merged PR are already closed.
    - For any issue that was fixed by the release but not auto-closed, close it manually and add a comment, e.g.:
      ```bash
      gh issue close <ID> --comment "Shipped in vX.Y.Z. See CHANGELOG.md and release notes."
      ```

### When to Close an Issue

| Situation | Action |
|-----------|--------|
| PR merges and PR body contains `Closes #N` or `Fixes #N` | GitHub closes the issue automatically. |
| PR merges but did not reference the issue | After merge, close manually: `gh issue close N --comment "Fixed in #<PR>. Shipped in vX.Y.Z."` |
| Fix/feature shipped in a release, no PR referenced | Close with: `gh issue close N --comment "Shipped in vX.Y.Z. See CHANGELOG."` |

### 📋 Changelog Entry Template

Each new release section in `CHANGELOG.md` should follow [Keep a Changelog](https://keepachangelog.com/) and this structure:

```markdown
## [X.Y.Z] - YYYY-MM-DD - "[Theme Name]"

> **[One-line catchy summary of the release]**

[Brief 2-3 sentence intro about the release's impact]

## 🚀 New Skills

### [Emoji] [Skill Name](skills/skill-name/)

**[Bold high-level benefit]**
[Description of what it does]

- **Key Feature 1**: [Detail]
- **Key Feature 2**: [Detail]

> **Try it:** `(User Prompt) ...`

---

## 📦 Improvements

- **Registry Update**: Now tracking [N] skills.
- **[Component]**: [Change detail]

## 👥 Credits

A huge shoutout to our community contributors:

- **@username** for `skill-name`
- **@username** for `fix-name`

---

_Upgrade now: `git pull origin main` to fetch the latest skills._
```

---

## 5. 🚨 Emergency Fixes

If a skill is found to be harmful or broken:

1.  **Move to broken folder** (don't detect): `mv skills/bad-skill skills/.broken/`
2.  **Or Add Warning**: Add `> [!WARNING]` to the top of `SKILL.md`.
3.  **Push Immediately**.

---

## 6. 📁 Data directory note

`data/package.json` exists for historical reasons; the build and catalog scripts run from the repo root and use root `node_modules`. You can ignore or remove `data/package.json` and `data/node_modules` if present.
