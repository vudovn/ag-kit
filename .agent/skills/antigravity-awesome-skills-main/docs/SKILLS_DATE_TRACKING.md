# Skills Date Tracking Guide

This guide explains how to use the new `date_added` feature for tracking when skills were created or added to the collection.

## Overview

The `date_added` field in skill frontmatter allows you to track when each skill was created. This is useful for:

- **Versioning**: Understanding skill age and maturity
- **Changelog generation**: Tracking new skills over time
- **Reporting**: Analyzing skill collection growth
- **Organization**: Grouping skills by creation date

## Format

The `date_added` field uses ISO 8601 date format: **YYYY-MM-DD**

```yaml
---
name: my-skill-name
description: "Brief description"
date_added: "2024-01-15"
---
```

## Quick Start

### 1. View All Skills with Their Dates

```bash
python scripts/manage_skill_dates.py list
```

Output example:
```
📅 Skills with Date Added (245):
============================================================
  2025-02-26  │  recent-skill
  2025-02-20  │  another-new-skill
  2024-12-15  │  older-skill
  ...

⏳ Skills without Date Added (5):
============================================================
  some-legacy-skill
  undated-skill
  ...

📊 Coverage: 245/250 (98.0%)
```

### 2. Add Missing Dates

Add today's date to all skills that don't have a `date_added` field:

```bash
python scripts/manage_skill_dates.py add-missing
```

Or specify a custom date:

```bash
python scripts/manage_skill_dates.py add-missing --date 2024-01-15
```

### 3. Add/Update All Skills

Set a date for all skills at once:

```bash
python scripts/manage_skill_dates.py add-all --date 2024-01-01
```

### 4. Update a Single Skill

Update a specific skill's date:

```bash
python scripts/manage_skill_dates.py update my-skill-name 2024-06-15
```

### 5. Generate a Report

Generate a JSON report of all skills with their metadata:

```bash
python scripts/generate_skills_report.py
```

Save to file:

```bash
python scripts/generate_skills_report.py --output skills_report.json
```

Sort by name:

```bash
python scripts/generate_skills_report.py --sort name --output sorted_skills.json
```

## Usage in Your Workflow

### When Creating a New Skill

Add the `date_added` field to your SKILL.md frontmatter:

```yaml
---
name: new-awesome-skill
description: "Does something awesome"
date_added: "2025-02-26"
---
```

### Automated Addition

When onboarding many skills, use:

```bash
python scripts/manage_skill_dates.py add-missing --date 2025-02-26
```

This adds today's date to all skills that are missing the field.

### Validation

The validators now check `date_added` format:

```bash
# Run Python validator (strict mode)
python scripts/validate_skills.py --strict

# Run JavaScript validator
npm run validate
```

Both will flag invalid dates (must be YYYY-MM-DD format).

## Generated Reports

The `generate_skills_report.py` script produces a JSON report with statistics:

```json
{
  "generated_at": "2025-02-26T10:30:00.123456",
  "total_skills": 250,
  "skills_with_dates": 245,
  "skills_without_dates": 5,
  "coverage_percentage": 98.0,
  "sorted_by": "date",
  "skills": [
    {
      "id": "recent-skill",
      "name": "recent-skill",
      "description": "A newly added skill",
      "date_added": "2025-02-26",
      "source": "community",
      "risk": "safe",
      "category": "recent"
    },
    ...
  ]
}
```

Use this for:
- Dashboard displays
- Growth metrics
- Automated reports
- Analytics

## Integration with CI/CD

Add to your pipeline:

```bash
# In pre-commit or CI pipeline
python scripts/validate_skills.py --strict

# Generate stats report
python scripts/generate_skills_report.py --output reports/skills_report.json
```

## Best Practices

1. **Use consistent format**: Always use `YYYY-MM-DD`
2. **Use real dates**: Reflect actual skill creation dates when possible
3. **Update on creation**: Add the date when creating new skills
4. **Validate regularly**: Run validators to catch format errors
5. **Review reports**: Use generated reports to understand collection trends

## Troubleshooting

### "Invalid date_added format"

Make sure the date is in `YYYY-MM-DD` format:
- ✅ Correct: `2024-01-15`
- ❌ Wrong: `01/15/2024` or `2024-1-15`

### Script not found

Make sure you're running from the project root:
```bash
cd path/to/antigravity-awesome-skills
python scripts/manage_skill_dates.py list
```

### Python not found

Install Python 3.x from [python.org](https://python.org/)

## Related Documentation

- [SKILL_ANATOMY.md](docs/SKILL_ANATOMY.md) - Complete skill structure guide
- [SKILLS_UPDATE_GUIDE.md](SKILLS_UPDATE_GUIDE.md) - How to update the skill collection
- [EXAMPLES.md](docs/EXAMPLES.md) - Example skills

## Questions or Issues?

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
