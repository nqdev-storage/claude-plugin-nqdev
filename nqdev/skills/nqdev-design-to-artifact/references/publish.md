# Publish, gỡ canvas và theo dõi phiên bản

Nạp khi có `--publish`, `--unpublish`, hoặc `--update`.

## Dừng ở local (mặc định) hoặc publish (chỉ khi có `--publish`)

**Không có `--publish`:** kết thúc ở đây, **không gọi `Artifact`**. Đưa đường dẫn `project/<màn>.dc.html`, tóm tắt 1–2 câu, nhắc chỉnh tiếp hoặc chạy lại với `--publish`. Yêu cầu chỉnh thì quay lại sửa nguồn.

**Có `--publish`** (là sự đồng ý của user, không hỏi lại). Màn phải đã dựng và qua kiểm tra (`check.py`, hoặc `interact.py --all --strict` sạch). Không có brief và không `--revert-design` thì publish những gì đã dựng sẵn; chưa có màn nào thì báo và gợi ý tạo trước.

1. **Xác định canvas đích:** `--update=<url>` → `url` đã lưu trong `.artifact.json` → chưa có.
2. **Chưa có canvas (lần đầu):** gọi `Artifact` với `action: "quickstart"`, `intent: "design"`; chọn loại **Design** trong danh sách (`list`, `scope: "types"`); tạo bằng `type_url` + `title` (tên project) + `auto_open: "after_first_write"`; đọc hướng dẫn trả về (định dạng `.dc.html`, schema `canvas.json`, design system) và chỉnh nguồn/khung/`canvas.json` cho khớp nếu cần, dựng lại; rồi publish vào `url` vừa tạo với `file_path` = `<gốc>/project/canvas.json`, `root` = `<gốc>`, `files` = **tất cả** `project/*.dc.html`. Ghi `url` vào `.artifact.json`. Session không liệt kê loại Design thì nói rõ, dừng ở local và hỏi user có muốn một trang HTML tổng hợp các màn để publish như artifact thường không.
3. **Đã có canvas (cập nhật từng phần):** nếu cuộc hội thoại này chưa đọc hay publish artifact đó thì `read` nó trước (công cụ bắt buộc). Lấy danh sách màn đã đổi bằng `python3 docs/prototype/_gen/interact.py --changed` (bộ dựng của project không có `--changed` thì so băm với `published` trong `.artifact.json`, hoặc dùng `git status` trên `project/`). Publish với:

| Tham số | Giá trị |
|---|---|
| `url` | canvas hiện có |
| `file_path` | `<gốc>/project/canvas.json` |
| `root` | `<gốc>` |
| `files` | **chỉ** các `project/*.dc.html` đã đổi (đường dẫn tương đối `root`, không có `/` đầu) |

   File không gửi giữ nguyên bản đang có trên máy chủ. Không bao giờ dùng `force`.
4. **Xung đột:** máy chủ từ chối kèm bản hiện tại, hoặc HTML trên canvas khác bản đã đọc. `read` bản hiện tại, so với bản dựng. Phân biệt **khác biệt do bộ dựng sinh ra** (khối giữa `<!--proto:begin-->` và `<!--proto:end-->`, bỏ qua) với **chỉnh sửa thật của người dùng trên canvas** (đưa ngược vào nguồn `_gen/` rồi dựng lại, không để bị ghi đè). Không chắc là gì thì hỏi user. Xử lý xong mới publish lại.
5. **Lỗi `page must be .html`** (hoặc bị từ chối kiểu publish của Design): thường do phiên đang đăng nhập khác tài khoản sở hữu canvas, nên công cụ coi canvas thuộc tài khoản/tổ chức khác. Kiểm tra tài khoản đang đăng nhập và quyền truy cập canvas, đăng nhập đúng tài khoản sở hữu rồi publish lại như bình thường. **Không tự tạo canvas mới** và không gợi ý cách host ở nơi khác. Phân biệt với lỗi xung đột phiên bản (mục 4).
6. **Sau khi publish xong:**
   - `python3 docs/prototype/_gen/interact.py --record` để ghi băm các màn đã đăng.
   - Ghi `version` (lấy từ kết quả publish nếu có) và `updated` vào `.artifact.json`.
   - Project có tài liệu theo dõi phiên bản prototype (vd `docs/CONTEXT.md`, kế hoạch UX/UI) thì cập nhật số phiên bản ở chỗ đã có mục ghi; không thấy thì bỏ qua, không tự tạo file.
   - Kiểm tra trên bản đã đăng: mở artifact và thử các luồng tương tác bằng công cụ trình duyệt nếu có.
