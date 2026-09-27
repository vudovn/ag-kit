<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  A lean multi-runtime operating layer for AI coding agents: one tiny core, hot-loaded skills, one shared local brain, gated execution, context economy, privacy controls, and independent verification.
</p>

<div align="center">
  <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="AG Kit on Unikorn.vn" width="210" height="54" /></a>
  <a href="https://trendshift.io/repositories/21490" target="_blank"><img src="https://trendshift.io/api/badge/repositories/21490" alt="AG Kit on Trendshift" width="250" height="55" /></a>
  <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="AG Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

<p align="center">
  <a href="./README-VI.md">Tiếng Việt</a> · <a href="./docs/PARITY_IJFW.md">IJFW parity</a> · <a href="./MIGRATION.md">Migration</a> · <a href="./SECURITY.md">Security</a>
</p>

---

## The v2 shape

AG Kit deliberately keeps the always-on surface small:

- **1 resident core** — operating rules only.
- **18 hot-loaded skills** — behavior enters context only when relevant.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development spine** — QUICK / STANDARD / DEEP with explicit gates.
- **16 runtime targets** — capability tiers instead of fake parity.
- **Domain packs** — knowledge lives outside resident behavior.
- **One local brain** — Markdown memory is canonical; SQLite/FTS5 is optional acceleration; cross-project recall is explicit opt-in.
- **Executable evidence** — doctor, preflight, cross-audit, receipts, dependency audits, and CI.

```text
shared/                  # canonical runtime-neutral behavior
├── core/                # tiny always-on core
├── skills/              # 18 hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # one development spine

packs/                   # domain knowledge
runtimes/                # thin capability-aware adapters
cli/                     # memory, MCP, flow, audit, lifecycle, context tools
.agents/                 # generated native Antigravity projection
```

`shared/` is the source of truth. Runtime trees are projections/adapters, not independent forks.

Lean does not mean discarded knowledge. The v1 baseline of **47 skills** is fully mapped in [`packs/legacy-knowledge-map.json`](packs/legacy-knowledge-map.json); deep guidance and supporting assets are preserved as cold references under `shared/skills/*/references/` and `packs/*/references/`, while current v2 contracts remain authoritative. `check:v2` fails if a mapped reference or asset disappears or if a legacy `SKILL.md` becomes discoverable again.

## Runtime coverage

| Tier | Runtimes |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

The exact contract is machine-readable in [`platform-capabilities.json`](platform-capabilities.json). AG Kit prefers project-scoped activation. Global-only integrations are staged for explicit user activation instead of silently mutating home-directory configuration.

## Install once for the tools you already use

Requirements: Node.js **22+** and Git.

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

`runtime detect` uses executable/project/user markers and lifecycle evidence. `install-present` downloads the AG Kit source once, installs only detected runtimes, and skips already-managed targets unless `--force` is explicit.

You can still install one target directly:

```bash
ag-kit runtime install antigravity
ag-kit runtime doctor antigravity
ag-kit runtime uninstall antigravity
```

Runtime installs have pre-install backups and ownership manifests. Uninstall restores originals where safe, removes only AG Kit-owned marker/MCP regions, preserves drifted user content, and keeps memory by default.

## One shared local brain

Project memory:

```bash
ag-kit memory init
ag-kit memory add "Use pnpm in this repo" --kind convention --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory dream
ag-kit memory status
```

Markdown under `.ag-kit/memory/` is canonical. Candidates can become durable after repeated cross-session evidence, carry validity windows, supersede older facts, and be archived by the dream cycle. SQLite FTS5 is a disposable warm index.

Cross-project recall is opt-in; AG Kit never crawls your home directory automatically:

```bash
ag-kit brain register .
ag-kit brain list
ag-kit brain search "deployment convention"
```

Registered paths are realpath-checked, root/home registration is rejected, outside-home projects require explicit consent, and `AG_KIT_MINIMAL=1` or `AG_KIT_NO_CROSS_PROJECT=1` disables cross-project search. MCP can search the approved registry but cannot register projects.

## One development spine

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Compared approaches and selected signed one-time tokens"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

Every phase needs an artifact before approval; AG Kit never auto-approves a user gate. DEEP mode also requires an explicit dependency-wave table before convergence.

