# Theme

Nạp khi có `--themes` hoặc khi đổi theme. Token áp vào `_gen/frame.html`; màn System Design xem `references/system-design.md`.

## Chế độ `--themes=<name_theme>`

Thiết kế theo quy chuẩn của một theme/design system và **ghi nhớ theme cho cả bộ prototype**, để các thiết kế sau đồng nhất.

Cú pháp: `--themes=<name>`. Tên có khoảng trắng thì đặt trong nháy (`--themes="material v3"`). `--theme=` được chấp nhận như bí danh. Tên được chuẩn hóa: chữ thường, khoảng trắng/gạch dưới thành `-` (`material v3` → `material-v3`).

### Theme đã biết

| Tên | Tài liệu chính thức | Ghi chú |
|---|---|---|
| `heroui` | https://heroui.com/ | HeroUI bản v2 trở xuống (đọc mục docs đúng phiên bản) |
| `heroui-v3` | https://heroui.com/ | HeroUI v3 (đọc mục docs của v3) |
| `bootstrap` | https://getbootstrap.com/ | Bootstrap (theo phiên bản của project nếu biết, không thì docs hiện hành) |
| `material-v3` | https://m3.material.io/ | Material Design 3 |
| `animate-ui` | https://animate-ui.com/docs | Lớp chuyển động (v2.4 theo trang docs, đọc ngày 2026-10-30), không có token màu. Xem "Theme bổ trợ" |
| `lucianux-uiprompt` | https://lucianlabs.dev/en/uxui-prompt/ | Thư viện phần tử UI và animation (không phải design system), không có token hex. Xem "Theme bổ trợ" |

Muốn thêm theme đã biết: thêm một dòng vào bảng này.

### Theme bổ trợ (`animate-ui`, `lucianux-uiprompt`)

Hai theme này **không công bố token màu, chữ, bo góc** (đã đọc docs ngày 2026-10-30). Không bịa giá trị: coi là theme bổ trợ.

- Ghi `.theme.json` với `"kind": "overlay"` và `"approximate": true`. Không điền `tokens`, `radii`, `weights`, nên `lint_theme.py` không bắt lệch màu.
- Màu, chữ, bo góc, spacing: giữ nguyên token đang có trong `frame.html` (hoặc theme nền đã lưu). Chưa có theme nào đã lưu thì dùng token mặc định của skill và nói rõ trong tóm tắt. Theme bổ trợ **không thay** theme nền, nên khi bộ đã có theme nền, `--themes=` bổ trợ chỉ thêm quy tắc, không hỏi đổi cả bộ. [cần xác nhận với user nếu muốn hành vi khác]
- Comment đầu file: `<!-- Theme: <name> (<docs>) - overlay -->`.

**`animate-ui`** (animation cho primitive của shadcn/ui; stack React, Motion, Radix/Base UI/React Aria): áp **quy tắc chuyển động** theo docs vào token `--motion-*` và màn System Design (mục Layout/Spacing/Motion):
- spring hoặc tween ngắn với ease-out mạnh; thoát nhanh hơn vào;
- chỉ animate `transform` và `opacity`, không animate thuộc tính layout; có thể bị ngắt giữa chừng;
- điều hướng bằng bàn phím không animate;
- tôn trọng `prefers-reduced-motion` (tắt hoặc giảm chuyển động).
Prototype là HTML/CSS thuần nên mô phỏng bằng CSS transition, không nhúng thư viện. Ghi chú tên component thật (`@animate-ui/react`) vào comment nguồn để bàn giao.

**`lucianux-uiprompt`** (400 phần tử: 200 component, 200 animation; skill tên `lucian-uxui`):
- phạm vi style theo `.ux` và tiền tố `.uNNN`; màu qua biến `--ux-*` nối vào biến theme của project (dùng khi nhúng phần tử của thư viện);
- demo chạy lại khi cuộn vào view; tương tác hoặc focus bàn phím thì tạm dừng, thả ra một lúc thì chạy lại từ đầu.
Muốn dùng phần tử cụ thể, người dùng nêu tên hoặc số phần tử; skill đọc từ trang nguồn, không chép từ trí nhớ.

### Nơi ghi nhớ

`docs/prototype/.theme.json`: **một file cho cả bộ prototype** (không phải từng thiết kế):

```json
{ "theme": "material-v3", "docs": "https://m3.material.io/", "saved": "YYYY-MM-DD" }
```

### Xác định theme (sau `--help`, trước khi thiết kế)

