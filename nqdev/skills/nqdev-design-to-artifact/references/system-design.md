# Màn System Design (bắt buộc)

Nạp khi khởi tạo bộ prototype, khi bộ chưa có màn `system-design`, khi đổi theme hoặc token, và khi bàn giao.

Mỗi bộ prototype **bắt buộc** có một màn độc lập **System Design** (slug `system-design`, nguồn `_gen/frag/system-design.html`, khai báo trong `canvas.json` như mọi màn). Đây là tài liệu tham chiếu quy chuẩn UI, nơi kiểm thử component và bàn giao kỹ thuật.

## Nguồn sự thật

- **Token và class component nằm trong `_gen/frame.html`** (biến CSS ở `:root`, dark mode, class `.t-*`, `.btn*`, `.input`, `.badge`, `.alert`, `.table`, `.skeleton`...). Mọi màn dùng khung chung dùng lại chúng.
- Màn System Design **chỉ hiển thị lại** các token và class đó: mã hex, thông số chữ và giá trị token được đọc bằng `getComputedStyle`, nên không ghi hex cứng trong màn. Đổi token chỉ sửa `frame.html` rồi dựng lại.
- Màn dùng nguồn `orig/` (bố cục riêng, không qua khung) thì phải dùng cùng tên biến token; kiểm bằng `lint_theme.py`.

## Nội dung bắt buộc (8 khối)

1. **Màu và design token**: Brand (Primary, Secondary, Accent, mỗi màu có default, hover, active, nền nhạt); Neutrals (nền trang, surface, border, text primary, text secondary, muted); Semantic (success, warning, danger, info và nền nhạt); Elevation (`shadow-sm/md/lg/xl`); Border radius (`none, sm, md, lg, xl, full`).
2. **Typography**: font family; Display, H1–H6, Subtitle, Body Large/Regular/Small, Caption, Overline, mỗi cấp hiện văn bản mẫu kèm `font-size / line-height / font-weight`.
3. **Form controls**: Buttons (Primary, Secondary, Outline, Ghost, Link, Danger; sm, md, lg; Default, Hover, Active, Focus ring, Disabled, Loading có spinner); Inputs (text, textarea, select, search; Default, Hover, Focus, Disabled, Error kèm thông báo lỗi); Input kèm nút (i) và tooltip (hover/focus/chạm, Esc đóng, vẫn thấy khi thẻ tùy chọn gập); Checkbox, Radio, Toggle (checked, unchecked, indeterminate, disabled).
4. **Icons và avatars**: icon cốt lõi và cỡ 16/20/24/32px; avatar XS 24, SM 32, MD 40, LG 48, XL 64, dạng tròn, bo góc, có chấm trạng thái online/offline/busy.
5. **Component cơ bản**: badge/tag (solid, soft, outline, xóa được); alert (success, warning, error, info) và toast; tabs (underline, pill), breadcrumb, phân trang; modal, tooltip, dropdown menu; bảng (header, dòng kẻ sọc, hover, badge trạng thái, nút thao tác dạng icon).
6. **Trạng thái giao diện**: skeleton (text, avatar, card, dòng bảng); empty state (icon, tiêu đề, mô tả, nút chính); lỗi kết nối.
7. **Layout, spacing, motion**: spacing 4/8/12/16/24/32/48/64; breakpoint sm 640, md 768, lg 1024, xl 1280 và container; chiều cao điều khiển; thời gian fast 150, base 250, slow 350ms và easing.
8. **Quy định chung**: ngôn ngữ, định dạng ngày/số/tiền, icon, tương tác, thao tác nguy hiểm, trạng thái dữ liệu, tiếp cận, dữ liệu mẫu.

Bộ mẫu `templates/_gen/frag/system-design.html` đã có đủ 8 khối với giá trị trung tính; thay token trong `frame.html` theo theme hoặc sản phẩm, không bỏ khối nào. Khối không áp dụng cho sản phẩm (ví dụ không có avatar) vẫn giữ và ghi "không dùng" trong comment, không xóa.

## Tương tác

Màn phải bấm được như component thật: hộp thoại, thông báo, xác nhận xóa, nút thao tác trong bảng có hành vi trong `actions.py` (khóa `"system-design"`); tab, phân trang, menu, xóa tag, nút loading chạy bằng script trong nguồn; nút chỉ minh họa trạng thái dùng `data-proto="skip"`. Project có `actions.py` riêng (bộ mẫu không được chép đè) thì thêm khóa `"system-design"` vào đó.

## Quy tắc

1. **Khởi tạo bộ** (hoặc bộ chưa có màn này): dựng `system-design` **trước** các màn khác, điền token thật của theme/khung đang dùng, khai báo trong `canvas.json`.
2. **Bộ cũ có màn `blank`** (tên cũ trước 3.1.0): hỏi user có gộp sang `system-design` không. Đồng ý thì chuyển nội dung `blank` (quy định chung, token) vào `system-design`, đổi mục trong `canvas.json`, xóa `blank` khỏi nguồn; không đồng ý thì giữ `blank` và vẫn tạo `system-design`. Chạy tự động thì tạo `system-design`, giữ `blank`, báo lại.
3. **Đồng bộ tài liệu cho dev**: `docs/specs/ui-ux.md` (tạo thư mục nếu chưa có) có cùng nội dung dạng Markdown, kèm bảng token với giá trị thật. Bộ có màn ghi `<!--traces: ...-->` thì thêm mục `## Truy vết màn ↔ UC/AC`: bảng `Màn | File đầu ra | UC | AC`, mỗi màn một dòng, dựng lại từ dòng `traces` của mọi nguồn mỗi khi thêm, đổi hay bỏ màn. Thêm một dòng link tới file đó vào `CLAUDE.md` của project. `CLAUDE.md` chưa có thì hỏi trước khi tạo; đã có thì chỉ **thêm** dòng link.
4. **Đổi theme hay token thì cập nhật cả ba nơi** trong cùng lượt: `frame.html` (token), màn `system-design` (nếu thêm/bớt token), `docs/specs/ui-ux.md`. Token xấp xỉ thì ghi "xấp xỉ" ở comment màn và trong tài liệu.
5. Màn là tài liệu thiết kế, không thuộc sản phẩm của client: chữ giải thích được phép (`check.py` bỏ qua màn này khi quét UI sạch). Khi `--publish` mà user không muốn khách thấy thì hỏi một câu có đưa màn lên canvas không.
6. Kiểm tra trước khi giao: responsive tới 375px không tràn ngang, dark mode đổi đúng token, mọi tương tác ở trên chạy được.
