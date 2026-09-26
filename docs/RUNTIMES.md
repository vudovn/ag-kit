# Runtime support

AG Kit v2 uses honest capability tiers instead of pretending every AI coding runtime has the same extension model.

## First-class
Antigravity, Claude Code, Codex, Gemini CLI, Qwen Code, and Kimi Code. These runtimes receive native or near-native skills plus project instructions and MCP where verified. Antigravity, Qwen, and Kimi also receive project agents; richer hooks/plugins are only enabled where the upstream runtime supports them.

## Connected
Cursor, Windsurf, and GitHub Copilot. AG Kit provides portable instructions and MCP integration without inventing native skill/agent surfaces.

## Bridge
OpenCode, OpenClaw, and Aider. OpenCode/OpenClaw get portable instructions and access to the shared brain where their MCP setup permits it. Aider gets a read-only conventions projection because it has no native MCP client.

Run:

```bash
ag-kit runtime list
ag-kit runtime install antigravity
ag-kit runtime install qwen
ag-kit runtime install kimi
```

The installer only edits project-scoped files automatically. User-global MCP registries are never silently mutated.
