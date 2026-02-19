---
name: monorepo-patterns
description: Monorepo architecture and management patterns using Turborepo and NX — package boundaries, shared packages, CI optimization, and dependency management.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: MEDIUM
---

# Monorepo Patterns Skill

> One repo, many packages. Done right, a monorepo is a superpower. Done wrong, it's a nightmare.

---

## Monorepo Tool Selection

| Tool | Best For | Strengths |
|------|----------|-----------|
| **Turborepo** | JS/TS monorepos, Next.js | Remote caching, simple config |
| **NX** | Enterprise, polyglot | Smart builds, generators, graph |
| **pnpm workspaces** | Simple multi-package | Native, no extra tooling needed |

---

## Standard Monorepo Structure (Turborepo)

```
my-monorepo/
├── apps/
│   ├── web/          → Next.js app
│   ├── mobile/       → Expo / React Native
│   └── api/          → NestJS / Express server
├── packages/
│   ├── ui/           → Shared React components
│   ├── eslint-config/ → Shared ESLint config
│   ├── tsconfig/     → Shared TypeScript configs
│   ├── utils/        → Shared pure utilities
│   └── types/        → Shared TypeScript types
├── turbo.json
├── package.json
└── pnpm-workspace.yaml
```

---

## turbo.json Configuration

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "dist/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

---

## Package Boundary Rules

```
apps/ → CAN import from packages/
packages/ → MUST NOT import from apps/
packages/utils → MUST NOT import from packages/ui
packages/ui → CAN import from packages/utils, packages/types
```

### Enforce with ESLint

```javascript
// eslint.config.js
rules: {
  'no-restricted-imports': ['error', {
    patterns: ['@myapp/web/*', '@myapp/api/*'] // apps are off-limits for packages
  }]
}
```

---

## Shared packages/ui Pattern

```typescript
// packages/ui/src/button.tsx
export interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export function Button({ variant, size, children, ...props }: ButtonProps) {
  return <button className={cn(variants[variant], sizes[size])} {...props}>{children}</button>;
}

// packages/ui/src/index.ts  ← single entry point
export { Button } from './button';
export { Input } from './input';
export { Modal } from './modal';
```

---

## CI/CD Optimization (Build Only Affected)

```yaml
# .github/workflows/ci.yml
- name: Run Turbo
  run: |
    turbo run build test lint \
      --filter=...[origin/main] \ # only changed packages + dependents
      --remote-only              # use remote cache
```

---

## Monorepo Setup Checklist

- [ ] `pnpm-workspace.yaml` defines all package globs
- [ ] `turbo.json` pipeline covers build, test, lint, dev
- [ ] Each package has its own `package.json` with correct `name`
- [ ] `packages/tsconfig` provides base configs
- [ ] `packages/eslint-config` provides base rules
- [ ] Package boundaries enforced via ESLint
- [ ] Remote caching enabled (Vercel Remote Cache or self-hosted)
- [ ] CI only builds affected packages (`--filter=[origin/main]`)
- [ ] Internal packages use `"*"` version to always use workspace version
