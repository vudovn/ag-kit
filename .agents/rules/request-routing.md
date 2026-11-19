---
name: request-routing
version: 1.1.0
priority: P0
trigger: always_on
---

# Request Routing - AG Kit

> Always-active. Classify every request, then auto-route to the best specialist agent(s) before responding.

---

## 📥 REQUEST CLASSIFIER (STEP 1)

**Before ANY action, classify the request:**

| Request Type     | Trigger Keywords                           | Active Tiers                   | Result                      |
| ---------------- | ------------------------------------------ | ------------------------------ | --------------------------- |
| **QUESTION**     | "what is", "how does", "explain"           | TIER 0 only                    | Text Response               |
| **SURVEY/INTEL** | "analyze", "list files", "overview"        | TIER 0 + Explorer              | Session Intel (No File)     |
| **SIMPLE CODE**  | "fix", "add", "change" (single file)       | TIER 0 + TIER 1 (lite)         | Inline Edit                 |
| **COMPLEX CODE** | "build", "create", "implement", "refactor" | TIER 0 + TIER 1 (full) + Agent | **{task-slug}.md Required** |
| **NEW APP**      | "new app", "from scratch", "build me a/an", multi-page | `project-planner` (loads `app-builder`) → `orchestrator` | **{task-slug}.md + app-builder** |
| **DESIGN/UI**    | "design", "UI", "page", "dashboard"        | TIER 0 + TIER 1 + Agent        | **{task-slug}.md Required** |
| **SLASH CMD**    | /create, /orchestrate, /debug              | Command-specific flow          | Variable                    |

> 🔴 **NEW APP / scaffold from scratch:** route through `project-planner` or `orchestrator` (both load `app-builder`), NOT a lone specialist like `frontend-specialist`. A specialist alone has no project-detection, tech-stack selection, or template knowledge — `app-builder` does. Or run `/create`.

---

## 🤖 INTELLIGENT AGENT ROUTING (STEP 2 - AUTO)

**ALWAYS ACTIVE: Before responding to ANY request, automatically analyze and select the best agent(s).**

> 🔴 **MANDATORY:** You MUST follow the protocol defined in `@[skills/intelligent-routing]`.

### Auto-Selection Protocol

1. **Analyze (Silent)**: Detect domains (Frontend, Backend, Security, etc.) from user request.
2. **Select Agent(s)**: Choose the most appropriate specialist(s).
3. **Inform User**: Concisely state which expertise is being applied.
4. **Apply**: Generate response using the selected agent's persona and rules.

### Response Format (MANDATORY)

When auto-applying an agent, inform the user:

```markdown
🤖 **Applying knowledge of `@[agent-name]`...**

[Continue with specialized response]
```

**Rules:**

1. **Silent Analysis**: No verbose meta-commentary ("I am analyzing...").
2. **Respect Overrides**: If user mentions `@agent`, use it.
3. **Complex Tasks**: For multi-domain requests, use `orchestrator` and ask Socratic questions first.

### ⚠️ AGENT ROUTING CHECKLIST (MANDATORY BEFORE EVERY CODE/DESIGN RESPONSE)

**Before ANY code or design work, you MUST complete this mental checklist:**

| Step | Check | If Unchecked |
|------|-------|--------------|
| 1 | Did I identify the correct agent for this domain? | → STOP. Analyze request domain first. |
| 2 | Did I READ the agent's `.md` file (or recall its rules)? | → STOP. Open `.agents/agent/{agent}.md` |
| 3 | Did I announce `🤖 Applying knowledge of @[agent]...`? | → STOP. Add announcement before response. |
| 4 | Did I load required skills from agent's frontmatter? | → STOP. Check `skills:` field and read them. |

**Failure Conditions:**

- ❌ Writing code without identifying an agent = **PROTOCOL VIOLATION**
- ❌ Skipping the announcement = **USER CANNOT VERIFY AGENT WAS USED**
- ❌ Ignoring agent-specific rules (e.g., Purple Ban) = **QUALITY FAILURE**

> 🔴 **Self-Check Trigger:** Every time you are about to write code or create UI, ask yourself:
> "Have I completed the Agent Routing Checklist?" If NO → Complete it first.

---

## 🧭 WORKFLOW INTENT DECISION TREE (STEP 3)

