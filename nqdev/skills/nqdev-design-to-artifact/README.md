# nqdev-design-to-artifact

Design UI ở local bằng Claude Code theo kiến trúc **`_gen` + canvas**: sửa nguồn trong `_gen/`, dựng màn hoàn chỉnh có tương tác vào `project/`, publish từng phần lên canvas Artifact. Mặc định dừng ở local; chỉ khi có `--publish` mới đưa lên và lưu link để lần sau cập nhật đúng canvas đó.
Giao diện tạo ra **sạch**: không có chữ mô tả tính năng trên UI, mô tả nằm trong comment code.

## Overview

| Mục | Nội dung |
|---|---|
| Tên skill | `nqdev-design-to-artifact` |
| Version | 3.3.0 |
| Tác giả | QuyIT Platform |
| Tạo / cập nhật | 2026-10-21 / 2026-10-30 |
| Kích hoạt | Chỉ khi user gọi (`disable-model-invocation: true`) |

## Cấu trúc skill (nạp tăng dần)

`SKILL.md` chỉ giữ phần lõi (vai trò, 8 điều bất biến, bảng điều phối đối số), khoảng 6,5 KB. Phần chi tiết của từng cờ nằm trong `references/` và chỉ được đọc khi cờ đó xuất hiện:

| File | Nạp khi |
|---|---|
| `references/source-layout.md` | thêm màn, sửa hành vi nút, dựng bộ lần đầu |
| `references/themes.md` | `--themes`, đổi theme |
| `references/system-design.md` | khởi tạo bộ, bộ chưa có `system-design`, đổi token |
| `references/publish.md` | `--publish`, `--unpublish`, `--update` |
| `references/revert-design.md` | `--revert-design` |
| `references/check-and-handover.md` | `--check`, bàn giao, đối chiếu UI thật, sửa repo thật |

`--help` hoặc gọi không đối số chỉ đọc `EXAMPLES.md`. Mọi quy tắc chỉ viết một lần (SKILL.md hoặc file tham chiếu tương ứng); `SYSTEM_PROMPT.md` là bản rút gọn để nhúng vào agent.

## Purpose

Rút ngắn vòng "ý tưởng → thiết kế → link xem được". Designer/dev làm việc ở local với file thật, chỉnh nhiều vòng, rồi đưa lên Artifact để chia sẻ.

## Target users

- Dev/designer của QuyIT Platform cần mockup, landing page nhanh để đưa client xem.
- Người muốn giữ thiết kế dưới dạng file local và có link Artifact để chia sẻ.

## Input format

```text
/nqdev:nqdev-design-to-artifact <brief> [--revert-design[=<path|feature>]] [--themes=<name>] [--publish] [--unpublish] [--check] [--update=<artifact-url>] [--help]
```

- `<brief>`: màn hình/trang cần thiết kế, đối tượng dùng, nội dung chính (không cần khi dùng `--revert-design`). Brief trỏ tới `docs/brd/<module>.md` (vd `màn đặt hàng, theo docs/brd/order.md`) thì skill đọc UC/AC, ghi `<!--traces: ...-->` vào nguồn từng màn và bảng "Truy vết màn ↔ UC/AC" trong `docs/specs/ui-ux.md` (từ 3.4.0).
- `--revert-design[=<path|feature>]`: project đã có UI nhưng chưa có thiết kế. Skill khôi phục UI hiện có thành các trang hoàn chỉnh (HTML/CSS/JS) liên kết với nhau như sản phẩm thật, và chạy sản phẩm để đối chiếu khi có thể.
- `--themes=<name>`: thiết kế theo quy chuẩn của theme và ghi nhớ cho cả bộ prototype (xem mục "Theme").
- `--help`: hiển thị hướng dẫn lấy từ `EXAMPLES.md`. **Tự kích hoạt khi gọi skill mà không truyền brief hay flag nào** (`/nqdev:nqdev-design-to-artifact`). Khi tự gõ `--help` thì chỉ có hiệu lực nếu là đối số duy nhất; đi kèm brief hoặc flag khác thì bị bỏ qua.
- `--publish`: publish lên Artifact. Không có flag này thì luôn dừng ở local. Dùng không kèm brief để publish thiết kế đã có trong `docs/prototype/`.
- `--check`: kiểm tra bộ prototype, **chỉ đọc** (nút/hành vi, canvas, đầu ra cũ, lệch theme, UI sạch, trạng thái publish) và gợi ý cách sửa; không sửa file, không publish, không chạy app.
- `--unpublish`: gỡ canvas đã publish (có xác nhận), giữ nguyên nguồn `_gen/` và `project/`, ghi `{"published": {}, "unpublished": "YYYY-MM-DD"}` vào `.artifact.json`.
- `--update=<url>`: chỉ định artifact đích, chỉ có tác dụng khi đi cùng `--publish`.

