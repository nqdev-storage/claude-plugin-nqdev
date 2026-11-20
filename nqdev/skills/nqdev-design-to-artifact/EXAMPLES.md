# Examples — nqdev-design-to-artifact

File này cũng là nội dung hướng dẫn khi chạy `/nqdev:nqdev-design-to-artifact --help`, hoặc khi gọi skill mà không truyền gì (`/nqdev:nqdev-design-to-artifact`).

## Danh sách flag

| Flag | Tác dụng | Ví dụ |
|---|---|---|
| `<brief>` | Mô tả màn hình cần thiết kế | `/nqdev:nqdev-design-to-artifact Dashboard đơn hàng` |
| `--revert-design[=<path\|feature>]` | Khôi phục UI đã có thành các màn hoàn chỉnh có tương tác, chạy sản phẩm để đối chiếu khi có thể | `--revert-design=src/pages/orders` |
| `--themes=<name>` | Design theo theme và ghi nhớ cho cả bộ: `heroui`, `heroui-v3`, `bootstrap`, `material-v3`, `animate-ui`, `lucianux-uiprompt` | `--themes=material-v3` |
| `--publish` | Publish lên canvas Artifact, chỉ gửi màn đã đổi. Không có flag này thì luôn dừng ở local. Không kèm brief = publish những gì đã dựng | `--publish` |
| `--unpublish` | Gỡ canvas đã publish (có xác nhận), giữ nguyên nguồn để publish lại sau | `--unpublish` |
| `--check` | Kiểm tra bộ prototype, chỉ đọc (không sửa, không publish, không chạy app) | `--check` |
| `--update=<artifact-url>` | Chỉ định canvas đích, chỉ có tác dụng khi đi cùng `--publish` | `--publish --update=<artifact-url>` |
| `--help` | Hiển thị hướng dẫn này. Tự chạy khi gọi skill không kèm đối số nào | `/nqdev:nqdev-design-to-artifact --help` |

## Cấu trúc làm việc

```text
docs/prototype/
├── _gen/                    nguồn chỉnh sửa chính thức (sửa ở đây, không sửa project/)
│   ├── orig/<màn>.dc.html   bố cục đầy đủ của màn
│   ├── frag/<màn>.html      phần nội dung riêng, ghép vào frame.html
│   ├── frame.html, build.py khung chung và bộ ghép
│   ├── actions.py           hành vi các nút, gắn theo CHỮ trên nút
│   ├── interact.py          dựng màn hoàn chỉnh có tương tác
│   ├── icons.py             nút trong bảng -> icon
│   ├── check.py             kiểm tra tổng hợp, chỉ đọc
│   ├── lint_theme.py        rà lệch theme
│   └── frag/system-design.html  màn System Design (token, component, trạng thái, quy định chung)
├── project/
│   ├── <màn>.dc.html        đầu ra, dùng để publish
│   └── canvas.json          danh mục màn trên canvas
├── .artifact.json           link canvas, phiên bản, băm file đã publish
└── .theme.json              theme của cả bộ (khi dùng --themes)
```

Project đã có sẵn `_gen/interact.py` thì skill dùng nguyên bộ đó, không ghi đè. Chưa có thì skill chép bộ mẫu (cần Python 3).

Mặc định skill **dừng ở local**. Chỉ khi có `--publish` mới đưa lên canvas Artifact; link nằm trong **một** file `docs/prototype/.artifact.json` cho cả bộ (thiết kế từ brief lẫn revert) nên các lần sau cập nhật đúng canvas đó. Gọi skill không kèm đối số thì hiển thị hướng dẫn này; `--help` đi kèm đối số khác thì bị bỏ qua.

## Ví dụ 1 — Design local (mặc định)

```text
/nqdev:nqdev-design-to-artifact Màn hình danh sách đơn hàng: bảng đơn, bộ lọc trạng thái, nút Thêm đơn và Xuất Excel
```

1. Chuẩn bị `docs/prototype/` (tạo thư mục, chép bộ `_gen` mẫu nếu project chưa có).
2. Viết `_gen/frag/danh-sach-don.html` (bảng có nút Xem, Sửa, Xóa), khai báo hành vi trong `_gen/actions.py`:

```python
ACTIONS = {
    "danh-sach-don": {
        "thêm đơn": {"type": "modal", "title": "Thêm đơn hàng", "toast": "Đã thêm đơn hàng",
                     "fields": [{"label": "Khách hàng", "type": "text", "required": True}]},
        "bộ lọc":   {"type": "toggle", "region": "filters"},
        "xuất excel": {"type": "toast", "message": "Đã xuất file", "delay": 800},
        "xóa":      {"type": "confirm", "title": "Xóa đơn hàng?", "body": "Thao tác này không hoàn tác được."},
        "xem":      {"type": "goto", "screen": "chi-tiet-don"},
    },
}
```

