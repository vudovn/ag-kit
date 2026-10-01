---
name: astro-static
description: Astro static site template principles. Content-focused websites, blogs, documentation.
---

# Astro Static Site Template

> Versions reflect the latest stable line verified 2026-05. Pin to the current stable when scaffolding.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Astro 6.x |
| Content | MDX + Content Collections (Content Layer API) |
| Styling | Tailwind CSS v4 (@tailwindcss/vite) |
| Integrations | Sitemap, RSS, SEO |
| Output | Static/SSG |

---

## Directory Structure

```
project-name/
├── src/
│   ├── components/      # .astro components
│   ├── content/         # Collection entries (blog/, docs/ .md/.mdx)
│   ├── layouts/         # Page layouts
│   ├── pages/           # File-based routing (only reserved dir)
│   ├── styles/
│   │   └── global.css   # @import "tailwindcss";
│   └── content.config.ts # Collection definitions (Content Layer, in src/ root)
├── public/              # Static assets
├── astro.config.mjs
└── package.json
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Content Layer API | Collections defined in `src/content.config.ts` with `loader`s (glob/file) + Zod schemas |
| Islands Architecture | Partial hydration for interactivity |
| Zero JS by default | Static HTML unless needed |
| MDX Support | Markdown with components |

---

## Setup Steps

1. `npm create astro@latest {{name}}`
2. Add integrations: `npx astro add mdx sitemap`
3. Add Tailwind v4: `npx astro add tailwind` (installs @tailwindcss/vite, not the legacy @astrojs/tailwind)
4. Define collections in `src/content.config.ts` using `loader`s + Zod schemas
5. `npm run dev`

---

## Deployment

| Platform | Method |
|----------|--------|
| Vercel | Auto-detected |
| Netlify | Auto-detected |
| Cloudflare Pages | Auto-detected |
| GitHub Pages | Build + deploy action |

---

## Best Practices

- Use Content Collections for type safety
- Leverage static generation
- Add islands only where needed
- Optimize images with Astro Image
