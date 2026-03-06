# CI Drift Fix Guide

**Problem**: The failing job is caused by uncommitted changes detected in `README.md`, `skills_index.json`, or catalog files after the update scripts run.

**Error**:

```
❌ Detected uncommitted changes produced by registry/readme/catalog scripts.
```

**Cause**:
Scripts like `scripts/generate_index.py`, `scripts/update_readme.py`, and `scripts/build-catalog.js` modify `README.md`, `skills_index.json`, `data/catalog.json`, `data/bundles.json`, `data/aliases.json`, and `CATALOG.md`. The workflow expects these files to have no changes after the scripts run. Any differences mean the committed repo is out-of-sync with what the generation scripts produce.

**How to Fix (DO THIS EVERY TIME):**

1. Run the **FULL Validation Chain** locally:

   ```bash
   npm run chain
   npm run catalog
   ```

2. Check for changes:

   ```bash
   git status
   git diff
   ```

3. Commit and push any updates:
   ```bash
   git add README.md skills_index.json data/catalog.json data/bundles.json data/aliases.json CATALOG.md
   git commit -m "chore: sync generated registry files"
   git push
   ```

**Summary**:
Always commit and push all changes produced by the registry, readme, and catalog scripts. This keeps the CI workflow passing by ensuring the repository and generated files are synced.
