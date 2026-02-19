---
name: self-correction
description: Self-reflection and self-correction protocol for AI agents — confidence scoring, internal critique, quality gates, and output refinement before delivery.
allowed-tools: Read, Write, Edit
version: 1.0
priority: HIGH
---

# Self-Correction Skill

> Before delivering, critique. Before critiquing, generate. Before generating, understand.
> The loop: Generate → Critique → Refine → Deliver.

---

## When to Activate

Activate Self-Correction for:

- Any code response > 50 lines
- Any architectural proposal
- Any plan affecting multiple files
- Any security-sensitive output
- Any output that will be hard to reverse

---

## The G-C-R-D Loop

```
GENERATE:  Produce initial output
CRITIQUE:  Apply Self-Reflection Checklist
REFINE:    Fix identified issues
DELIVER:   Ship the refined output
```

---

## Self-Reflection Checklist

| Dimension | Question | Pass Criteria |
|-----------|----------|---------------|
| **Correctness** | Is this technically correct? | No known errors |
| **Completeness** | Am I missing edge cases? | All obvious paths handled |
| **Consistency** | Matches established patterns? | Aligns with CODEBASE.md |
| **Side Effects** | What does this break? | No unintended regressions |
| **Simplicity** | Is there a simpler solution? | No over-engineering |
| **Security** | Any vulnerabilities introduced? | Passes OWASP quick check |

---

## Confidence Scoring

Rate your confidence (0-100%) before delivering complex outputs:

```
Confidence: [X]%
Uncertain about: [specific aspect]
Recommendation: [what to verify]
```

| Score | Meaning | Action |
|-------|---------|--------|
| 90-100% | High confidence | Deliver normally |
| 70-89% | Moderate confidence | Add note, suggest review |
| 50-69% | Low confidence | Flag explicitly, ask for validation |
| <50% | Very uncertain | STOP — ask user for clarification first |

---

## Quality Gates by Artifact Type

### Code

- [ ] Compiles/runs without errors
- [ ] All imports resolve
- [ ] Edge cases handled (null, empty, error)
- [ ] No hardcoded values that should be config
- [ ] No secrets or PII exposed

### Architecture Plan

- [ ] All components have clear boundaries
- [ ] Data flows are specified
- [ ] Security model defined
- [ ] Failure modes considered
- [ ] Migration path from current state noted

### API Design

- [ ] All endpoints have request/response schemas
- [ ] Error codes standardized
- [ ] Auth requirements specified
- [ ] Rate limits considered

---

## Self-Correction Output Format

When surfacing an issue found during self-reflection:

```
⚠️ Self-Correction: Found issue during review.
   Issue: [what the problem is]
   Impact: [what it would break]
   Fix: [how I'm resolving it]
   [corrected output below]
```
