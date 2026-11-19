---
name: plan
description: Create project plan using project-planner agent. No code writing - only plan file generation.
version: 1.0.0
requires_agents: project-planner
requires_skills: plan-writing, architecture
artifact_outputs: implementation-plan
---

# /plan - Project Planning Mode

$ARGUMENTS

---

## 🔴 CRITICAL RULES

1. **NO CODE WRITING** - This command creates plan file only
2. **Use project-planner agent** - NOT AG Kit Agent's native Plan mode
3. **Socratic Gate** - Ask clarifying questions before planning
4. **Dynamic Naming** - Plan file named based on task

---

## Task

Use the `project-planner` agent with this context:

```
CONTEXT:
- User Request: $ARGUMENTS
- Mode: PLANNING ONLY (no code)
- Output: {task-slug}.md in project root (dynamic naming)

NAMING RULES:
1. Extract 2-3 key words from request
2. Lowercase, hyphen-separated
3. Max 30 characters
4. Example: "e-commerce cart" → ecommerce-cart.md

RULES:
1. Follow project-planner.md Phase -1 (Context Check)
2. Follow project-planner.md Phase 0 (Socratic Gate)
3. Create {slug}.md with task breakdown
4. DO NOT write any code files
5. REPORT the exact file name created
```

---

## Expected Output

| Deliverable | Location |
|-------------|----------|
| Project Plan | `{task-slug}.md` in project root |
| Task Breakdown | Inside plan file |
| Agent Assignments | Inside plan file |
| Verification Checklist | Phase X in plan file |

---

## After Planning

Tell user:
```
[OK] Plan created: {slug}.md in project root

Next steps:
- Review the plan
- Run `/create` to start implementation
- Or modify plan manually
```

---

## Naming Examples

| Request | Plan File |
|---------|-----------|
| `/plan e-commerce site with cart` | `ecommerce-cart.md` |
| `/plan mobile app for fitness` | `fitness-app.md` |
| `/plan add dark mode feature` | `dark-mode.md` |
| `/plan fix authentication bug` | `auth-fix.md` |
| `/plan SaaS dashboard` | `saas-dashboard.md` |

---

## Usage

```
/plan e-commerce site with cart
/plan mobile app for fitness tracking
/plan SaaS dashboard with analytics
```

---

## 🔗 Next Step

After the plan is reviewed and approved:
→ Run `/create` (or `/orchestrate` for multi-agent execution) to implement the approved plan.
