---
name: create
description: Create new application command. Triggers App Builder skill and starts interactive dialogue with user.
version: 1.0.0
requires_agents: orchestrator, project-planner
requires_skills: app-builder, design-spec, verify-changes
artifact_outputs: implementation-plan, changed-files, verification-report
---

# /create - Create Application

$ARGUMENTS

---

## Task

This command starts a new application creation process.

### Steps:

1. **Request Analysis**
   - Understand what the user wants
   - If information is missing, use the `brainstorming` skill to ask clarifying questions

2. **Project Planning**
   - Use `project-planner` agent for task breakdown
   - Determine tech stack
   - Plan file structure
   - Create the `{task-slug}.md` plan file in the project root, then proceed to building

3. **Design Source-of-Truth (UI projects only)**
   - If the app has a UI, create `DESIGN.md` at the project root BEFORE building UI — follow the `design-spec` skill (read `collection.md` for real-world references first).
   - Skip only for headless/CLI/API-only projects.

4. **Application Building (After Approval)**
   - Orchestrate with `app-builder` skill
   - Coordinate expert agents:
     - `database-architect` → Schema
     - `backend-specialist` → API
     - `frontend-specialist` → UI (builds against `DESIGN.md` tokens)

5. **Preview**
   - Start with `auto_preview.py` when complete
   - Present URL to user

---

## Usage Examples

```
/create blog site
/create e-commerce app with product listing and cart
/create todo app
/create Instagram clone
/create crm system with customer management
```

---

## Before Starting

If request is unclear, ask these questions:
- What type of application?
- What are the basic features?
- Who will use it?

Use defaults, add details later.

---

## 🔗 Next Step

Once scaffolding, building, and dev preview are complete:
→ Run `/verify` to execute tests and prove application behavior before deployment.
