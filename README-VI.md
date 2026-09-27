<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  Lớp vận hành multi-runtime gọn cho AI coding agents: một tiny core, hot-loaded skills, shared local brain, gated execution, context economy, privacy controls và independent verification.
</p>

<p align="center">
  <a href="./README.md">English</a> · <a href="./docs/PARITY_IJFW.md">IJFW parity</a> · <a href="./MIGRATION.md">Migration</a> · <a href="./SECURITY.md">Bảo mật</a>
</p>

---

## Hình dạng v2

AG Kit cố tình giữ phần luôn nằm trong context thật nhỏ:

- **1 resident core** — chỉ rule vận hành.
- **18 hot-loaded skills** — capability chỉ load khi liên quan.
- **4 permanent agents** — `scout`, `architect`, `builder`, `reviewer`.
- **1 development spine** — QUICK / STANDARD / DEEP với gate rõ ràng.
- **16 runtime targets** — chia tier theo capability thật, không giả parity.
- **Domain packs** — knowledge nằm ngoài resident behavior.
- **Một local brain** — Markdown là canonical; SQLite/FTS5 chỉ là lớp tăng tốc; cross-project recall phải opt-in.
- **Executable evidence** — doctor, preflight, cross-audit, receipts, dependency audit và CI.

```text
shared/                  # source canonical, runtime-neutral
├── core/                # tiny always-on core
├── skills/              # 18 hot-loaded skills
├── agents/              # scout / architect / builder / reviewer
└── flows/               # một development spine

packs/                   # domain knowledge
runtimes/                # thin adapters theo capability
cli/                     # memory, MCP, flow, audit, lifecycle, context tools
.agents/                 # generated native Antigravity projection
```

`shared/` là source of truth. Runtime tree chỉ là projection/adapter, không phải fork độc lập.

## Runtime coverage

| Tier | Runtime |
| --- | --- |
| First-class | Antigravity, Claude, Codex, Gemini, Qwen, Kimi, Cline |
| Connected | Cursor, Windsurf, GitHub Copilot |
| Bridge | OpenCode, OpenClaw, Aider, Wayland, Hermes, Pi |

Contract chi tiết nằm trong [`platform-capabilities.json`](platform-capabilities.json). AG Kit ưu tiên project-scoped activation; integration chỉ có global config sẽ được stage để người dùng bật rõ ràng, không tự sửa home directory.

## Một lần cài cho những runtime đang có

Yêu cầu Node.js **22+** và Git.

```bash
npm install -g @vudovn/ag-kit
ag-kit runtime detect
ag-kit runtime install-present
ag-kit runtime doctor
```

`runtime detect` dùng executable/project/user markers và lifecycle evidence. `install-present` tải source AG Kit một lần, chỉ cài runtime đã detect và bỏ qua target đã managed trừ khi bạn dùng `--force`.

Cài/gỡ riêng một runtime vẫn được hỗ trợ:

```bash
ag-kit runtime install antigravity
ag-kit runtime doctor antigravity
ag-kit runtime uninstall antigravity
```

Mỗi install có pre-install backup và ownership manifest. Uninstall chỉ gỡ vùng do AG Kit sở hữu, khôi phục bản gốc khi an toàn, giữ file đã drift và giữ memory mặc định.

## Một shared local brain

Project memory:

```bash
ag-kit memory init
ag-kit memory add "Repo dùng pnpm" --kind convention --session s1
ag-kit memory recall "package manager" --session s2
ag-kit memory dream
ag-kit memory status
```

Markdown dưới `.ag-kit/memory/` là canonical. Candidate có thể thành durable sau repeated evidence qua nhiều session, có validity window, supersede fact cũ và được dream cycle archive khi stale. SQLite FTS5 là warm index có thể xóa/rebuild.

Cross-project recall phải opt-in; AG Kit không tự crawl `$HOME`:

```bash
ag-kit brain register .
ag-kit brain list
ag-kit brain search "deployment convention"
```

Path được realpath-check, không cho register filesystem root/home, project ngoài home cần explicit consent. `AG_KIT_MINIMAL=1` hoặc `AG_KIT_NO_CROSS_PROJECT=1` tắt cross-project search. MCP chỉ search registry đã được duyệt, không có quyền tự register project.

## Một development spine

```bash
ag-kit flow start "Ship account recovery" --mode deep
ag-kit flow artifact "Đã so sánh phương án và chọn signed one-time token"
ag-kit flow approve "Shape approved"
ag-kit flow status
```

Mỗi phase phải có artifact trước khi approve; AG Kit không tự approve user gate. DEEP mode còn yêu cầu dependency-wave table rõ ràng trước convergence.

