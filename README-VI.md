<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  Lớp vận hành multi-runtime gọn cho AI coding agents: một shared core, skill tải theo nhu cầu, local-first memory, gated execution, context economy, privacy controls và independent verification.
</p>

<p align="center">
  <a href="./README.md">English</a> · <a href="./docs/RUNTIMES.md">Runtimes</a> · <a href="./docs/PARITY_IJFW.md">IJFW parity</a> · <a href="./MIGRATION.md">Migration</a> · <a href="./SECURITY.md">Bảo mật</a>
</p>

---

## AG Kit v2 là gì?

AG Kit runtime-neutral từ lõi. Behavior dùng chung chỉ tồn tại một lần trong `shared/`; từng runtime adapter dịch nó sang native surface của host mà không biến thành fork riêng.

- **1 resident core** — rule vận hành luôn bật nhưng rất nhỏ.
- **18 hot-loaded skills** — chỉ vào context khi task cần.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development spine** — QUICK / STANDARD / DEEP với gate rõ ràng.
- **16 runtime targets** — chia tier theo capability thật, không giả parity.
- **Domain packs** — knowledge sâu giữ lạnh đến lúc cần.
- **Local-first memory** — Markdown canonical; FTS/semantic chỉ là lớp tăng tốc tùy chọn, có thể rebuild.
- **Executable evidence** — preflight, runtime doctor, cross-audit, receipts, benchmark artifacts, dependency audit và CI.

```text
shared/                  # behavior canonical, runtime-neutral
├── core/                # tiny always-on core
├── skills/              # hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # một development spine

packs/                   # cold domain/reference knowledge
runtimes/                # thin adapters theo capability
engine/                  # memory / planning / audit / preflight / observability
cli/                     # lifecycle, MCP, context, memory, audit tools
```

Những host tree như `.agents/`, `.claude/` hay `.gemini/` chỉ là projection do adapter tạo. `shared/` vẫn là source of truth.

## Runtime coverage

| Tier | Runtime |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

Contract machine-readable nằm ở [`platform-capabilities.json`](platform-capabilities.json). Không runtime nào là primary runtime của AG Kit.

## Cài đặt

Yêu cầu Node.js **22+** và Git.

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

Cài package chỉ cài CLI. Project chỉ thay đổi sau khi bạn chủ động cài runtime adapter.

```bash
ag-kit runtime install claude
ag-kit runtime doctor claude
ag-kit runtime uninstall claude
```

Mỗi runtime install có ownership manifest và pre-install backup. Uninstall chỉ gỡ/restore state AG Kit sở hữu khi chứng minh được ownership, giữ user drift và mặc định giữ project memory.

### Migrate project Antigravity đời cũ

CLI managed-tree Antigravity-only đời cũ đã bị loại bỏ. Commit hoặc backup project, sau đó migrate bằng đúng lifecycle chung:

```bash
ag-kit runtime install antigravity
ag-kit runtime doctor antigravity
```

Xem [`MIGRATION.md`](MIGRATION.md) để biết chi tiết backup/recovery từ pre-v2.

## Memory và continuity

```bash
ag-kit memory init
ag-kit memory add "Repo dùng pnpm" --kind convention --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory dream
ag-kit memory status

ag-kit memory semantic status
ag-kit memory semantic on
ag-kit memory semantic rebuild

ag-kit brain register .
ag-kit brain search "deployment convention"
```

Markdown dưới `.ag-kit/memory/` là canonical. SQLite/FTS5 và semantic tier local chỉ là acceleration layer có thể rebuild. Semantic mặc định tắt. Cross-project recall phải opt-in và không bao giờ tự crawl `$HOME`.

Tạo handoff:

```bash
ag-kit handoff create --goal "hoàn tất runtime rollout" --state "core đang xanh" --next "run full CI"
ag-kit handoff show
```

## Một development spine

```bash
ag-kit prompt-check "update it"
ag-kit route "thiết kế migration nhiều service"
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Đã so sánh phương án"
ag-kit flow waves '[{"id":"foundation","mode":"parallel","tasks":["A","B"],"dependsOn":[]}]'
ag-kit flow ready
ag-kit flow wave-complete foundation "Foundation verified"
ag-kit flow approve "approved"
```