## Output format

Gốc prototype là `./docs/prototype/` (hoặc thư mục cha của `_gen/` nếu project đã có sẵn). Thư mục chưa có thì skill tạo (`mkdir -p`) và chép bộ dựng mẫu `_gen/` (không ghi đè).

```text
docs/prototype/
├── _gen/                    nguồn chỉnh sửa chính thức
│   ├── orig/<màn>.dc.html   bố cục đầy đủ
│   ├── frag/<màn>.html      nội dung riêng, ghép vào frame.html
│   ├── frame.html, build.py
│   ├── actions.py           hành vi nút, gắn theo chữ hiển thị
│   ├── interact.py          dựng màn hoàn chỉnh (--all, --strict, --changed, --record)
│   ├── icons.py             nút trong bảng -> icon
│   ├── check.py             kiểm tra tổng hợp, chỉ đọc
│   ├── lint_theme.py        rà lệch theme
│   └── frag/system-design.html  màn System Design bắt buộc
├── project/
│   ├── <màn>.dc.html        đầu ra để publish (đừng sửa tay)
│   └── canvas.json          danh mục màn trên canvas
├── .artifact.json           url, version, updated, published (băm)
└── .theme.json              theme của cả bộ (chỉ khi dùng --themes)
```

- Cả bộ (thiết kế từ brief và từ `--revert-design`) là **một canvas**, **một** `.artifact.json`.
- Canvas Artifact private trên claude.ai (chỉ khi có `--publish`).

## Workflow

1. **Nguồn**: viết `_gen/orig` hoặc `_gen/frag`, khai báo hành vi mọi nút trong `actions.py`.
2. **Dựng**: `interact.py <màn>` → `project/<màn>.dc.html`; xử lý cảnh báo.
3. **Canvas**: thêm màn mới vào `project/canvas.json`.
4. **Kiểm tra**: UI sạch, `--all --strict` sạch, thử luồng chính khi có trình duyệt.
5. **Dừng ở local (mặc định)** hoặc **publish (có `--publish`)**: lần đầu tạo canvas từ loại Design; các lần sau publish từng phần (chỉ màn đã đổi + `canvas.json`), xử lý xung đột, ghi băm/phiên bản.

Nguyên tắc: một nguồn chỉnh sửa chính thức (`_gen/`), tách giao diện khỏi hành vi, publish theo phần thay đổi, không bỏ qua xung đột, theo dõi phiên bản. Hành vi gắn theo **chữ trên nút**: đổi nhãn phải đổi khóa trong `actions.py`.

## Chế độ `--revert-design`

Dành cho project đã có UI chạy được nhưng chưa có bản thiết kế. Skill khôi phục UI thành **các màn hoàn chỉnh có tương tác, giống UI gốc**, đi qua cùng kiến trúc `_gen`, rồi (nếu chạy được) chạy sản phẩm để đối chiếu.

1. Xác định màn cần khôi phục, lập **bản đồ điều hướng** từ định tuyến/menu, kéo theo màn có quan hệ trực tiếp (chi tiết, sửa, tạo mới).
2. Đọc markup, CSS, token, component, handler sự kiện, định tuyến.
3. Viết nguồn `_gen/` khớp UI gốc; hành vi trong `actions.py` theo đúng chữ nút gốc (điều hướng thành `goto`); dựng `project/` và cập nhật `canvas.json`.
4. Comment đầu nguồn ghi nguồn gốc và phần đã đơn giản hóa.
5. **Chạy sản phẩm và đối chiếu** (khi chạy được): mở từng tính năng, chụp màn hình, thử click, lặp lại trên bản khôi phục để so UI, quan hệ và sự kiện. Lệch thì sửa nguồn (tối đa 2 vòng).
6. Dừng ở local; thêm `--publish` để đưa lên canvas.

