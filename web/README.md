# AG Kit

> AI Agent templates with Skills, Agents, and Workflows

<div  align="center">
    <a href="https://unikorn.vn/p/ag-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/ag-kit?theme=dark" alt="AG Kit - Nổi bật trên Unikorn.vn" style="width: 210px; height: 54px;" width="210" height="54" /></a>
    <a href="https://unikorn.vn/p/ag-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/ag-kit/rank?theme=dark&type=daily" alt="AG Kit - Hàng ngày" style="width: 250px; height: 64px;" width="250" height="64" /></a>
    <a href="https://launch.j2team.dev/products/ag-kit" target="_blank"><img src="https://launch.j2team.dev/badge/ag-kit/dark" alt="AG Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

## Quick Install

```bash
npx @vudovn/ag-kit init
```

Or install globally:

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

This installs the `.agent` folder containing all templates into your project.

## Usage

### Using Agents

**No need to mention agents explicitly!** The system automatically detects and applies the right specialist(s):

```
You: "Add JWT authentication"
AI: 🤖 Applying @security-auditor + @backend-specialist...

You: "Fix the dark mode button"
AI: 🤖 Using @frontend-specialist...

You: "Login returns 500 error"
AI: 🤖 Using @debugger for systematic analysis...
```

**How it works:**

- Analyzes your request silently
- Detects domain(s) automatically (frontend, backend, security, etc.)
- Selects the best specialist(s)
- Informs you which expertise is being applied
- You get specialist-level responses without needing to know the system architecture

**Benefits:**

- ✅ Zero learning curve - just describe what you need
- ✅ Always get expert responses
- ✅ Transparent - shows which agent is being used
- ✅ Can still override by mentioning agent explicitly

### Using Workflows

Invoke workflows with slash commands:

| Command          | Description                           |
| ---------------- | ------------------------------------- |
| `/brainstorm`    | Explore options before implementation |
| `/create`        | Create new features or apps           |
| `/debug`         | Systematic debugging                  |
| `/deploy`        | Deploy application                    |
| `/enhance`       | Improve existing code                 |
| `/orchestrate`   | Multi-agent coordination              |
| `/plan`          | Create task breakdown                 |
| `/preview`       | Preview changes locally               |
| `/status`        | Check project status                  |
| `/test`          | Generate and run tests                |
| `/ui-ux-pro-max` | Design with 50 styles                 |

Example:

```
/brainstorm authentication system
/create landing page with hero section
/debug why login fails
```

### Using Skills

Skills are loaded automatically based on task context. The AI reads skill descriptions and applies relevant knowledge.

## CLI Tool

| Command         | Description                               |
| --------------- | ----------------------------------------- |
| `ag-kit init`   | Install `.agent` folder into your project |
| `ag-kit update` | Update to the latest version              |
| `ag-kit status` | Check installation status                 |

### Options

```bash
ag-kit init --force        # Overwrite existing .agent folder
ag-kit init --path ./myapp # Install in specific directory
ag-kit init --branch dev   # Use specific branch
ag-kit init --quiet        # Suppress output (for CI/CD)
ag-kit init --dry-run      # Preview actions without executing
```

## Documentation

- **[Web App Example](https://ag-kit.vercel.app//docs/guide/examples/web-app)** - Step-by-step guide to creating a web application
- **[Online Docs](https://ag-kit.vercel.app//docs)** - Browse all documentation online

## Buy me coffee

<p align="center">
  <a href="https://buymeacoffee.com/vudovn">
    <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" />
  </a>
</p>

<p align="center"> - or - </p>

<p align="center">
  <img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Buy me coffee" width="200" />
</p>

## License

MIT © Vudovn
