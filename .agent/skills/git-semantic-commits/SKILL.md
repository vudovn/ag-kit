---
name: git-semantic-commits
description: Expertise in generating semantic, context-aware, and highly organized git commits. Follows Conventional Commits 1.0.0.
---

# Git Semantic Commits Skill

Directives for analyzing changes and generating professional commit messages.

## 🔴 CORE PRINCIPLES

1. **Semantic Typing**: Use standard prefixes (`feat:`, `fix:`, `refactor:`, `style:`, `docs:`, `chore:`, `test:`, `perf:`, `ci:`).
2. **Context-Aware**: Analyze the *intent* beyond just file changes.
3. **Imperative Mood**: Use "add", "fix", "change", not "added", "fixed", "changed".
4. **Conciseness First**: Prefer a single-line `<type>(<scope>): <summary>` for simple changes.
5. **Impact Summary**: Group related changes into logical units only if a single line is insufficient.
6. **Body Only if Necessary**: Only include a body if the changes are complex and need more detail than a single line.
7. **Breaking Changes**: Use `!` (e.g., `feat!:`) and describe the breaking change in the footer.

## 🛠️ THE SEMANTIC MAP

| Type | When to Use |
|------|-------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `style` | Formatting, missing semi-colons, etc. (no logic change) |
| `docs` | Documentation changes only |
| `test` | Adding missing tests or correcting existing tests |
| `perf` | Code change that improves performance |
| `chore` | Maintenance tasks, library updates, config changes |
| `ci` | Changes to CI/CD configuration files and scripts |

## 📋 WORKFLOW (FOR AGENT)

1. **Analyze Diff**: Run `git diff --cached` to see staged changes.
2. **Summarize Intent**: Determine the primary goal (e.g., "Standardizing buttons in dashboard").
3. **Draft Message**:
   - **Subject**: `<type>(<scope>): <short description>` (max 50-72 chars)
   - **Body**: (Optional) Bulleted list of specific changes if complex.
4. **Execute**: Propose or run `git commit -m "[message]"`.

## 🛑 BANS

- ❌ NO vague subjects like "update files" or "fix things".
- ❌ NO long subjects (keep under 72 characters).
- ❌ NO redundant descriptions in the body if the subject is clear enough.
- ❌ NO passive voice.