**An toàn khi chạy sản phẩm:** chỉ local/dev, không production/secret thật; nói rõ lệnh và hỏi trước nếu cần cài dependency hoặc thiếu cấu hình; không bấm hành động ghi/xóa/gửi/thanh toán lên dữ liệu thật; ảnh chụp và dữ liệu chỉ để đối chiếu, không đưa vào `docs/prototype/`; tắt tiến trình khi xong. Không chạy được thì đối chiếu từ code và nói rõ.

## Theme (`--themes`)

Thiết kế theo quy chuẩn của một theme và ghi nhớ theme cho cả bộ prototype trong `docs/prototype/.theme.json`.

| Tên | Tài liệu |
|---|---|
| `heroui` | https://heroui.com/ |
| `heroui-v3` | https://heroui.com/ |
| `bootstrap` | https://getbootstrap.com/ |
| `material-v3` | https://m3.material.io/ |
| `animate-ui` | https://animate-ui.com/docs (bổ trợ: quy tắc chuyển động) |
| `lucianux-uiprompt` | https://lucianlabs.dev/en/uxui-prompt/ (bổ trợ: phần tử UI và animation) |

- Hai theme cuối là **theme bổ trợ**: không có token màu, nên chỉ thêm quy tắc chuyển động/phần tử, giữ token nền hiện có, `.theme.json` ghi `kind: overlay` và `approximate: true`.
- Tên có khoảng trắng thì đặt trong nháy: `--themes="material v3"`.
- Đã lưu theme và lần sau không truyền `--themes`: skill tự dùng theme đã lưu.
- Truyền theme **khác** theme đã lưu: skill hỏi có bỏ qua theme mới và design tiếp theo theme cũ không. Chọn "không" thì **đổi theme của cả bộ**: re-theme toàn bộ nguồn (frame, pane, frag, file token, canvas.json, .theme.json), dựng lại `--all --strict`, rà lệch bằng `lint_theme.py`. Tài liệu không có hex thì dùng token xấp xỉ, ghi rõ và báo cần chủ sản phẩm xác nhận.
- Tên theme chưa có trong bảng: hỏi chọn theme đã biết hoặc đưa link tài liệu chính thức.
- Skill đọc tài liệu chính thức của theme để lấy token và quy chuẩn, nên cần truy cập web.

## Màn System Design (bắt buộc)

Mỗi bộ **bắt buộc** có màn **System Design** (`_gen/frag/system-design.html`, khai báo trong `canvas.json`, dựng trước các màn khác) gồm 8 khối: màu và design token (brand, neutrals, semantic, elevation, bo góc), typography, form controls (buttons, inputs, checkbox/radio/toggle với đủ trạng thái), icons và avatars, component cơ bản (badge, alert/toast, tabs, breadcrumb, phân trang, modal, tooltip, dropdown, bảng), trạng thái giao diện (skeleton, empty, lỗi kết nối), layout/spacing/motion, quy định chung. Token và class component nằm trong `_gen/frame.html`; màn chỉ hiển thị lại và đọc giá trị thật bằng `getComputedStyle`. Đồng bộ ra `docs/specs/ui-ux.md` và link từ `CLAUDE.md`; đổi token thì cập nhật `frame.html`, màn và tài liệu cùng lượt. Bộ cũ có màn `blank` thì skill hỏi gộp sang `system-design`.

## Sau khi prototype xong

- **Bàn giao sang code thật**: skill đề xuất (không tự tạo) plan theo `nqdev-write-plan` (không có thì khuôn plan của `nqdev-task-flow`) và Jira theo `jira-nqdev-insight-create-issue` hoặc `/nqdev:tracker-jira-nqdev` (tuỳ chọn), chia task theo lớp, hỏi 1 issue tổng hay tách nhiều và sprint nào.
- **Đối chiếu UI thật với prototype** (khi bạn yêu cầu): Playwright + mock API, so `getBoundingClientRect`, checklist responsive/hộp thoại/dark mode/trạng thái, báo rõ mục chưa kiểm tra.
- **Làm việc với repo thật**: không tự commit (submodule thì hai commit riêng), sửa hàng loạt phải xét ngữ cảnh nền, cuối đợt cập nhật plan/Jira.

