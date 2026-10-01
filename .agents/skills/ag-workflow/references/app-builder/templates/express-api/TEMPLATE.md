---
name: express-api
description: Express.js REST API template principles. TypeScript, Prisma, JWT.
---

# Express.js API Template

> Versions reflect the latest stable line verified 2026-05. Pin to the current stable when scaffolding.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Node.js 24 (Krypton LTS) |
| Framework | Express 5 (stable, default on npm) |
| Language | TypeScript |
| Database | PostgreSQL + Prisma |
| Validation | Zod |
| Auth | JWT + bcrypt |

---

## Directory Structure

```
project-name/
├── prisma/
│   └── schema.prisma
├── src/
│   ├── app.ts           # Express app + middleware wiring (no listen)
│   ├── server.ts        # Bootstrap: listen() — split for testability
│   ├── config/          # Environment
│   ├── routes/          # Route definitions only
│   ├── controllers/     # HTTP layer (req/res, calls services)
│   ├── services/        # Business logic
│   ├── middlewares/
│   │   ├── auth.ts      # JWT verify
│   │   ├── error.ts     # Error handler
│   │   └── validate.ts  # Zod validation
│   ├── schemas/         # Zod schemas
│   └── utils/
├── tests/
└── package.json
```

---

## Middleware Stack

| Order | Middleware |
|-------|------------|
| 1 | helmet (security) |
| 2 | cors |
| 3 | compression |
| 4 | body parsing |
| 5 | morgan (logging) |
| 6 | routes |
| 7 | error handler (last, 4-arg signature) |

---

## API Response Format

| Type | Structure |
|------|-----------|
| Success | `{ success: true, data: {...} }` |
| Error | `{ error: "message", details: [...] }` |

---

## Setup Steps

1. Create project directory
2. `npm init -y`
3. Install deps: `npm install express @prisma/client zod bcrypt jsonwebtoken`
4. Install devDeps: `npm install -D prisma typescript @types/node @types/express @types/bcrypt @types/jsonwebtoken`
5. Configure Prisma (`npx prisma init`)
6. `npm run db:push`
7. `npm run dev`


---

## Best Practices

- Split `app.ts` (wiring) from `server.ts` (`listen`) so the app imports cleanly into tests
- Layer architecture (routes → controllers → services)
- Validate all inputs with Zod at the route boundary
- Centralized error handler last (Express 5 auto-forwards rejected promises — no manual catch wrapper needed)
- Environment-based config
- Use Prisma for type-safe DB access
