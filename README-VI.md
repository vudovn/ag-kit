<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  Lớp vận hành multi-runtime gọn cho AI coding agents: tiny core, skills tải theo nhu cầu, project memory, specialist team, MCP, preflight gates và cross-audit chỉ đọc.
</p>

<div align="center">
  <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="AG Kit trên Unikorn.vn" width="210" height="54" /></a>
  <a href="https://trendshift.io/repositories/21490" target="_blank"><img src="https://trendshift.io/api/badge/repositories/21490" alt="AG Kit trên Trendshift" width="250" height="55" /></a>
  <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="AG Kit trên J2TEAM Launch" width="250" height="54" /></a>
</div>

<p align="center">
  <a href="./README.md">English</a> · <a href="./docs/PARITY_IJFW.md">Parity map</a> · <a href="./MIGRATION.md">Migration</a> · <a href="./SECURITY.md">Bảo mật</a>
</p>

---

## Vì sao có AG Kit v2

Agent kit càng lớn càng dễ tự phá context: quá nhiều role luôn bật, instruction trùng nhau, mỗi runtime một bản riêng và nhiều workflow engine cùng tranh quyền điều phối.

AG Kit v2 đi theo hướng ngược lại:

- **1 tiny resident core** — chỉ giữ rule vận hành luôn cần thiết.
- **18 top-level skills tải theo nhu cầu** — capability chỉ vào context khi liên quan.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development flow** — ba mức QUICK, STANDARD, DEEP thay vì nhiều workflow engine rời rạc.
- **Domain packs** — tri thức tham khảo nằm trong `packs/`, không nhồi vào giant skill.
- **Một source of truth** — behavior portable nằm trong `shared/`; runtime chỉ là projection/adapter.
- **Memory local-first** — Markdown là canonical; SQLite FTS5 chỉ là warm index có thể rebuild.
- **MCP bridge cấp project** — runtime có thể dùng chung memory/team/audit mà không giả vờ có native parity.
- **Cross-audit read-only** — reviewer CLI chỉ nhận snapshot/diff trong temp directory, không được mount writable repo.

## Kiến trúc

```text
shared/                  # source canonical, runtime-neutral
├── core/                # tiny always-on core
├── skills/              # 18 hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # 1 development flow, 3 depth modes

packs/                   # domain knowledge tải khi cần
runtimes/                # thin adapters theo capability thật
engine/                  # memory, team, audit, preflight wrappers/tests
cli/                     # @vudovn/ag-kit CLI + MCP server
.agents/                 # generated Antigravity projection
```

`shared/` là source of truth. `.agents/` không còn là một toolkit thứ hai; nó là projection native cho Antigravity được sinh từ shared core.

## Độ phủ runtime

AG Kit hiện khai báo **12 runtime targets đã được phân tier rõ ràng**.

| Tier | Runtime |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider |

Capability chi tiết nằm trong [`platform-capabilities.json`](platform-capabilities.json). AG Kit không quảng bá agents/hooks/plugins/skills native ở runtime nào chưa có contract được xác minh.

## Yêu cầu

- Node.js **22+**.
- Git để update/rollback có thể review.
- Tùy chọn: Codex, Gemini, Qwen, OpenCode hoặc reviewer CLI khác để chạy cross-audit.
- Tùy chọn: SQLite support từ Node runtime để có warm memory index; nếu không có, Markdown recall vẫn hoạt động.

## Bắt đầu nhanh

### Cài CLI

```bash
npm install -g @vudovn/ag-kit
```

Hoặc chạy trực tiếp:

```bash
npx @vudovn/ag-kit --help
```

### Cài runtime adapter

```bash
ag-kit runtime list
ag-kit runtime install antigravity
ag-kit runtime install claude
ag-kit runtime install qwen
```

Installer chỉ ghi các file project-scoped mà AG Kit có contract đã verify. Nó không tự ý sửa cấu hình user-global không liên quan.

### Project memory

```bash
ag-kit memory init
ag-kit memory add "Repo này dùng pnpm" --kind convention --title "Package manager"
ag-kit memory recall "package manager"
ag-kit memory reindex
ag-kit memory status
```

Memory nằm dưới `.ag-kit/memory/`. Markdown là bản canonical. SQLite/FTS5 chỉ là lớp tăng tốc có thể xóa và rebuild bất cứ lúc nào.

