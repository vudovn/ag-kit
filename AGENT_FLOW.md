# 🔄 Agent Flow Architecture

> **AG Kit 2026.5.13** — Comprehensive AI Agent Workflow Documentation

---

## 📊 Overview Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REQUEST CLASSIFICATION                        │
│  • Analyze intent (build, debug, test, deploy, etc.)           │
│  • Identify domain (frontend, backend, mobile, etc.)           │
│  • Detect complexity (simple, medium, complex)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
    ┌───────────────────┐      ┌──────────────────┐
    │ WORKFLOW COMMAND  │      │  DIRECT AGENT    │
    │  (Slash Command)  │      │  ASSIGNMENT      │
    └─────────┬─────────┘      └────────┬─────────┘
              │                         │
              ▼                         ▼
    ┌───────────────────┐      ┌──────────────────┐
    │ /brainstorm       │      │ Agent Selection  │
    │ /create           │      │ Based on Domain  │
    │ /debug            │      │                  │
    │ /deploy           │      │ • frontend-*     │
    │ /enhance          │      │ • backend-*      │
    │ /orchestrate      │      │ • mobile-*       │
    │ /plan             │      │ • database-*     │
    │ /preview          │      │ • devops-*       │
    │ /status           │      │ • test-*         │
    │ /test             │      │ • security-*     │
    │ /ui-ux-pro-max    │      │ • game-*         │
    └─────────┬─────────┘      └────────┬─────────┘
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
         ┌─────────────────────────────────────┐
         │       AGENT INITIALIZATION          │
         │  • Load agent persona/role          │
         │  • Load required skills             │
         │  • Set behavioral mode              │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │      SKILL LOADING PROTOCOL         │
         │                                      │
         │  1. Read SKILL.md metadata          │
         │  2. Load references/ (if needed)    │
         │  3. Execute scripts/ (if needed)    │
         │  4. Apply rules and patterns        │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │         TASK EXECUTION              │
         │                                      │
         │  • Analyze codebase                 │
         │  • Apply best practices             │
         │  • Generate/modify code             │
         │  • Run validations                  │
         │  • Execute tests                    │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │      VALIDATION LAYER               │
         │                                      │
         │  Quick Check (checklist.py):        │
         │  • Security scan                    │
         │  • Code quality (lint/types)        │
         │  • Schema validation                │
         │  • Test suite                       │
         │  • UX audit                         │
         │  • SEO check                        │
         │                                      │
         │  Full Check (verify_all.py):        │
         │  • All above + Lighthouse           │
         │  • E2E tests (Playwright)           │
         │  • Bundle analysis                  │
         │  • Mobile audit                     │
         │  • i18n check                       │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │         RESULT DELIVERY             │
         │  • Present changes to user          │
         │  • Provide explanations             │
         │  • Suggest next steps               │
         └─────────────────────────────────────┘
```

---

## 🎯 Detailed Agent Workflow

### 1️⃣ **Request Entry Points**

```
User Input Types:
┌─────────────────────────────────────────────────────────────┐
│ A. Natural Language Request                                 │
│    "Build a React dashboard with charts"                    │
│                                                              │
│ B. Slash Command                                            │
│    "/create feature: user authentication"                   │
│                                                              │
│ C. Domain-Specific Request                                  │
│    "Optimize database queries" → database-architect         │
│    "Fix security vulnerability" → security-auditor          │
│    "Deploy to AWS" → devops-engineer                        │
└─────────────────────────────────────────────────────────────┘
```

#### Socratic Gate Protocol

Before implementation, verify:

- **New Feature** → ASK 3 strategic questions
- **Bug Fix** → Confirm understanding + ask impact
- **Vague request** → Ask Purpose, Users, Scope

### 2️⃣ **Agent Selection Matrix**

#### Agent Routing Checklist (Mandatory)

Before ANY code/design work:

| Step | Check                        | If Unchecked                             |
| ---- | ---------------------------- | ---------------------------------------- |
| 1    | Identify correct agent       | → Analyze request domain                 |
| 2    | Read agent's .md file        | → Open `.agent/agents/{agent}.md`        |
| 3    | Announce agent               | → `🤖 Applying knowledge of @[agent]...` |
| 4    | Load skills from frontmatter | → Check `skills:` field                  |

```
Request Domain → Agent Mapping:

