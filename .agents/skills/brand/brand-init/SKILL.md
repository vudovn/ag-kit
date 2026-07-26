---
name: brand-init
description: Initialize a structured, versioned brand package (and optionally register it in a brand portfolio). Use when the user says "start a new brand", "create a brand", "set up a brand project", "new brand package", "init brand", "brand from scratch", or before any other brand work when no brand package exists yet. Creates brand.yaml + folder structure so every other brand skill reads and writes one coherent, queryable brand instead of regenerating from chat.
metadata:
  version: 1.0.0
---

# Brand Init

You set up the **persistence layer** for a brand: a structured package on disk that every other
brand skill reads first and writes into. A brand becomes a queryable artifact (`brand.yaml`), not
ephemeral chat output. Full spec: [`../../references/brand-package-spec.md`](../../references/brand-package-spec.md).

## When to run

- Starting any new brand and no package exists yet (no `brand.yaml` in `./`, `./brand/`, or `brands/<slug>/`).
- Migrating a legacy `.agents/brand-context.md` into a proper package.

If a package already exists, do NOT re-init — load it and continue with the relevant skill.

## Steps

### 1. Establish the essentials

Ask only for what you need to scaffold (the deep capture happens in `brand-context`):
- **Brand name** (required)
- **One-liner** — one sentence on what it is (the recall headline). If unknown yet, leave blank.
- **Where it lives** — pick the mode:
  - `./brand/` — in-situ, you're branding the current project (default)
  - `brands/<slug>/` — portfolio mode, you manage several brands
  - `<product>/brand/` — the brand belongs to a product repo
- **Portfolio?** — if managing multiple brands, register this one in `brands/registry.yaml`.

### 2. Scaffold the package

Run the bundled script (dependency-free). It lives at `scripts/brand.sh` relative to
this skill's directory:

```bash
# In Claude Code, ${CLAUDE_SKILL_DIR} expands to this skill's directory. In other
# agents, resolve scripts/brand.sh relative to where this SKILL.md was loaded.
bash ${CLAUDE_SKILL_DIR}/scripts/brand.sh init \
  --name "Acme" --one-liner "…" --out brand --date "$(date +%F)" \
  --register brands/registry.yaml      # omit --register for a single in-situ brand
```

This creates `<out>/brand.yaml` + `<out>/assets/` and (if `--register`) upserts the registry.
**Pass `--date` explicitly** when you want a reproducible run.

### 3. Hand off

Tell the user the package is created and what's next: run **`brand-context`** to capture the brand
DNA into `context.md`, then `naming` / `brand-strategy` / etc. — each writes into this package and
flips its flag in `brand.yaml`.

## Querying the portfolio

```bash
# ${CLAUDE_SKILL_DIR} = this skill's directory in Claude Code; elsewhere use scripts/brand.sh
# relative to where this SKILL.md was loaded.
bash ${CLAUDE_SKILL_DIR}/scripts/brand.sh list --registry brands/registry.yaml
# slug · name · one-liner · path · [status]
```

Use this to answer "what brands do we have / where do they live / what's the one-liner" without
opening each package.

## Rules

- **The registry is a SSOT file, never agent memory.** Brand locations + one-liners are data → they
  belong in `registry.yaml` (git-tracked, shareable), not an LLM's per-machine memory.
- **Don't pre-create empty section files.** Only `brand.yaml` + `assets/` at init; each skill creates
  its own `*.md` when it runs.
- **Never overwrite an existing package.** The script refuses; respect that.
