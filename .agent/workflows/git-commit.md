---
description: Automated semantic git commit workflow
---

# /git-commit - Automated Semantic Commits

This workflow automates the process of staging changes and committing them with a context-aware semantic message.

## 🔴 PREREQUISITES

1. The `git-semantic-commits` skill must be loaded.
2. The agent must have permission to run `git` commands.

---

## 📋 STEPS

1. **Check Status**
   Run `git status` to see what changes are available.

2. **Stage Changes**
   // turbo
   Run `git add -A` (or ask the user if they want to stage specific files).

3. **Analyze & Propose**
   - Run `git diff --cached` to analyze the staged changes.
   - Using the `git-semantic-commits` skill, formulate a **concise, single-line** semantic message by default.
   - Present the message to the user for approval (mentioning they can ask for more detail if needed).

4. **Execute Commit**
   // turbo
   Once approved, run `git commit -m "[message]"`.

5. **Final Status**
   Show the user the result: `[OK] Committed: [message]`.

---

## 🛠️ USAGE

```
/git-commit
```
