---
name: plan-review
description: Critique and review implementation plans using an 8-point checklist before presenting them to the user.
when_to_use: "Use immediately after generating a plan to review and improve it before presenting. NOT for reviewing code or PRs."
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Plan Review (Critic Skill)

Use this skill to automatically review and improve plans before presenting them to the user.

## Review Protocol (8-Point Checklist)

Evaluate the plan against these 8 criteria. A passing criterion gets 1 point.

1. **Scope Realism**: Plan has < 15 tasks per phase. No "kitchen sink" PRs.
2. **Agent Coverage**: All affected domains have assigned experts (e.g., security-auditor for auth).
3. **Verification Steps**: Concrete test/verify steps are present (not just "run tests").
4. **Security Consideration**: Auth, validation, and secrets are considered for user-facing features.
5. **Edge Cases**: At least 1 error or edge case is explicitly addressed.
6. **Dependency Awareness**: File dependencies are identified (per CODEBASE.md if applicable).
7. **Tech Stack Consistency**: No conflicting libraries or patterns are introduced.
8. **Completeness**: Plan has a clear start, deliverables, and done criteria.

## Scoring Rubric

*   **Score 0-3 (🔴 CRITICAL GAPS)**: Plan needs major revision before presenting. DO NOT PRESENT. Rewrite the plan first.
*   **Score 4-5 (🟡 IMPROVEMENT NEEDED)**: Plan has gaps. Auto-fix the obvious ones, add notes for the rest, then present.
*   **Score 6-7 (🟢 GOOD)**: Minor suggestions. Present with notes.
*   **Score 8 (⭐ EXCELLENT)**: Present as-is.

## Anti-Pattern Detection

Ensure the plan does not contain these common anti-patterns:
- **"Kitchen Sink"** — Plan tries to do everything in one PR
- **"Agent Spam"** — Assigning 10 agents when 3 would suffice
- **"Vague Verification"** — "Run tests" without specifying which tests or how
- **"Missing Security"** — No mention of auth, validation, or secrets for user-facing features
- **"Copy-Paste Steps"** — Identical task descriptions across different agents

## Output Format

When reviewing a plan, silently evaluate the 8 criteria and assign a score. Then present the final plan to the user along with its score and any remaining warnings.