## Quy tắc "UI sạch"

| Trên giao diện | Trong comment code |
|---|---|
| Tiêu đề, nhãn nút, nhãn trường, dữ liệu mẫu, thông báo | Mô tả tính năng, ý đồ thiết kế, ghi chú cho dev |

Client không phải đọc giải thích về tính năng.

## Supported tools

| Tool | Hành vi |
|---|---|
| Claude Code | Đủ workflow: nguồn `_gen`, dựng bằng Python 3, publish bằng `Artifact` tool khi có `--publish` |
| OpenCode | Design và dựng local. Không có `Artifact` tool: `--publish` fallback giao thư mục `project/`, không publish |
| Claude.ai | Không có shell nên không chạy được bước dựng; chỉ dùng để xem tài liệu và soạn nguồn |

Skill đặt tại `.claude/skills/nqdev-design-to-artifact/` (Claude Code) hoặc `.opencode/skills/...` (OpenCode).

## Edge cases

- Thiếu brief cốt tử: hỏi tối đa 2 câu.
- Project đã có `_gen/interact.py`: dùng nguyên bộ đó, không ghi đè `_gen/`.
- Không có Python 3: báo, dừng ở bước dựng.
- Đổi nhãn nút mà không đổi khóa `actions.py`: cảnh báo hai chiều; `--strict` chặn.
- Thêm màn mà quên `canvas.json`: cảnh báo; thêm mục theo schema sẵn có.
- `--publish` mà đã có `.artifact.json`: cập nhật đúng canvas cũ từng phần, không tạo mới. Link mất quyền/không truy cập được: hỏi user, không tự tạo.
- Xung đột khi publish: đọc bản hiện tại, tách phần bộ dựng sinh khỏi chỉnh sửa tay, xử lý rồi publish lại. Không dùng `force`.
- Lỗi `page must be .html`: kiểm tra tài khoản đăng nhập có phải chủ canvas; không tạo canvas mới.
- `--update` không kèm `--publish`: bỏ qua. `--no-publish` (flag cũ): bỏ qua.
- `--themes` khác theme đã lưu: hỏi người dùng; không hỏi được thì giữ theme cũ.
- Yêu cầu giả mạo tổ chức/thương hiệu thật hoặc luồng đăng nhập/thanh toán trông như thật: từ chối, đề xuất thương hiệu hư cấu.

## Limitations

- Cần Python 3 và quyền chạy shell để dựng.
- Bộ dựng mẫu có sáu loại hành vi (modal, confirm, toggle, toast, goto, close); hành vi phức tạp viết `<script>` trong nguồn. Mỗi màn tự chứa, không chia sẻ trạng thái với màn khác.
- Schema `canvas.json` và định dạng `.dc.html` do loại Design của Artifact quy định; skill lấy từ canvas hiện có hoặc hướng dẫn của loại đó, không tự suy ra. `frame.html` mẫu chỉ là khung giữ chỗ.
- Cập nhật chỉ trên canvas có quyền sửa (đúng tài khoản).
- Chưa dùng DesignSync (chưa xác nhận cơ chế).
- `--revert-design` khôi phục phía giao diện; backend được giả lập. Đối chiếu bằng chạy sản phẩm chỉ làm được khi chạy được ở local/dev và có công cụ trình duyệt, và có thể cần bạn cấp quyền.

## Best practices

- Chỉnh kỹ ở local, hài lòng rồi mới chạy `--publish`.
- Commit `_gen/`, `project/`, `.artifact.json` nếu muốn cả team dựng lại và cập nhật chung một canvas.
- Giữ slug màn ổn định; đổi nhãn nút thì đổi khóa trong `actions.py`.
- Comment nêu ý đồ, không lặp lại code.

## Recommended improvements

- Hỗ trợ slide, poster, design system như loại thiết kế riêng.
- Tích hợp DesignSync khi cơ chế được xác nhận.
- Hành vi dùng chung giữa các màn (dữ liệu mẫu chia sẻ) trong bộ dựng.
- Script kiểm tra "UI sạch" tự động (quét text node dài ngoài comment).
- Xuất ảnh chụp (screenshot) kèm artifact để gửi nhanh.
- Cờ `--share` có xác nhận để chia sẻ artifact.
