# AG Kit MCP bridge

AG Kit exposes a deliberately small project-local MCP surface so thin runtimes can share the same memory and operating state without pretending to have native skill/agent support.

Run:

```bash
ag-kit mcp serve
```

The server uses stdio and fixes its project root to `AG_KIT_PROJECT` or the process working directory. Tools never accept arbitrary filesystem roots.

Tools:
- `ag_memory_recall`
- `ag_memory_status`
- `ag_memory_add`
- `ag_team_init`
- `ag_runtime_status`
- `ag_cross_audit_probe`

This bridge is connective tissue, not a second framework API. New behavior should normally be a shared skill or engine capability, not another MCP tool.