┌──────────────────────┬─────────────────────┬──────────────────────────┐
│ Domain               │ Primary Agent       │ Skills Loaded            │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ UI/UX Design         │ frontend-specialist │ react-best-practices      │
│                      │                     │ frontend-design          │
│                      │                     │ tailwind-patterns        │
|                      │                     │ web-design-guidelines    │
│                      │                     │ frontend-design          │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ API Development      │ backend-specialist  │ api-patterns             │
│                      │                     │ nodejs-best-practices    │
│                      │                     │ nestjs-expert            │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Database Design      │ database-architect  │ database-design          │
│                      │                     │ prisma-expert            │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Mobile App           │ mobile-developer    │ mobile-design            │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Game Development     │ game-developer      │ game-development         │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ DevOps/Deployment    │ devops-engineer     │ docker-expert            │
│                      │                     │ deployment-procedures    │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Security Audit       │ security-auditor    │ vulnerability-scanner    │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Penetration Testing  │ penetration-tester  │ red-team-tactics         │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Testing              │ test-engineer       │ testing-patterns         │
│                      │                     │ webapp-testing           │
│                      │                     │ tdd-workflow             │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Debugging            │ debugger            │ systematic-debugging     │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Performance          │ performance-        │ performance-profiling    │
│                      │ optimizer           │                          │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ SEO                  │ seo-specialist      │ seo-fundamentals         │
│                      │                     │ geo-fundamentals         │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Documentation        │ documentation-      │ documentation-templates  │
│                      │ writer              │                          │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Planning/Discovery   │ project-planner     │ brainstorming            │
│                      │                     │ plan-writing             │
│                      │                     │ architecture             │
├──────────────────────┼─────────────────────┼──────────────────────────┤
│ Multi-Agent Tasks    │ orchestrator        │ parallel-agents          │
│                      │                     │ behavioral-modes         │
└──────────────────────┴─────────────────────┴──────────────────────────┘
```

### 3️⃣ **Skill Loading Protocol**

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILL LOADING FLOW                        │
└─────────────────────────────────────────────────────────────┘

Step 1: Match Request to Skill
┌──────────────────────────────────────────┐
│ User: "Build a REST API"                 │
│   ↓                                       │
│ Keyword Match: "API" → api-patterns      │
└──────────────────────────────────────────┘
                    ↓
Step 2: Load Skill Metadata
┌──────────────────────────────────────────┐
│ Read: .agent/skills/api-patterns/        │
│       └── SKILL.md (main instructions)   │
└──────────────────────────────────────────┘
                    ↓
Step 3: Load References (if needed)
┌──────────────────────────────────────────┐
│ Read: api-patterns/rest.md               │
│       api-patterns/graphql.md            │
│       api-patterns/auth.md               │
│       api-patterns/documentation.md      │
└──────────────────────────────────────────┘
                    ↓
Step 4: Execute Scripts (if needed)
┌──────────────────────────────────────────┐
│ Run: scripts/api_validator.py            │
│      (validates API design)              │
└──────────────────────────────────────────┘
                    ↓
Step 5: Apply Knowledge
┌──────────────────────────────────────────┐
│ Agent now has:                           │
│ • API design patterns                    │
│ • Authentication strategies              │
│ • Documentation templates                │
│ • Validation scripts                     │
└──────────────────────────────────────────┘

### Related Skills Pattern

Skills now link to each other:
- `frontend-design` → `web-design-guidelines` (after coding)
- `web-design-guidelines` → `frontend-design` (before coding)

> **Note**: Scripts are NOT auto-executed. AI suggests running them, user approves.
```

