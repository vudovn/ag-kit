---
ag_kit_version: 2026.8.31
schema: 1
primary_runtime: antigravity
source_of_truth: .agents
---

# AG Kit — Agent Runtime Contract

AG Kit is a local-first agent engineering layer. The canonical source lives in `.agents/`; platform adapters may project that source into runtime-specific formats, but they must not become independent forks of the rules or skills.

## Runtime priorities

1. **Antigravity is first-class.** Prefer native Antigravity skills, custom subagents, hooks, rules, MCP, plugins, permissions, sandboxing, and task primitives.
2. **Shared behavior comes before adapters.** Put reusable knowledge in `.agents/skills`, `.agents/rules`, `.agents/memory`, and portable scripts. Platform-specific files should be thin adapters.
3. **Capability claims must be verifiable.** `platform-capabilities.json` is the machine-readable support matrix. Do not mark a surface active until its files and checks exist.
4. **Plan before destructive changes.** Respect user review gates, native permissions, sandboxing, and repository safety hooks. Never weaken a native security boundary to make automation easier.
5. **Evidence over completion claims.** Run the relevant validation commands and report what actually passed, failed, or was unavailable.

## Antigravity discovery

The production workspace uses these native locations:

- Rules: `.agents/rules/*.md`
- Skills: `.agents/skills/<skill>/SKILL.md`
- Custom subagents: `.agents/agents/*.md` or `.agents/agents/<name>/agent.md`
- Hooks: `.agents/hooks.json`
- MCP: `.agents/mcp_config.json`
- Workspace plugins: `.agents/plugins/<plugin>/plugin.json`

Legacy compatibility files may exist during migrations, but new work should target the native locations above.

## Working protocol

Before implementation:

1. Read `.agents/rules/core-protocol.md`.
2. Inspect `platform-capabilities.json` and `.agents/antigravity.json` when runtime behavior is involved.
3. Load only the skills relevant to the task.
4. For complex work, define a plan with explicit verification before editing.

After implementation:

```bash
npm run check:agents
npm run test:toolkit
npm run check:antigravity
npm run test:antigravity
npm run check:platforms
```

Run web/CLI checks as needed for files touched by the change.

## Portability rule

Platform adapters may translate file locations, hook payloads, command syntax, or MCP configuration schemas. They must preserve the same underlying AG Kit intent and must not silently invent capabilities that the target runtime does not support.