Project-specific specialists remain temporary:

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship safely"
```

Generated roles live under `.ag-kit/agents/`; the framework itself stays at four permanent agents.

## Context economy

Route work without hard-coding a vendor model:

```bash
ag-kit route "read the auth module and explain the flow"
ag-kit route "design a multi-service migration"
```

Large-output commands can keep full stdout/stderr off-context:

```bash
ag-kit run npm test
ag-kit run npm run build --max-lines 30
```

The complete log goes under `.ag-kit/session-sandbox/`; the caller gets a bounded summary. Commands execute without shell-string interpolation.

Compact context artifacts without inventing a semantic summary:

```bash
ag-kit compress notes.md
ag-kit compress notes.md --write        # explicit overwrite + timestamped backup
```

Compression reports actual byte reduction. By default it writes a new file.

Create a structured continuation artifact:

```bash
ag-kit handoff create \
  --goal "finish runtime rollout" \
  --state "core and CLI are green" \
  --evidence "npm test passed" \
  --risk "web audit still pending" \
  --next "run full CI"

ag-kit handoff show
```

The handoff records goal, state, decisions, Git-changed files, evidence, risks, and the next concrete action; previous handoffs are archived.

## Independent cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

External reviewer lineages receive only a snapshot/diff in temporary directories, never a writable source mount. Findings are clustered into **consensus** and **contested** groups and written with receipts.

## Observability without invented savings

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
```

The ledger is bounded/rotating and the dashboard binds to localhost. AG Kit records measured or explicitly supplied values; it does not fabricate a “without AG Kit” multiplier.

Antigravity additionally uses an official `PostToolUse` hook to auto-record privacy-minimal events: tool name, success/error class, runtime, and session only. Commands, prompts, file contents, and tool arguments are not recorded by that hook. Telemetry is fail-open and can never block the agent loop.

## Personalization and privacy

```bash
ag-kit personalize learn "Use compact prose" --evidence "User shortened the release note" --session s1
ag-kit personalize learn "Use compact prose" --evidence "User shortened the next report" --session s2
ag-kit personalize inject on
ag-kit personalize preview --host claude
ag-kit personalize egress
ag-kit personalize forget all
```

Preferences require verbatim evidence and cross-session confirmation. Injection is off by default. `AG_KIT_PROFILE_KILL=1` overrides stored settings. `forget` removes both the preference and egress rows that referenced it.

## Design contract

```bash
ag-kit design list
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
```

`DESIGN.md` carries brand intent, colors, typography, layout, components, imagery, motion, accessibility, and constraints across runtimes without adding another resident prompt.

## MCP bridge

```bash
ag-kit mcp serve
```

The MCP surface intentionally stays small: evolving project memory, opt-in cross-project search/status, team initialization, runtime status, and audit probing. Richer local operations remain CLI/state modules instead of inflating every agent's tool list.

## Antigravity native projection

Antigravity remains AG Kit's richest native target:

- **18 skills / 4 agents / 0 legacy workflow files**
- native rules and safety gate
- privacy-minimal `PostToolUse` observability
- project MCP configuration
- native plugin packaging

```bash
npm run sync:antigravity
npm run check:antigravity-projection
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

## Release gates

```bash
ag-kit preflight
npm run check:v2
npm run test:v2
npm run test:cli
```

CI additionally checks Antigravity projection/plugin compatibility, runtime builds, web lint/typecheck/build, dependency review, and production dependency audits. Security advisories stay blocking; the web app tracks the patched Next.js security line rather than suppressing audit failures.

## Legacy lifecycle compatibility

Existing AG Kit installations still have a safe migration path:

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit rollback
ag-kit status
```

Legacy updates remain merge-aware and backup-aware while v2 is canonical.

## Principles

1. **Context is a budget.**
2. **Behavior is not knowledge.** Skills act; packs inform.
3. **One source, many runtimes.**
4. **Capability claims must be machine-checkable.**
5. **Memory stays human-readable and user-owned.**
6. **Judgment stays explicit.** No silent phase approval.
7. **Verification produces evidence.**
8. **Privacy is inspectable and kill-switchable.**
9. **Dangerous automation stays narrow.**

AG Kit v2 independently implements the useful feature classes behind the IJFW-style tiny-core operating model while keeping AG Kit's own code, names, privacy posture, and stronger native Antigravity integration. See [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) for the detailed capability map and intentional differences.

## Documentation

- [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) — functional parity map
- [`MIGRATION.md`](MIGRATION.md) — migration guidance
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) — release checklist
- [`SECURITY.md`](SECURITY.md) — security model
- [`AGENT_FLOW.md`](AGENT_FLOW.md) — flow architecture
- [`.agents/hooks/README.md`](.agents/hooks/README.md) — Antigravity integration
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## Support the project

<p align="center"><a href="https://buymeacoffee.com/vudovn" target="_blank"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" /></a></p>
<p align="center">- or -</p>
<p align="center"><img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Buy me coffee" width="200" /></p>
<p align="center"><code>CA: Gjpatn3d24dCRhUng7F37K6xJba4R8SDBC18xs1Apump</code></p>

## License

Released under the [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
