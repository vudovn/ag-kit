# Cache Components: `use cache` & `cacheLife`

> [!IMPORTANT]
> This is a Next.js 16+ specific skill. Do NOT apply these patterns to Next.js 15 or earlier without explicitly checking compatibility.

## Core Philosophy
Next.js 16 marks the transition from "Segment-level caching" to "Component-level caching". We no longer rely on `export const revalidate = 3600`. Instead, we use granular directives and profiles.

## 1. The `use cache` Directive
The `use cache` directive can be applied to **Server Components** or **Functions**.

### Rule: Granular Application
Wrap only the data-fetching logic or the specific component that needs caching.

```tsx
// Good: Granular function caching
async function getProduct(id: string) {
  'use cache'
  return await db.product.findUnique({ where: { id } })
}

// Good: Component-level caching
export default async function ProductCard({ id }: { id: string }) {
  'use cache'
  const product = await getProduct(id)
  return <div>{product.name}</div>
}
```

## 2. Using `cacheLife`
`cacheLife` defines the "Freshness" and "Staleness" of a cached item using pre-defined or custom profiles.

### Usage Pattern
```tsx
import { cacheLife } from 'next/cache'

async function getStockInfo() {
  'use cache'
  cacheLife('minutes') // Using a pre-defined profile
  return await fetchStocks()
}
```

### Profile Reference
- `default`: Base profile (1 year stale time).
- `seconds`: High-frequency updates.
- `minutes`: Standard dynamic content.
- `hours`: Stable content (e.g., blog posts).
- `days`: Semi-static content.
- `weeks`: Static-like content.
- `max`: Permanent cache until invalidated.

## 3. On-Demand Invalidation with `cacheTag`
`cacheTag` allows you to label cached data for selective purging.

### Implementation
```tsx
import { cacheTag } from 'next/cache'

async function getProfile(user: string) {
  'use cache'
  cacheTag(`profile-${user}`)
  return await db.user.findUnique(...)
}
```

### Revalidation
In a Server Action:
```tsx
import { revalidateTag, updateTag } from 'next/cache'

export async function updateProfile(user: string, data: any) {
  await db.user.update(...)
  
  // Choice A: Background revalidation (Stale-While-Revalidate)
  revalidateTag(`profile-${user}`)
  
  // Choice B: Immediate "Read-Your-Writes" update
  updateTag(`profile-${user}`)
}
```

## 4. Partial Pre-Rendering (PPR)
Next.js 16 stabilizes PPR via the `cacheComponents` flag in `next.config.ts`. 

### Pattern: Suspense Boundaries
Always wrap dynamic "Cache Components" in `<Suspense>` to enable PPR.

```tsx
import { Suspense } from 'react'
import { Skeleton } from '@/components/ui/skeleton'

export default function Page() {
  return (
    <main>
      <h1>Static Header</h1>
      <Suspense fallback={<Skeleton />}>
        <DynamicCacheComponent />
      </Suspense>
    </main>
  )
}
```
