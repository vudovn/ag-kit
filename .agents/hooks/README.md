# AG Kit Antigravity Hooks

This directory contains the native Antigravity integration hooks used by the generated v2 `.agents/` projection.

Hooks are **runtime boundaries**, not a replacement for Antigravity permissions, workspace trust, operating-system isolation, or human review.

## `validate-tool-call.mjs` — PreToolUse safety gate

Registered for command execution through `.agents/hooks.json`.

The gate is deliberately narrow. It blocks only high-confidence destructive root/disk patterns such as:

- recursive deletion of a Unix filesystem root;
- filesystem-format commands;
- raw disk overwrite with `dd`;
- Windows drive format;
- recursive forced deletion of a Windows drive root.

Normal project cleanup such as deleting `dist/` or `node_modules/` remains allowed.

Input is JSON on stdin and is capped at 1 MiB. The hook returns Antigravity decision JSON:

- destructive recognized command → `deny`;
- ordinary recognized command → `allow`;
- invalid/oversized payload → `force_ask`;
- payload without a recognized command field → `allow` with a compatibility reason.

Direct-run detection resolves the entrypoint with `realpath` + file-URL conversion so npm/symlink and Windows path differences cannot silently skip the hook body.

Mock the hook; never execute a destructive command for testing:

```bash
printf '%s' '{"toolCall":{"name":"run_command","args":{"CommandLine":"rm -rf /"}}}' \
  | node .agents/hooks/validate-tool-call.mjs
```

## `observe-tool-use.mjs` — PostToolUse observability

This hook records bounded project-local metadata and must never become a dependency of the agent loop.

It may record:

- sanitized tool name;
- success/error class;
- runtime/session identifier;
- timestamp and bounded local receipt metadata.

It must **not** record:

- prompts or conversation bodies;
- command arguments;
- file contents;
- secrets or environment values;
- user-home configuration.

The hook is fail-open and always returns `{}` to Antigravity.

## Validation

From the repository root:

```bash
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

`test:antigravity` includes direct process execution and symlink-entry regression coverage for the safety hook.

Reusable behavior still belongs in `shared/`; this directory is part of the native Antigravity projection/runtime integration, not a second canonical toolkit.
