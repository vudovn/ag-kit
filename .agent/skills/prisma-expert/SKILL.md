---
name: prisma-expert
description: Prisma ORM expertise for schema design, migrations, query performance, and production-safe database changes.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Prisma Expert

Use this skill when working with Prisma models, migrations, seed scripts, or query logic.

## Core Rules

1. Prefer additive, backward-compatible schema changes.
2. Never drop or rename a column in one step on production paths.
3. Use transactions for multi-step writes that must be atomic.
4. Avoid N+1 query patterns; use `include`, `select`, and batching deliberately.

## Migration Safety Checklist

- Confirm current schema and generated SQL before applying.
- Add new columns as nullable or with safe defaults first.
- Backfill data in controlled steps.
- Enforce constraints only after backfill is complete.
- Validate rollback strategy before deployment.

## Query Practices

- Select only required fields.
- Add pagination (`take`/`skip` or cursor pagination) for list endpoints.
- Ensure indexed filters for frequent read paths.
- Use `upsert` carefully and verify unique constraints align with business rules.
