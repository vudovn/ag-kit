# Smart Auto-Categorization Guide

## Overview

The skill collection now uses intelligent auto-categorization to eliminate "uncategorized" and organize skills into meaningful categories based on their content.

## Current Status

✅ **946 total skills**
- 820 skills in meaningful categories (87%)
- 126 skills still uncategorized (13%)
- 11 primary categories
- Categories sorted by skill count (most first)

## Category Distribution

| Category | Count | Examples |
|----------|-------|----------|
| Backend | 164 | Node.js, Django, Express, FastAPI |
| Web Development | 107 | React, Vue, Tailwind, CSS |
| Automation | 103 | Workflow, Scripting, RPA |
| DevOps | 83 | Docker, Kubernetes, CI/CD, Git |
| AI/ML | 79 | TensorFlow, PyTorch, NLP, LLM |
| Content | 47 | Documentation, SEO, Writing |
| Database | 44 | SQL, MongoDB, PostgreSQL |
| Testing | 38 | Jest, Cypress, Unit Testing |
| Security | 36 | Encryption, Authentication |
| Cloud | 33 | AWS, Azure, GCP |
| Mobile | 21 | React Native, Flutter, iOS |
| Game Dev | 15 | Unity, WebGL, 3D |
| Data Science | 14 | Pandas, NumPy, Analytics |

## How It Works

### 1. **Keyword-Based Analysis**
The system analyzes skill names and descriptions for keywords:
- **Backend**: nodejs, express, fastapi, django, server, api, database
- **Web Dev**: react, vue, angular, frontend, css, html, tailwind
- **AI/ML**: ai, machine learning, tensorflow, nlp, gpt
- **DevOps**: docker, kubernetes, ci/cd, deploy
- And more...

### 2. **Priority System**
Frontmatter category > Detected Keywords > Fallback (uncategorized)

If a skill already has a category in frontmatter, that's preserved.

### 3. **Scope-Based Matching**
- Exact phrase matches weighted 2x higher than partial matches
- Uses word boundaries to avoid false positives

## Using the Auto-Categorization

### Run on Uncategorized Skills
```bash
python scripts/auto_categorize_skills.py
```

### Preview Changes First (Dry Run)
```bash
python scripts/auto_categorize_skills.py --dry-run
```

### Output
```
======================================================================
AUTO-CATEGORIZATION REPORT
======================================================================

Summary:
   ✅ Categorized: 776
   ⏭️  Already categorized: 46
   ❌ Failed to categorize: 124
   📈 Total processed: 946

Sample changes:
   • 3d-web-experience
     uncategorized → web-development
   • ab-test-setup
     uncategorized → testing
   • agent-framework-azure-ai-py
     uncategorized → backend
```

## Web App Improvements

### Category Filter
**Before:**
- Unordered list including "uncategorized"
- No indication of category size

**After:**
- Categories sorted by skill count (most first, "uncategorized" last)
- Shows count: "Backend (164)" "Web Development (107)"
- Much easier to browse

### Example Dropdowns

**Sorted Order:**
1. All Categories
2. Backend (164)
3. Web Development (107)
4. Automation (103)
5. DevOps (83)
6. AI/ML (79)
7. ... more categories ...
8. Uncategorized (126) ← at the end

## For Skill Creators

### When Adding a New Skill

Include category in frontmatter:
```yaml
---
name: my-skill
description: "..."
category: web-development
date_added: "2025-02-26"
---
```

### If You're Not Sure

The system will automatically categorize on next index regeneration:
```bash
python scripts/generate_index.py
```

## Keyword Reference

Available auto-categorization keywords by category:

**Backend**: nodejs, node.js, express, fastapi, django, flask, spring, java, python, golang, rust, server, api, rest, graphql, database, sql, mongodb

**Web Development**: react, vue, angular, html, css, javascript, typescript, frontend, tailwind, bootstrap, webpack, vite, pwa, responsive, seo

**Database**: database, sql, postgres, mysql, mongodb, firestore, redis, orm, schema

**AI/ML**: ai, machine learning, ml, tensorflow, pytorch, nlp, llm, gpt, transformer, embedding, training

**DevOps**: docker, kubernetes, ci/cd, git, jenkins, terraform, ansible, deploy, container, monitoring

**Cloud**: aws, azure, gcp, serverless, lambda, storage, cdn

**Security**: encryption, cryptography, jwt, oauth, authentication, authorization, vulnerability

**Testing**: test, jest, mocha, pytest, cypress, selenium, unit test, e2e

**Mobile**: mobile, react native, flutter, ios, android, swift, kotlin

**Automation**: automation, workflow, scripting, robot, trigger, integration

**Game Development**: game, unity, unreal, godot, threejs, 2d, 3d, physics

**Data Science**: data, analytics, pandas, numpy, statistics, visualization

## Customization

### Add Custom Keywords

Edit [scripts/auto_categorize_skills.py](scripts/auto_categorize_skills.py):

```python
CATEGORY_KEYWORDS = {
    'your-category': [
        'keyword1', 'keyword2', 'exact phrase', 'another-keyword'
    ],
    # ... other categories
}
```

Then re-run:
```bash
python scripts/auto_categorize_skills.py
python scripts/generate_index.py
```

## Troubleshooting

### "Failed to categorize" Skills

Some skills may be too generic or unique. You can:

1. **Manually set category** in the skill's frontmatter:
```yaml
category: your-chosen-category
```

2. **Add keywords** to CATEGORY_KEYWORDS config

3. **Move to folder** if it fits a broader category:
```
skills/backend/my-new-skill/SKILL.md
```

### Regenerating Index

After making changes to SKILL.md files:
```bash
python scripts/generate_index.py
```

This will:
- Parse frontmatter categories
- Fallback to folder structure
- Generate new skills_index.json
- Copy to web-app/public/skills.json

## Next Steps

1. **Test in web app**: Try the improved category filter
2. **Add missing keywords**: If certain skills are still uncategorized
3. **Organize remaining 126**: Either auto-assign or manually review
4. **Monitor growth**: Use reports to track new vs categorized skills

---

**Result**: Much cleaner category filter with smart, meaningful organization! 🎉
