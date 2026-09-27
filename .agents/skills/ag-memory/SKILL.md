---
name: ag-memory
version: 2.0.0
resident: false
triggers: ["remember", "recall", "continue", "resume", "pick up where we left off", "handoff", "what did we decide", "project context"]
---
# AG Memory
Maintain local-first durable project context.

Markdown is the canonical source of truth. Indexes are disposable acceleration layers. Store decisions, constraints, conventions, handoffs, and verified learnings; avoid dumping raw conversation history.

On continue/resume intent, recall relevant durable constraints before project mutation. Confirmed project conventions remain active until the current user overrides them; when that happens, surface the conflict and update stale memory instead of silently ignoring it.