| Tình huống | Hành vi |
|---|---|
| Có `--themes`, bộ prototype chưa lưu theme | Dùng theme đó và ghi vào `.theme.json` |
| Có `--themes`, trùng theme đã lưu | Dùng bình thường |
| Có `--themes`, **khác** theme đã lưu | **Hỏi user** (xem bên dưới) |
| Không có `--themes`, đã lưu theme | Tự dùng theme đã lưu, nêu trong tóm tắt |
| Không có `--themes`, chưa lưu theme | Không áp theme, phong cách tự do |
| Tên không có trong bảng theme đã biết | Hỏi user: chọn một theme đã biết, hoặc đưa link tài liệu chính thức để dùng theme mới (link đó được ghi vào `.theme.json`). Không tự đoán quy chuẩn từ tên |

**Khi `--themes` khác theme đã lưu**, hỏi (dùng `AskUserQuestion` nếu có, không thì hỏi một câu):
> Bộ prototype này đang dùng theme `<X>`, bạn vừa truyền `<Y>`. Bỏ qua `<Y>` và design tiếp theo theme `<X>` đã biết?
- **[A] Có, bỏ qua `<Y>`, dùng `<X>`** (đề xuất, giữ cả bộ đồng nhất)
- **[B] Không, dùng `<Y>`**: **đổi theme của cả bộ** sang `<Y>`: ghi đè `.theme.json` và re-theme toàn bộ nguồn, không chỉ màn mới (xem "Đổi theme cho cả bộ"). Nói rõ điều này trong câu hỏi để user biết các màn cũ cũng đổi.

Không hỏi được (chạy tự động) → chọn [A].

### Đổi theme cho cả bộ

Chạy khi user chọn [B] ở trên (hoặc yêu cầu đổi theme của bộ). Re-theme **mọi** nguồn đang có, không chỉ màn mới:

1. Phạm vi: `_gen/frame*.html`, `_gen/pane-*`, `_gen/orig/*`, `_gen/frag/*` (kể cả `system-design.html`), và các file token nếu project có (`design/tailwind.config.js`, `input.css`, `to_design.py`), `project/canvas.json`, `.theme.json`. Thấy file nào thì sửa, không có thì bỏ qua; không tạo file token mới ngoài những file đã có.
2. Đọc tài liệu chính thức của theme mới để lấy token (xem "Áp quy chuẩn theme"). Tài liệu không công bố hex (404 hoặc không có) thì dùng **token xấp xỉ**: ghi `"approximate": true` trong `.theme.json`, ghi rõ chữ "xấp xỉ" trong comment nguồn, màn `system-design` và `docs/specs/ui-ux.md`, và **báo user cần chủ sản phẩm xác nhận**.
3. Dựng lại: `python3 docs/prototype/_gen/interact.py --all --strict` phải sạch.
4. **Rà lệch theme và sửa hết** bằng `python3 docs/prototype/_gen/lint_theme.py` (kèm đường dẫn file token của project nếu có) cộng đọc lại bằng mắt:
   - gradient, bóng đổ có màu, bo góc tùy ý, trọng số chữ ngoài quy chuẩn, màu ngoài token;
   - kích thước nút và ô nhập theo theme (ví dụ HeroUI: cao 40px, bo 12px);
   - hover, nhấn, focus theo theme.
   Đổi màu hàng loạt phải xét ngữ cảnh nền (xem "Quy tắc làm việc với repo thật").
5. Cập nhật token trong `frame.html`, màn `system-design` và `docs/specs/ui-ux.md` theo token mới, ghi tóm tắt: số màn đã đổi, các token xấp xỉ.

### Áp quy chuẩn theme

1. Đọc **tài liệu chính thức** (`WebFetch`/`WebSearch`) để lấy token và quy chuẩn đúng phiên bản. Không dựa vào trí nhớ cho giá trị cụ thể (màu, bo góc, cỡ chữ). Không truy cập được → nói rõ, dùng hiểu biết chung và ghi chú là giá trị xấp xỉ.
2. Bám theo: bảng màu và màu ngữ nghĩa, typography, spacing/grid, bo góc và độ nổi (elevation), quy ước component (nút, input, bảng, modal, điều hướng), dark mode theo theme, trạng thái (hover/focus/disabled), khả năng tiếp cận.
3. Cài đặt: đưa token vào biến CSS ở `:root`. Thư viện CSS thuần (vd Bootstrap) được nạp từ CDN cho phép; framework cần build (HeroUI, MUI...) thì mô phỏng bằng HTML/CSS theo token, không nhúng.
4. Comment đầu file: `<!-- Theme: <name> (<docs>) -->`.
5. Quy tắc "UI sạch" vẫn áp dụng.

**Với `--revert-design`:** UI gốc vẫn là nguồn sự thật. `--themes` ở chế độ này khai báo theme của UI gốc (để mô phỏng đúng và lưu lại). Không truyền thì skill dò thư viện UI đang dùng (từ `package.json`, `*.csproj`...) và gợi ý trong tóm tắt ("UI đang dùng X, chạy lại với `--themes=X` để ghi nhớ"), **không tự lưu**.
