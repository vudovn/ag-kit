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

AG Kit runtime-neutral từ lõi. Behavior dùng chung chỉ tồn tại một lần trong `shared/`; từng runtime adapter dịch nó sang native surface của host mà không biến thành một fork riêng.

- **1 resident core** — rule vận hành luôn bật nhưng rất nhỏ.
- **18 hot-loaded skills** — chỉ vào context khi task cần.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development spine** — QUICK / STANDARD / DEEP với gate rõ ràng.
- **16 runtime targets** — chia tier theo capability thật, không giả parity.
- **Domain packs** — knowledge sâu giữ lạnh đến lúc cần.
- **Local-first memory** — Markdown canonical; SQLite/FTS5 chỉ là lớp tăng tốc tùy chọn.
- **Executable evidence** — preflight, runtime doctor, cross-audit, receipts, dependency audit và CI.

```text
shared/                  # behavior canonical, runtime-neutral
├── core/                # tiny always-on core
├── skills/              # hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # một development spine

packs/                   # domain knowledge
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

Contract machine-readable nằm ở [`platform-capabilities.json`](platform-capabilities.json). AG Kit chỉ claim capability khi adapter tương ứng thật sự khai báo và kiểm được capability đó.

Không runtime nào là “primary runtime” của AG Kit. Host nào giàu native surface hơn thì adapter của host đó có thể làm nhiều hơn, nhưng product behavior vẫn phải portable qua shared core.

## Cài đặt

Yêu cầu Node.js **22+** và Git.

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

Cài riêng một runtime khi cần:

```bash
ag-kit runtime install claude
ag-kit runtime install codex
ag-kit runtime uninstall claude
```

Mỗi runtime install có ownership manifest và pre-install backup. Uninstall chỉ gỡ state do AG Kit sở hữu khi chứng minh được ownership, giữ user drift và mặc định giữ project memory.

## Local-first memory

```bash
ag-kit memory init
ag-kit memory add "Repo dùng pnpm" --kind convention --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory dream
ag-kit memory status
```

Markdown dưới `.ag-kit/memory/` là canonical. Candidate có thể thành durable sau repeated evidence qua nhiều session, có validity window, supersede fact cũ và được archive bởi dream cycle. SQLite FTS5 là warm index có thể rebuild.

Cross-project recall phải opt-in:

```bash
ag-kit brain register .
ag-kit brain list
ag-kit brain search "deployment convention"
```

AG Kit không tự crawl home directory. Filesystem root/home bị từ chối; integration chỉ có global config sẽ được stage để người dùng tự kích hoạt thay vì âm thầm sửa config.

## Một development spine

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Đã so sánh phương án và chọn signed one-time token"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

Mỗi gated phase cần artifact trước khi approve. DEEP mode còn cần dependency-wave table rõ ràng trước khi hội tụ execution.

Specialist theo dự án chỉ sinh tạm thời:

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship an toàn"
```

Generated role nằm dưới `.ag-kit/agents/`; framework vẫn chỉ giữ bốn permanent agents.

## Context economy

Route task mà không hard-code vendor model:

```bash
ag-kit route "đọc auth module và giải thích flow"
ag-kit route "thiết kế migration nhiều service"
```

Giới hạn output command lớn:

```bash
ag-kit run npm test
ag-kit run npm run build --max-lines 30
```

Full stdout/stderr nằm dưới `.ag-kit/session-sandbox/`; caller chỉ nhận bounded summary.

Tạo handoff để tiếp tục session:

```bash
ag-kit handoff create \
  --goal "hoàn tất runtime rollout" \
  --state "core và CLI đang xanh" \
  --evidence "npm test passed" \
  --risk "web audit còn pending" \
  --next "run full CI"

ag-kit handoff show
```

## Independent cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

Reviewer lineage khác chỉ nhận snapshot/diff trong temp directory, không có writable source mount. Finding vẫn được tách thành consensus và contested, kèm receipt.

## Observability và privacy

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
```

Local ledger có giới hạn/rotation và dashboard chỉ bind localhost. AG Kit chỉ ghi giá trị đo được hoặc do integration truyền rõ ràng, không tự bịa savings multiplier.

Adapter có thể dùng native observability hook của host khi host hỗ trợ. Những hook đó chỉ là implementation detail của runtime, phải privacy-minimal và fail-open.

## Design contract

```bash
ag-kit design list
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
```

`DESIGN.md` mang brand intent, color, typography, layout, component, imagery, motion, accessibility và constraints xuyên runtime mà không cần thêm resident prompt.

## MCP bridge

```bash
ag-kit mcp serve
```

MCP surface được giữ nhỏ có chủ đích: project memory, opt-in cross-project search/status, team init, runtime status và audit probe. Adapter chỉ wire hoặc stage MCP bridge khi configuration model của runtime đó đã được verify.

## Runtime adapters

Mỗi adapter nằm dưới `runtimes/<runtime>/` và khai capability trong `platform-capabilities.json`.

Ví dụ:

- Antigravity có thể project native rules, skills, agents, hooks, MCP và plugin packaging.
- Claude có native skills/agents và project MCP ở cấp project.
- Codex nhận portable instructions, skills và plugin/MCP projection.
- Connected/bridge target chỉ expose đúng surface AG Kit đã verify.

Code/test runtime-specific ở trong adapter boundary. Validation cấp root luôn runtime-neutral.

## Validation repo

```bash
npm run check:v2
npm run check:docs
npm run test:v2
npm run check:runtimes
npm run test:runtimes
npm run build:runtimes
npm run build:runtime-artifacts
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

`check:runtimes` còn khóa invariant runtime-neutral: không được khai primary runtime, không có root script/workflow gate mang tên một runtime, và không cho tooling thời Antigravity-only quay lại trong generated `.agents/` surface.

## Tương thích lifecycle cũ

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit rollback
ag-kit status
```

Legacy update vẫn merge-aware và backup-aware để người dùng cũ migrate an toàn sang v2.

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

AG Kit v2 tự triển khai các feature class hữu ích của mô hình tiny-core multi-runtime kiểu IJFW nhưng giữ code, naming, lifecycle model và privacy posture riêng của AG Kit. Xem [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) để biết capability map và intentional differences.

## Tài liệu

- [`docs/ARCHITECTURE_V2.md`](docs/ARCHITECTURE_V2.md) — kiến trúc v2
- [`docs/RUNTIMES.md`](docs/RUNTIMES.md) — runtime tiers và adapters
- [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) — functional parity map
- [`MIGRATION.md`](MIGRATION.md) — hướng dẫn migration
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) — release checklist
- [`SECURITY.md`](SECURITY.md) — security model
- [`AGENT_FLOW.md`](AGENT_FLOW.md) — flow architecture
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## Giấy phép

Phát hành theo [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
