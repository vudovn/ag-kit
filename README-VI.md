<p align="center">
  <img src="https://raw.githubusercontent.com/vudovn/ag-kit/main/web/public/images/logo.png" width="128" height="128" alt="AGKIT">
</p>

<h1 align="center">AG KIT</h1>

<p align="center">
    Bộ template AI Agent đi kèm Skills, Agents, và Workflows — tích hợp sẵn Coordinator Mode, Bộ nhớ Dài hạn (Persistent Memory), và Nén Ngữ cảnh (Context Compression).
</p>

<div align="center">
    <a href="https://unikorn.vn/p/antigravity-kit?ref=unikorn" target="_blank"><img src="https://unikorn.vn/api/widgets/badge/antigravity-kit?theme=dark" alt="AG Kit - Nổi bật trên Unikorn.vn" style="width: 210px; height: 54px;" width="210" height="54" /></a>
    <a href="https://trendshift.io/repositories/21490" target="_blank"><img src="https://trendshift.io/api/badge/repositories/21490" alt="vudovn%2Fantigravity-kit | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
    <a href="https://launch.j2team.dev/products/antigravity-kit" target="_blank"><img src="https://launch.j2team.dev/badge/antigravity-kit/dark" alt="AG Kit on J2TEAM Launch" width="250" height="54" /></a>
</div>

<p align="center">
  <strong>🇬🇧 <a href="./README.md">English Version (Bản Tiếng Anh)</a></strong>
</p>

---

## ⚡ Bắt đầu nhanh

Cài đặt và khởi tạo AG Kit để tích hợp thư mục cấu hình chuyên sâu `.agent/` trực tiếp vào dự án cục bộ của bạn.

### Cách 1: Chạy trực tiếp (Khuyên dùng)

```bash
npx @vudovn/ag-kit init
```

### Cách 2: Cài đặt toàn cục (Global)

```bash
npm install -g @vudovn/ag-kit
ag-kit init
```

---

## 🌍 Cấu hình Symlink Toàn cục (Global Shared Setup)

Nếu bạn làm việc trên nhiều dự án khác nhau và muốn tránh sao chép thư mục `.agent/` lặp đi lặp lại, bạn có thể tập trung hóa cấu hình AG Kit và sử dụng các liên kết tượng trưng (Symbolic Links).

1. **Cài đặt tập trung** (ví dụ: tạo thư mục toàn cục tại `~/.ag-kit`):
   ```bash
   mkdir -p ~/.ag-kit && cd ~/.ag-kit
   npx @vudovn/ag-kit init
   ```

2. **Liên kết cục bộ** từ thư mục gốc của dự án bạn đang làm việc:
   - **macOS / Linux:**
     ```bash
     ln -s ~/.ag-kit/.agent .agent
     ```
   - **Windows (CMD - Chạy với quyền Administrator):**
     ```cmd
     mklink /D .agent "%USERPROFILE%\.ag-kit\.agent"
     ```
   - **Windows (PowerShell - Chạy với quyền Administrator):**
     ```powershell
     New-Item -ItemType SymbolicLink -Path ".agent" -Target "$env:USERPROFILE\.ag-kit\.agent"
     ```

---

## ⚠️ Lưu ý Quan trọng về `.gitignore`

Nếu bạn đang sử dụng các trình soạn thảo mã nguồn tích hợp sẵn AI (như **Cursor** hoặc **Windsurf**), việc thêm thư mục `.agent/` vào file `.gitignore` sẽ khiến trình phân tích ngôn ngữ của trình soạn thảo không thể lập chỉ mục (index) các workflow. Điều này sẽ làm mất tính năng gợi ý tự động (autocomplete) cho các lệnh slash (ví dụ: `/plan`, `/debug`).

### Giải pháp tối ưu:
Để thư mục `.agent/` vừa không bị đẩy lên Git remote, vừa giữ nguyên khả năng hỗ trợ đắc lực từ AI editor:
1. Đảm bảo thư mục `.agent/` **KHÔNG** nằm trong file `.gitignore` của dự án.
2. Thay vào đó, hãy thêm `.agent/` vào file loại trừ cục bộ của Git: `.git/info/exclude`

---

## 📦 Các thành phần đi kèm

AG Kit đóng gói sẵn kho tri thức chuyên sâu cho từng domain cụ thể, các vai trò Agent chuyên biệt, và các quy trình phát triển tự động hóa tối ưu cho các công cụ lập trình AI hiện đại.

| Thành phần | Số lượng | Mô tả |
| :--- | :--- | :--- |
| **Agents** | 20 | Các chuyên gia AI độc lập (Frontend, Backend, Security, PM, QA, v.v.) |
| **Skills** | 45 | Các mô-đun tri thức chuyên sâu đi kèm các quy tắc kích hoạt tự động |
| **Workflows** | 13 | Quy trình tương tác tự động hóa lập trình viên (lệnh Slash) |

---

## 🛠️ Hướng dẫn Sử dụng

### 1. Cơ chế Tự động Điều hướng Agent (Zero-Setup)

