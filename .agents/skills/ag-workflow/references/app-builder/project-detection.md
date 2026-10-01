# Project Type Detection

> Analyze user requests to determine project type and template.

## Keyword Matrix

| Keywords | Project Type | Template |
|----------|--------------|----------|
| blog, post, article | Blog | astro-static |
| e-commerce, product, cart, payment | E-commerce | nextjs-saas |
| dashboard, panel, management | Admin Dashboard | nextjs-fullstack |
| ai, chat, bot, llm, rag, agent app | AI / Chatbot App | nextjs-fullstack (AI SDK / Streaming) |
| game, 2d, 3d, canvas, phaser, godot | Game Application | game-development skill (via `game-developer`) |
| api, backend, service, rest | API Service | express-api |
| python, fastapi, django | Python API | python-fastapi |
| mobile, android, ios, react native | Mobile App (RN) | react-native-app |
| flutter, dart | Mobile App (Flutter) | flutter-app |
| portfolio, personal, cv | Portfolio | nextjs-static |
| crm, customer, sales | CRM | nextjs-fullstack |
| saas, subscription, stripe | SaaS | nextjs-saas |
| landing, promotional, marketing | Landing Page | nextjs-static |
| docs, documentation | Documentation | astro-static |
| extension, plugin, chrome | Browser Extension | chrome-extension |
| desktop, electron | Desktop App | electron-desktop |
| cli, command line, terminal | CLI Tool | cli-tool |
| monorepo, workspace | Monorepo | monorepo-turborepo |


## Detection Process

```
1. Tokenize user request
2. Extract keywords
3. Determine project type
4. Detect missing information → forward to project-planner / orchestrator
5. Suggest tech stack
```

## Conflict Resolution

When a request matches multiple keywords (e.g. "a CLI to manage my e-commerce products" matches both `cli` and `e-commerce`), resolve in this order:

| Priority | Rule | Example |
|----------|------|---------|
| 1 | **Platform wins over domain.** A concrete platform (mobile / desktop / cli / extension) outranks a web/business domain (e-commerce, crm, blog). | "CLI to manage e-commerce" → **cli-tool** (e-commerce is the data domain, not the deliverable) |
| 2 | **Head noun wins.** The keyword describing what is being built (grammatical subject) outranks modifiers. | "a **dashboard** for my Shopify store" → **nextjs-fullstack** (dashboard is the thing; Shopify is context) |
| 3 | **Still ambiguous → ask.** If no rule breaks the tie, do NOT guess. Surface the options through the Socratic Gate (Phase 0) and let the user choose. | "an app for my shop" → ask: web, mobile, or desktop? |