Specialist theo dự án chỉ sinh khi cần:

```bash
ag-kit team --archetype auto --name product-v2 --brief "Ship an toàn"
```

Role generated nằm dưới `.ag-kit/agents/`; framework vẫn chỉ giữ bốn permanent agents.

## Context economy

Route task mà không hard-code vendor model:

```bash
ag-kit route "đọc auth module và giải thích flow"
ag-kit route "thiết kế migration nhiều service"
```

Command output lớn có thể nằm ngoài context:

```bash
ag-kit run npm test
ag-kit run npm run build --max-lines 30
```

Full stdout/stderr được lưu dưới `.ag-kit/session-sandbox/`; caller chỉ nhận bounded summary. Command chạy không qua shell-string interpolation.

Compress artifact theo kiểu deterministic, không tự bịa semantic summary:

```bash
ag-kit compress notes.md
ag-kit compress notes.md --write        # explicit overwrite + timestamped backup
```

AG Kit báo byte reduction thực đo; mặc định luôn ghi file mới.

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

Handoff giữ goal, state, decisions, Git-changed files, evidence, risks và next action; handoff cũ được archive.

## Independent cross-audit

```bash
ag-kit cross-audit --probe
ag-kit cross-audit . --reviewers 3 --exclude-lineage openai
```

Reviewer lineage khác chỉ nhận snapshot/diff trong temp directory, không có writable source mount. Finding được cluster thành **consensus** và **contested**, kèm receipt.

## Observability không bịa savings

```bash
ag-kit observe turn --runtime claude --input 1200 --output 300 --cached 500 --cost 0.02
ag-kit dashboard summary
ag-kit dashboard start
```

Ledger có rotation/cap và dashboard chỉ bind localhost. AG Kit chỉ ghi số liệu đo được hoặc integration cung cấp rõ ràng, không tạo multiplier “nếu không dùng AG Kit”.

Antigravity còn dùng official `PostToolUse` hook để auto-record event tối thiểu: tool name, success/error class, runtime và session. Hook không ghi command args, prompt, file content hay tool arguments; telemetry fail-open nên không thể chặn agent loop.

## Personalization và privacy

```bash
ag-kit personalize learn "Viết ngắn gọn" --evidence "User rút release note" --session s1
ag-kit personalize learn "Viết ngắn gọn" --evidence "User tiếp tục rút report" --session s2
ag-kit personalize inject on
ag-kit personalize preview --host claude
ag-kit personalize egress
ag-kit personalize forget all
```

Preference cần verbatim evidence và xác nhận qua nhiều session. Injection mặc định tắt. `AG_KIT_PROFILE_KILL=1` luôn thắng setting đã lưu. `forget` xóa cả preference lẫn egress rows tham chiếu tới nó.

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

MCP surface được giữ nhỏ có chủ đích: evolving project memory, opt-in cross-project search/status, team init, runtime status và audit probe. Capability giàu hơn vẫn ở CLI/local state để không làm tool surface của mọi agent phình ra.

## Antigravity native projection

Antigravity vẫn là target native mạnh nhất của AG Kit:

- **18 skills / 4 agents / 0 legacy workflow files**
- native rules + safety gate
- privacy-minimal `PostToolUse` observability
- project MCP config
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

CI còn kiểm Antigravity projection/plugin compatibility, runtime build, web lint/typecheck/build, dependency review và production dependency audit. Security advisory vẫn là blocking gate; không tắt audit để “cho xanh”.

## Tương thích lifecycle cũ

```bash
ag-kit init
ag-kit update --dry-run
ag-kit update
ag-kit rollback
ag-kit status
```

Legacy update vẫn merge-aware và backup-aware để người dùng cũ migration an toàn sang v2.

## Nguyên tắc

1. **Context là budget.**
2. **Behavior khác knowledge.** Skill hành động; pack cung cấp tri thức.
3. **Một source, nhiều runtime.**
4. **Capability claim phải machine-checkable.**
5. **Memory phải human-readable và user-owned.**
6. **Judgment phải explicit.** Không silent phase approval.
7. **Verification phải tạo evidence.**
8. **Privacy phải inspect được và có kill switch.**
9. **Dangerous automation phải hẹp.**

AG Kit v2 tự triển khai các feature class hữu ích của mô hình tiny-core kiểu IJFW nhưng giữ code, naming, privacy posture và native Antigravity integration riêng của AG Kit. Xem [`docs/PARITY_IJFW.md`](docs/PARITY_IJFW.md) để biết capability map và intentional differences.

## Giấy phép

Phát hành theo [MIT License](LICENSE) © [Vudovn](https://github.com/vudovn).
