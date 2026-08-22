# AG Kit toolkit operator guide

AG Kit is a modular `.agents/` toolkit for Google Antigravity. It routes software-engineering work to specialist roles, progressively loads focused skills, preserves durable project context, and verifies changes with executable checks.

## Runtime contract

Antigravity is the primary production runtime. The machine-readable contract is `.agents/antigravity.json` and covers six phases:

1. rules, skills, and workflow discovery;
2. MCP configuration and explicit synchronization;
3. native lifecycle hooks and command safety;
4. agent/subagent orchestration;
5. optional plugin packaging;
6. validation and production smoke testing.

See [hooks/README.md](hooks/README.md) for the implementation and security boundaries.

## Quick start

From the project root:

```bash
npm run check:agents
npm run check:antigravity
npm run test:antigravity
```

Open the repository as a trusted Antigravity workspace. The runtime should discover:

- `rules/*.md` as workspace constraints;
- `skills/*/SKILL.md` as progressively loaded domain context;
- `workflows/*.md` as slash commands;
- `agent/*.md` as specialist role definitions;
- `memory/` as durable project context.

Use `/coordinate` for separable parallel research/review work and `/orchestrate` for plan approval followed by specialist implementation. Antigravity `/agents` and `/tasks` remain the runtime source of truth.

## Native safety hook

`.agents/hooks.json` registers a `PreToolUse` gate for `run_command`. The policy blocks only high-confidence root/disk destructive patterns. It does not replace Antigravity permissions, workspace trust, sandboxing, or user approval.

Test with mocked stdin only:

```bash
printf '%s' '{"tool_args":{"CommandLine":"rm -rf /"}}' \
  | node .agents/hooks/validate-tool-call.mjs
```

The process must exit non-zero. To diagnose a compatibility issue, set `"enabled": false` temporarily and reopen the workspace.

## MCP setup

`mcp_config.json` is a workspace example. Replace `YOUR_API_KEY` before enabling the server and keep real credentials outside version control.

```bash
node .agents/hooks/sync-mcp.mjs --check
node .agents/hooks/sync-mcp.mjs --print
```

Select a ready entry without applying unrelated placeholder examples:

```bash
node .agents/hooks/sync-mcp.mjs --print --server xquik
node .agents/hooks/sync-mcp.mjs --apply --target suite --server xquik
```

No home-directory file is changed without `--apply`. Existing server names are preserved unless `--force` is explicit, and an existing target is backed up before writing.

## Plugin bundle

```bash
npm run build:antigravity-plugin
```

Review `dist/antigravity-plugin/` and its `PLUGIN_CONTENTS.json` inventory before optional local installation. The repository `.agents/` directory remains the source of truth.

## Core concepts

- **Agents** define role, boundaries, tools, and skill dependencies.
- **Skills** contain selectively loaded domain knowledge and optional executable scripts.
- **Rules** define workspace-wide precedence, safety, and routing behavior.
- **Workflows** provide reusable slash-command procedures.
- **Memory** stores durable project conventions, preferences, decisions, and feedback.
- **Hooks** supplement runtime permissions with narrow policy checks.
- **Runtime scripts** turn guidance into repeatable evidence.
- **Manifest and lock** make managed components and runtime tooling reproducible.

## Validation

Validate a target project:

```bash
python .agents/scripts/checklist.py .
```

Run full project verification when a preview URL exists:

```bash
python .agents/scripts/verify_all.py . --url http://localhost:3000
```

Verify AG Kit itself after editing agents, skills, rules, workflows, memory, runtime tooling, schemas, scripts, or links:

```bash
npm run generate:agents
npm run check:agents
npm run check:antigravity
npm run test:antigravity
```

## Documentation

- [Architecture and inventory](ARCHITECTURE.md)
- [Antigravity integration](hooks/README.md)
- [Dependency graph](DEPENDENCY_GRAPH.md)
- [Runtime scripts](scripts/README.md)
- [Root migration guide](../MIGRATION.md)
- [Production checklist](../PRODUCTION_CHECKLIST.md)
- [Security policy](../SECURITY.md)
- [Change history](../CHANGELOG.md)
- [Quick routing reference](rules/quick-reference.md)
