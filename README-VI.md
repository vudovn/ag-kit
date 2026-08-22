<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AG Kit">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
  Bộ công cụ kỹ nghệ AI Agent ưu tiên Antigravity, gồm rules, skills, agent chuyên môn, workflows, bộ nhớ dài hạn, hướng dẫn MCP, điều phối và native safety hook.
</p>

<div align="center">
  <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="AG Kit trên Unikorn.vn" width="210" height="54" /></a>
  <a href="https://trendshift.io/repositories/21490" target="_blank"><img src="https://trendshift.io/api/badge/repositories/21490" alt="AG Kit trên Trendshift" width="250" height="55" /></a>
  <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="AG Kit trên J2TEAM Launch" width="250" height="54" /></a>
</div>

<p align="center">
  <strong>Runtime production chính: Google Antigravity</strong><br/>
  <a href="./README.md">English</a> · <a href="./MIGRATION.md">Hướng dẫn migration</a> · <a href="./PRODUCTION_CHECKLIST.md">Checklist production</a> · <a href="./SECURITY.md">Bảo mật</a>
</p>

---

## Hồ sơ production

AG Kit cài một workspace contract hoàn chỉnh trong `.agents/`. Antigravity là runtime được hỗ trợ chính thức cho production trong bản phát hành này. Các công cụ khác có thể đọc nội dung Markdown, nhưng hành vi runtime ngoài Antigravity không nằm trong cam kết tương thích production.

| Năng lực | Cách triển khai production |
| --- | --- |
| Khám phá rules và skills | `.agents/rules/`, `.agents/skills/`, `.agents/workflows/` |
| Điều hướng chuyên gia | 20 agent chuyên môn và intelligent-routing skills |
| Ngữ cảnh dài hạn | `.agents/memory/` và hướng dẫn context compression |
| Điều phối | `/coordinate`, `/orchestrate`, `/agents` và `/tasks` của Antigravity |
| MCP | Cấu hình workspace cùng công cụ đồng bộ có review và backup |
| An toàn tool | Native `PreToolUse` gate cho các lệnh phá hủy có độ chắc chắn cao |
| Đóng gói | Plugin bundle cục bộ kèm inventory SHA-256 |
| Xác thực | Toolkit CI, Antigravity Doctor, regression tests, Dependency Review, CLI và web checks |

Safety hook được thiết kế hẹp: chặn xóa filesystem root, format ổ đĩa và ghi đè raw disk, nhưng vẫn cho phép cleanup thông thường như xóa `dist/` hoặc `node_modules/`. Hook không thay thế permission, workspace trust, sandbox hay phê duyệt của người dùng trong Antigravity.

## Yêu cầu

- Node.js 22 trở lên cho tooling Antigravity ở cấp repository.
- Python 3.10 trở lên cho validator và utility scripts.
- Workspace Google Antigravity đáng tin cậy.
- Git để cập nhật, review và rollback an toàn.

CLI được publish hiện hỗ trợ Node.js 18 trở lên; bộ kiểm tra Antigravity chạy trên Node.js 22.

## Bắt đầu nhanh

### Cài vào dự án

```bash
npx @vudovn/ag-kit init
```

Hoặc cài CLI toàn cục:

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

Không thêm `.agents/` vào `.gitignore` khi cần Antigravity index rules, skills và workflows. Để giữ thư mục này ở local mà không tắt discovery, thêm `.agents/` vào `.git/info/exclude`.

### Kiểm tra workspace

```bash
npm run check:agents
npm run check:antigravity
npm run test:antigravity
```

`check:antigravity` chỉ đọc, không thay đổi file. MCP example mặc định chứa `YOUR_API_KEY`, vì vậy doctor thông thường sẽ cảnh báo cho đến khi placeholder được cấu hình. Chỉ dùng strict mode sau khi đã xử lý toàn bộ placeholder:

```bash
node .agents/hooks/antigravity-doctor.mjs --strict
```

### Mở bằng Antigravity

Sau khi mở repository dưới dạng trusted workspace:

1. Xác nhận các slash command như `/plan`, `/coordinate`, `/orchestrate` được nhận diện.
2. Xác nhận skill phù hợp được chọn từ `.agents/skills/`.
3. Chạy một lệnh bình thường như `npm test` và kiểm tra lệnh được cho phép.
4. Kiểm tra safety hook bằng payload giả lập, không chạy lệnh phá hủy thật:

```bash
printf '%s' '{"tool_args":{"CommandLine":"rm -rf /"}}' \
  | node .agents/hooks/validate-tool-call.mjs
```

Lệnh phải trả exit code khác 0 và in `BLOCKED by AG Kit`.

## Cập nhật an toàn và rollback

AG Kit cập nhật theo cơ chế merge-aware. File do người dùng sở hữu và file managed đã sửa cục bộ được giữ nguyên theo mặc định.

```bash
ag-kit update --dry-run          # Xem chính xác kế hoạch cập nhật
ag-kit update                    # Merge an toàn và tạo backup
ag-kit update --strategy replace # Thay toàn bộ có chủ đích, vẫn tạo backup
ag-kit rollback                  # Khôi phục backup gần nhất
```

Metadata được lưu trong `.agents/.ag-kit/`; backup nằm tại `.ag-kit-backups/`, bên ngoài managed toolkit tree. Đọc [MIGRATION.md](MIGRATION.md) trước khi nâng một bản cài đặt cũ lên bản Antigravity-native.

## Tích hợp Antigravity native

### Runtime contract

