# Cấu trúc nguồn và bộ dựng

Nạp khi lần đầu dựng bộ prototype, khi thêm màn hoặc khi sửa hành vi nút. Chi tiết loại hành vi và ví dụ nằm trong chú thích đầu `_gen/actions.py` và `_gen/interact.py`: đọc ở đó, không lặp lại ở đây.

### Gốc prototype

1. Dò bộ dựng có sẵn: `Glob` tìm `**/_gen/interact.py` (bỏ `node_modules`, `.git`). **Thấy** thì thư mục cha của `_gen/` là gốc prototype. Dùng nguyên bộ dựng của project, **không ghi đè bất kỳ file nào trong `_gen/`**. Lệnh dựng lấy từ README hoặc `CLAUDE.md` của project, không có thì `python <gốc>/_gen/interact.py <màn>`. Thấy nhiều gốc thì hỏi chọn.
2. **Không thấy** thì gốc mặc định là `./docs/prototype/`. Tạo thư mục nếu chưa có (`mkdir -p docs/prototype`), rồi chép bộ dựng mẫu cạnh `SKILL.md` của skill này mà không ghi đè: `cp -rn "<gốc skill>/templates/_gen" docs/prototype/_gen`, trong đó `<gốc skill>` là thư mục gốc của skill (dòng *Base directory for this skill* mà Claude Code hiện khi nạp skill), cũng là thư mục chứa `SKILL.md` này. Không tìm thấy `templates/_gen` thì dừng và báo, không tự viết lại bộ dựng. Tạo thêm `_gen/orig/`, `_gen/frag/` (nếu thiếu).
3. Bộ dựng mẫu chỉ dùng thư viện chuẩn của Python 3. Máy không có Python thì báo, không tự cài, rồi dừng ở bước dựng.

Các đường dẫn bên dưới (`docs/prototype/...`) tính từ gốc prototype; thay bằng gốc thật nếu khác.

### Thành phần

```text
docs/prototype/                  (gốc prototype)
├── _gen/                        nguồn chỉnh sửa chính thức
│   ├── orig/<màn>.dc.html       bố cục đầy đủ của màn
│   ├── frag/<màn>.html          phần giao diện riêng của màn, ghép vào khung chung
│   ├── frame.html               khung chung (header, sidebar, theme) cho màn dựng từ frag
│   ├── build.py                 ghép frag vào frame
│   ├── actions.py               hành vi của các nút, gắn theo CHỮ HIỂN THỊ của nút
│   ├── interact.py              ghép bố cục + hành vi thành màn hoàn chỉnh
│   ├── icons.py                 nút thao tác trong bảng -> icon
│   ├── check.py                 kiểm tra tổng hợp, chỉ đọc (dùng cho --check)
│   ├── lint_theme.py            rà lệch theme (gradient, bóng màu, bo góc, trọng số, màu ngoài token)
│   └── frag/system-design.html  màn System Design bắt buộc (xem references/system-design.md)
├── project/
│   ├── <màn>.dc.html            đầu ra, dùng để publish. Đừng sửa tay
│   └── canvas.json              danh mục màn hình trên canvas
├── .artifact.json               link canvas, phiên bản, băm các file đã publish
└── .theme.json                  theme của cả bộ (khi dùng --themes)
```

| Thành phần | Vai trò |
|---|---|
| `_gen/orig/<màn>.dc.html` | Bố cục đầy đủ của màn (màn có bố cục riêng, hoặc UI khôi phục từ `--revert-design`) |
| `_gen/frag/<màn>.html` + `frame.html` + `build.py` | Màn dùng khung chung: chỉ viết phần nội dung, tiêu đề khai báo bằng `<!--title: ...-->` ở đầu file |
| `<!--traces: UC-..., AC-...-->` | Mã UC/AC trong BRD mà màn thoả, đặt ngay dưới `title` (frag) hoặc đầu file (orig). Chỉ ghi khi có BRD (xem "Truy vết với BRD" trong `SKILL.md`). Bộ dựng không đọc dòng này; nó đi theo vào HTML đầu ra nhưng không hiện trên UI, nên chỉ chứa mã, không chứa ghi chú |
| `_gen/actions.py` | Khai báo hành vi: mở hộp thoại, ô nhập, bật/tắt vùng, thông báo, mô phỏng phản hồi sau thao tác, chuyển màn |
| `_gen/interact.py` | Gắn hành vi vào nút theo chữ hiển thị, bọc vùng ẩn/hiện, chèn hộp thoại và mã tương tác, đổi nút trong bảng thành icon, xuất HTML hoàn chỉnh cho từng màn |
| `_gen/icons.py` | Quy ước icon cho nút trong bảng (xem, sửa, xóa, tải về, sao chép, duyệt) |
| `project/<màn>.dc.html` | HTML đầu ra để publish |
| `project/canvas.json` | Khai báo màn trên canvas: tiêu đề, vị trí, kích thước, thứ tự, liên kết design system |
| `.artifact.json` | `{ "url": "...", "version": "...", "updated": "YYYY-MM-DD", "published": { "<màn>.dc.html": "<băm>" } }`. `published` do `interact.py --record` ghi |