Mỗi gated phase cần artifact trước khi approve. Boundary VERIFY/CROSS_AUDIT cần mechanical evidence mới. DEEP mode dùng dependency waves rõ ràng trước khi ship.

Specialist theo dự án chỉ sinh tạm thời:

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship an toàn"
```

## Context economy

```bash
ag-kit run npm test
ag-kit run npm run build --max-lines 30
ag-kit compress docs/long-context.md
```

Full command output nằm dưới `.ag-kit/session-sandbox/`; caller chỉ nhận bounded summary. Compression deterministic và mặc định không ghi đè source.

## Independent cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

Reviewer lineage khác chỉ nhận bounded snapshot chunk trong temp directory, không có writable source mount. Nhiều lineage có thể chạy bounded-parallel; finding được tách consensus/contested và có traceable receipt.

## Observability và privacy

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
```

Local ledger có giới hạn/rotation, rollup theo runtime/trace và dashboard chỉ bind localhost. AG Kit chỉ ghi giá trị đo được hoặc integration truyền rõ ràng, không tự bịa savings multiplier.

Personalization là evidence-backed và opt-in:

```bash
ag-kit personalize status
ag-kit personalize learn "Dùng prose gọn" --evidence "User rút ngắn report" --session s1
ag-kit personalize inject on
ag-kit personalize forget all
```

`AG_KIT_PROFILE_KILL=1` là hard kill switch.

## Design và MCP

```bash
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
ag-kit mcp serve
```

`DESIGN.md` mang design intent portable xuyên runtime. MCP bridge cố ý giữ surface nhỏ và runtime-neutral.

## Runtime adapters

Mỗi adapter nằm dưới `runtimes/<runtime>/` và khai capability đã verify trong `platform-capabilities.json`.

- Antigravity có thể project native rules, skills, agents, hooks, MCP và plugin packaging.
- Claude có native skills/agents và project integration.
- Codex nhận portable instructions, skills và hook/plugin surface khi đã verify.
- Connected/bridge target chỉ expose đúng surface AG Kit kiểm chứng được.

Native richness của một adapter không biến runtime đó thành trung tâm sản phẩm.

## Validation repo

```bash
npm run check:v2
npm run check:docs
npm run test:v2
npm run benchmark:v2 -- --output dist/evidence/benchmark-v2.json
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

`check:runtimes` khóa invariant runtime-neutral. `check:docs` kiểm link và claim machine-checkable. CI còn publish deterministic benchmark receipt cho memory recall, routing, compression và runtime lifecycle.

## Nguyên tắc

1. **Context là budget.**
2. **Behavior khác knowledge.** Skill hành động; pack cung cấp tri thức.
3. **Một source, nhiều runtime.**
4. **Không có primary runtime.** Native richness nằm sau adapter boundary.
5. **Capability claim phải machine-checkable.**
6. **Memory phải human-readable và user-owned.**
7. **Judgment phải explicit.** Không silent phase approval.
8. **Verification phải tạo evidence.**
9. **Privacy phải inspect được và có kill switch.**
10. **Một lifecycle duy nhất.** `runtime install/doctor/uninstall` thay thế lifecycle ẩn theo từng runtime.

AG Kit v2 tự triển khai các feature class hữu ích kiểu IJFW nhưng giữ code, naming, lifecycle model và privacy posture riêng. Xem [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md).

## Tài liệu

- [`docs/ARCHITECTURE_V2.md`](docs/ARCHITECTURE_V2.md) — kiến trúc
- [`docs/RUNTIMES.md`](docs/RUNTIMES.md) — runtime tiers/adapters
- [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) — functional parity map
- [`MIGRATION.md`](MIGRATION.md) — hướng dẫn migration
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) — release checklist
- [`SECURITY.md`](SECURITY.md) — security model
- [`AGENT_FLOW.md`](AGENT_FLOW.md) — flow architecture
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## Giấy phép

Phát hành theo [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
