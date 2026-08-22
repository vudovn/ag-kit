# AG Kit — Antigravity Native Integration

AG Kit now treats Google Antigravity as its primary runtime. The integration is intentionally built from Antigravity's workspace-native conventions instead of a cross-runtime abstraction.

## What is active

| Phase | Native surface | AG Kit implementation |
| --- | --- | --- |
| 1. Discovery | `.agents/rules/`, `.agents/skills/`, `.agents/workflows/` | Doctor validates discovery paths and required frontmatter |
| 2. MCP | `.agents/mcp_config.json` | Workspace validation plus explicit, backup-aware sync helper |
| 3. Hooks | `.agents/hooks.json` | `PreToolUse` gate for clearly destructive `run_command` calls |
| 4. Orchestration | workflows, specialist definitions, Antigravity subagents | Validates `/coordinate`, `/orchestrate`, core roles, and routing skills |
| 5. Plugin | Antigravity CLI plugin import | Deterministic local plugin bundle builder |
| 6. Validation | CI and smoke tests | Doctor, hook regression tests, MCP tests, and plugin build tests |

## Quick verification

```bash
node .agents/hooks/antigravity-doctor.mjs
node --test .agents/hooks/tests/antigravity.test.mjs
```

The doctor checks the installed workspace without changing files. Use `--json` for machine-readable output and `--strict` to treat unresolved configuration placeholders as failures.

## Native safety hook

Antigravity reads `.agents/hooks.json`. AG Kit registers one native hook:

```json
{
  "enabled": true,
  "PreToolUse": [
    {
      "matcher": "run_command",
      "command": "node .agents/hooks/validate-tool-call.mjs",
      "timeout": 10
    }
  ]
}
```

The policy blocks only high-confidence destructive operations such as deleting a filesystem root, formatting a drive, or overwriting a raw disk. It deliberately allows normal cleanup such as deleting `dist/` or `node_modules/`.

The hook is not a sandbox and does not replace Antigravity's permission settings. Invalid or unknown payload shapes fail open with a warning to prevent a runtime-wide lockout after upstream payload changes.

## MCP setup

Antigravity CLI supports workspace MCP configuration at `.agents/mcp_config.json`. Antigravity IDE and the wider suite may also use a shared global configuration.

Inspect the merge plan:

```bash
node .agents/hooks/sync-mcp.mjs --check
node .agents/hooks/sync-mcp.mjs --print
```

Apply only after replacing placeholders such as `YOUR_API_KEY`:

```bash
node .agents/hooks/sync-mcp.mjs --apply --target suite
node .agents/hooks/sync-mcp.mjs --apply --target cli
```

Use `--server` to review or apply one named server without selecting unrelated placeholder entries. Repeat the flag to select more than one server:

```bash
node .agents/hooks/sync-mcp.mjs --print --server xquik
node .agents/hooks/sync-mcp.mjs --apply --target suite --server xquik
```

The helper never overwrites an existing server with the same name unless `--force` is supplied. It creates a timestamped backup before writing.

## Orchestration

AG Kit uses the existing Antigravity-native workflows:

- `/coordinate` for parallel read/research and synthesis;
- `/orchestrate` for plan approval followed by specialist implementation;
- `.agents/agent/*.md` as role definitions;
- `coordinator-mode`, `parallel-agents`, `intelligent-routing`, and `verify-changes` as orchestration skills.

Antigravity's `/agents` and `/tasks` views remain the runtime source of truth for active work. AG Kit does not create a second scheduler.

## Build a plugin bundle

```bash
node .agents/hooks/build-plugin.mjs
# or
npm run build:antigravity-plugin
```

The generated `dist/antigravity-plugin/` contains:

- a `gemini-extension.json` compatible manifest used by Antigravity CLI's plugin importer;
- packaged skills and specialist definitions;
- workflows converted into namespaced command TOML files;
- rules, native hooks, and an MCP example;
- `PLUGIN_CONTENTS.json` with deterministic SHA-256 inventory data.

Install the local build after reviewing it:

```bash
agy plugin install ./dist/antigravity-plugin
agy plugin list
```

## Security boundaries

- No MCP configuration is copied to the home directory without explicit `--apply`.
- Placeholder credentials block any selected MCP set that contains them.
- The plugin builder does not include secrets from environment variables or home-directory configuration.
- The hook only reads one tool payload from stdin and performs no network calls.
- AG Kit does not weaken Antigravity permission prompts or workspace trust controls.

## Release and operations

- [Root README](../../README.md) — installation and production quick start.
- [Migration guide](../../MIGRATION.md) — upgrade and rollback from earlier AG Kit versions.
- [Production checklist](../../PRODUCTION_CHECKLIST.md) — automated and hands-on release gates.
- [Security policy](../../SECURITY.md) — threat model, incident handling, and hook recovery.

## Primary Antigravity references

- Workspace rules and workflows: <https://codelabs.developers.google.com/antigravity-ide>
- Workspace skills: <https://codelabs.developers.google.com/antigravity-skills>
- Workspace MCP: <https://codelabs.developers.google.com/antigravity-cli>
- Native `PreToolUse` hooks: <https://codelabs.developers.google.com/secure-agentic-coding>
- Plugin installation: <https://codelabs.developers.google.com/antigravity-cli-plugins> and <https://codelabs.developers.google.com/antigravity-conductor>
