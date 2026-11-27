# trietnm-user-doc-writer

Quét source code của một phần mềm và viết tài liệu hướng dẫn sử dụng (user guide) bằng tiếng Việt cho người dùng cuối, có sẵn vị trí gợi ý chèn ảnh và ví dụ minh hoạ cho từng tính năng.

- **Phiên bản:** 1.0.0 · **Tác giả:** ViHAT · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- "Viết tài liệu hướng dẫn sử dụng", "tạo user guide", "soạn tài liệu HDSD", "viết user manual".
- "Viết tài liệu cho module X" hoặc "lên kế hoạch viết tài liệu người dùng".

Skill không gắn với tech stack nào: tự phát hiện ngôn ngữ, framework và cấu trúc thư mục. Tài liệu viết dưới góc nhìn người dùng cuối ("Nhấn nút **Lưu**"), không nhắc tên hàm, class, bảng cơ sở dữ liệu hay endpoint.

## Đầu vào / Đầu ra

Skill nhận một lệnh. Gọi không kèm lệnh thì skill in phần hướng dẫn rồi hỏi bạn chọn chế độ, không tự chạy tiếp.

| Lệnh | Việc làm | Quét source | Ghi file |
|---|---|---|---|
| `help` | In hướng dẫn sử dụng chính skill này | Không | Không |
| `plan` | Khảo sát source, liệt kê module / màn hình / tính năng chính, tạo hoặc cập nhật `DOC-PLAN.md`, `_style-guide.md`, `README.md` | Có | Có |
| `full` | Viết tài liệu cho toàn bộ phần mềm: chạy `plan` nếu chưa có, rồi viết lần lượt từng module | Có | Có |
| `module <tên hoặc slug>` | Viết hoặc cập nhật tài liệu cho một module | Có | Có |

Kết quả nằm ở `docs/user-guide/` (gốc dự án đang mở):

```text
docs/user-guide/
├── README.md          # mục lục, link tới từng module
├── _style-guide.md    # quy ước format và bảng thuật ngữ (nguồn sự thật)
├── DOC-PLAN.md        # danh sách module, trạng thái, nhật ký các đợt viết
├── images/            # ảnh chụp màn hình do bạn bổ sung theo placeholder
└── <module-slug>.md   # mỗi module một file
```

Mỗi mục tính năng gồm: mục đích và khi nào dùng, tiền điều kiện, các bước thao tác đánh số, ví dụ minh hoạ (dữ liệu mẫu và kết quả mong đợi), vị trí chèn ảnh, lỗi thường gặp và lưu ý. Vị trí chèn ảnh có dạng cố định:

```md
<!-- SCREENSHOT: Màn hình danh sách Đơn hàng | Gợi ý: khoanh đỏ nút "Tạo đơn hàng" -->
![Danh sách đơn hàng và nút tạo mới](./images/quan-ly-don-hang-01-danh-sach.png)
```

Ví dụ:

```text
/vhs:trietnm-user-doc-writer plan
/vhs:trietnm-user-doc-writer module Quản lý đơn hàng
/vhs:trietnm-user-doc-writer full
```

Quy trình khuyến nghị: `plan` để chốt danh sách và thứ tự module, rồi `module <A>` cho module quan trọng nhất, rồi các module còn lại; hoặc `full` nếu muốn làm một mạch.

## Cài đặt

Cài qua plugin: `claude plugin install vhs@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/trietnm-user-doc-writer/` | `~/.claude/skills/trietnm-user-doc-writer/` |
| OpenCode | `.opencode/skills/trietnm-user-doc-writer/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/trietnm-user-doc-writer/` |
| Gemini CLI | `.gemini/skills/trietnm-user-doc-writer/` (hoặc `.agents/skills/`) | `~/.gemini/skills/trietnm-user-doc-writer/` |
| Codex CLI | `.agents/skills/trietnm-user-doc-writer/` | `~/.agents/skills/trietnm-user-doc-writer/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- Skill không khai báo `allowed-tools`: quyền theo cấu hình của từng tool. Tự kích hoạt được khi yêu cầu khớp mô tả.
- Skill cần quét source và ghi file vào `docs/user-guide/`, nên dùng trên tool có truy cập repo. **Claude.ai** thường không có repo.

## Giới hạn

- Mỗi đợt viết đọc lại `_style-guide.md` và `DOC-PLAN.md` trước khi viết, để các đợt nối nhau nhất quán về cấu trúc, giọng văn và thuật ngữ. Muốn đổi cấu trúc thì cập nhật style guide trước, các module cũ rà lại sau.
- Phần nào chưa chắc thì ghi vào cột "Ghi chú" của `DOC-PLAN.md` thay vì đoán. Source quá lớn thì ưu tiên các màn hình có route hoặc menu rõ ràng.
- Chỉ tạo file trong `docs/user-guide/`; không tự commit, push.
- Ảnh chụp màn hình không được tạo: skill chỉ đặt placeholder, bạn tự chụp và bỏ vào `images/`.
- Toàn bộ nội dung bằng tiếng Việt, giữ nguyên thuật ngữ kỹ thuật khi cần.

## Cấu trúc

```text
trietnm-user-doc-writer/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── templates/
    ├── _style-guide.md   # quy ước format, copy vào docs/user-guide/ ở lần plan đầu
    ├── DOC-PLAN.md       # bảng theo dõi module và nhật ký
    ├── module.md         # khung một file module
    └── feature.md        # khung một mục tính năng
```
