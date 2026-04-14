# Next.js 14 + TypeScript Setup Guide
## Antigravity Kit Standard Implementation

This document outlines the industry-best practices for initializing a production-ready Next.js project with a strict TypeScript configuration.

### 1. New Project Initialization
Run the following command in your terminal to create the project using the latest stable release:
```bash
npx create-next-app@latest my-antigravity-app \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
```

### 2. Strict TypeScript Configuration (`tsconfig.json`)
Ensure your `tsconfig.json` enforces high-quality code patterns:
- `strict: true` (Mandatory)
- `noImplicitAny: true`
- `strictNullChecks: true`
- `noUnusedLocals: true`
- `noUnusedParameters: true`

### 3. Recommended Directory Structure
```text
src/
├── app/              # App Router (Layouts, Pages, Server Components)
├── components/       # UI Components (Atomic Design preferred)
│   ├── ui/           # Shared primitive components (shadcn pattern)
│   └── dashboard/    # Feature-specific components
├── lib/              # Shared utility functions and library configs
├── hooks/            # Custom React Hooks
├── types/            # Global TypeScript interfaces and types
└── services/         # API and data fetching logic
```

### 4. Essential Environment Setup
Create a `.env.example` to track required environment variables:
```bash
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_ANALYTICS_ID=
DATABASE_URL=
AUTH_SECRET=
```

### 5. Deployment Pre-flight
Before pushing to production, always run the full verification suite:
```bash
npm run build && npm run lint
```
