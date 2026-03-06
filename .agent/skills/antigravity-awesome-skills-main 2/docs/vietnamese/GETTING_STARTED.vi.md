# Hướng dẫn Bắt đầu với Antigravity Awesome Skills (V4)

**Bạn mới đến đây? Hướng dẫn này sẽ giúp bạn tăng cường sức mạnh cho trợ lý trợ lý AI của mình chỉ trong 5 phút.**

---

## 🤔 "Skills" (Kỹ năng) là gì?

Các trợ lý AI (như **Claude Code**, **Gemini**, **Cursor**) rất thông minh, nhưng chúng thiếu kiến thức cụ thể về các công cụ và quy trình làm việc của bạn.  
**Skills** là các hướng dẫn sử dụng chuyên biệt (dưới dạng file markdown) dạy cho AI của bạn cách thực hiện các tác vụ cụ thể một cách hoàn hảo trong mọi lần thực hiện.

**Một phép so sánh:** AI của bạn là một thực tập sinh xuất sắc. **Skills** là các SOP (Quy trình vận hành tiêu chuẩn) biến họ thành một Kỹ sư cao cấp.

---

## ⚡️ Khởi động nhanh: Các "Gói khởi đầu" (Starter Packs)

Đừng lo lắng về con số hơn 560 kỹ năng. Bạn không cần dùng tất cả chúng cùng một lúc.  
Chúng tôi đã tuyển chọn các **Gói khởi đầu** để bạn có thể bắt đầu sử dụng ngay lập tức.

### 1. Cài đặt Repository

Sao chép các kỹ năng vào thư mục agent của bạn:

```bash
# Cài đặt phổ thông (hoạt động với hầu hết các agent)
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

### 2. Chọn vai trò của bạn

Tìm gói kỹ năng phù hợp với vị trí của bạn (xem [BUNDLES.md](BUNDLES.vi.md)):

| Vai trò               | Tên Gói kỹ năng | Bên trong có những gì?                            |
| :-------------------- | :-------------- | :------------------------------------------------ |
| **Web Developer**     | `Web Wizard`    | React Patterns, Tailwind mastery, Frontend Design |
| **Security Engineer** | `Hacker Pack`   | OWASP, Metasploit, Pentest Methodology            |
| **Manager / PM**      | `Product Pack`  | Brainstorming, Planning, SEO, Strategy            |
| **Cơ bản cho tất cả** | `Essentials`    | Clean Code, Planning, Validation (Những thứ cơ bản nhất) |

---

## 🚀 Cách sử dụng một Skill

Sau khi cài đặt, bạn chỉ cần trò chuyện với AI một cách tự nhiên.

### Ví dụ 1: Lập kế hoạch cho một Tính năng (**Essentials**)

> "Sử dụng **@brainstorming** để giúp tôi thiết kế một luồng đăng nhập mới."

**Điều gì sẽ xảy ra:** AI sẽ tải kỹ năng brainstorming, đặt cho bạn các câu hỏi có cấu trúc và tạo ra một bản đặc tả chuyên nghiệp.

### Ví dụ 2: Kiểm tra Code của bạn (**Web Wizard**)

> "Chạy **@lint-and-validate** trên file này và sửa các lỗi."

**Điều gì sẽ xảy ra:** AI sẽ tuân theo các quy tắc linting nghiêm ngặt được định nghĩa trong skill để làm sạch code của bạn.

### Ví dụ 3: Kiểm tra Bảo mật (**Hacker Pack**)

> "Sử dụng **@api-security-best-practices** để xem xét các endpoint API của tôi."

**Điều gì sẽ xảy ra:** AI sẽ kiểm tra code của bạn dựa trên các tiêu chuẩn OWASP.

---

## 🔌 Các công cụ được hỗ trợ

| Công cụ          | Trạng thái      | Đường dẫn         |
| :--------------- | :-------------- | :---------------- |
| **Claude Code**  | ✅ Hỗ trợ đầy đủ | `.claude/skills/` |
| **Gemini CLI**   | ✅ Hỗ trợ đầy đủ | `.gemini/skills/` |
| **Antigravity**  | ✅ Hỗ trợ gốc   | `.agent/skills/`  |
| **Cursor**       | ✅ Hỗ trợ gốc   | `.cursor/skills/` |
| **Copilot**      | ⚠️ Chỉ văn bản  | Copy-paste thủ công |

---

## 🛡️ Sự tin cậy & An toàn (Mới trong bản V4)

Chúng tôi phân loại các kỹ năng để bạn biết mình đang chạy những gì:

- 🟣 **Official (Chính thức)**: Được duy trì bởi Anthropic/Google/Nhà cung cấp (Độ tin cậy cao).
- 🔵 **Safe (An toàn)**: Các kỹ năng cộng đồng không gây hại (Chỉ đọc/Lập kế hoạch).
- 🔴 **Risk (Rủi ro)**: Các kỹ năng sửa đổi hệ thống hoặc thực hiện kiểm thử bảo mật (Sử dụng khi được cấp phép).

_Kiểm tra [Danh mục Skill (Skill Catalog)](../CATALOG.vi.md) để xem danh sách đầy đủ._

---

## ❓ FAQ

**H: Tôi có cần cài đặt tất cả 560 kỹ năng không?**  
Đ: Bạn tải toàn bộ repo về, nhưng AI của bạn chỉ _đọc_ những kỹ năng bạn yêu cầu (hoặc những kỹ năng có liên quan). Nó rất nhẹ!

**H: Tôi có thể tự tạo kỹ năng cho riêng mình không?**  
Đ: Có! Sử dụng kỹ năng **@skill-creator** để tự xây dựng.

**H: Nó có miễn phí không?**  
Đ: Có, Giấy phép MIT. Mã nguồn mở mãi mãi.

---

## ⏭️ Các bước tiếp theo

1. [Duyệt qua các Gói kỹ năng (Bundles)](BUNDLES.vi.md)
2. [Xem các Ví dụ thực tế (Examples)](EXAMPLES.vi.md)
3. [Đóng góp một Skill mới](../CONTRIBUTING.vi.md)
