<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG Kit Web</h1>

<p align="center">
  Next.js documentation and product portal for the AG Kit v2 lean multi-runtime operating layer.
</p>

---

## Local development

The `web/` package uses Next.js 16, React 19, Tailwind CSS v4, and MDX.

```bash
npm ci
npm run dev
```

Open <http://localhost:3000> for local development.

Production checks:

```bash
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev --audit-level=high
```

`next build --webpack` is intentional for the current MDX configuration.

## Product model shown by the docs

The web site must describe the same v2 architecture that the repository validates:

| Surface | Current v2 contract |
| --- | --- |
| Resident core | 1 tiny always-on core |
| Skills | 18 top-level hot-loaded behavior skills |
| Permanent agents | 4 (`scout`, `architect`, `builder`, `reviewer`) |
| Development workflow | 1 gated spine with QUICK / STANDARD / DEEP modes |
| Runtime targets | 16 across first-class / connected / bridge tiers |
| Canonical source | `shared/` + capability-aware adapters under `runtimes/` |
| Memory | local Markdown canonical store with optional rebuildable SQLite/FTS5 index |
| Primary runtime | none |

Generated host trees are adapter projections, not product identity or canonical source. Runtime-specific hooks/plugins may be documented as capabilities of that adapter, but public copy must not present one host as AG Kit itself.

The CLI supports both explicit single-runtime installation and detected-runtime activation:

```bash
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

Legacy `ag-kit init/update/rollback/status` remains for safe managed-tree migration compatibility, not as the canonical v2 runtime architecture.

## Content integrity

Repository CI runs documentation-link and runtime-neutrality checks in addition to web lint/typecheck/build. When changing product counts, runtime support, Node requirements, or CLI commands, keep these sources aligned:

- root `README.md` / `README-VI.md`;
- `docs/ARCHITECTURE_V2.md` / `docs/RUNTIMES.md`;
- `MIGRATION.md`, `SECURITY.md`, and `PRODUCTION_CHECKLIST.md`;
- `cli/README.md`;
- web i18n dictionaries and landing dictionaries;
- this file.

Do not reintroduce the historical 20-agent / 45–47-skill / 13-workflow inventory or Antigravity-only product framing into current v2 documentation.

## Stack

- [Next.js 16](https://nextjs.org/) (App Router)
- [React 19](https://react.dev/)
- [Tailwind CSS v4](https://tailwindcss.com/)
- [@next/mdx](https://github.com/vercel/next.js/tree/canary/packages/next-mdx)
- [Base UI](https://base-ui.com/)
- Lucide React icons

## Links

- [Repository documentation](../README.md)
- [Runtime support](../docs/RUNTIMES.md)
- [Migration guide](../MIGRATION.md)
- [Security policy](../SECURITY.md)
- [Production checklist](../PRODUCTION_CHECKLIST.md)
- [Official documentation portal](https://ag-kit.unikorn.vn/docs)

## License

Released under the [MIT License](../LICENSE) © [Vudovn](https://github.com/vudovn).