3. Chạy `python3 docs/prototype/_gen/interact.py danh-sach-don` → `project/danh-sach-don.dc.html`. Nút Xem/Sửa/Xóa trong bảng thành icon có tooltip; Xóa có xác nhận; Thêm đơn kiểm tra ô bắt buộc rồi báo thành công.
4. Thêm màn vào `project/canvas.json` (theo schema có sẵn), chạy `--all --strict` không còn cảnh báo.
5. Dừng ở local, không gọi `Artifact`; nhắc chỉnh tiếp hoặc `--publish`.

## Ví dụ 2 — Publish lần đầu (`--publish`)

```text
/nqdev:nqdev-design-to-artifact --publish
```

1. Không có brief nên publish những gì đã dựng; chạy `interact.py --all --strict`.
2. Chưa có canvas: tạo từ loại **Design** của Artifact (`quickstart`, `type_url`), đọc hướng dẫn trả về, publish `canvas.json` cùng tất cả `project/*.dc.html`.
3. Chạy `interact.py --record` (ghi băm các màn đã đăng), lưu `url` và `version` vào `docs/prototype/.artifact.json`.
4. Báo: "đã tạo canvas mới, gửi 2 màn".

Dựng và publish liền: `/nqdev:nqdev-design-to-artifact Màn hình ... --publish`.

## Ví dụ 3 — Publish lần sau: chỉ gửi màn đã đổi

```text
/nqdev:nqdev-design-to-artifact Thêm cột "Ngày giao" vào bảng đơn hàng --publish
```

1. Sửa `_gen/frag/danh-sach-don.html`, dựng lại.
2. `interact.py --changed` chỉ liệt kê `danh-sach-don.dc.html` (so băm với `published`).
3. Đọc canvas hiện có (bắt buộc), publish với `url` đã lưu, `file_path` = `project/canvas.json`, `root` = `docs/prototype`, `files` = chỉ màn đã đổi. Không dùng `force`.
4. Lỗi xung đột: đọc bản hiện tại, bỏ qua phần khối `proto:begin`…`proto:end` do bộ dựng sinh, đưa chỉnh sửa tay trên canvas ngược vào `_gen/` rồi dựng và publish lại.
5. Lỗi `page must be .html`: thường do đang đăng nhập khác tài khoản sở hữu canvas. Đăng nhập đúng tài khoản rồi publish lại; skill không tự tạo canvas mới.

Trỏ sang canvas khác: `--publish --update=<artifact-url>`.

## Ví dụ 4 — Khôi phục UI có sẵn (`--revert-design`)

```text
/nqdev:nqdev-design-to-artifact --revert-design=src/pages/orders
```

1. Đọc template, CSS, token, handler sự kiện, định tuyến. Lập bản đồ điều hướng: Orders → chi tiết → sửa → quay lại. Chi tiết và sửa được kéo theo để luồng không cụt.
2. Viết nguồn trong `_gen/` (`orig/` hoặc `frag/` + khung chung) khớp UI gốc, comment đầu file ghi nguồn:

```html
<!-- Nguồn: src/pages/orders/index.tsx, src/styles/orders.css
     Đơn giản hóa: bỏ gọi API, phản hồi mô phỏng trong actions.py -->
```

3. Khai báo hành vi trong `actions.py` theo đúng chữ nút của UI gốc; điều hướng thành `goto`. Dựng `project/*.dc.html`, cập nhật `canvas.json`.
4. **Chạy sản phẩm để đối chiếu**: nói rõ lệnh (vd `npm run dev`), chạy ở local, mở từng màn bằng trình duyệt, chụp màn hình, thử click (bấm hàng → chi tiết, Sửa → form, lọc, sắp xếp). Xóa/Gửi không bấm lên dữ liệu thật, đọc handler thay thế.
5. Lặp lại đúng thao tác trên `project/*.dc.html`, so UI, đích của nút, kết quả click; lệch thì sửa nguồn `_gen/`, dựng lại (tối đa 2 vòng). Tắt tiến trình khi xong.
6. Tóm tắt: "Đã khôi phục 3 màn, đối chiếu với sản phẩm đang chạy: 14/15 mục khớp, còn lệch bóng đổ ở thẻ tổng."
7. Dừng ở local; thêm `--publish` để đưa lên canvas.

