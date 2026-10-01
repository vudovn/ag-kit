# Project Scaffolding

> Directory structure and core files for new projects.

---

## Next.js Full-Stack Structure (Next.js 16 Optimized)

```
project-name/
├── src/
│   ├── app/                        # Routes only (thin layer)
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css             # Tailwind v4 config (@theme) lives here
│   │   ├── (auth)/                 # Route group - auth pages
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (dashboard)/            # Route group - dashboard layout
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── api/                    # Route Handlers (webhooks/external only)
│   │       └── [resource]/route.ts
│   │
│   ├── components/                 # UI components
│   │   ├── ui/                     # Reusable primitives (Button, Input)
│   │   └── forms/                  # Client forms (useActionState)
│   │
│   ├── lib/                        # Shared utilities & server-only logic
│   │   ├── db.ts                   # Prisma singleton client
│   │   ├── dal.ts                  # Data Access Layer (server-only, DTOs)
│   │   └── utils.ts                # Helper functions
│   │
│   ├── actions/                    # Server Actions (mutations)
│   │
│   └── types/                      # Global TypeScript types
│
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts
│
├── public/
├── proxy.ts                        # Network boundary (auth, redirects)
├── DESIGN.md                       # Design source-of-truth tokens & rationale (MANDATORY for UI)
├── .env.example
├── .env.local
├── package.json
├── next.config.ts
├── tsconfig.json
└── README.md
```

---

## Structure Principles

| Principle | Implementation |
|-----------|----------------|
| **Thin routes** | `app/` only for routing + layouts, logic lives in `actions/` and `lib/` |
| **Server/Client separation** | Server-only logic in `lib/dal.ts`, prevents accidental client imports |
| **Data Access Layer** | `lib/dal.ts` centralizes DB access and returns DTOs for safe reuse |
| **Mutations via Server Actions** | `actions/` holds Server Actions, called from forms with `useActionState` |
| **Route groups** | `(groupName)/` for layout sharing without URL impact |
| **Reusable UI** | `components/ui/` for primitives, `components/forms/` for client forms |

---

| File | Purpose |
|------|---------|
| `proxy.ts` | Next.js 16 network boundary logic (auth, redirects). Renamed from `middleware.ts`, runs on Node.js runtime |
| `DESIGN.md` | Single source of truth for visual tokens (YAML frontmatter) & rationale (MANDATORY before UI) |
| `package.json` | Dependencies |
| `next.config.ts` | Next.js config (TypeScript) |
| `tsconfig.json` | TypeScript + path aliases (`@/*`) |
| `.env.example` | Environment template |
| `README.md` | Project documentation |
| `.gitignore` | Git ignore rules |
| `prisma/schema.prisma` | Database schema |
| `src/app/globals.css` | Tailwind v4 config via `@theme` (no `tailwind.config.js`) |


---

## Path Aliases (tsconfig.json)

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/actions/*": ["./src/actions/*"]
    }
  }
}
```

---

## When to Use What

| Need | Location |
|------|----------|
| New page/route | `app/(group)/page.tsx` |
| Reusable button/input | `components/ui/` |
| Client form | `components/forms/` |
| Server action (mutation) | `actions/` |
| Data fetching / DB query | `lib/dal.ts` |
| Prisma client | `lib/db.ts` |
| Helper function | `lib/utils.ts` |
| Auth / redirect logic | `proxy.ts` |