Bạn không cần chỉ định Agent một cách thủ công. Hệ thống sẽ tự động phân tích yêu cầu của bạn, điều hướng thông minh đến đúng chuyên gia phù hợp và áp dụng các nguyên tắc lập trình của họ ngay lập tức:

```
You: "Thêm xác thực JWT vào API đăng nhập"
Agent: Applying @security-auditor + @backend-specialist...

You: "Căn giữa nút thanh toán và sửa lỗi giao diện tối"
Agent: Using @frontend-specialist...
```

### 2. Các Quy trình Tương tác (Slash Commands)

Thực hiện các quy trình phát triển mã nguồn bài bản bằng cách gõ trực tiếp các lệnh slash trong khung trò chuyện với AI:

| Lệnh | Mô tả chi tiết |
| :--- | :--- |
| `/brainstorm` | Lên ý tưởng, phân tích kiến trúc và giải pháp tối ưu trước khi viết code |
| `/coordinate` | Điều phối song song nhiều Agent chuyên gia cho các tác vụ kiểm tra phức tạp |
| `/create` | Tạo mới một tính năng hoặc xây dựng toàn bộ ứng dụng từ đầu |
| `/debug` | Kích hoạt quy trình gỡ lỗi chuyên sâu và có bằng chứng xác thực |
| `/deploy` | Thực hiện các kiểm tra an toàn pre-flight và triển khai lên production |
| `/enhance` | Thêm mới hoặc cải tiến các tính năng trong codebase hiện tại một cách an toàn |
| `/plan` | Lập kế hoạch chi tiết và tạo checklist triển khai công việc |
| `/preview` | Khởi động, dừng hoặc kiểm tra trạng thái máy chủ xem trước cục bộ |
| `/remember` | Ghi nhớ các quy chuẩn riêng của dự án vào bộ nhớ dài hạn |
| `/status` | Báo cáo chi tiết tiến độ công việc đang chạy của AI |
| `/test` | Tự động tạo và thực thi các bộ kiểm thử (test suite) toàn diện |
| `/verify` | Chứng minh code hoạt động thông qua chạy thực tế thay vì chỉ kiểm tra lý thuyết |

---

## 🧠 Triết lý Kiến trúc Cốt lõi

AG Kit được xây dựng dựa trên các mô hình thiết kế AI Agent đã qua kiểm chứng thực tế, giúp giảm lượng tiêu thụ token từ **13% đến 33%** đồng thời cải thiện chất lượng phản hồi:

*   **Coordinator Mode:** Cơ chế điều phối đa tác vụ song song, tránh việc thử lại tuần tự tốn kém tài nguyên.
*   **Bộ nhớ Dài hạn (Persistent Memory):** Cơ chế phân loại và lập chỉ mục qua `MEMORY.md`, loại bỏ việc phải giải thích lại các quy tắc dự án trong mỗi phiên chat mới.
*   **Nén Ngữ cảnh (Context Compression):** Tự động tóm tắt và thu gọn dữ liệu lịch sử để ngăn chặn hiện tượng tràn bộ nhớ trong các phiên làm việc kéo dài.
*   **Kích hoạt Skill có Điều kiện:** Chỉ tải các nguyên tắc lập trình có liên quan đến ngữ cảnh hiện tại nhờ cấu hình frontmatter thông minh, giữ cho cửa sổ ngữ cảnh luôn nhẹ nhàng nhất.

---

## 📚 Tham chiếu & Bản quyền

AG Kit là sản phẩm nghiên cứu và phát triển độc lập trong lĩnh vực kỹ nghệ prompt và luật thiết kế markdown. Dự án được tối ưu hóa dựa trên việc phân tích các mô hình AI Agent hàng đầu trong môi trường production:
*   *Không sao chép bất kỳ mã nguồn hay file bảo mật thương mại nào.*
*   Toàn bộ mã nguồn, cấu hình và kịch bản đều là phiên bản viết mới hoàn toàn, được phân phối dưới dạng mã nguồn mở theo giấy phép MIT.

---

## ☕ Ủng hộ Dự án

Nếu AG Kit giúp cho tiến trình lập trình với AI của bạn hiệu quả và năng suất hơn, hãy ủng hộ nhà phát triển:

| ☕ Ủng hộ & Quyên góp | 🚀 Đồng Support |
| :---: | :---: |
| <a href="https://buymeacoffee.com/vudovn" target="_blank"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee" /></a><br/><br/>**Ngân hàng Việt Nam (MBBank QR):**<br/><img src="https://img.vietqr.io/image/mbbank-0779440918-compact.jpg" alt="Donate QR" width="140" style="border-radius: 8px; margin-top: 10px;" /> | **Địa chỉ Hợp đồng donation (CA):**<br/><br/>`Gjpatn3d24dCRhUng7F37K6xJba4R8SDBC18xs1Apump`<br/><br/>*Sao chép địa chỉ CA ở trên để giao dịch trực tiếp trên Raydium, Jupiter, hoặc các sàn DEX donation khác.* |

---

## 📄 Giấy phép

Được phát hành dưới [Giấy phép MIT](LICENSE) © [Vudovn](https://github.com/vudovn).