Không chạy được sản phẩm: đối chiếu từ code và nói rõ "chưa đối chiếu với sản phẩm đang chạy".

Màn khôi phục và màn từ brief **cùng một bộ**: cùng `canvas.json`, cùng `.artifact.json`, cùng canvas.

## Ví dụ 5 — Xem hướng dẫn (`--help`)

```text
/nqdev:nqdev-design-to-artifact --help
/nqdev:nqdev-design-to-artifact
```

Skill hiển thị file này, không tạo file, không publish. `--help` đi kèm brief hoặc flag khác (`Dashboard đơn hàng --help`, `--revert-design --help`) thì bị bỏ qua.

## Ví dụ 6 — Design theo theme (`--themes`)

**Lần đầu**

```text
/nqdev:nqdev-design-to-artifact Dashboard đơn hàng --themes=material-v3
```

1. Bộ chưa lưu theme: đọc tài liệu chính thức https://m3.material.io/ lấy token và quy chuẩn.
2. Viết nguồn theo Material 3 (đặt token vào `_gen/frame.html`), comment `<!-- Theme: material-v3 (https://m3.material.io/) -->`.
3. Ghi `docs/prototype/.theme.json`: `{ "theme": "material-v3", "docs": "https://m3.material.io/", "saved": "..." }`.

**Lần sau không truyền flag**: dùng `material-v3` đã lưu.

**Lần sau truyền theme khác** (`--themes=bootstrap`): skill hỏi

> Bộ prototype này đang dùng theme `material-v3`, bạn vừa truyền `bootstrap`. Bỏ qua `bootstrap` và design tiếp theo theme `material-v3` đã biết?

- **[A]** Có, dùng `material-v3` (đề xuất)
- **[B]** Không, dùng `bootstrap`: đổi theme của **cả bộ**, re-theme toàn bộ nguồn (không chỉ màn mới)

Tên có khoảng trắng: `--themes="material v3"` (chuẩn hóa thành `material-v3`).

Theme bổ trợ: `--themes=animate-ui` thêm quy tắc chuyển động (ease-out, chỉ transform/opacity, tôn trọng reduced motion) và giữ nguyên token màu hiện có; `--themes=lucianux-uiprompt` dùng phạm vi `.ux`/`--ux-*` của thư viện. Cả hai ghi `.theme.json` ở mức xấp xỉ vì docs không công bố token.

## Ví dụ 7 — Đổi theme cho cả bộ

Chọn [B] ở ví dụ 6, hoặc yêu cầu trực tiếp: `/nqdev:nqdev-design-to-artifact --themes=heroui`.

1. Re-theme mọi nguồn: `_gen/frame*.html`, `pane-*`, `orig/*`, `frag/*` (kể cả `system-design`), và `design/tailwind.config.js`, `input.css`, `to_design.py` nếu project có, rồi `canvas.json`, `.theme.json`.
2. Tài liệu chính thức không công bố hex (404 hoặc không có): dùng token **xấp xỉ**, ghi `"approximate": true` trong `.theme.json` và chữ "xấp xỉ" trong nguồn, `blank`, `docs/specs/ui-ux.md`; skill báo bạn cần chủ sản phẩm xác nhận.
3. Chạy `interact.py --all --strict`, rồi `python3 docs/prototype/_gen/lint_theme.py`. Ví dụ báo: `frag/don-hang.html:42  bo góc ngoài quy chuẩn [20]`. Sửa hết gradient, bóng màu, bo góc tùy ý, trọng số chữ và màu ngoài token; nút/ô nhập đúng cỡ theme (HeroUI: cao 40px, bo 12px); hover, nhấn, focus theo theme.
4. Cập nhật token trong `frame.html`, màn `system-design` và `docs/specs/ui-ux.md`.

## Ví dụ 8 — Màn System Design (bắt buộc)

```text
/nqdev:nqdev-design-to-artifact Màn danh sách đơn hàng
```

Bộ chưa có `system-design` nên skill dựng màn này **trước**, rồi mới dựng màn danh sách.

Mỗi bộ **bắt buộc** có màn **System Design** (`_gen/frag/system-design.html`, khai báo trong `canvas.json`, dựng trước các màn khác) gồm 8 khối: màu và design token (brand, neutrals, semantic, elevation, bo góc), typography, form controls (buttons, inputs, checkbox/radio/toggle với đủ trạng thái), icons và avatars, component cơ bản (badge, alert/toast, tabs, breadcrumb, phân trang, modal, tooltip, dropdown, bảng), trạng thái giao diện (skeleton, empty, lỗi kết nối), layout/spacing/motion, quy định chung. Token và class component nằm trong `_gen/frame.html`; màn chỉ hiển thị lại và đọc giá trị thật bằng `getComputedStyle`. Đồng bộ ra `docs/specs/ui-ux.md` và link từ `CLAUDE.md`; đổi token thì cập nhật `frame.html`, màn và tài liệu cùng lượt. Bộ cũ có màn `blank` thì skill hỏi gộp sang `system-design`.

