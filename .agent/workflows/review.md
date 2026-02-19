---
description: Intelligent code review with severity ratings — security, quality, performance. Run on any PR or code block to get a structured, actionable review.
---

# /review — Intelligent Code Review

$ARGUMENTS

---

## When to Use

- Before merging a Pull Request
- After implementing a complex feature
- When asking "is this code good enough?"
- Before a security audit

---

## Task

Perform a structured, prioritized code review of the specified files or diff.

### Review Protocol

#### Step 1: Load Skills

- `code-review-checklist`
- `clean-code`
- `vulnerability-scanner`

#### Step 2: Automated Checks

Run validation scripts on the target code:

```bash
python .agent/skills/lint-and-validate/scripts/lint_runner.py .
python .agent/skills/vulnerability-scanner/scripts/security_scan.py .
```

#### Step 3: Structured Review

For each finding, classify by severity:

| Severity | Definition | Must Fix? |
|----------|-----------|-----------|
| 🔴 **Blocker** | Security vulnerability, data corruption risk, crash | YES — before merge |
| 🟠 **Major** | Logic error, significant performance issue, broken contract | YES — this sprint |
| 🟡 **Minor** | Code smell, violation of established pattern | Recommended |
| 🔵 **Nitpick** | Style, naming, optional improvement | Optional |

#### Step 4: Output Format

```markdown
## Code Review: [file/PR name]

### Summary
[2-3 sentence overview of the code quality]

### 🔴 Blockers ([N] items)
- [File:Line] — [Issue] — [Suggested fix]

### 🟠 Major ([N] items)
- [File:Line] — [Issue] — [Suggested fix]

### 🟡 Minor ([N] items)
- [File:Line] — [Issue] — [Suggested fix]

### 🔵 Nitpicks ([N] items)
- [File:Line] — [Optional improvement]

### ✅ What's Good
- [Positive observation 1]
- [Positive observation 2]

### Verdict
[ ] ✅ LGTM — Ready to merge
[ ] ⚠️ LGTM with minor fixes
[ ] ❌ Needs changes — See Blockers/Majors above
```

---

## Review Checklist (Full)

### Security

- [ ] No secrets or API keys in code
- [ ] Input validation on all user-controlled data
- [ ] No SQL injection via string concatenation
- [ ] Auth checks on all sensitive endpoints

### Code Quality

- [ ] Functions under 20 lines
- [ ] No duplication (DRY)
- [ ] Clear, intent-revealing names
- [ ] No magic numbers/strings

### Performance

- [ ] No N+1 query problems
- [ ] No unnecessary re-renders (React)
- [ ] Large operations are async/non-blocking

### Testing

- [ ] New code has test coverage
- [ ] Edge cases are tested
- [ ] No removed test coverage

### Architecture

- [ ] Follows established patterns in this project
- [ ] No circular dependencies introduced
- [ ] Domain boundaries respected
