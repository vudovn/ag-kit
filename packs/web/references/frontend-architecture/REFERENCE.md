# Legacy knowledge: frontend-architecture

> **Cold reference only.** Migrated from AG Kit v1 for knowledge preservation. Current v2 skill, flow, safety, runtime, and path contracts override any legacy activation/tool/agent/workflow instructions below. Supporting files are preserved only as on-demand reference assets; scripts are never auto-executed by the migration contract.

Source: `.agents/skills/frontend-architecture/` at `549ba3dc2eb1`.

---

# Frontend Architecture

> How to organize frontend code so it scales. Separation of concerns over file-type folders.
> Applies to React/Next and Vue. For directory layout, follow [app-builder](../app-builder/scaffolding.md). For visual design, see [frontend-design](../frontend-design/REFERENCE.md). For React/Next performance, see [nextjs-react-expert](../nextjs-react-expert/REFERENCE.md).

---

## 1. Separation of Concerns — the core rule

Split code into four layers by responsibility. A unit of code does ONE of these, not several:

| Layer | Holds | Lives in |
|-------|-------|----------|
| **UI** | Rendering, markup, presentational state | `components/` |
| **Logic** | State, effects, data transforms, reusable UI logic | `hooks/` (React) · `composables/` (Vue) |
| **Data** | API calls, fetch/axios, cache keys | `lib/` / service files (`*.api.ts`) |
| **Type** | TypeScript types, domain models | `types.ts` / `*.types.ts` |
| **Validation** | Form/data schemas | `*.schema.ts` (zod/yup/valibot) |

> **Directory layout** (top-level folders) follows the project's scaffolding skill — do not invent a competing structure here. This skill is about *which layer code belongs to*, not where the folders sit.

---

## 2. File Responsibility & Size

One clear responsibility per file. Size is a **signal, not a hard limit** — a clear 230-line file beats a 90-line file that fetches, validates, renders, and juggles modals + toasts.

| File type | Comfortable range |
|-----------|-------------------|
| UI component | 80–180 lines |
| Page / screen | 100–220 lines |
| Hook / composable | 40–150 lines |
| API service | 50–200 lines |
| Type / schema | flexible |

Split a file when it mixes UI + API + business logic + validation + state. Don't split a coherent file just to hit a number.

---

## 3. Components render UI; logic goes elsewhere

Components should primarily render. Push fetching/state/transforms into a hook or composable.

```tsx
// ❌ Component owns the data layer
function ProductList() {
  const [products, setProducts] = useState([])
  useEffect(() => { fetch('/api/products').then(r => r.json()).then(setProducts) }, [])
  return <div>{/* render */}</div>
}

// ✅ Component renders; logic lives in a hook
function ProductList() {
  const { products, isLoading } = useProducts()
  if (isLoading) return <Loading />
  return <div>{/* render */}</div>
}
```

- Custom hooks must start with `use`.
- A component calling an API directly is acceptable only for the smallest one-off cases.

---

## 4. Next.js — Server Components by default

In the App Router, `page.tsx` and `layout.tsx` are Server Components. Reach for `"use client"` only when you actually need the client.

| Server Component | Client Component |
|------------------|------------------|
| Fetch data, read DB/API | Form, modal, dropdown |
| Handle secret tokens | Event handlers, animation |
| Render static/semi-static layout | `useState`/`useEffect`, browser APIs (`window`, `localStorage`) |

Keep client components small. Don't `"use client"` a whole page for one interactive button — extract the button into its own client component and keep the page a Server Component.

---

## 5. Vue — Composition API + composables

For full production apps, prefer the Composition API with `<script setup>` Single File Components. (Options API is fine for simple cases / progressive enhancement.)

- `components/` → UI
- `composables/` → reusable pure logic (`useX`)
- service files → API calls

Use a composable for reusable pure logic; use a component when reusing both logic and layout.

---

## 6. State — start local, escalate only when needed

| Need | Use |
|------|-----|
| Component-internal state | `useState` / `ref` |
| Reusable state/logic in one feature | custom hook / composable |
| Shared UI state in a subtree | Context (React) / `provide`-`inject` (Vue) |
| Cross-app, complex, persisted | Zustand / Pinia / Redux |
| Server state / API cache | TanStack Query (react-query) / similar |

Don't reach for global state (or Redux) on day one of a small app. Server state belongs in a query library, not a global store.

---

## 7. API in service files

Never scatter raw `fetch`/`axios` across components.

```ts
// user.api.ts
export async function getUsers() {
  const res = await http.get('/users')
  return res.data
}

// useUsers.ts
export function useUsers() {
  return useQuery({ queryKey: ['users'], queryFn: getUsers })
}
```

Always handle loading, error, and empty states explicitly.

---

## 8. Forms validate against a schema

Don't inline long validation inside a component.

- React/Next: react-hook-form + zod (or yup)
- Vue: vee-validate + zod/yup

Keep schemas in `*.schema.ts` next to the form they validate.

---

## 9. Naming

Descriptive, not cryptic. Context from the folder is allowed, but lean explicit.

| Prefer | Avoid |
|--------|-------|
| `UserProfileCard.tsx` | `Card.tsx` |
| `useCreateBooking.ts` | `handle.ts` |
| `booking.api.ts` | `api.ts` (bare) |
| `booking.schema.ts` | `data.ts` |

---

## 10. Props

Type props explicitly. When a component takes many related fields, pass the object, not a scatter of primitives.

```tsx
// ✅
type ProductCardProps = { product: Product; onSelect?: (p: Product) => void }

// ❌ seven loose props
<ProductCard id={id} name={name} price={price} image={image} discount={discount} stock={stock} />
```

---

## 11. Anti "god component"

Split a component when it shows these tells:

- longer than ~200 lines
- more than ~3 `useEffect`/`watch`
- many `useState`/`ref`
- renders UI **and** fetches API
- many `if/else` business branches
- multiple modals/tables/forms in one file

Decompose along the page seams:

```
Page
 ├─ Header
 ├─ Filter
 ├─ Table / List
 ├─ Pagination
 └─ Modal / Form
```

---

## 12. Tailwind class hygiene

- If a `className` runs past ~5–8 logical groups, extract a component.
- Repeated patterns → a reusable component or variant helper.
- No complex conditional logic inline in `className` — use `cn()`.

```tsx
// ✅
const cardClassName = cn(
  'rounded-xl border p-4',
  isActive && 'bg-blue-500 text-white',
  isError && 'border-red-500',
)
```

---

## 13. TypeScript

- Enable `strict: true`.
- Avoid `any`.
- Type props, API responses, and domain models explicitly.
- Prefer union types over enums when a union suffices.
- Validate external data with schemas (zod) — types alone don't guard runtime input.

---

## 14. Minimum testing

Don't test everything up front; do cover:

- utilities → unit tests
- important hooks/composables → unit tests
- main forms → validation tests
- critical flows → e2e

Colocate (`useBooking.test.ts` next to `useBooking.ts`) or keep `tests/unit` + `tests/e2e` — pick one and stay consistent.

---

## 15. Accessibility floor

- Use `<button>` for actions, not `<div onClick>`.
- Every input has a label; every image has `alt`.
- Modals support keyboard escape + focus trap.
- Forms surface errors clearly.

---

> **Remember:** one file = one responsibility · UI doesn't own logic · logic → hook/composable · API → service · validation → schema · types separate · Next is server-first · Vue is composable-first. Directory structure comes from the scaffolding skill, not from here.
