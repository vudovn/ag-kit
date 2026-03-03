# Ralph Agent Instructions — LUNA OS

You are an autonomous coding agent working on the LUNA OS project.

## Stack MCT

- **Backend:** FastAPI (Python 3.11) + Supabase (PostgreSQL) + OpenRouter
- **Frontend:** Next.js 14 + TypeScript + SWR + Framer Motion
- **WhatsApp:** Evolution API
- **Design System:** `frontend/design-system/MASTER.md` (Soft UI Evolution)
- **Philosophy:** Truth in Data — dados reais ou estado vazio, nunca simulação

## Your Task

1. Read the PRD at `prd.json` (in `scripts/ralph/`)
2. Read the progress log at `progress.txt` (check Codebase Patterns section
   first)
3. Check you're on the correct branch from PRD `branchName`. If not, check it
   out or create from main
4. Pick the **highest priority** user story where `passes: false`
5. Implement that single user story
6. Run quality checks:
   - Backend: `cd backend && python -m pytest tests/ -v`
   - Frontend: `cd frontend && npm run build`
   - Lint:
     `cd backend && python -c "import ast; [ast.parse(open(f).read()) for f in __import__('glob').glob('app/**/*.py', recursive=True)]"`
7. If checks pass, commit ALL changes with message:
   `feat: [Story ID] - [Story Title]`
8. Update the PRD to set `passes: true` for the completed story
9. Append your progress to `progress.txt`

## MCT Rules (P0 — Unbreakable)

- **Zero dados mock/fake/placeholder em produção**
- **Never use n8n** (decisão arquitetural permanente)
- **Estado vazio** → mostrar "Sem dados ainda" ou equivalente honesto
- **Design System:** Always read `frontend/design-system/MASTER.md` before UI
  work
- **Anti-patterns:** No bright neon colors, no harsh animations, no AI
  purple/pink gradients

## Progress Report Format

APPEND to progress.txt (never replace, always append):

```
## [Date/Time] - [Story ID]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered
  - Gotchas encountered
  - Useful context
---
```

## Stop Condition

After completing a user story, check if ALL stories have `passes: true`.

If ALL stories are complete and passing, reply with:
<promise>COMPLETE</promise>

If there are still stories with `passes: false`, end your response normally
(another iteration will pick up the next story).

## Important

- Work on ONE story per iteration
- Commit frequently
- Keep CI green
- Read the Codebase Patterns section in progress.txt before starting
- Always check `design-system/MASTER.md` before any UI change