### 4️⃣ **Workflow Command Execution**

```
Slash Command Flow:

/brainstorm
    ↓
    1. Load: brainstorming skill
    2. Apply: Socratic questioning
    3. Output: Structured discovery document

/create
    ↓
    1. Detect: Project type (web/mobile/api/game)
    2. Load: app-builder skill + domain-specific skills
    3. Select: Template from app-builder/templates/
    4. Scaffold: Generate project structure
    5. Validate: Run checklist.py

/debug
    ↓
    1. Load: systematic-debugging skill
    2. Analyze: Error logs, stack traces
    3. Apply: Root cause analysis
    4. Suggest: Fix with code examples
    5. Test: Verify fix works

/deploy
    ↓
    1. Load: deployment-procedures skill
    2. Detect: Platform (Vercel, AWS, Docker, etc.)
    3. Prepare: Build artifacts
    4. Execute: Deployment scripts
    5. Verify: Health checks
    6. Output: Deployment URL

/test
    ↓
    1. Load: testing-patterns + webapp-testing skills
    2. Detect: Test framework (Jest, Vitest, Playwright)
    3. Generate: Test cases
    4. Execute: Run tests
    5. Report: Coverage + results

/orchestrate
    ↓
    1. Load: parallel-agents skill
    2. Decompose: Task into subtasks
    3. Assign: Each subtask to specialist agent
    4. Coordinate: Parallel execution
    5. Merge: Combine results
    6. Validate: Run full verification

/plan
    ↓
    1. Load: plan-writing + architecture skills
    2. Analyze: Requirements
    3. Break down: Tasks with estimates
    4. Output: Structured plan with milestones

/ui-ux-pro-max
    ↓
    1. Load: ui-ux-pro-max skill
    2. Access: 50 design styles
    3. Access: 21 color palettes
    4. Access: 50 font combinations
    5. Generate: Professional UI with selected style
```

### 5️⃣ **Multi-Agent Orchestration**

```
Complex Task → /orchestrate → Multiple Specialist Personas

Example: "Build a full-stack e-commerce app"

┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR AGENT                       │
│  Decomposes task into sequential workstreams                │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ FRONTEND      │   │ BACKEND       │   │ DATABASE      │
│ SPECIALIST    │   │ SPECIALIST    │   │ ARCHITECT     │
│               │   │               │   │               │
│ Skills:       │   │ Skills:       │   │ Skills:       │
│ • react-*     │   │ • api-*       │   │ • database-*  │
│ • nextjs-*    │   │ • nodejs-*    │   │ • prisma-*    │
│ • tailwind-*  │   │ • nestjs-*    │   │               │
│               │   │               │   │               │
│ Builds:       │   │ Builds:       │   │ Builds:       │
│ • UI/UX       │   │ • REST API    │   │ • Schema      │
│ • Components  │   │ • Auth        │   │ • Migrations  │
│ • Pages       │   │ • Business    │   │ • Indexes     │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └─────────────────┬─┴───────────────────┘
                          │
                          ▼
        ┌─────────────────────────────────────┐
        │      CODE COHERENCE                 │
        │  • AI maintains consistency         │
        │  • Sequential context switching     │
        │  • Ensure API contracts match       │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │    VALIDATION (All Agents)          │
        │  • test-engineer → Tests            │
        │  • security-auditor → Security      │
        │  • performance-optimizer → Perf     │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │    DEPLOYMENT                       │
        │  • devops-engineer → Deploy         │
        └─────────────────────────────────────┘
```

### 6️⃣ **Validation & Quality Gates**

