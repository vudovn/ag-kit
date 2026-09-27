# Feature Building

> How to analyze and implement new features.

## Feature Analysis

```
Request: "add payment system"

Analysis:
├── Required Changes:
│   ├── Database: orders, payments tables
│   ├── Backend: /api/checkout, /api/webhooks/stripe
│   ├── Frontend: CheckoutForm, PaymentSuccess
│   └── Config: Stripe API keys
│
├── Dependencies:
│   ├── stripe package
│   └── Existing user authentication
│
└── Scope: DB + 2 API routes + 2 components + config
```

## Iterative Enhancement Process

```
1. Analyze existing project & architecture
2. Create change plan ({task-slug}.md)
3. If UI modified/added: check & align with DESIGN.md
4. Present plan to user & get approval
5. Apply changes with specialist agents
6. Test & validate (lint, typecheck, unit tests)
7. Start preview (python .agents/scripts/auto_preview.py)
```


## Error Handling

| Error Type | Solution Strategy |
|------------|-------------------|
| TypeScript Error | Fix type, add missing import |
| Missing Dependency | Run npm install |
| Port Conflict | Suggest alternative port |
| Database Error | Check migration, validate connection |

## Recovery Strategy

```
1. Detect error
2. Try automatic fix
3. If failed, report to user
4. Suggest alternative
5. Rollback if necessary
```
