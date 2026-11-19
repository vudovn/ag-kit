---
name: enhance
description: Add or update features in existing application. Used for iterative development.
version: 1.0.0
requires_agents: code-archaeologist
requires_skills: simplify-code, clean-code, verify-changes
artifact_outputs: change-plan, changed-files, verification-report
---

# /enhance - Update Application

$ARGUMENTS

---

## Task

This command adds features or makes updates to existing application.

### Steps:

1. **Understand Current State**
   - Load project state with `python .agents/scripts/session_manager.py info`
   - Understand existing features, tech stack

2. **Plan Changes**
   - Determine what will be added/changed
   - Detect affected files
   - Check dependencies

3. **Present Plan to User** (for major changes)
   ```
   "To add admin panel:
   - New files: admin routes, components, and access control
   - Updates: navigation, auth middleware
   - Scope: moderate (touches auth + routing)
   
   Should I start?"
   ```

4. **Apply**
   - Call relevant agents
   - Make changes
   - Test

5. **Update Preview**
   - Hot reload or restart

---

## Usage Examples

```
/enhance add dark mode
/enhance build admin panel
/enhance integrate payment system
/enhance add search feature
/enhance edit profile page
/enhance make responsive
```

---

## Caution

- Get approval for major changes
- Warn on conflicting requests (e.g., "use Firebase" when project uses PostgreSQL)
- Commit each change with git

---

## 🔗 Next Step

After changes are applied and previewed:
→ Run `/verify` to confirm enhancements pass verification without regression.