```
┌─────────────────────────────────────────────────────────────┐
│                 VALIDATION PIPELINE                          │
└─────────────────────────────────────────────────────────────┘

During Development (Quick Checks):
┌──────────────────────────────────────────┐
│ python .agent/scripts/checklist.py .     │
├──────────────────────────────────────────┤
│ ✓ Security Scan (vulnerabilities)        │
│ ✓ Code Quality (ESLint, TypeScript)      │
│ ✓ Schema Validation (Prisma/DB)          │
│ ✓ Test Suite (Unit tests)                │
│ ✓ UX Audit (Accessibility)               │
│ ✓ SEO Check (Meta tags, performance)     │
└──────────────────────────────────────────┘
        Time: ~30 seconds

Pre-Deployment (Full Verification):
┌──────────────────────────────────────────────────────┐
│ python .agent/scripts/verify_all.py .                │
│        --url http://localhost:3000                   │
├──────────────────────────────────────────────────────┤
│ ✓ All Quick Checks                                   │
│ ✓ Lighthouse Audit (Core Web Vitals)                 │
│ ✓ Playwright E2E Tests                               │
│ ✓ Bundle Analysis (Size, tree-shaking)               │
│ ✓ Mobile Audit (Responsive, touch targets)           │
│ ✓ i18n Check (Translations, locale)                  │
└──────────────────────────────────────────────────────┘
        Time: ~3-5 minutes
```

---

## 🧩 Skill-to-Script Mapping

```
Skills with Automated Scripts:

┌─────────────────────────┬──────────────────────────────────┐
│ Skill                   │ Script                           │
├─────────────────────────┼──────────────────────────────────┤
│ api-patterns            │ scripts/api_validator.py         │
│ database-design         │ scripts/schema_validator.py      │
│ frontend-design         │ scripts/accessibility_checker.py │
│                         │ scripts/ux_audit.py              │
│ geo-fundamentals        │ scripts/geo_checker.py           │
│ i18n-localization       │ scripts/i18n_checker.py          │
│ lint-and-validate       │ scripts/lint_runner.py           │
│                         │ scripts/type_coverage.py         │
│ mobile-design           │ scripts/mobile_audit.py          │
│ performance-profiling   │ scripts/lighthouse_runner.py     │
│                         │ scripts/bundle_analyzer.py       │
│ seo-fundamentals        │ scripts/seo_checker.py           │
│ testing-patterns        │ scripts/test_runner.py           │
│ vulnerability-scanner   │ scripts/security_scanner.py      │
│ webapp-testing          │ scripts/e2e_runner.py            │
└─────────────────────────┴──────────────────────────────────┘
```

---

## 🔄 Complete Request Lifecycle Example

```
User Request: "Build a Next.js dashboard with authentication"

1. REQUEST CLASSIFICATION
   ├─ Type: Build new feature
   ├─ Domain: Frontend + Backend
   ├─ Complexity: Medium-High
   └─ Suggested: /create or /orchestrate

2. WORKFLOW SELECTION
   └─ User chooses: /orchestrate (multi-agent approach)

3. ORCHESTRATOR DECOMPOSITION
   ├─ Frontend: Dashboard UI (React components)
   ├─ Backend: Auth API (JWT, session management)
   ├─ Database: User schema (Prisma)
   └─ Testing: E2E auth flow

4. AGENT ASSIGNMENT
   ├─ frontend-specialist
   │   └─ Skills: react-best-practices, tailwind-patterns, frontend-design
   ├─ backend-specialist
   │   └─ Skills: api-patterns, nodejs-best-practices
   ├─ database-architect
   │   └─ Skills: database-design, prisma-expert
   └─ test-engineer
       └─ Skills: testing-patterns, webapp-testing

5. SEQUENTIAL MULTI-DOMAIN EXECUTION
   Note: AI processes each domain sequentially, switching context between specialist "personas."
   This is NOT true parallel execution but simulated multi-agent behavior.

   ├─ Frontend builds:
   │   ├─ app/dashboard/page.tsx (Server Component)
   │   ├─ components/DashboardLayout.tsx
   │   ├─ components/LoginForm.tsx
   │   └─ lib/auth-client.ts
   ├─ Backend builds:
   │   ├─ app/api/auth/login/route.ts
   │   ├─ app/api/auth/logout/route.ts
   │   ├─ lib/jwt.ts
   │   └─ middleware.ts
   ├─ Database builds:
   │   ├─ prisma/schema.prisma (User, Session models)
   │   └─ prisma/migrations/
   └─ Testing builds:
       ├─ tests/auth.spec.ts (Playwright)
       └─ tests/dashboard.spec.ts

6. CODE INTEGRATION
   Reality Note: AI writes code as a continuous stream, maintaining consistency.
   There is no "merge" step - it's all generated coherently from the start.

   └─ AI maintains coherence across domains
       ├─ Resolves import paths
       ├─ Ensures type safety
       └─ Connects API routes to UI

7. VALIDATION
   ├─ checklist.py
   │   ✓ Security: No leaked secrets
   │   ✓ Lint: No ESLint errors
   │   ✓ Types: TypeScript passes
   │   ✓ Tests: Auth flow passes
   └─ verify_all.py
       ✓ E2E: Login → Dashboard → Logout works
       ✓ Accessibility: WCAG AA compliant
       ✓ Performance: Lighthouse score > 90

8. RESULT DELIVERY
   └─ User receives:
       ├─ Complete codebase
       ├─ Documentation (how to run)
       ├─ Test reports
       └─ Deployment instructions
```