`.agents/antigravity.json` khai báo sáu giai đoạn tích hợp và các capability Antigravity CLI mà AG Kit sử dụng. File này không tự đặt một minimum semantic version khi tài liệu upstream chưa công bố version floor rõ ràng.

### Native safety hook

Antigravity đọc `.agents/hooks.json` và đăng ký:

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

Để tạm tắt hook khi điều tra lỗi tương thích, đặt `"enabled": false`, mở lại workspace và báo cáo payload theo kênh riêng nếu có thể chứa dữ liệu nhạy cảm. Không xóa permission controls của Antigravity.

### Cấu hình MCP

Xem kế hoạch merge mà không ghi vào home directory:

```bash
node .agents/hooks/sync-mcp.mjs --check
node .agents/hooks/sync-mcp.mjs --print
```

Sau khi thay placeholder, áp dụng rõ ràng vào một target:

```bash
node .agents/hooks/sync-mcp.mjs --apply --target suite
node .agents/hooks/sync-mcp.mjs --apply --target cli
```

Server trùng tên được giữ nguyên trừ khi dùng `--force`. Công cụ tạo backup có timestamp trước khi thay đổi target đã tồn tại. Không commit credential MCP thật.

Chọn riêng một server đã sẵn sàng khi ví dụ khác vẫn còn placeholder:

```bash
node .agents/hooks/sync-mcp.mjs --print --server xquik
node .agents/hooks/sync-mcp.mjs --apply --target suite --server xquik
```

Mục Xquik dùng cơ chế khám phá OAuth từ xa. Nó hỗ trợ quy trình thu thập bằng chứng X công khai, có giới hạn của Skill `deep-research`.

### Build và kiểm tra plugin

```bash
npm run build:antigravity-plugin
```

Review `dist/antigravity-plugin/` trước khi cài. Bundle gồm skills, agents, rules, workflow commands đã chuyển đổi, native hook, MCP example và `PLUGIN_CONTENTS.json` chứa SHA-256.

```bash
agy plugin install ./dist/antigravity-plugin
agy plugin list
```

Cài plugin là tùy chọn; `.agents/` trong repository vẫn là source of truth của dự án.

## Thành phần đi kèm

| Thành phần | Số lượng | Mục đích |
| --- | ---: | --- |
| Agents | 20 | Vai trò chuyên môn và điều phối |
| Skills | 48 | Tri thức domain tải theo nhu cầu và helper có thể chạy |
| Workflows | 13 | Quy trình slash command lặp lại được |
| Rules | 6 | Ràng buộc routing, safety, design và coding toàn workspace |
| Memory topics | 4 topic bắt buộc cùng index | Quy ước, quyết định, preference và feedback dài hạn |

Mỗi agent, skill, workflow và rule có hợp đồng SemVer. `.agents/manifest.json`, `.agents/manifest.lock.json` và `.agents/DEPENDENCY_GRAPH.md` giúp toolkit có thể tái tạo và phát hiện drift.

```bash
npm run generate:agents
npm run check:agents
```

## Workflows thường dùng

| Lệnh | Mục đích |
| --- | --- |
| `/brainstorm` | Phân tích phương án và kiến trúc trước khi code |
| `/coordinate` | Chạy song song các tác vụ research/review có thể tách rời rồi tổng hợp |
| `/create` | Tạo tính năng hoặc ứng dụng theo các gate có cấu trúc |
| `/debug` | Phân tích nguyên nhân gốc dựa trên bằng chứng |
| `/deploy` | Thực hiện pre-flight và quy trình triển khai production |
| `/enhance` | Thay đổi codebase hiện tại một cách an toàn |
| `/orchestrate` | Lập kế hoạch, xin phê duyệt, giao việc và verify |
| `/plan` | Tạo kế hoạch và checklist triển khai |
| `/preview` | Quản lý preview server cục bộ |
| `/remember` | Lưu thông tin bền vững vào memory |
| `/status` | Tóm tắt công việc và blocker |
| `/test` | Thiết kế và chạy kiểm thử |
| `/verify` | Chứng minh thay đổi bằng thực thi thay vì chỉ đọc code |

## Gate release và production

Release candidate chưa được xem là production-approved cho đến khi toàn bộ automated checks và smoke test Antigravity trong [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) hoàn tất.

Các GitHub check bắt buộc:

- Toolkit validation
- CLI tests and package validation
- Web lint, typecheck, build, and audit
- Antigravity native contract
- Dependency Review

AG Kit không yêu cầu auto-merge, auto-deploy hay tự động đồng bộ MCP. Thay đổi production phải có thể review và rollback.

## Tài liệu

- [Chi tiết tích hợp Antigravity](.agents/hooks/README.md)
- [Hướng dẫn migration](MIGRATION.md)
- [Checklist phát hành production](PRODUCTION_CHECKLIST.md)
- [Security policy và runtime threat model](SECURITY.md)
- [Kiến trúc luồng agent](AGENT_FLOW.md)
- [Kiến trúc toolkit](.agents/ARCHITECTURE.md)
- [Changelog](CHANGELOG.md)
- [Cấu hình release](.github/RELEASE_SETUP.md)

## Tham chiếu và bản quyền

AG Kit là triển khai mã nguồn mở nguyên bản của các mô hình kỹ nghệ agent dựa trên Markdown. Dự án không chứa source file độc quyền. Quyết định tích hợp runtime dựa trên tài liệu và codelab Antigravity công khai được liên kết trong [.agents/hooks/README.md](.agents/hooks/README.md).

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
