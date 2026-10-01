---
name: nuxt-app
description: Nuxt 4 full-stack template. Vue 3, Pinia, Tailwind v4, Prisma.
---

# Nuxt 4 Full-Stack Template (2026 Edition)

> Modern full-stack template for Nuxt 4. Versions reflect the latest stable line verified 2026-05; pin to current stable when scaffolding.

## Tech Stack

| Component | Technology | Version / Notes |
|-----------|------------|-----------------|
| Framework | Nuxt | v4+ (app/ srcDir structure) |
| UI Engine | Vue | v3 (stable) |
| Language | TypeScript | v5+ (Strict Mode) |
| State | Pinia | v3+ (setup store syntax) |
| Database | PostgreSQL | Prisma ORM |
| Styling | Tailwind CSS | v4 (@tailwindcss/vite plugin) |
| UI Lib | Nuxt UI | v3 (Tailwind v4 native) |
| Validation | Zod | Schema validation |

---

## Directory Structure (Nuxt 4 Standard)

Nuxt 4 defaults `srcDir` to `app/`, keeping client code separate from `server/` and root config.

```
project-name/
├── app/                  # Application source (Nuxt 4 srcDir)
│   ├── assets/css/
│   │   └── main.css      # Tailwind v4 import
│   ├── components/       # Auto-imported components
│   ├── composables/      # Auto-imported logic
│   ├── layouts/
│   ├── middleware/
│   ├── pages/            # File-based routing
│   ├── plugins/
│   ├── stores/           # Pinia stores
│   ├── app.vue           # Root component
│   └── app.config.ts     # Reactive runtime config
├── server/               # Nitro server engine
│   ├── api/              # API routes (e.g. /api/users)
│   ├── routes/           # Server routes
│   └── utils/            # Server-only helpers (Prisma client)
├── shared/               # Isomorphic code (types, Zod schemas)
├── prisma/
│   └── schema.prisma
├── public/
├── nuxt.config.ts
└── package.json
```

---

## Key Concepts (2026)

| Concept | Description |
|---------|-------------|
| **app/ srcDir** | Client code lives under `app/`, cleanly separated from `server/` and config |
| **shared/** | Isomorphic code (types, Zod validators) usable in both Vue app and Nitro server |
| **Server Engine** | Nitro-based; API routes in `server/api/`, Prisma client in `server/utils/` |
| **Tailwind v4** | CSS-first config; theme lives in CSS via `@theme`, no `tailwind.config.js` |
| **Vapor Mode** | Experimental no-VDOM renderer (not GA in 2026). Opt-in per component via `<script setup vapor>` when shipped |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | Prisma connection string (PostgreSQL) |
| NUXT_PUBLIC_APP_URL | Canonical URL |
| NUXT_SESSION_PASSWORD | Session encryption key |

---

## Setup Steps

1. Initialize project:
   ```bash
   npx nuxi@latest init my-app
   ```

2. Install core deps:
   ```bash
   npm install @pinia/nuxt @prisma/client zod
   npm install -D prisma
   ```

3. Setup Tailwind v4 (first-party Vite plugin, NOT @nuxtjs/tailwindcss):
   ```bash
   npm install tailwindcss @tailwindcss/vite
   ```

   Add to `nuxt.config.ts`:
   ```ts
   import tailwindcss from '@tailwindcss/vite'
   export default defineNuxtConfig({
     vite: { plugins: [tailwindcss()] },
     css: ['~/assets/css/main.css']
   })
   ```

4. Configure CSS in `app/assets/css/main.css`:
   ```css
   @import "tailwindcss";
   @theme {
     --color-primary: oklch(0.6 0.15 150);
   }
   ```

5. Run development:
   ```bash
   npm run dev
   ```

---

## Best Practices

- **Data Fetching**: Use `useFetch`/`useAsyncData` for SSR-friendly data; reserve `server: false` for client-only work.
- **State**: Use Pinia (`defineStore`) for global state, Nuxt's `useState` for simple shared SSR state.
- **Validation**: Define Zod schemas in `shared/` and reuse on client forms and Nitro API routes.
- **Type Safety**: API route types are inferred automatically with `$fetch`.
- **Server-only**: Instantiate the Prisma client in `server/utils/` so it never leaks to the client bundle.
