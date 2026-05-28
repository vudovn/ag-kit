# AG-Kit CLI

CLI tool to install [Antigravity Kit](https://github.com/vudovn/ag-kit) - AI Agent templates with Skills, Agents, and Workflows.

## Installation

```bash
npx @vudovn/ag-kit init
```

Or install globally:

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

## Commands

| Command | Description |
|---------|-------------|
| `ag-kit init` | Install `.agents` folder into your project |
| `ag-kit update` | Update to the latest version |
| `ag-kit status` | Check installation status |

## Options

```bash
ag-kit init --force        # Overwrite existing .agents folder
ag-kit init --path ./myapp # Install in specific directory
ag-kit init --branch dev   # Use specific branch
ag-kit init --quiet        # Suppress output (for CI/CD)
ag-kit init --dry-run      # Preview actions without executing
```

## What it does

Downloads and installs the `.agents` folder from [ag-kit](https://github.com/vudovn/ag-kit) containing:
- **20 Specialist Agents** - Role-based AI personas
- **45 Skills** - Domain-specific knowledge modules
- **13 Workflows** - Slash command procedures

## License

MIT