---

## 📈 Statistics & Metrics

```
┌──────────────────────────────────────────────────────────┐
│                    SYSTEM CAPABILITIES                    │
├──────────────────────────────────────────────────────────┤
│ Total Agents:              20                            │
│ Total Skills:              45 (+8 new in 2026.5.13)      │
│ Total Workflows:           14 (+3 new in 2026.5.13)      │
│ Master Scripts:            2 (checklist, verify_all)     │
│ Skill-Level Scripts:       18                            │
│ Coverage:                  ~95% web/mobile + orchestration│
│ Token Efficiency:          13-33% better (2026.5.13)     │
│                                                          │
│ New in 2026.5.13:                                        │
│ ├─ Coordinator Mode (parallel orchestration)             │
│ ├─ Persistent Memory System (MEMORY.md)                  │
│ ├─ Context Compression (auto-compact)                    │
│ ├─ Conditional Skill Loading (when_to_use)               │
│ └─ Verification by Execution (/verify)                   │
│                                                          │
│ Supported Frameworks:                                    │
│ ├─ Frontend: React, Next.js, Vue, Nuxt, Astro          │
│ ├─ Backend: Node.js, NestJS, FastAPI, Express          │
│ ├─ Mobile: React Native, Flutter                        │
│ ├─ Database: Prisma, TypeORM, Sequelize                │
│ ├─ Testing: Jest, Vitest, Playwright, Cypress          │
│ └─ DevOps: Docker, Vercel, AWS, GitHub Actions         │
└──────────────────────────────────────────────────────────┘
```

---

## 🎓 Best Practices

### When to Use Each Workflow

```
/brainstorm
  ✓ Unclear requirements
  ✓ Need to explore options
  ✓ Complex problem needs breaking down

/create
  ✓ New feature in existing project
  ✓ Small-to-medium complexity
  ✓ Single domain (frontend OR backend)

/orchestrate
  ✓ Full-stack features
  ✓ Complex multi-step tasks
  ✓ Need multiple specialist agents

/debug
  ✓ Bug reports
  ✓ Unexpected behavior
  ✓ Performance issues

/test
  ✓ Need test coverage
  ✓ Before deployment
  ✓ After major changes

/deploy
  ✓ Ready to ship
  ✓ After all tests pass
  ✓ Need production URL

/plan
  ✓ Large projects
  ✓ Need time estimates
  ✓ Team coordination needed
```

---

## 🔗 Quick Reference Links

- **Architecture**: `.agent/ARCHITECTURE.md`
- **Agents**: `.agent/agents/`
- **Skills**: `.agent/skills/`
- **Workflows**: `.agent/workflows/`
- **Scripts**: `.agent/scripts/`

---

**Last Updated**: 2026-05-13
**Version**: 2026.5.13