**When a request maps to a workflow or slash command, route directly to the optimal procedure:**

### 🔄 End-to-End SDLC Lifecycle

```
[ Discovery: /brainstorm ] ──► [ Task Plan: /plan ] ──► [ Scaffold: /create ] ──► [ Refine: /enhance ]
                                                                                         │
   ┌─────────────────────────────────────────────────────────────────────────────────────┘
   ▼
[ Run Tests: /test ] ──► [ Live Proof: /verify ] ──► [ Production: /deploy ] ──► [ Remember: /remember ]
         │
         ▼ (Failures)
[ Triage & Fix: /debug ] ──► (Verify Fix) ──► [ /test ]
```

### 🎯 Intent-to-Workflow Decision Matrix

| User Intent / Signal Keywords | Primary Workflow | Key Agents & Skills | Next Step Chaining |
|-------------------------------|:----------------:|---------------------|:------------------:|
| "I have an idea", "explore options", "brainstorm", vague requirements | `/brainstorm` | `project-planner` + `brainstorming` | ➔ `/plan` |
| "Plan this", "breakdown tasks", "create roadmap", architectural design | `/plan` | `project-planner` + `plan-writing`, `plan-review` | ➔ `/create` or `/enhance` |
| "Build new app", "create feature from scratch", "scaffold project" | `/create` | `app-builder`, `orchestrator` | ➔ `/enhance` or `/test` |
| "Refactor", "improve", "add field", "style UI", modify existing code | `/enhance` | Domain specialist (`frontend`, `backend`, etc.) | ➔ `/test` |
| "Cross-domain initiative", "multi-phase project", full execution | `/orchestrate` | `orchestrator` + domain specialists | ➔ `/test` or `/verify` |
| "Run in parallel", "distribute tasks", multiple agents/threads | `/coordinate` | `coordinator` + `coordinator-mode` | ➔ `/verify` |
| "Bug", "error", "failing test", "incident", "CrashLoopBackOff", 500 | `/debug` | `debugger` + `systematic-debugging`, `verify-changes` | ➔ `/test` or `/verify` |
| "Run test suite", "check unit tests", "integration tests", "coverage" | `/test` | `test-engineer` + `testing-patterns`, `tdd-workflow` | ➔ `/verify` or `/deploy` |
| "Prove it works", "verify live", empirical execution check | `/verify` | `debugger` / `test-engineer` + `verify-changes` | ➔ `/deploy` |
| "Show me", "preview UI", "render in browser", visual inspection | `/preview` | `frontend-specialist` + browser sidecar | ➔ `/verify` |
| "Deploy to prod", "ship release", staging rollout, publish | `/deploy` | `devops-engineer` + `deployment-procedures` | ➔ `/remember` |
| "Remember this preference", "save decision", "add to project memory" | `/remember` | Memory manager + `MEMORY.md` | Flow Complete |
| "Project health", "what's pending", "status overview" | `/status` | `orchestrator` | Next pending task |

### 🛡️ Workflow Routing Guardrails
1. **Never Skip Planning for Complex Work:** Requests involving `COMPLEX CODE` or `NEW APP` must route through `/brainstorm` ➔ `/plan` before code generation.
2. **Strict Circuit Breaker on Debugging:** Never loop indefinitely on failures. `/debug` enforces a hard limit of `max_iterations: 2` before escalating via `escalation-report.md`.
3. **Always Verify Before Deploy:** Code must never flow directly from `/create` or `/enhance` to `/deploy` without running `/test` and `/verify`.
4. **Lean Dispatching:** Do not invoke heavy multi-agent workflows (`/coordinate` or `/orchestrate`) for single-file or localized edits; use direct inline edits with the domain specialist.

---

## 🎭 Gemini Mode Mapping

| Mode     | Agent             | Behavior                                     |
| -------- | ----------------- | -------------------------------------------- |
| **plan** | `project-planner` | 4-phase methodology. NO CODE before Phase 4. |
| **ask**  | -                 | Focus on understanding. Ask questions.       |
| **edit** | `orchestrator`    | Execute. Check `{task-slug}.md` first.       |

> 🔴 **Edit mode:** If multi-file or structural change → Offer to create `{task-slug}.md`. For single-file fixes → Proceed directly.
> Full Plan Mode (4-Phase) protocol lives in `code-rules.md`.

---
