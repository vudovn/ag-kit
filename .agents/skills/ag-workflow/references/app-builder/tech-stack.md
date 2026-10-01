# Tech Stack Selection (2026)

> Default and alternative technology choices for web applications.

## Default Stack (Web App - 2026)

```yaml
Frontend:
  framework: Next.js 16 (Stable)
  language: TypeScript 5.7+
  styling: Tailwind CSS v4
  state: React 19 Actions / Server Components
  caching: Next.js 16 Cache Components (Stable)
  bundler: Turbopack (Stable for Dev & Build)

Backend:
  runtime: Node.js 24 (Krypton LTS)
  framework: Next.js API Routes / Hono (for Edge)
  validation: Zod / TypeBox

Database:
  primary: PostgreSQL
  orm: Prisma / Drizzle
  hosting: Supabase / Neon

Auth:
  provider: Auth.js (v5) / Clerk

Monorepo:
  tool: Turborepo 2.0
```

## Alternative Options

| Need | Default | Alternative |
|------|---------|-------------|
| Real-time | Supabase Realtime | Socket.io, Ably |
| File storage | Supabase Storage | Cloudinary, AWS S3 |
| Payment | Stripe | LemonSqueezy, Paddle |
| Email | Resend | SendGrid, Postmark |
| Search | Algolia | Typesense, Orama |
| AI / LLM SDK | Vercel AI SDK (`ai` + `@ai-sdk/*`) | LangChain.js, direct REST API |
| Vector Database | PostgreSQL (pgvector via Supabase / Neon) | Pinecone, Qdrant |
| ORM (SQL-first) | Prisma ORM | Drizzle ORM (`drizzle-orm` + `drizzle-kit`) |

---

## AI Application Pattern (2026 Standard)

When building an AI or LLM-powered application:
- **Streaming**: Use Vercel AI SDK `streamText` / `streamUI` in Route Handlers or Server Actions.
- **UI State**: Leverage `useChat` / `useCompletion` with React 19 optimistic updates.
- **Embeddings & Vector**: Store vectors in PostgreSQL using `pgvector` extension; query via cosine similarity.
- **Safety & Rate Limits**: Protect AI endpoints with rate limiting (`@[skills/api-patterns/rate-limiting]`) and Zod schema parsing.