Màn bấm được như component thật: "Mở hộp thoại" (kiểm tra ô bắt buộc), "Hiện thông báo", nút Xem/Sửa/Xóa trong bảng thành icon có tooltip và Xóa có xác nhận, tab, phân trang, menu thả xuống, xóa tag, nút loading. Hành vi khai báo trong `actions.py` dưới khóa `"system-design"`.

## Ví dụ 9 — Gỡ canvas (`--unpublish`)

```text
/nqdev:nqdev-design-to-artifact --unpublish
```

1. Đọc `url` trong `.artifact.json`; chưa có thì báo "chưa publish gì để gỡ".
2. Hỏi xác nhận (gỡ vĩnh viễn, link ngừng hoạt động; nguồn được giữ). Chạy tự động không hỏi được thì không gỡ.
3. Gọi `Artifact` `delete`, ghi `.artifact.json` thành `{"published": {}, "unpublished": "2026-10-24"}`.
4. Giữ nguyên `_gen/` và `project/`. Dòng nhắc link trong README, `plans/` được gỡ hoặc ghi "đã gỡ ngày …".
5. Lần `--publish` sau tạo canvas mới từ nguồn còn nguyên.

## Ví dụ 10 — Bàn giao sang code thật

Sau khi prototype xong, skill **đề xuất** (không tự tạo) lập plan và Jira để cập nhật UI thật. Bạn đồng ý thì:

1. Plan theo `nqdev-write-plan`, chia task theo lớp: token và font, `components/ui`, layout, từng nhóm màn, tài liệu, QA; có ước lượng giờ (bước 0.5, AI làm và DEV review) và rủi ro.
2. Jira theo `jira-nqdev-insight-create-issue` nếu đã cài, không thì `/nqdev:tracker-jira-nqdev create`: hỏi một issue tổng hay tách nhiều, và sprint nào.
3. Phần chưa có prototype (ví dụ dark mode) thành plan và issue riêng.

## Ví dụ 11 — Đối chiếu UI thật với prototype

```text
/nqdev:nqdev-design-to-artifact Kiểm tra UI app đã khớp prototype chưa
```

1. Chạy app thật bằng Playwright (local/dev), mock API theo envelope `{success:true,data}`, đặt phiên qua `localStorage`; phục vụ prototype bằng `python3 -m http.server` kèm query chống cache.
2. So `getBoundingClientRect` giữa app và prototype, lập bảng lệch.
3. Checklist: responsive dưới 768px (375px, tìm tràn ngang), hộp thoại, màn chưa có prototype, dark mode (nếu có), cổng API trong `.env.local`, trạng thái đang tải/rỗng/lỗi.
4. Mock gây lỗi giả thì sửa mock trước rồi mới kết luận lỗi code. Báo rõ mục nào **chưa kiểm tra**.

Khi sửa repo thật: không tự commit (repo có submodule thì hai commit riêng, hỏi từng cái); đổi màu hàng loạt phải xét ngữ cảnh nền; cuối mỗi đợt cập nhật plan/Jira và nói rõ việc chưa xong.

## Ví dụ 12 — Kiểm tra bộ prototype (`--check`)

```text
/nqdev:nqdev-design-to-artifact --check
```

Chỉ đọc: không ghi file, không dựng lại, không publish, không chạy app. Báo cáo mẫu:

```text
== 1. Nút, hành vi, canvas, đầu ra ==
CẢNH BÁO [danh-sach-don] nút 'Xuất Excel' chưa có hành vi trong actions.py
CẢNH BÁO [chi-tiet-don] project/chi-tiet-don.dc.html cũ so với nguồn _gen/ (cần dựng lại)
CẢNH BÁO [bao-cao] chưa thấy khai báo trong project/canvas.json
== 2. Lệch theme ==
_gen/frag/danh-sach-don.html:42  bo góc ngoài quy chuẩn [20]
== 3. UI sạch ==
danh-sach-don.html  đoạn chữ dài (có thể là mô tả tính năng): Khu vực này cho phép bạn xem…
== 4. Publish (thông tin) ==
Màn đã đổi so với bản đã publish: project/chi-tiet-don.dc.html
Tổng: 5 vấn đề.
```

