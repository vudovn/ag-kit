# Thư mục Kỹ năng (Skills Directory)

**Chào mừng đến với thư mục Kỹ năng!** Đây là nơi tập hợp tất cả 179+ kỹ năng AI chuyên biệt.

## 🤔 Kỹ năng là gì?

Kỹ năng là các bộ hướng dẫn chuyên biệt dạy trợ lý AI cách xử lý các tác vụ cụ thể. Hãy nghĩ về chúng như các module kiến thức chuyên gia mà AI của bạn có thể tải theo yêu cầu.

**Hình dung đơn giản:** Giống như bạn có thể tham khảo ý kiến các chuyên gia khác nhau (một nhà thiết kế, một chuyên gia bảo mật, một chuyên gia Marketing), các kỹ năng cho phép AI trở thành chuyên gia trong các lĩnh vực khác nhau ngay khi bạn cần.

---

## 📂 Cấu trúc Thư mục

Mỗi kỹ năng nằm trong thư mục riêng với cấu trúc sau:

```
skills/
├── skill-name/              # Thư mục kỹ năng riêng lẻ
│   ├── SKILL.md             # Định nghĩa kỹ năng chính (bắt buộc)
│   ├── scripts/             # Scripts hỗ trợ (tùy chọn)
│   ├── examples/            # Ví dụ sử dụng (tùy chọn)
│   └── resources/           # Templates & tài nguyên (tùy chọn)
```

**Lưu ý quan trọng:** Chỉ file `SKILL.md` là bắt buộc. Mọi thứ khác là tùy chọn!

---

## Cách sử dụng Kỹ năng

### Bước 1: Đảm bảo kỹ năng đã được thiết lập
Các file kỹ năng nên nằm trong thư mục `.agent/skills/` của bạn (hoặc `.claude/skills/`, `.gemini/skills/`, v.v.)

### Bước 2: Kích hoạt kỹ năng trong cuộc trò chuyện với AI
Sử dụng biểu tượng `@` theo sau bởi tên kỹ năng:

```
@brainstorming giúp tôi thiết kế một ứng dụng todo
```

hoặc

```
@stripe-integration thêm xử lý thanh toán vào ứng dụng của tôi
```

### Bước 3: AI trở thành chuyên gia
AI tải kiến thức của kỹ năng đó và giúp bạn với chuyên môn đặc thù!

---

## Tìm kiếm Kỹ năng

### Cách 1: Duyệt thư mục này
```bash
ls skills/
```

### Cách 2: Tìm kiếm theo từ khóa
```bash
ls skills/ | grep "từ khóa"
```

### Cách 3: Kiểm tra README chính
Xem [README chính](../README.vi.md) để biết danh sách đầy đủ tất cả 179+ kỹ năng được tổ chức theo danh mục.

---

## 💡 Các Kỹ năng Phổ biến để Thử nghiệm

**Cho người mới bắt đầu:**
- `@brainstorming` - Thiết kế trước khi code
- `@systematic-debugging` - Sửa lỗi một cách có phương pháp
- `@git-pushing` - Commit với thông báo tốt

**Cho lập trình viên:**
- `@test-driven-development` - Viết test trước
- `@react-best-practices` - Các mẫu React hiện đại
- `@senior-fullstack` - Phát triển Full-stack

**Cho bảo mật:**
- `@ethical-hacking-methodology` - Cơ bản về bảo mật
- `@burp-suite-testing` - Kiểm thử bảo mật ứng dụng web

---

## Tạo Kỹ năng Riêng của Bạn

Muốn tạo một kỹ năng mới? Hãy xem:
1. [CONTRIBUTING.vi.md](../docs/vietnamese/CONTRIBUTING.vi.md) - Cách đóng góp
2. [docs/vietnamese/SKILL_ANATOMY.vi.md](../docs/vietnamese/SKILL_ANATOMY.vi.md) - Hướng dẫn cấu trúc kỹ năng
3. `@skill-creator` - Sử dụng kỹ năng này để tạo kỹ năng mới!

---

## Tài liệu Tham khảo

- **[Bắt đầu](../docs/vietnamese/GETTING_STARTED.vi.md)** - Hướng dẫn bắt đầu nhanh
- **[Ví dụ](../docs/vietnamese/EXAMPLES.vi.md)** - Ví dụ sử dụng thực tế
- **[FAQ](../docs/vietnamese/FAQ.vi.md)** - Các câu hỏi thường gặp
- **[Hướng dẫn Trực quan](../docs/vietnamese/VISUAL_GUIDE.vi.md)** - Biểu đồ và lưu đồ

---

**Cần trợ giúp?** Kiểm tra [FAQ](../docs/vietnamese/FAQ.vi.md) hoặc mở một issue trên GitHub!