**Hành vi tương tác (`actions.py`)** có các loại: `modal` (hộp thoại có ô nhập, kiểm tra bắt buộc, trạng thái đang xử lý, thông báo thành công hoặc lỗi), `confirm` (xác nhận thao tác nguy hiểm), `toggle` (bật/tắt vùng khai báo bằng `<!--region:tên-->...<!--/region-->`, thêm `hidden` sau tên để ẩn mặc định), `toast`, `goto` (chuyển màn), `close`. Chi tiết và ví dụ nằm trong chú thích đầu `actions.py`. Hành vi phức tạp hơn (sắp xếp, lọc, phân trang) thì viết `<script>` ngay trong nguồn.

**Nhãn nút là khóa liên kết.** Vì hành vi gắn theo chữ trên nút, đổi tên nút mà không đổi khóa trong `actions.py` sẽ làm mất tương tác. `interact.py` cảnh báo hai chiều: nút chưa có hành vi, và hành vi không khớp nút nào. `--strict` biến cảnh báo thành lỗi để dùng làm cổng trước khi publish. Cũng cảnh báo khi màn chưa được khai báo trong `canvas.json`.

**`project/canvas.json`.** Schema do canvas Artifact (loại Design) quy định, **không tự bịa**. Đã có file thì thêm mục cho màn mới bằng cách sao chép cấu trúc một mục sẵn có. Chưa có thì lấy schema từ hướng dẫn trả về khi tạo canvas lần đầu (xem publish.md). Thêm file HTML chưa đủ để thêm màn vào canvas: phải khai báo trong `canvas.json`.

### Nguyên tắc

1. **Một nguồn chỉnh sửa chính thức.** Sửa trong `_gen/`, dựng lại, publish. Không sửa trực tiếp `project/*.dc.html` hay HTML trên canvas vì lần dựng sau sẽ ghi đè.
2. **Tách giao diện khỏi hành vi.** Bố cục và fragment ở `orig/`, `frag/`; hành vi ở `actions.py`.
3. **Publish theo phần thay đổi.** Chỉ gửi màn đã đổi và giữ `canvas.json` đồng bộ với cấu trúc canvas.
4. **Không bỏ qua xung đột.** Máy chủ báo HTML trên canvas khác bản đã đọc thì đọc bản hiện tại, so sánh, xử lý trước khi publish lại.
5. **Theo dõi phiên bản.** Mỗi lần publish tạo một phiên bản mới; ghi lại sau khi xong.

## Dựng một màn

- Slug màn: chữ thường nối bằng `-`, cố định để màn giữ đúng chỗ. Slug đã có và brief là thiết kế mới thì hỏi ghi đè hay dùng slug mới (chạy tự động thì dùng slug mới, nêu rõ); chỉnh tiếp đúng màn đó thì không cần hỏi.
- Viết `_gen/orig/<màn>.dc.html` hoặc `_gen/frag/<màn>.html` (dùng khung chung), kèm dòng `<!--traces: ...-->` khi có BRD. Định dạng `.dc.html` và khung theo hướng dẫn của loại Design nếu đã có; chưa có thì HTML tự chứa (CSS trong `<style>`, thư viện chỉ nạp từ CDN cho phép: cdnjs, jsdelivr, unpkg).
- Bộ chưa có màn `system-design` thì dựng nó trước (xem `references/system-design.md`) để mọi màn dùng chung token và component trong `frame.html`.
- Khai báo hành vi của mọi nút trong `actions.py` theo đúng chữ trên nút. Nút chỉ minh họa kiểu dáng, không tương tác thì gắn `data-proto="skip"`. Nút trong bảng dùng nhãn có trong `icons.py` để thành icon.
- Dựng: `python3 docs/prototype/_gen/interact.py <màn>` (hoặc `--all`). Cảnh báo "nút chưa có hành vi" thì thêm hành vi; "hành vi không khớp nút" thì sửa khóa theo nhãn mới; "màn chưa có trong canvas.json" thì thêm mục vào `canvas.json`.
- Trước khi cho user xem hoặc publish: `python3 docs/prototype/_gen/check.py` (nút/hành vi, canvas, đầu ra cũ, lệch theme, UI sạch).

## Ô nhập kèm nút (i) và tooltip

Mọi ô nhập (text, textarea, select, search) dùng mẫu có sẵn trong `_gen/frame.html`:

```html
<div class="field">
  <div class="field-label"><label for="id">Tên ô</label>
    <span class="info"><button type="button" class="info-btn" aria-label="Gợi ý cho ô Tên ô" aria-describedby="id-tip">i</button>
    <span role="tooltip" id="id-tip">Gợi ý ngắn về nội dung cần nhập.</span></span></div>
  <input id="id" class="input">
</div>
```

- Tooltip hiện khi hover, focus bàn phím hoặc chạm; Esc hoặc bấm ra ngoài để đóng. Logic nằm ở CSS và script của khung, không cần khai báo trong `actions.py` (`interact.py` bỏ qua nút `.info-btn`).
- Nội dung tooltip là chữ ngắn của sản phẩm (một câu, nêu nội dung cần nhập hoặc ví dụ), không phải đoạn mô tả tính năng. `id` của tooltip phải duy nhất trong màn.
- Thẻ tùy chọn gập: chỉ ẩn **ô nhập**, giữ hàng nhãn có (i). Không đặt nhãn và (i) trong vùng `<!--region:... hidden-->`. Mẫu chạy được ở màn `system-design` (`data-sd-fold`).
- Checkbox, radio, toggle không có (i) theo mặc định; thêm khi user yêu cầu.