7. **Mặc định private:** không chia sẻ, không pin nếu user chưa yêu cầu.
8. Báo một câu: gửi bao nhiêu màn, **tạo mới** hay **cập nhật canvas đã có**, phiên bản. Không dán lại URL vì thẻ artifact đã có link.

**Fallback:** không có `Artifact` tool (OpenCode, hoặc session không bật) thì nói "chưa publish được ở đây", giao thư mục `project/` và hướng dẫn đưa lên khi có công cụ. Publish bị từ chối vì lý do khác thì báo lý do chính xác.

### Checklist mỗi lần cập nhật prototype
- [ ] Sửa nguồn trong `_gen/` (không sửa tay `project/` hay canvas)
- [ ] Cập nhật hành vi trong `actions.py`, nhãn nút khớp khóa
- [ ] Chạy bộ dựng, `--strict` sạch cảnh báo
- [ ] Cập nhật `canvas.json` (bắt buộc khi thêm màn mới)
- [ ] Đổi theme/token thì cập nhật `frame.html`, màn `system-design` và `docs/specs/ui-ux.md`, chạy `lint_theme.py`
- [ ] Kiểm tra HTML đầu ra và UI sạch
- [ ] Publish đúng canvas: đúng `url`, `root`, `canvas.json`, chỉ file đã đổi
- [ ] Xử lý xung đột nếu có
- [ ] Kiểm tra kết quả trên canvas, các tương tác chạy đúng
- [ ] Ghi băm, phiên bản và tài liệu theo dõi

## Chế độ `--unpublish` (gỡ canvas đã publish)

Dùng khi user muốn gỡ canvas khỏi Artifact. Nguồn vẫn còn nên có thể publish lại sau.

1. Đọc `docs/prototype/.artifact.json` lấy `url`. Không có `url` thì báo "chưa publish gì để gỡ" và dừng. Đi cùng `--publish` thì hỏi user muốn làm cái nào, không làm cả hai.
2. **Xác nhận trước** (dùng `AskUserQuestion` nếu có, không thì hỏi một câu): gỡ vĩnh viễn, link ngừng hoạt động với mọi người đã được chia sẻ; nguồn `_gen/` và `project/` được giữ. Chạy tự động (không hỏi được) thì **không gỡ**, báo lại và dừng, vì không hoàn tác được.
3. Gọi `Artifact` với `action: "delete"` và `url`. Lỗi (không có quyền, đã bị xóa) thì báo đúng lý do, không sửa `.artifact.json`.
4. Ghi `.artifact.json` thành `{"published": {}, "unpublished": "YYYY-MM-DD"}` (bỏ `url`, `version` vì canvas không còn; lần `--publish` sau sẽ tạo canvas mới theo mục publish ở trên).
5. **Giữ nguyên** `_gen/`, `project/`, `canvas.json`, `.theme.json`; không xóa file nào.
6. Cập nhật tài liệu của project có nhắc link canvas (README, `plans/`, `docs/`): `Grep` tìm `url` cũ, gỡ link hoặc đổi thành "đã gỡ ngày YYYY-MM-DD", chỉ sửa đúng dòng nhắc link. Liệt kê các file đã sửa.
7. Báo một câu: đã gỡ canvas, nguồn còn nguyên, `--publish` để đưa lên lại.
