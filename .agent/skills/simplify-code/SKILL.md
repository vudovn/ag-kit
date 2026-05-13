---
name: simplify-code
description: Reduce complexity of over-engineered code. Identify unnecessary abstractions, remove dead code, flatten deep nesting, and simplify logic while preserving behavior.
when_to_use: "When code is over-engineered, overly abstract, deeply nested, or more complex than needed. When user asks to 'simplify', 'clean up', 'reduce complexity', or 'make this simpler'. NOT for adding new features."
allowed-tools: Read, Write, Edit, Grep, Glob
effort: medium
---

# Simplify Code — Reduce Unnecessary Complexity

> The best code is the code you don't have to write. The second best is the code anyone can read.

## Core Principle

```
Complexity is a cost. Every abstraction, every indirection, every clever pattern
adds cognitive load. Simplify ruthlessly unless complexity serves a clear purpose.
```

---

## Simplification Checklist

### 1. Unnecessary Abstractions
| Smell | Simplification |
|---|---|
| Wrapper class that just delegates | Remove wrapper, use the inner class directly |
| Factory that creates only one type | Replace with direct constructor |
| Strategy pattern with one strategy | Replace with simple function |
| Interface with one implementation | Remove interface, use the class |
| Abstract class with one child | Merge into the child class |
| Config object for 2 values | Use function parameters |

### 2. Dead Code
| Smell | Action |
|---|---|
| Unused imports | Remove |
| Unreachable branches | Remove (check tests first) |
| Commented-out code | Remove (it's in git history) |
| Unused variables/functions | Remove |
| TODO comments older than 6 months | Remove or create issue |
| Feature flags for launched features | Remove flag, keep the code |

### 3. Deep Nesting
```javascript
// ❌ Before: 4 levels deep
function process(data) {
  if (data) {
    if (data.items) {
      for (const item of data.items) {
        if (item.active) {
          doSomething(item)
        }
      }
    }
  }
}

// ✅ After: Early returns + filter
function process(data) {
  if (!data?.items) return

  data.items
    .filter(item => item.active)
    .forEach(doSomething)
}
```

### 4. Over-Parameterized Functions
```typescript
// ❌ Before: 8 parameters
function createUser(name, email, age, role, dept, active, verified, avatar) { }

// ✅ After: Object parameter
function createUser(opts: CreateUserOpts) { }
```

### 5. Premature Optimization
| Smell | Simplification |
|---|---|
| Custom cache for <100 items | Remove cache, measure first |
| Memoization on cheap functions | Remove memo |
| Lazy loading for small modules | Use direct import |
| Complex state machine for 3 states | Use simple if/else or switch |

---

## Simplification Protocol

### Step 1: Identify Complexity
```
- Count nesting levels (target: ≤3)
- Count function parameters (target: ≤4)
- Count lines per function (target: ≤30)
- Count abstractions per feature (target: ≤2)
- Check for dead code (target: 0)
```

### Step 2: Verify Understanding
Before simplifying, ensure you understand:
- What the code does (not what it looks like it does)
- Why it was written this way (maybe there's a reason)
- What tests cover it (simplification must not break tests)

### Step 3: Simplify Incrementally
```
1. Remove dead code first (safest)
2. Flatten nesting with early returns
3. Inline trivial abstractions
4. Merge related functions
5. Simplify data structures
```

### Step 4: Verify Behavior Preserved
```bash
npm run test    # All existing tests still pass
npm run build   # Still compiles
```

---

## When NOT to Simplify

| Situation | Why Keep Complexity |
|---|---|
| Performance-critical hot path | Optimization may look complex but is necessary |
| Required by framework/library | External constraints |
| Explicitly requested pattern | User chose this architecture |
| Will need extension soon | Abstraction prepares for known growth |

> **Ask first:** "This pattern seems over-engineered. Should I simplify it, or is there a reason for the abstraction?"
