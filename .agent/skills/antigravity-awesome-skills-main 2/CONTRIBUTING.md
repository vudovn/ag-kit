# 🤝 Contributing Guide - V4 Enterprise Edition

**Thank you for wanting to make this repo better!** This guide shows you exactly how to contribute, even if you're new to open source.
With V4, we raised the bar for quality. Please read the **new Quality Standards** below carefully.

---

## 🧐 The "Quality Bar" (V4 Standard)

**Critical for new skills:** Every skill submitted must pass our **5-Point Quality Check** (see `docs/QUALITY_BAR.md` for details):

1.  **Metadata**: Correct Frontmatter (`name`, `description`).
    - The `name` MUST exactly match the folder name.
    - The `description` MUST be concise (under 200 characters) and focus on WHEN to trigger the skill.
2.  **Safety**: No harmful commands without "Risk" labels.
3.  **Clarity**: Clear "When to use" section.
4.  **Examples**: At least one copy-paste usage example.
5.  **Actions**: Must define concrete steps, not just "thoughts".

---

## Ways to Contribute

You don't need to be an expert! Here are ways anyone can help:

### 1. Improve Documentation (Easiest!)

- Fix typos or grammar
- Make explanations clearer
- Add examples to existing skills
- Translate documentation to other languages

### 2. Report Issues

- Found something confusing? Tell us!
- Skill not working? Let us know!
- Have suggestions? We want to hear them!

### 3. Create New Skills

- Share your expertise as a skill
- Fill gaps in the current collection
- Improve existing skills

### 4. Test and Validate

- Try skills and report what works/doesn't work
- Test on different AI tools
- Suggest improvements

---

## Local development setup

To run validation, index generation, and README updates locally:

1. **Node.js** (for catalog and installer): `npm ci`
2. **Python 3** (for validate, index, readme scripts): install dependencies with
   ```bash
   pip install -r requirements.txt
   ```
   Then you can run `npm run chain` (validate → index → readme) and `npm run catalog`.

**Validation:** The canonical validator is **Python** (`scripts/validate_skills.py`). Use `npm run validate` (or `npm run validate:strict` for CI-style checks). The JavaScript validator (`scripts/validate-skills.js`) is legacy/optional and uses a different schema; CI and PR checks rely on the Python validator only.

**npm audit:** CI runs `npm audit --audit-level=high`. To fix issues locally: run `npm audit`, then `npm update` or `npm audit fix` as appropriate; for breaking changes, update dependencies manually and run tests.

---

## How to Create a New Skill

### Step-by-Step Guide

#### Step 1: Choose Your Skill Topic

Ask yourself: "What do I wish my AI assistant knew better?".
Example: "I'm good at Docker, let me create a Docker skill".

#### Step 2: Create the Folder Structure

Skills live in the `skills/` directory. Use `kebab-case` for folder names.

```bash
# Navigate to skills
cd skills/

# Create your skill folder
mkdir my-awesome-skill
cd my-awesome-skill

# Create the SKILL.md file
touch SKILL.md
```

#### Step 3: Write Your SKILL.md

Every skill needs this basic structure. **Copy this template:**

```markdown
---
name: my-awesome-skill
description: "Brief one-line description of what this skill does"
---

# Skill Title

## Overview

Explain what this skill does and when to use it.

## When to Use This Skill

- Use when [scenario 1]
- Use when [scenario 2]

## How It Works

Detailed step-by-step instructions for the AI...

## Examples

### Example 1

\`\`\`
code example here
\`\`\`

## Best Practices

- ✅ Do this
- ❌ Don't do this
```

#### Step 4: Validate (CRITICAL V4 STEP)

Use the canonical validator `scripts/validate_skills.py` via `npm run validate`. **We will not merge PRs that fail this check.**

```bash
npm run validate        # soft mode (warnings only)
npm run validate:strict # strict mode (what CI runs)
```

This checks:

- ✅ `SKILL.md` exists
- ✅ Frontmatter is correct
- ✅ Name matches folder name
- ✅ Quality Bar checks passed

#### Step 5: Submit Your Skill

```bash
git add skills/my-awesome-skill/
git commit -m "feat: add my-awesome-skill"
git push origin my-branch
```

---

## Skill Template (Copy & Paste)

Save time! Copy this template:

```markdown
---
name: your-skill-name
description: "One sentence describing what this skill does and when to use it"
---

# Your Skill Name

## Overview

[2-3 sentences explaining what this skill does]

## When to Use This Skill

- Use when you need to [scenario 1]
- Use when you want to [scenario 2]

## Step-by-Step Guide

### 1. [First Step Name]

[Detailed instructions]

## Examples

### Example 1: [Use Case Name]

\`\`\`language
// Example code here
\`\`\`

## Best Practices

- ✅ **Do:** [Good practice]
- ❌ **Don't:** [What to avoid]

## Troubleshooting

**Problem:** [Common Issue]
**Solution:** [How to fix it]
```

---

## Commit Message Guidelines

Use these prefixes:

- `feat:` - New skill or major feature
- `docs:` - Documentation improvements
- `fix:` - Bug fixes
- `refactor:` - Code improvements without changing functionality
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

**Examples:**

```
feat: add kubernetes-deployment skill
docs: improve getting started guide
fix: correct typo in stripe-integration skill
```

---

## Learning Resources

### New to Git/GitHub?

- [GitHub's Hello World Guide](https://guides.github.com/activities/hello-world/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

### New to Markdown?

- [Markdown Guide](https://www.markdownguide.org/basic-syntax/)

---

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- **No harmful content**: See `docs/SECURITY_GUARDRAILS.md`.

---

**Thank you for making this project better for everyone!**
Every contribution, no matter how small, makes a difference. Whether you fix a typo, improve a sentence, or create a whole new skill - you're helping thousands of developers!
