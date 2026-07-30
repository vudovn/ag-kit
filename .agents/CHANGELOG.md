# AG Kit Toolkit Changelog

## Unreleased

### Changed

- Updated the `mcp-builder` skill for the stable MCP `2026-07-28` specification: stateless per-request metadata, `server/discover`, explicit state handles, extension negotiation, JSON Schema 2020-12, compatibility behavior, and migration guidance for deprecated features.
- Clearly separated stable core features from opt-in Tasks, Skills over MCP, and MCP Apps extensions.
- Reworked the orchestrator and `parallel-agents` guidance around Antigravity-native agents and tasks while retaining best-effort portability for other runtimes.
- Removed Claude-specific built-in agent and model-tier assumptions from managed orchestration instructions; runtime capabilities must now be discovered before delegation.

### Security

- Added required safeguards for external `$ref` resolution, schema-validation resource limits, untrusted tool annotations, explicit consent, least privilege, secret handling, and execution isolation.
- Added explicit trust boundaries for repository content, MCP responses, tool annotations, web content, logs, and subagent outputs.
- Added finite agent, delegation-depth, turn/retry, timeout, cancellation, and no-progress controls to prevent recursive delegation and indefinite ReAct loops.
- Parallel writers now require isolated worktrees, sandboxes, branches, or non-overlapping path grants, followed by coordinator-owned integration and repository-wide verification.

## 2026.7.26

### Added

- Antigravity runtime contract with six production integration phases.
- Native `PreToolUse` hook and destructive-command policy.
- Antigravity Doctor, MCP synchronization helper, plugin builder, schemas, and regression tests.
- Complete migration, production checklist, security, and operator documentation.

### Changed

- Toolkit version advanced from `2026.7.18` to `2026.7.26`.
- Google Antigravity is the primary production runtime; other Markdown-compatible tools are best-effort consumers.
- Component manifest now records Antigravity runtime metadata.
- Integrity lock now covers `antigravity.json`, `hooks.json`, and the complete `hooks/` runtime-tooling tree.
- Self-validation and Antigravity Doctor enforce synchronized root, CLI, web, and toolkit versions.

### Security

- High-confidence root/disk destructive commands are blocked before tool execution.
- Invalid or unknown hook payloads fail open with a warning to avoid runtime-wide lockout.
- MCP writes remain explicit, placeholder-blocked, conflict-aware, and backup-protected.
- Plugin artifacts are reviewable and contain no home-directory configuration or environment secrets.

### Compatibility

- Existing agent, skill, workflow, rule, and memory names remain compatible.
- The native safety hook is enabled by default and can be temporarily disabled for compatibility diagnosis.
- Plugin installation is optional; repository `.agents/` remains the project source of truth.

## 2026.7.18

### Added

- Strict SemVer metadata for all 20 agents, 47 skills, 13 workflows, and 6 rules.
- Machine-readable `manifest.json` with agent-to-skill and workflow dependencies.
- Deterministic `manifest.lock.json` with SHA-256 integrity hashes.
- Generated `DEPENDENCY_GRAPH.md` for workflow → agent → skill orchestration.
- JSON schemas for component metadata, manifest, lock, and memory topics.
- Standard memory topic files for user preferences, technical decisions, and feedback history.
- Registry and graph generation scripts with non-mutating `--check` modes.

### Changed

- Toolkit version advanced from `2026.7.12` to `2026.7.18`.
- Self-validation now checks component versions, workflow references, dependency compatibility, registry drift, lock integrity, graph drift, and memory contracts.
- CI now treats generated registry files as release artifacts that must remain synchronized.

### Compatibility

- Official runtime support remained Gemini CLI and Google Antigravity for that release.
- The component metadata and dependency format remain portable and avoid unnecessary platform coupling.

## 2026.7.12

- Release-safety upgrade, non-destructive CLI updates, rollback support, CI, dependency review, and hardened publishing.
