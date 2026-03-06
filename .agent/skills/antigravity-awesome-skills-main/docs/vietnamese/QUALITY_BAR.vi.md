# 🏆 Tiêu chuẩn Chất lượng & Xác thực

Để biến **Antigravity Awesome Skills** từ một tập hợp các script thành một nền tảng đáng tin cậy, mỗi skill (kỹ năng) phải đáp ứng một tiêu chuẩn cụ thể về chất lượng và an toàn.

## Huy hiệu "Đã xác thực" (Validated) ✅

Một skill chỉ nhận được huy hiệu "Đã xác thực" nếu nó vượt qua **5 bước kiểm tra tự động** sau:

### 1. Tính toàn vẹn của siêu dữ liệu (Metadata Integrity)

Phần frontmatter trong `SKILL.md` phải là mã YAML hợp lệ và chứa:

- `name`: Định dạng Kebab-case, khớp với tên thư mục.
- `description`: Dưới 200 ký tự, nêu rõ giá trị mang lại.
- `risk`: Thuộc một trong các loại `[none, safe, critical, offensive]`.
- `source`: URL dẫn đến nguồn gốc (hoặc "self" nếu là nội dung gốc).

### 2. Điều kiện kích hoạt rõ ràng ("Khi nào nên dùng")

Skill BẮT BUỘC phải có một phần nêu rõ thời điểm nên kích hoạt nó.

- **Tốt**: "Sử dụng khi người dùng yêu cầu debug (gỡ lỗi) một component React."
- **Tệ**: "Skill này giúp bạn xử lý code."

### 3. Phân loại An toàn & Rủi ro

Mỗi skill phải khai báo mức độ rủi ro của nó:

- 🟢 **none**: Chỉ là văn bản/tư duy thuần túy (ví dụ: Brainstorming).
- 🔵 **safe**: Đọc file, chạy các lệnh an toàn (ví dụ: Linter).
- 🟠 **critical**: Sửa đổi trạng thái, xóa file, push lên môi trường production (ví dụ: Git Push).
- 🔴 **offensive**: Các công cụ Pentesting/Red Team. **BẮT BUỘC** phải có cảnh báo "Chỉ dành cho mục đích sử dụng đã được cấp phép".

### 4. Ví dụ thực tế (Copy-Pasteable)

Ít nhất một khối code hoặc ví dụ tương tác mà người dùng (hoặc agent) có thể sử dụng ngay lập tức.

### 5. Giới hạn rõ ràng (Explicit Limitations)

Danh sách các trường hợp biên hoặc những việc mà skill _không thể_ thực hiện.

- _Ví dụ_: "Không hoạt động trên Windows nếu không có WSL."

---

## Các cấp độ Hỗ trợ

Chúng tôi cũng phân loại skill dựa trên người duy trì chúng:

| Cấp độ        | Huy hiệu | Ý nghĩa                                              |
| :------------ | :------- | :--------------------------------------------------- |
| **Official**  | 🟣       | Do đội ngũ cốt lõi duy trì. Độ tin cậy cao.          |
| **Community** | ⚪       | Do cộng đồng đóng góp. Hỗ trợ theo khả năng tốt nhất. |
| **Verified**  | ✨       | Skill cộng đồng đã vượt qua vòng kiểm duyệt thủ công chuyên sâu. |

---

## Cách Xác thực Skill của bạn

Chạy script xác thực trước khi gửi Pull Request (PR):

```bash
python3 scripts/validate_skills.py --strict
```