Sau báo cáo, skill gợi ý cách sửa từng nhóm (vd dựng lại bằng `interact.py chi-tiet-don`, thêm hành vi vào `actions.py`) và để bạn quyết định có sửa không. Không có `docs/prototype/_gen/` thì báo chưa có bộ để kiểm tra, không tạo gì.

## Ví dụ 13 — Ô nhập kèm nút (i)

```text
/nqdev:nqdev-design-to-artifact Mỗi ô nhập có nút (i): di chuột hoặc focus bằng bàn phím để hiện tooltip gợi ý nội dung. Nút (i) vẫn thấy khi thẻ tùy chọn đang gập.
```

Skill dùng mẫu `.field-label` + `.info` trong `_gen/frame.html` cho mọi ô nhập: tooltip hiện khi hover, focus bàn phím hoặc chạm, Esc để đóng; thẻ tùy chọn gập chỉ ẩn ô nhập, nút (i) ở hàng nhãn vẫn thấy. Màn System Design có mẫu chạy được ("Input kèm nút (i)"). `interact.py` không đòi khai báo hành vi cho nút (i).

## Quy tắc UI sạch — sai và đúng

**Sai**: mô tả tính năng hiển thị trên UI

```html
<section class="orders">
  <h2>Đơn hàng</h2>
  <p>Khu vực này cho phép bạn xem, lọc và quản lý toàn bộ đơn hàng của cửa hàng.</p>
  <table>...</table>
</section>
```

**Đúng**: mô tả nằm trong comment

```html
<!-- Đơn hàng: quét nhanh trạng thái, lọc theo trạng thái và ngày; hàng mới nhất lên đầu -->
<section class="orders">
  <h2>Đơn hàng</h2>
  <table>...</table>
</section>
```

## Edge case

| Tình huống | Hành vi |
|---|---|
| Brief chỉ ghi "làm giúp tôi cái UI" | Hỏi tối đa 2 câu: màn hình nào, nội dung chính |
| Project đã có `_gen/interact.py` | Dùng nguyên bộ đó, không ghi đè `_gen/` |
| Không có Python 3 | Báo, dừng ở bước dựng, không tự cài |
| Đổi nhãn nút mà quên đổi khóa trong `actions.py` | `interact.py` cảnh báo hai chiều; `--strict` chặn trước khi publish |
| Thêm file HTML nhưng quên `canvas.json` | Cảnh báo màn chưa khai báo; phải thêm mục vào `canvas.json` |
| Không liệt kê được loại Design của Artifact | Nói rõ, dừng ở local, hỏi có muốn trang HTML tổng hợp không |
| HTML trên canvas bị sửa tay | Đọc, đưa chỉnh sửa thật vào `_gen/`, không ghi đè mù |
| Lỗi `page must be .html` | Kiểm tra tài khoản đăng nhập có phải chủ canvas; không tạo canvas mới |
| Không có `Artifact` tool | Giao thư mục `project/`, nói rõ chưa publish |
| `--unpublish` mà chưa có `url` trong `.artifact.json` | Báo chưa publish gì để gỡ, dừng |
| `--unpublish` chạy tự động, không hỏi được | Không gỡ (không hoàn tác được), báo lại |
| `--unpublish` kèm `--publish` | Hỏi muốn làm cái nào, không làm cả hai |
| Tài liệu theme không có hex | Dùng token xấp xỉ, ghi "xấp xỉ", báo cần chủ sản phẩm xác nhận |
| Mock API gây lỗi giả khi đối chiếu | Sửa mock trước rồi mới kết luận lỗi code |
| `--check` mà chưa có `docs/prototype/_gen/` | Báo chưa có bộ prototype để kiểm tra, không scaffold |
| `--check` kèm `--publish`/`--unpublish`/`--revert-design` | Hỏi muốn làm cái nào, không làm cả hai |
| Yêu cầu trang giống ngân hàng/cổng thanh toán có thật | Từ chối, đề xuất thương hiệu hư cấu |
| `--revert-design` mà project không có UI | Báo không tìm thấy, hỏi đường dẫn |
| `--revert-design` cần cài dependency hoặc thiếu cấu hình | Báo và hỏi trước, không tự cài hay sửa cấu hình |
| Hành động Xóa/Gửi/Thanh toán khi đối chiếu | Không bấm lên dữ liệu thật; đọc handler trong code |
| Dữ liệu thật/secret trong code gốc | Không đưa vào design, thay bằng dữ liệu mẫu |
