---
description: Multi-perspective architectural review. Involves Software, Enterprise, and Data Architects for a 360º analysis.
---

# /architect-review - 360º Architectural Review

$ARGUMENTS

---

## 🛑 ORCHESTRATION PROTOCOL

This workflow **MANDATORY** invokes three specialist agents to provide a comprehensive review:

1.  **software-architect**: Focuses on patterns, coupling, and system-level NFRs.
2.  **enterprise-architect**: Focuses on roadmap alignment, cost/FinOps, and standards.
3.  **data-architect**: Focuses on data strategy, AI readiness (RAG), and governance.

---

## Step 1: Parallel Analysis
Invoke all three agents to analyze the provided scope/code.

```
CONTEXT:
$ARGUMENTS

TASK: Review this scope from your specific architectural perspective.
```

## Step 2: Synthesis & Conflict Resolution
The `orchestrator` (or the agent running the workflow) combines the findings into a **Consolidated Architectural Report**.

### Report Structure:
1.  **Software Perspective**: Design patterns & scalability.
2.  **Enterprise Perspective**: Alignment & TCO.
3.  **Data Perspective**: Strategy, AI readiness & Privacy.
4.  **Consolidated Risks**: Any conflict between agents or critical blockers.
5.  **Final Recommendation**: Unified path forward.

---

## Deliverable

| Artifact | Content |
|----------|---------|
| **Architectural Report** | Markdown file or chat response with the 5 sections above |

---

## Usage

```
/architect-review Review our plan to migrate from a Monolith to Microservices
/architect-review Audit the integration of the new Vector Database into the existing API
/architect-review Evaluate the 2026 Technology Roadmap for compliance and scalability
```
