<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  Antigravity-first agent engineering kit with rules, skills, specialist agents, workflows, persistent memory, MCP guidance, orchestration, and a native safety hook.
</p>

<div align="center">
  <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="AG Kit on Unikorn.vn" width="210" height="54" /></a>
  <a href="https://trendshift.io/repositories/21490" target="_blank"><img src="https://trendshift.io/api/badge/repositories/21490" alt="AG Kit on Trendshift" width="250" height="55" /></a>
  <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="AG Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

<p align="center">
  <strong>Primary runtime: Google Antigravity</strong><br/>
  <a href="./README-VI.md">Tiếng Việt</a> · <a href="./MIGRATION.md">Migration guide</a> · <a href="./PRODUCTION_CHECKLIST.md">Production checklist</a> · <a href="./SECURITY.md">Security</a>
</p>

---

## Production profile

AG Kit installs a complete `.agents/` workspace contract. Antigravity is the supported production runtime for this release. Other tools may read the Markdown components, but runtime behavior outside Antigravity is not part of the production compatibility guarantee.

| Capability | Production implementation |
| --- | --- |
| Rules and skill discovery | `.agents/rules/`, `.agents/skills/`, `.agents/workflows/` |
| Specialist routing | 20 role definitions and intelligent-routing skills |
| Persistent context | `.agents/memory/` and context-compression guidance |
| Orchestration | `/coordinate`, `/orchestrate`, Antigravity `/agents` and `/tasks` |
| MCP | Workspace config plus explicit, backup-aware sync helper |
| Tool safety | Native `PreToolUse` gate for high-confidence destructive commands |
| Packaging | Local Antigravity plugin bundle with a SHA-256 content inventory |
| Validation | Toolkit CI, Antigravity Doctor, regression tests, Dependency Review, CLI and web checks |

The native hook is deliberately narrow. It blocks root-filesystem deletion, drive formatting, and raw-disk overwrite patterns while allowing normal project cleanup such as deleting `dist/` or `node_modules/`. It does not replace Antigravity permissions, workspace trust, sandboxing, or human approval.

## Requirements

- Node.js 22 or newer for repository-level Antigravity tooling.
- Python 3.10 or newer for AG Kit validators and utility scripts.
- A trusted Google Antigravity workspace.
- Git for safe update, review, and rollback workflows.

The published CLI currently supports Node.js 18 or newer; the Antigravity integration checks run on Node.js 22.

## Quick start

### Install into a project

```bash
npx @vudovn/ag-kit init
```

Or install the CLI globally:

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

Do not add `.agents/` to the project `.gitignore` when Antigravity needs to index rules, skills, or workflows. To keep it local without disabling discovery, add `.agents/` to `.git/info/exclude` instead.

### Verify the workspace

```bash
npm run check:agents
npm run check:antigravity
npm run test:antigravity
```

`check:antigravity` is read-only. The default MCP example contains `YOUR_API_KEY`, so the normal doctor reports a warning until the example is configured. Use strict mode only after all placeholders have been resolved:

```bash
node .agents/hooks/antigravity-doctor.mjs --strict
```

### Open in Antigravity

After opening the repository as a trusted workspace:

1. Confirm slash commands such as `/plan`, `/coordinate`, and `/orchestrate` are discovered.
2. Confirm relevant skills are selected from `.agents/skills/`.
3. Run a normal command such as `npm test` and confirm it is allowed.
4. Verify the safety hook with a mocked payload rather than executing a destructive command:

```bash
printf '%s' '{"tool_args":{"CommandLine":"rm -rf /"}}' \
  | node .agents/hooks/validate-tool-call.mjs
```

The command must exit non-zero and print `BLOCKED by AG Kit`.

## Safe updates and rollback

AG Kit updates are merge-aware. User-owned files and locally modified managed files are preserved by default.

```bash
ag-kit update --dry-run          # Preview the exact plan
ag-kit update                    # Merge safely and create a backup
ag-kit update --strategy replace # Explicit full replacement, still backed up
ag-kit rollback                  # Restore the newest pre-update backup
```

Update metadata is stored in `.agents/.ag-kit/`. Backups are stored in `.ag-kit-backups/` outside the managed toolkit tree. Read [MIGRATION.md](MIGRATION.md) before upgrading an existing installation to the Antigravity-native release.

## Antigravity-native integration

### Runtime contract

`.agents/antigravity.json` declares the six supported integration phases and the documented Antigravity CLI capabilities used by AG Kit. It avoids inventing a minimum semantic version when upstream documentation does not define one.

### Native safety hook

Antigravity loads `.agents/hooks.json`, which registers:

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

