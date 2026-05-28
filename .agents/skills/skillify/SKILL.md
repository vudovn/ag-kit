---
name: skillify
description: Auto-create new skills from repetitive workflows. When you notice yourself doing the same multi-step process repeatedly, extract it into a reusable SKILL.md that any agent can use.
when_to_use: "When the user says 'make this a skill', 'create a skill for this', 'I keep doing this same thing', or when a repetitive multi-step pattern is observed. NOT for one-off tasks."
allowed-tools: Read, Write, Glob, Grep
effort: low
---

# Skillify — Auto-Create Skills from Workflows

> Turn repetitive patterns into reusable skills. If you've done it three times, it should be a skill.

## When to Skillify

✅ **Good candidates:**
- You've seen the user ask for the same type of work 3+ times
- A workflow involves 5+ consistent steps
- The pattern works across different projects
- Other agents could benefit from this knowledge

❌ **Bad candidates:**
- One-off tasks (just do them)
- Project-specific hacks (use memory instead)
- Already covered by existing skills (check first)

---

## Skill Creation Protocol

### Step 1: Identify the Pattern
```
What triggers this workflow? (user says X, file type Y, domain Z)
What steps are always the same?
What parts vary between uses?
What's the expected output?
```

### Step 2: Generate SKILL.md

Use this template:

```markdown
---
name: [kebab-case-name]
description: [One sentence describing what this skill does]
when_to_use: "[When the user asks X, works with Y files, or Z domain. NOT for A.]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash — only what's needed]
effort: [low | medium | high]
---

# [Skill Name] — [Short Subtitle]

> [One-line philosophy or principle]

## Overview
[2-3 sentences explaining what this skill enables]

## When to Use
✅ Good for: [list]
❌ Not for: [list]

## Protocol
### Step 1: [First Action]
[Instructions]

### Step 2: [Second Action]
[Instructions]

### Step N: [Verification]
[How to verify the skill worked correctly]

## Best Practices
[3-5 key rules]
```

### Step 3: Place the Skill
```
.agent/skills/[skill-name]/SKILL.md
```

### Step 4: Verify
- [ ] Frontmatter has all required fields (name, description, when_to_use)
- [ ] `when_to_use` clearly defines triggers AND exclusions
- [ ] Steps are actionable, not vague
- [ ] Skill doesn't duplicate an existing one

---

## Naming Conventions

| Pattern | Skill Name | Example |
|---|---|---|
| Action-based | `[verb]-[noun]` | `verify-changes`, `batch-operations` |
| Domain-based | `[domain]-[aspect]` | `database-design`, `api-patterns` |
| Tool-based | `[tool]-patterns` | `tailwind-patterns`, `prisma-expert` |

**Rules:**
- kebab-case only
- 2-3 words maximum
- Descriptive, not clever
- No abbreviations unless universally known

---

## Quality Checklist

Before finalizing a new skill:

| Check | Criteria |
|---|---|
| **Uniqueness** | No existing skill covers this (grep `.agent/skills/`) |
| **Reusability** | Useful across multiple projects, not just one |
| **Completeness** | Has overview, when to use, protocol, verification |
| **Frontmatter** | All required fields present and accurate |
| **Clarity** | A new agent could follow these instructions cold |
