# Runtime support

AG Kit v2 uses capability tiers instead of pretending every AI coding runtime has the same extension model. `shared/` is canonical; each target has a thin adapter under `runtimes/<runtime>/`.

No runtime is the product's primary runtime.

## First-class

Antigravity, Claude, Codex, Gemini, Qwen, Kimi, and Cline.

These targets receive native or near-native instructions/skills and MCP where verified. Agents, hooks, plugins, and other richer surfaces are enabled only when both the host and the AG Kit adapter support them.

## Connected

Cursor, Windsurf, and GitHub Copilot.

AG Kit provides verified portable instructions and/or MCP integration without inventing native skill/agent surfaces that the host does not expose.

## Bridge

OpenCode, OpenClaw, Aider, Wayland, Hermes, and Pi.

Bridge targets receive the narrowest safe integration AG Kit can verify: portable instructions, staged MCP configuration, or runtime-managed integration notes. User-global registries are never silently mutated.

## Commands

Inspect the matrix and current project state:

```bash
ag-kit runtime list
ag-kit runtime detect
ag-kit runtime doctor
```

Install detected runtimes:

```bash
ag-kit runtime install-present
```

Install or remove one target explicitly:

```bash
ag-kit runtime install claude
ag-kit runtime install codex
ag-kit runtime uninstall claude
```

## Capability contract

The machine-readable source is [`../platform-capabilities.json`](../platform-capabilities.json). Each entry points to an adapter contract such as `runtimes/claude/adapter.json`.

Repository validation uses generic commands:

```bash
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
```

Adapter-specific checks and packaging stay inside the adapter boundary. Root-level scripts and CI gates remain runtime-neutral.

## Lifecycle guarantees

- project-scoped writes are preferred;
- pre-install state is backed up where needed;
- ownership manifests track AG Kit-managed state;
- doctor distinguishes live / standing-by / degraded / untouched state;
- uninstall preserves user drift and project memory;
- filesystem root and user home are rejected as project targets;
- global-only configuration is staged for explicit activation.

For exact capability flags and tier membership, use `platform-capabilities.json` rather than assuming parity from this prose summary.