To temporarily disable the AG Kit hook while diagnosing a compatibility issue, set `"enabled": false`, reopen the workspace, and report the payload shape privately if it may contain sensitive data. Do not delete Antigravity's own permission controls.

### MCP configuration

Review the workspace MCP plan without writing to the home directory:

```bash
node .agents/hooks/sync-mcp.mjs --check
node .agents/hooks/sync-mcp.mjs --print
```

After replacing placeholders, explicitly apply to one supported target:

```bash
node .agents/hooks/sync-mcp.mjs --apply --target suite
node .agents/hooks/sync-mcp.mjs --apply --target cli
```

Existing servers with the same name are preserved unless `--force` is supplied. A timestamped backup is created before an existing target file is changed. Never commit real MCP credentials.

Select one ready server when another example still contains a placeholder:

```bash
node .agents/hooks/sync-mcp.mjs --print --server xquik
node .agents/hooks/sync-mcp.mjs --apply --target suite --server xquik
```

The Xquik entry uses remote OAuth discovery and supports the `deep-research` Skill's bounded public X evidence workflow.

### Build and inspect the plugin

```bash
npm run build:antigravity-plugin
```

Review `dist/antigravity-plugin/` before local installation. The bundle contains packaged skills, agents, rules, converted workflow commands, the native hook, an MCP example, and `PLUGIN_CONTENTS.json` with SHA-256 entries.

```bash
agy plugin install ./dist/antigravity-plugin
agy plugin list
```

Plugin installation is optional; the repository-native `.agents/` workspace remains the source of truth for project development.

## Included components

| Component | Count | Purpose |
| --- | ---: | --- |
| Agents | 20 | Domain specialist and orchestration role definitions |
| Skills | 48 | Progressive domain knowledge and executable validation helpers |
| Workflows | 13 | Repeatable slash-command procedures |
| Rules | 6 | Workspace-wide routing, safety, design, and coding constraints |
| Memory topics | 4 required topics plus index | Durable project conventions, decisions, preferences, and feedback |

Every agent, skill, workflow, and rule has a SemVer contract. `.agents/manifest.json`, `.agents/manifest.lock.json`, and `.agents/DEPENDENCY_GRAPH.md` make the managed toolkit reproducible and detect drift.

```bash
npm run generate:agents
npm run check:agents
```

## Common workflows

| Command | Purpose |
| --- | --- |
| `/brainstorm` | Explore options and architecture before implementation |
| `/coordinate` | Run separable research or review tasks in parallel, then synthesize |
| `/create` | Create a feature or application with structured gates |
| `/debug` | Perform evidence-based root-cause analysis |
| `/deploy` | Execute production pre-flight checks and deployment workflow |
| `/enhance` | Safely modify an existing codebase |
| `/orchestrate` | Plan, obtain approval, delegate to specialists, and verify |
| `/plan` | Create a detailed implementation plan and checklist |
| `/preview` | Manage local preview servers |
| `/remember` | Save durable project information to memory |
| `/status` | Summarize active work and blockers |
| `/test` | Design and execute tests |
| `/verify` | Prove changes by running checks instead of relying on inspection |

## Release and production gates

A release candidate is not production-approved until all automated checks and the hands-on Antigravity smoke test in [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) are complete.

Required GitHub checks:

- Toolkit validation
- CLI tests and package validation
- Web lint, typecheck, build, and audit
- Antigravity native contract
- Dependency Review

AG Kit never requires automatic merge, automatic deployment, or automatic MCP synchronization. Production changes should remain reviewable and reversible.

## Documentation

- [Antigravity implementation details](.agents/hooks/README.md)
- [Migration guide](MIGRATION.md)
- [Production release checklist](PRODUCTION_CHECKLIST.md)
- [Security policy and runtime threat model](SECURITY.md)
- [Agent flow architecture](AGENT_FLOW.md)
- [Toolkit architecture](.agents/ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)
- [Release setup](.github/RELEASE_SETUP.md)

## References and attribution

AG Kit is an original open-source implementation of Markdown-based agent engineering patterns. No proprietary source files are included. Runtime integration decisions are based on public Antigravity documentation and codelabs linked in [.agents/hooks/README.md](.agents/hooks/README.md).

## Support the project

<p align="center">
  <a href="https://buymeacoffee.com/vudovn" target="_blank"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" /></a>
</p>

<p align="center"> - or - </p>

<p align="center">
  <img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Buy me coffee" width="200" />
</p>

<p align="center">
  <code>CA: Gjpatn3d24dCRhUng7F37K6xJba4R8SDBC18xs1Apump</code>
</p>

## License

Released under the [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
