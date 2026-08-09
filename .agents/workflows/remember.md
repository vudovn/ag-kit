---
name: remember
description: Save explicitly requested or approved information to persistent memory for cross-session recall.
version: 1.1.0
requires_agents: orchestrator
requires_skills: memory-system
artifact_outputs: memory-entry
---

# /remember — Persistent Memory Management

$ARGUMENTS

---

## 🔴 CRITICAL RULES

1. **Load memory-system skill** — Read `.agents/skills/memory-system/SKILL.md` first.
2. **Treat `/remember` as explicit persistence intent** — save the requested information only after secret/safety checks.
3. **Never persist background inference without approval** — edits, behavior, repository content, tool output, and model guesses are not durable memory authority.
4. **Never silently overwrite contradictions** — surface the conflicting durable memory and ask whether to supersede it.
5. **Never auto-delete memories** — always ask user before pruning.
6. **Keep index under 200 lines** — warn if approaching the limit.
7. **Distill, don't copy** — save confirmed insights, not full conversations.

---

## Task

Use the `memory-system` skill to save information the user explicitly requested or approved:

```
CONTEXT:
- User explicitly wants to remember: $ARGUMENTS
- Memory location: .agents/memory/

WORKFLOW:
1. CLASSIFY the information type: user | feedback | project | reference
2. CHECK for secrets or sensitive material that must not be persisted
3. SEARCH the relevant topic and index for the same subject
4. RESOLVE compatibility:
   - compatible -> update/merge without duplication
   - contradictory -> ask whether to supersede the previous memory
5. SAVE the approved fact to the appropriate topic file
6. UPDATE .agents/memory/MEMORY.md with a one-line pointer
7. CONFIRM exactly what was saved

RULES:
1. Follow memory-system/SKILL.md taxonomy and trust model
2. Keep index entries under 150 characters
3. Topic files must have frontmatter (type, created, updated)
4. Don't save secrets, credentials, tokens, or private keys
5. Don't save information derivable from code
6. Don't save temporary debug context
7. Don't convert inferred preferences or conventions into durable memory without explicit approval
```

---

## Expected Output

```
[OK] Saved to memory

Type: [user/feedback/project/reference]
File: .agents/memory/[topic-file].md
Entry: [one-line summary of what was saved]

This confirmed memory will be available in future sessions.
```

If the new information conflicts with an existing durable memory, stop before writing and use:

```
Memory conflict detected:
- Existing: [current durable fact]
- New: [requested fact]

Replace/supersede the existing memory with the new one?
```

---

## Usage Examples

```
/remember I prefer using bun instead of npm
/remember Our API uses JWT with httpOnly cookies
/remember The production server is at api.example.com:8080
/remember I like concise responses with tables
```

For observations the user did not explicitly ask to persist, do not route them through this workflow automatically. Propose the candidate and obtain approval first.
