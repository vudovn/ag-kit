---
name: coordinator-mode
description: Advanced multi-agent orchestration with parallel workers, synthesis protocols, and coordinator lifecycle. Use when complex tasks require multiple agents working in parallel with intelligent result synthesis.
when_to_use: "When the user needs multi-agent coordination, parallel task execution, complex multi-domain work, or when /coordinate or /orchestrate is invoked. NOT for single-domain tasks."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
effort: high
---

# Coordinator Mode — Multi-Agent Orchestration

> Distilled from production-proven coordinator patterns. Transforms sequential agent chains into intelligent parallel orchestration.

## Overview

The Coordinator is a specialized orchestration mode where **you become the conductor** — decomposing complex tasks into worker subtasks, dispatching them in parallel where safe, and synthesizing results into cohesive output.

**You are NOT a worker. You are the coordinator.** Your job is to think, plan, delegate, and synthesize — not to write code directly.

---

## Coordinator Lifecycle

```
User Request
    ↓
1. DECOMPOSE — Break task into worker subtasks
    ↓
2. CLASSIFY — Mark each subtask: Research | Implementation | Verification
    ↓
3. DISPATCH — Launch workers (parallel for reads, sequential for writes)
    ↓
4. MONITOR — Track worker completion notifications
    ↓
5. SYNTHESIZE — Combine results into unified response
    ↓
6. VERIFY — Ensure completeness before reporting to user
```

---

## Phase-Based Workflow

| Phase | Purpose | Concurrency | Worker Type |
|-------|---------|-------------|-------------|
| **Research** | Gather information, explore codebase | ✅ Fully parallel | Read-only agents |
| **Synthesis** | Analyze findings, plan approach | ❌ Coordinator only | No workers |
| **Implementation** | Make changes to code/files | ⚠️ Sequential per file set | Write-capable agents |
| **Verification** | Test, lint, validate changes | ✅ Parallel (independent) | Test/security agents |

> 🔴 **Rule:** NEVER skip the Synthesis phase. Research → direct Implementation = poor results.

---

## Concurrency Rules

### Safe to Parallelize
- ✅ Multiple agents reading different files
- ✅ Security audit + performance audit (read-only)
- ✅ Test runner + linter (independent)
- ✅ Exploring different directories

### Must Be Sequential
- ❌ Two agents writing to the same file
- ❌ Implementation that depends on another agent's output
- ❌ Database migration + code that uses the new schema
- ❌ API change + frontend that consumes the API

---

## Worker Prompt Writing Guide

### 🔴 The Golden Rule: Never Delegate Understanding

```
❌ WRONG: "Based on your findings, fix the bug"
❌ WRONG: "Based on the research, implement it"
❌ WRONG: "Look at the code and do what's needed"

✅ RIGHT: "The bug is in src/auth/jwt.ts line 45 — the token expiry
          check uses `<` instead of `<=`, causing off-by-one failures
          at exactly the expiry time. Change line 45 from
          `if (now < expiry)` to `if (now <= expiry)`"
```

> **Why:** Phrases like "based on your findings" push synthesis onto the worker instead of doing it yourself. Write prompts that prove YOU understood — include file paths, line numbers, what specifically to change.

### Writing Effective Worker Prompts

Brief the worker like a **smart colleague who just walked into the room**:

1. **Explain what** you're trying to accomplish and why
2. **Describe what** you've already learned or ruled out
3. **Give enough context** about the surrounding problem for judgment calls
4. **Be specific** about scope: what's in, what's out, what another agent handles
5. **State the output format** you expect ("report in under 200 words")

### Prompt Templates

#### Research Worker
```
Investigate [specific question] in [file/directory scope].
Context: We're trying to [goal] because [reason].
I've already checked [what you checked] and found [what you found].
Report: List [specific deliverable]. Under 200 words.
```

#### Implementation Worker
```
Modify [specific file(s)] to [specific change].
Context: [Why this change is needed].
The current code at [file:line] does [X], change it to [Y].
Constraints: Don't touch [out-of-scope files]. Another agent handles [related area].
Verify: [How the worker should confirm success].
```

#### Verification Worker
```
Verify that [specific change] works correctly.
Run: [specific commands].
Check: [what success looks like].
Report: Pass/fail with details on any failures.
```

---

## Fork Semantics

### When to Fork (vs. Spawn Fresh Agent)

| Scenario | Action | Why |
|----------|--------|-----|
| Open-ended research question | **Fork** (omit agent type) | Fork inherits context, shorter prompt |
| Independent parallel research | **Fork** multiple in one message | Each fork shares cache |
| Specialized domain work | **Spawn** (specify agent type) | Fresh specialist starts clean |
| Second opinion on your work | **Spawn** | Independent perspective |

### Fork Rules

1. **Don't peek.** Don't read the fork's output file mid-flight. You'll get a completion notification. Reading the transcript pulls tool noise into your context.

2. **Don't race.** After launching, you know nothing about what the fork found. Never fabricate or predict fork results. If the user asks before notification lands, say "the fork is still running."

3. **Keep prompts short.** Forks inherit your full context — write a *directive* (what to do), not a *briefing* (what the situation is).

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|---|---|---|
| "Look at the code and fix it" | Zero context = workers make wrong assumptions | Provide specific file paths, line numbers, and what to change |
| Skipping Research phase | Implementation without understanding = rework | Always research first, even briefly |
| Launching 10+ workers at once | Overwhelms synthesis, diminishing returns | 2-5 workers per round, synthesize, then more if needed |
| Fabricating worker results | User gets wrong information | Wait for actual notification, say "still running" if asked |
| Coordinator writes code directly | Loses orchestration benefits | Always delegate to appropriate specialist |

---

## Synthesis Protocol

After all workers complete:

```markdown
## Coordinator Synthesis

### Task: [Original Request]

### Workers Dispatched
| Worker | Type | Status | Key Finding |
|--------|------|--------|-------------|
| agent-1 | Research | ✅ | Found X in file Y |
| agent-2 | Research | ✅ | Identified Y pattern |

### Consolidated Analysis
[Your synthesis — not a copy-paste of worker output]

### Decision & Rationale
[What you decided based on ALL worker findings and why]

### Implementation Plan
1. [Specific change with file path]
2. [Specific change with file path]

### Remaining Risk
- [Anything workers flagged but couldn't resolve]
```

---

## Continue vs. Spawn Decision

| Situation | Action |
|-----------|--------|
| Worker completed, need follow-up on same topic | **Continue** (send message to worker ID) |
| Worker completed, need different domain work | **Spawn new** specialist |
| Worker failed, need retry with same context | **Continue** with corrected instructions |
| Worker failed, need fundamentally different approach | **Spawn new** |

---

## Best Practices

1. **Start with 2-3 workers** — add more after synthesis if needed
2. **Research before implementation** — always, even for "simple" tasks
3. **Synthesize, don't copy** — your summary should add insight, not repeat
4. **Verify independently** — verification workers shouldn't trust implementation workers
5. **Track state** — note which workers are pending/completed/failed
6. **Share scratchpad** — use a known directory for cross-worker artifacts
