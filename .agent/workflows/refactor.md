---
description: Strategic, incremental refactoring with regression protection. Identifies code smells, proposes improvements, and refactors without breaking existing behavior.
---

# /refactor — Strategic Refactoring

$ARGUMENTS

---

## When to Use

- Code is working but hard to maintain
- Technical debt is blocking new features
- Performance issues traced to architecture
- After receiving a `code-archaeologist` report

---

## Task

Strategically refactor the specified code with full regression protection.

### Refactoring Protocol

#### Step 1: Load Skills

- `clean-code`
- `architecture`
- `testing-patterns`

#### Step 2: Analyze — Code Smell Detection

Run archaeology analysis:

```bash
python .agent/skills/lint-and-validate/scripts/lint_runner.py .
```

Then manually identify:

| Code Smell | Detection | Priority |
|-----------|-----------|----------|
| **God Class/Function** | > 200 lines, > 10 methods | High |
| **Duplicated Code** | DRY violations | High |
| **Deep Nesting** | > 3 levels | Medium |
| **Long Parameter List** | > 4 params | Medium |
| **Feature Envy** | Function accesses another class more than its own | Medium |
| **Dead Code** | Unreferenced functions/vars | Low |
| **Magic Numbers** | Unexplained raw values | Low |

#### Step 3: Plan — Incremental Refactoring Roadmap

```markdown
## Refactoring Plan: [target]

### Phase 1 (Safe — No behavior change)
- [ ] Rename confusing identifiers
- [ ] Extract constants from magic numbers
- [ ] Remove dead code

### Phase 2 (Structural)
- [ ] Extract methods from God functions
- [ ] Apply DRY to duplicated blocks
- [ ] Flatten deep nesting with guard clauses

### Phase 3 (Architectural)
- [ ] Split God classes into focused modules
- [ ] Apply appropriate design patterns
- [ ] Optimize performance bottlenecks
```

#### Step 4: Execute — Refactor with Regression Safety

```
For each refactoring step:
1. Verify existing tests cover the target code
   → If not: write characterization tests FIRST
2. Make the smallest possible change
3. Run tests → confirm all pass
4. Commit atomic change with clear message
5. Move to next step
```

#### Step 5: Validate

```bash
python .agent/skills/lint-and-validate/scripts/lint_runner.py .
python .agent/skills/testing-patterns/scripts/test_runner.py .
```

---

## Golden Rules of Refactoring

1. **Never refactor and add features simultaneously** — one or the other
2. **Tests before refactoring** — if no tests, write them first
3. **Small steps** — each commit should be a single, understandable improvement
4. **Keep it working** — every step should leave the code in a working state
5. **Measure impact** — verify performance claims with benchmarks

---

## Output Format

```markdown
## Refactoring Report: [target]

### Before (Code Smells Found)
- [Smell 1]: [description and location]
- [Smell 2]: [description and location]

### After (Improvements Made)
- [Improvement 1]: [what changed and why it's better]

### Tests
- [X] existing tests still pass
- [Y] new characterization tests added

### Performance Impact
- Before: [metric]
- After: [metric]
```
