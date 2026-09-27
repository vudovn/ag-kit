---
name: cli-tool
description: Node.js CLI tool template principles. Commander.js, interactive prompts.
---

# CLI Tool Template

> Versions reflect the latest stable line verified 2026-05. Pin to the current stable when scaffolding.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Node.js 24 (Krypton LTS) |
| Language | TypeScript (ESM) |
| CLI Framework | Commander.js (v15, needs Node ≥22.12) |
| Prompts | @inquirer/prompts (modular) |
| Output | chalk + ora |
| Config | cosmiconfig |

---

## Directory Structure

```
project-name/
├── src/
│   ├── index.ts         # Entry: #!/usr/bin/env node shebang, wires Commander
│   ├── commands/        # One file per command (factory functions)
│   ├── lib/             # Core logic (framework-agnostic, testable)
│   ├── utils/           # logger (chalk/ora), prompt wrappers
│   └── config.ts        # cosmiconfig loader
├── dist/                # Build output (tsup/tsc)
└── package.json         # "type":"module", "bin":{...}
```

---

## CLI Design Principles

| Principle | Description |
|-----------|-------------|
| Subcommands | Group related actions |
| Options | Flags with defaults |
| Interactive | Prompts when needed |
| Non-interactive | Support --yes flags |

---

## Key Components

| Component | Purpose |
|-----------|---------|
| Commander | Command parsing (use a local `new Command()` for testability) |
| @inquirer/prompts | Modular interactive prompts (`input`, `select`, `confirm`) |
| Chalk | Colored output |
| Ora | Spinners/loading |
| Cosmiconfig | Config file discovery |

---

## Setup Steps

1. Create project directory
2. `npm init -y` then set `"type": "module"`
3. Install deps: `npm install commander @inquirer/prompts chalk ora cosmiconfig`
4. Point `bin` at compiled `./dist/index.js`, keep `#!/usr/bin/env node` shebang
5. `npm link` for local testing

---

## Publishing

```bash
npm login
npm publish
```

---

## Best Practices

- Keep `src/index.ts` thin; attach commands via `.addCommand()` factories in `src/commands/`
- Put business logic in `lib/`/`utils/` so commands stay testable wrappers
- ESM by default; build with tsup/esbuild
- Support both interactive and non-interactive (`--yes`) modes
- Validate inputs with Zod; exit with proper codes (0 success, 1 error)
- Alternatives worth knowing: @clack/prompts (polished prompts), citty (lightweight ESM command framework)