### Tạo specialist team theo dự án

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship release tiếp theo an toàn"
```

Role theo dự án được sinh dưới `.ag-kit/agents/`; bản thân framework chỉ giữ bốn core agents cố định.

### Cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 2
ag-kit cross-audit src/auth.ts --reviewers 3
```

Cross-audit probe các reviewer lineage độc lập, snapshot target hoặc git diff, chạy reviewer trong temp directory và lưu report/receipt dưới `.ag-kit/`.

### Release gates

```bash
ag-kit preflight
```

Gate hiện tại bao gồm v2 architecture budget, engine tests, Antigravity projection drift, runtime build, Antigravity doctor/tests/plugin build; CI còn chạy CLI tests, web checks và dependency review.

## MCP bridge

Chạy shared MCP bridge qua stdio:

```bash
ag-kit mcp serve
```

Bridge cố tình giữ surface nhỏ: project memory, team assembly/status, runtime status và audit probing. Runtime installer chỉ wire project MCP config ở nơi format/runtime contract đã được xác minh.

## Antigravity native projection

Antigravity vẫn là target native giàu capability nhất. `.agents/` hiện chỉ giữ surface v2 gọn:

- **18 skills**
- **4 permanent agents**
- **0 legacy workflow files**
- native safety hook
- project MCP config
- native plugin packaging

Đồng bộ và kiểm tra projection bằng:

```bash
npm run sync:antigravity
npm run check:antigravity-projection
npm run check:antigravity
npm run test:antigravity
npm run build:antigravity-plugin
```

Behavior dùng lại phải sửa trong `shared/`, không copy thêm logic mới vào `.agents/`.

## Tương thích lifecycle cũ

CLI vẫn giữ safe managed-tree lifecycle cho installation AG Kit đời trước:

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit update --strategy replace
ag-kit rollback
ag-kit status
```

Update tiếp tục merge-aware và backup-aware để người dùng cũ có đường migration an toàn trong lúc v2 trở thành kiến trúc canonical.

## Validation trong repo

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

## Nguyên tắc thiết kế

1. **Context là tài nguyên hữu hạn.** Resident instructions phải nhỏ.
2. **Behavior khác knowledge.** Skill định nghĩa cách làm; pack chứa tri thức domain.
3. **Một source, nhiều runtime.** Adapter dịch shared core thay vì fork framework.
4. **Capability claim phải machine-checkable.** Parity là matrix, không phải marketing copy.
5. **Memory phải đọc được bằng mắt.** Index chỉ tăng tốc, không được thành bản duy nhất.
6. **Verify bằng thực thi.** Preflight, CI, doctor và cross-audit phải tạo evidence/receipt.
7. **Automation nguy hiểm phải hẹp.** Safety hook chặn hành vi phá hủy rõ ràng nhưng không thay thế runtime permission hay human review.

## Công việc parity với IJFW

AG Kit v2 học các ý tưởng kiến trúc như tiny resident core, hot-loaded skills, shared portable behavior, runtime tiers, local-first memory và independent audit lines. Code triển khai là của AG Kit; mục tiêu là functional/architectural parity khi có ích, không copy source code.

Theo dõi capability map tại [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md).

## Tài liệu

- [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) — functional parity map
- [`MIGRATION.md`](MIGRATION.md) — migration
- [`PRODUCTION_CHECKLIST.md`](PRODUCTION_CHECKLIST.md) — release checklist
- [`SECURITY.md`](SECURITY.md) — security model
- [`AGENT_FLOW.md`](AGENT_FLOW.md) — flow architecture
- [`.agents/hooks/README.md`](.agents/hooks/README.md) — Antigravity native integration
- [`CHANGELOG.md`](CHANGELOG.md) — lịch sử release

## Ủng hộ dự án

<p align="center">
  <a href="https://buymeacoffee.com/vudovn" target="_blank"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" /></a>
</p>

<p align="center"> - hoặc - </p>

<p align="center">
  <img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Ủng hộ dự án qua VietQR" width="200" />
</p>

<p align="center">
  <code>CA: Gjpatn3d24dCRhUng7F37K6xJba4R8SDBC18xs1Apump</code>
</p>

## Giấy phép

Phát hành theo [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
