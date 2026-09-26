<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  Lớp vận hành multi-runtime gọn cho AI coding agents: tiny core, hot-loaded skills, evolving project memory, gated execution, MCP, observability, privacy controls và independent cross-audit.
</p>

<p align="center">
  <a href="./README.md">English</a> · <a href="./docs/PARITY_IJFW.md">Parity map</a> · <a href="./MIGRATION.md">Migration</a> · <a href="./SECURITY.md">Bảo mật</a>
</p>

---

## Kiến trúc v2

AG Kit v2 giữ framework nhỏ theo mặc định:

- **1 tiny resident core**.
- **18 hot-loaded skills**.
- **4 permanent agents**: `scout`, `architect`, `builder`, `reviewer`.
- **1 development spine** với QUICK / STANDARD / DEEP và user gate rõ ràng.
- `shared/` là source of truth; runtime chỉ là adapter/projection.
- `packs/` chứa domain knowledge để không làm skill phình.
- Markdown là canonical memory; SQLite FTS5 chỉ là warm index có thể rebuild.
- Memory có candidate/durable/superseded/archived, temporal validity và dream cycle.
- Cross-audit chỉ đọc snapshot/diff, tách reviewer theo lineage và phân loại consensus/contested.
- Observability, personalization/privacy và `DESIGN.md` đều là local project state, không phải resident prompt mới.

```text
shared/        # canonical core / skills / agents / flow
packs/         # domain reference knowledge
runtimes/      # capability-aware adapters
cli/           # CLI + MCP + local engines
.agents/       # generated Antigravity projection
.ag-kit/       # project-local runtime state, memory, receipts, audits
```

## Độ phủ runtime

AG Kit hiện khai báo **16 runtime targets** theo capability thật.

| Tier | Runtime |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

AG Kit ưu tiên project-scoped config. Nếu runtime chỉ có user-global registry/config, AG Kit sẽ stage hướng dẫn/snippet thay vì tự ý sửa home directory.

## Bắt đầu nhanh

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime list
ag-kit runtime install antigravity
```

Yêu cầu Node.js **22+**.

## Gated development flow

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Đã so sánh ba phương án và chọn signed one-time token"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

Mỗi phase phải có artifact summary trước khi approve. DEEP mode bắt buộc có dependency-wave table ở CONVERGE. AG Kit không tự approve user gate.

## Evolving memory

```bash
ag-kit memory init
ag-kit memory add "Repo dùng pnpm" --kind convention --title "Package manager" --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory touch <memory-id> --session s3
ag-kit memory dream
ag-kit memory reindex
ag-kit memory status
```

Memory nằm trong `.ag-kit/memory/`. Candidate được promote thành durable sau repeated evidence qua nhiều session; fact cũ có thể supersede thay vì bị xóa khỏi lịch sử; `validFrom`/`validTo` hỗ trợ recall theo thời điểm.

## Specialist team

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship release an toàn"
```

Specialist theo dự án nằm trong `.ag-kit/agents/`; framework vẫn chỉ giữ bốn permanent agents.

## Cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

Reviewer chạy trong temp directory với snapshot/diff, không có writable source mount. Kết quả được cluster thành consensus hoặc contested và ghi report/receipt local.

## Observability local

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start --port 4737
```

Dashboard chỉ bind `127.0.0.1`. AG Kit chỉ lưu số liệu token/cost được integration cung cấp rõ ràng, không tự bịa “token saved”.

## Personalization và privacy

```bash
ag-kit personalize learn "Viết ngắn gọn" --evidence "User yêu cầu rút release note" --session s1
ag-kit personalize learn "Viết ngắn gọn" --evidence "User tiếp tục rút report" --session s2
ag-kit personalize inject on
ag-kit personalize preview --host claude
ag-kit personalize egress
ag-kit personalize forget all
```

Preference cần verbatim evidence và lặp qua nhiều session mới được confirm. Injection mặc định tắt. `AG_KIT_PROFILE_KILL=1` là hard kill switch. Disclosure được log local và `forget` xóa cả inference lẫn egress rows liên quan.

## Design contract

```bash
ag-kit design list
ag-kit design init --template graphite --brand "Acme"
ag-kit design check
```

`DESIGN.md` khóa brand intent, color, typography, layout, component, imagery, motion, accessibility và do/don't để visual behavior đi xuyên runtime mà không cần thêm giant prompt.

## MCP bridge

```bash
ag-kit mcp serve
```

MCP surface được giữ nhỏ có chủ đích: evolving memory, team init, runtime status và audit probe. Capability khác vẫn là CLI/local state module.

## Preflight

```bash
ag-kit preflight
```

Preflight kiểm architecture budget, v2 engines, Antigravity projection/runtime build, native doctor/tests/plugin và CLI. CI còn chạy web lint/typecheck/build, dependency audit và dependency review.

## Antigravity native projection

`.agents/` hiện chỉ giữ:

- **18 skills**
- **4 permanent agents**
- **0 legacy workflow files**
- native safety hook
- project MCP config
- native plugin packaging

```bash
npm run sync:antigravity
npm run check:antigravity-projection
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

Behavior reusable phải sửa trong `shared/`, không tạo source-of-truth thứ hai trong `.agents/`.

## Tương thích lifecycle cũ

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit update --strategy replace
ag-kit rollback
ag-kit status
```

Legacy update vẫn merge-aware và backup-aware để migration sang v2 an toàn.

## Validation

```bash
npm run check:v2
npm run test:v2
npm run check:antigravity-projection
npm run build:runtimes
npm run check:antigravity
npm run test:antigravity
npm run test:cli
npm run lint:web
npm run typecheck:web
npm run build:web
```

## Parity với IJFW

AG Kit v2 triển khai các feature class hữu ích của kiến trúc kiểu IJFW—tiny core, hot-loaded skills, runtime tiers, evolving local memory, gated phases, specialist assembly, independent audit, observability, personalization/privacy và design contract—bằng code, naming và runtime model riêng của AG Kit.

Xem [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) để biết phần đã parity và intentional differences.

## Giấy phép

Phát hành theo [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
