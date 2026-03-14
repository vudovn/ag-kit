---
name: refactoring-patterns
description: Practical refactoring playbook for improving legacy code safely with tests, incremental changes, and rollback awareness.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Refactoring Patterns

Use this skill when improving existing code structure without changing intended behavior.

## Core Rules

1. Preserve behavior first; optimize structure second.
2. Make small, reversible changes.
3. Add tests (or characterization tests) before risky edits.
4. Prefer extraction and simplification over broad rewrites.

## Safe Refactor Sequence

1. Identify behavior-critical paths and edge cases.
2. Add or expand tests to lock current behavior.
3. Apply one refactor at a time (rename, extract, isolate side effects).
4. Run tests after each step.
5. Document key design decisions and tradeoffs.

## Common Patterns

- Extract method for long functions.
- Replace nested conditionals with guard clauses.
- Introduce parameter object for long argument lists.
- Isolate side effects from pure computation.
