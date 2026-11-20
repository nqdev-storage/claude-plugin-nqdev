# Changelog — nqdev-design-to-artifact

## [3.5.1] - 2026-11-19

### Changed
- `references/check-and-handover.md`, `EXAMPLES.md`: ước lượng giờ của task theo bước 0.5 và mô hình AI làm, DEV review (khớp `nqdev-requirement-estimator` 5.0.0 và `nqdev-write-plan` 1.4.0).

## [3.5.0] - 2026-11-19

### Changed
- `README.md`, `references/check-and-handover.md`: đổi tên `nqdev-flow` thành `nqdev-task-flow` (kể cả đường dẫn `references/feature.md` của skill này).

## [3.4.1] - 2026-11-18

### Changed
- `references/check-and-handover.md`: `nqdev-write-plan` nay đi kèm plugin `nqdev`; bỏ cách nói "nếu đã cài", giữ khuôn plan của `nqdev-flow` làm phương án dự phòng khi không nạp được skill.

## [3.4.0] - 2026-11-18

### Added
- Mục "Truy vết với BRD" trong `SKILL.md`: có `docs/brd/<module>.md` thì đọc UC và AC trước khi thiết kế, ghi `<!--traces: UC-..., AC-...-->` vào nguồn từng màn. Nhiều BRD mà không rõ module thì hỏi; không có BRD thì chạy như cũ.
- `references/source-layout.md`: quy ước dòng `traces` (cạnh `title`). Bộ dựng không đọc dòng này, không cần sửa script trong `_gen/`.
- `references/system-design.md`: `docs/specs/ui-ux.md` có mục "Truy vết màn ↔ UC/AC".
- `references/check-and-handover.md`: `--check` báo màn thiếu `traces`, mã không có trong BRD, bảng truy vết lệch nguồn.

### Notes
- Để `nqdev-flow` (mục `## Màn hình` trong plan) và `nqdev-feature-implementer` (cột "Màn" trong bảng truy vết) nối được màn với BR/AC.

## [3.3.2] - 2026-11-17

### Fixed
- `references/source-layout.md`, `references/check-and-handover.md`: không dùng `${CLAUDE_PLUGIN_ROOT}` trong file tham chiếu (có thể không được thay giá trị); đường dẫn tính từ thư mục gốc của skill (dòng *Base directory for this skill*).

## [3.3.1] - 2026-11-17

### Fixed
- `references/source-layout.md`: đường dẫn chép bộ dựng dùng `${CLAUDE_PLUGIN_ROOT}` thay cho placeholder `<thư mục skill>`, để chạy đúng khi cài qua plugin.
- `references/check-and-handover.md`, `EXAMPLES.md`, `README.md`: `nqdev-write-plan` và `jira-nqdev-insight-create-issue` là tuỳ chọn; có phương án thay thế trong plugin (`nqdev-flow`, `/nqdev:tracker-jira-nqdev`).
- Thêm `agents/openai.yaml` (`allow_implicit_invocation: false`) cho Codex CLI, khớp với `disable-model-invocation: true`.

## [3.3.0] - 2026-10-30

### Added
- Hai theme đã biết: `animate-ui` (https://animate-ui.com/docs) và `lucianux-uiprompt` (https://lucianlabs.dev/en/uxui-prompt/).
- Mục "Theme bổ trợ" trong `references/themes.md`: cả hai docs không công bố token màu/chữ/bo góc nên được coi là overlay (`kind: overlay`, `approximate: true`), giữ token nền hiện có, không hỏi đổi cả bộ. `animate-ui` thêm quy tắc chuyển động; `lucianux-uiprompt` thêm quy ước `.ux`/`--ux-*` và hành vi demo.

### Notes
- Tên chuẩn hóa chọn mặc định: `animate-ui`, `lucianux-uiprompt`. Nội dung đọc từ trang docs ngày 2026-10-30; không có số phiên bản cho Lucian UX/UI Prompt, Animate UI hiển thị v2.4.

## [3.2.0] - 2026-10-30

### Added
- Ô nhập kèm nút (i) và tooltip: mẫu `.field-label` + `.info` (`.info-btn`, `role="tooltip"`) và script nhỏ trong `templates/_gen/frame.html`. Tooltip hiện khi hover, focus bàn phím hoặc chạm; Esc hoặc bấm ra ngoài để đóng; tooltip không tràn màn hình 375px; dark mode đúng token.
- Màn System Design thêm mục "Input kèm nút (i)" gồm thẻ tùy chọn gập: gập chỉ ẩn ô nhập, nút (i) ở hàng nhãn vẫn thấy và vẫn hiện tooltip.
- Mục "Ô nhập kèm nút (i) và tooltip" trong `references/source-layout.md`; `SKILL.md` thêm mục tiêu tương ứng.

### Changed
- `interact.py` bỏ qua nút `.info-btn` (không cảnh báo thiếu hành vi).

### Fixed
- `.field` bị kéo giãn trong lưới hai cột làm nhãn lệch hàng và icon của ô search nằm lệch xuống dưới (thêm `align-content: start`).

### Notes
- Quyết định mặc định khi chưa được xác nhận: (i) đặt cạnh nhãn; áp cho text, textarea, select, search (không cho checkbox/radio/toggle); nội dung tooltip do skill soạn ngắn theo từng ô; chạm mở tooltip trên thiết bị cảm ứng; thêm mẫu vào System Design.
- Đã kiểm thử Playwright 20/20 (hover, focus, Esc, blur, aria, gập thẻ, 375px, chạm, dark mode); `interact.py --all --strict` và `check.py` sạch.

## [3.1.0] - 2026-10-28

### Added
- Màn **System Design** bắt buộc (`templates/_gen/frag/system-design.html`, slug `system-design`) với 8 khối: màu và design token (brand có default/hover/active/nền nhạt, neutrals, semantic, elevation, bo góc), typography (Display, H1–H6, Subtitle, Body, Caption, Overline kèm size/line/weight), form controls (6 kiểu nút, 3 cỡ, 6 trạng thái gồm loading; input/textarea/select/search có lỗi; checkbox/radio/toggle gồm indeterminate), icons và avatars, component cơ bản (badge/tag, alert/toast, tabs, breadcrumb, phân trang, modal, tooltip, dropdown, bảng), skeleton/empty/lỗi kết nối, layout/spacing/motion, quy định chung.
- `references/system-design.md`: quy tắc dựng, đồng bộ `docs/specs/ui-ux.md`, chuyển đổi bộ cũ có `blank`.
- `templates/_gen/frame.html` thành nguồn duy nhất của token (brand, neutrals, semantic, shadow, radius, font, spacing, chiều cao điều khiển, breakpoint, motion, dark mode) và class component dùng chung (`.t-*`, `.btn*`, `.input`, `.check`, `.switch`, `.badge`, `.alert`, `.card`, `.table`, `.skeleton`). Màn System Design đọc giá trị thật bằng `getComputedStyle`, không ghi hex cứng.
- `actions.py` mẫu có khóa `"system-design"` (modal, toast, thử lại, xem/sửa/xóa).

### Changed
- Màn `blank` gộp vào `system-design` (theo lựa chọn của user). Bộ cũ có `blank`: skill hỏi gộp, không tự xóa. `check.py` bỏ qua cả hai tên khi quét UI sạch.

### Fixed
- `build.py` chèn nội dung vào cả chỗ giữ chỗ nằm trong comment của `frame.html`, làm nội dung màn bị lặp hai lần (comment trong fragment có thể đóng comment khung và hiện lặp). Nay chỉ thay ngoài comment, và comment khung không còn ghi nguyên văn chỗ giữ chỗ.

### Verified
- Dựng `system-design` qua `interact.py --all --strict` và `check.py` sạch; Playwright 24/24 (hex và thông số chữ đọc đúng token, modal kiểm tra bắt buộc, toast, xác nhận xóa, icon bảng, tab, phân trang, menu, tooltip, xóa tag, loading, thử lại, 375px không tràn ngang, dark mode đổi token).

## [3.0.0] - 2026-10-27

### Changed (BREAKING cấu trúc skill, hành vi giữ nguyên)
- Tách `SKILL.md` (49,8 KB) thành **lõi 6,5 KB + `references/`** nạp tăng dần: `source-layout.md`, `themes.md`, `publish.md`, `revert-design.md`, `check-and-handover.md`. Lõi chỉ có vai trò, 8 điều bất biến và bảng điều phối đối số; mỗi lần chạy thường nạp khoảng 13–20 KB thay vì 49,8 KB.
- Bước 1–5 và R1–R8 viết lại thành **kết quả cần đạt** để model tự lập kế hoạch; bỏ phần mô tả lại thứ code hoặc tool đã tự mô tả (loại hành vi, cảnh báo của `interact.py`, tham số `Artifact`).
- `revert-design.md` viết gọn; phần đối chiếu app đang chạy nên giao cho subagent (nếu có) và chỉ nhận lại bảng khớp/lệch.
- `SYSTEM_PROMPT.md` rút gọn thành bản tóm tắt bất biến, hết nhân bản 22 quy tắc.
- `description` ngắn lại (3 câu, dưới 400 ký tự).

### Security
- Bỏ `Artifact` khỏi `allowed-tools`: các lệnh `--publish` và `--unpublish` (xóa vĩnh viễn) nay hiện hộp xin quyền của tool, không chỉ dựa vào câu xác nhận trong prompt. Muốn publish không hỏi thì thêm lại `Artifact` vào `allowed-tools`.

### Notes
- `templates/_gen` không đổi. Backup bản 2.2.0 nằm ngoài gói, chưa kiểm thử lại theo từng cờ sau khi tách.
- Một số `references/` còn là văn bản cắt nguyên từ bản cũ, có thể rút gọn thêm.

## [2.2.0] - 2026-10-27

### Added
- Cờ `--check` (chỉ đọc): kiểm tra nút/hành vi, `canvas.json`, đầu ra cũ so với nguồn, lệch theme, UI sạch và trạng thái publish; báo cáo kèm gợi ý cách sửa. Không sửa file, không dựng lại, không publish, không chạy app.
- `templates/_gen/check.py` (kiểm tra tổng hợp) và `interact.py --dry` (kiểm tra không ghi file, phát hiện `project/*.dc.html` thiếu hoặc cũ).
- `allowed-tools` thêm `Bash(python3|python docs/prototype/_gen/check.py:*)`; `argument-hint` thêm `--check`.

### Notes
- Ngưỡng "đoạn chữ dài" của mục UI sạch là 90 ký tự (`LONG` trong `check.py`); chỉ là gợi ý, cần xem tay.
- Rút gọn câu trong `description` để còn dưới 1024 ký tự.

## [2.1.0] - 2026-10-24

### Added
- Cờ `--unpublish`: xác nhận, gọi `Artifact` `delete`, ghi `.artifact.json` thành `{"published": {}, "unpublished": "YYYY-MM-DD"}`, giữ nguyên `_gen/` và `project/`, cập nhật tài liệu nhắc link canvas. Chạy tự động thì không gỡ.
- Mục "Đổi theme cho cả bộ": re-theme toàn bộ nguồn, `interact.py --all --strict`, token xấp xỉ khi không có hex (ghi `"approximate": true`, báo cần chủ sản phẩm xác nhận), rà lệch theme và sửa hết.
- `templates/_gen/lint_theme.py`: quét gradient, bóng đổ có màu, bo góc ngoài quy chuẩn, trọng số chữ ngoài quy chuẩn, màu ngoài token (đọc quy chuẩn từ `.theme.json`).
- Màn quy chuẩn `blank` (`templates/_gen/frag/blank.html`): token, quy định chung; đồng bộ `docs/specs/ui-ux.md` và link từ `CLAUDE.md`.
- Mục "Bàn giao sang code thật" (plan `nqdev-write-plan`, Jira `jira-nqdev-insight-create-issue`, chỉ đề xuất), "Đối chiếu UI thật với prototype" (Playwright, mock API, `getBoundingClientRect`, checklist) và "Quy tắc làm việc với repo thật" (không tự commit, sửa hàng loạt có kiểm chứng, cập nhật plan/Jira cuối đợt).
- `allowed-tools` thêm `Bash(python3|python docs/prototype/_gen/lint_theme.py:*)`; `argument-hint` thêm `--unpublish`.

### Changed (sửa chỗ mâu thuẫn)
- Chọn đổi theme khác theme đã lưu giờ **đổi cả bộ** (trước đây: "thiết kế cũ giữ nguyên, không tự đổi"). Mục Giới hạn cập nhật theo.
- Bước 1 dựng `blank` trước khi dựng các màn còn lại; checklist cập nhật thêm mục `blank`/`lint_theme.py`.

### Notes
- Tên file token (`design/tailwind.config.js`, `input.css`, `to_design.py`, `pane-*`) là của pipeline project, chỉ sửa khi project có; skill không tạo mới.
- Hai skill `nqdev-write-plan`, `jira-nqdev-insight-create-issue` phải có trong session; không có thì skill soạn plan theo cấu trúc và hỏi cách tạo issue.

## [2.0.0] - 2026-10-21

### Changed (BREAKING) — chuyển sang kiến trúc `_gen` + canvas
- Nguồn chỉnh sửa chính thức là `docs/prototype/_gen/` (`orig/`, `frag/`, `frame.html`, `build.py`, `actions.py`, `interact.py`, `icons.py`); đầu ra là `docs/prototype/project/<màn>.dc.html` cùng `project/canvas.json`. Bỏ cấu trúc cũ `index.html` hub, `assets/`, `<slug>/index.html`.
- Hành vi nút khai báo trong `actions.py`, gắn theo chữ hiển thị (modal, confirm, toggle, toast, goto, close); nút trong bảng thành icon có tooltip; `interact.py` cảnh báo hai chiều (nút thiếu hành vi, hành vi không khớp nút, màn chưa có trong `canvas.json`), `--strict`, `--changed`, `--record`.
- Kèm bộ dựng mẫu `templates/_gen/` (chỉ dùng thư viện chuẩn Python 3); project đã có `_gen/interact.py` thì dùng nguyên, không ghi đè. Đã kiểm thử bằng Chromium (20/20 kịch bản).
- **Publish từng phần**: lần đầu tạo canvas từ loại Design của Artifact; các lần sau chỉ gửi `canvas.json` và các màn đã đổi (`root`, `files`), không dùng `force`.
- Xử lý xung đột (tách khối bộ dựng sinh khỏi chỉnh sửa tay), lỗi `page must be .html` (sai tài khoản sở hữu), theo dõi phiên bản (`published` băm trong `.artifact.json`, cập nhật tài liệu phiên bản của project nếu có).
- Thêm checklist cập nhật prototype và tiêu chí chất lượng (luồng nghiệp vụ, trạng thái, validate, icon + xác nhận, nhất quán, tái lập, kiểm thử sau publish).
- `--revert-design` viết lại quanh `_gen`: nguồn vào `_gen/orig` hoặc `frag`, hành vi vào `actions.py`, đối chiếu sản phẩm đang chạy giữ nguyên (R7).
- `--themes`, `--help`, `--publish`, `--update` giữ nguyên ý nghĩa; theme áp vào nguồn và `frame.html`.
- `allowed-tools` thêm `Bash(cp:*)` và `Bash(python3|python docs/prototype/_gen/interact.py:*)`.

### Removed
- Dữ liệu mẫu dùng chung giữa các màn (`assets/mock-data.js`) và trang tổng hợp `docs/prototype/index.html`; `screens` trong `.artifact.json`.

### Migration từ 1.x
- Chuyển nội dung `docs/prototype/<slug>/index.html` thành `_gen/orig/<slug>.dc.html` (hoặc `frag/`), tách hành vi vào `actions.py`, dựng lại, thêm màn vào `canvas.json`.
- `.artifact.json`: giữ `url`, bỏ `screens`; chạy `interact.py --record` sau lần publish đầu để có `published`.
- Artifact kiểu cũ (trang tổng hợp) không tự chuyển thành canvas; tạo canvas mới theo hướng dẫn của loại Design và xóa artifact cũ thủ công nếu muốn.

## [1.8.0] - 2026-10-21

### Changed (behavior) — `--revert-design`
- Khôi phục thành **các trang hoàn chỉnh (HTML, CSS, JS) liên kết với nhau như sản phẩm thật**, không còn một file `index.html` tĩnh mỗi màn hình.
- Thêm "Tiêu chuẩn trang hoàn chỉnh": đủ ba lớp, link giữa trang đúng đích, layout dùng chung, dữ liệu mẫu dùng chung (`assets/mock-data.js`, `localStorage` bọc `try/catch`), chạy được khi mở trực tiếp file (không `type="module"`, không `fetch` file cục bộ), API giả lập, đăng nhập giả lập.
- R1 lập **bản đồ điều hướng** từ định tuyến/menu và kéo theo các trang có quan hệ trực tiếp (chi tiết, sửa, tạo mới) để luồng không bị cụt.
- R2–R3 đọc thêm handler sự kiện và định tuyến, trích xuất hành vi (click làm gì, đi đâu, gọi API nào).
- **R7 viết lại: chạy sản phẩm và đối chiếu.** Chạy sản phẩm ở local/dev, truy cập từng tính năng bằng trình duyệt có trong session, chụp màn hình, thử các cú click; lặp lại trên bản khôi phục để so UI, quan hệ giữa trang và sự kiện; lệch thì sửa (tối đa 2 vòng); dọn tiến trình khi xong.
- An toàn khi chạy: chỉ local/dev, không production/secret thật; nói rõ lệnh trước khi chạy và hỏi trước nếu cần cài dependency hoặc thiếu cấu hình; không bấm hành động ghi/xoá/gửi/thanh toán lên dữ liệu thật; ảnh chụp và dữ liệu thấy khi chạy không đưa vào `docs/prototype/`.
- Không chạy được sản phẩm: đối chiếu từ code và nói rõ chưa đối chiếu với sản phẩm đang chạy.
- Tóm tắt R8 thêm kết quả đối chiếu (đã chạy sản phẩm hay chưa, số mục khớp/lệch).

### Changed
- Bộ prototype có thêm `docs/prototype/assets/` (CSS/JS/dữ liệu mẫu dùng chung); trang vào `docs/prototype/index.html` là trang chủ của sản phẩm nếu có, không thì trang điều hướng. Các trang tham chiếu nhau bằng đường dẫn tương đối; publish truyền mọi trang HTML và `assets/` qua `files`.
- Bước 4 kiểm tra link tương đối giữa các trang trước khi publish.
- Sửa lỗi xuống dòng ở mục Giới hạn của SKILL.md (hai gạch đầu dòng bị dính nhau).
- `description` và bảng Đầu vào cập nhật; `allowed-tools` giữ nguyên nên lệnh chạy sản phẩm sẽ hỏi quyền khi cần.

## [1.7.0] - 2026-10-21

### Changed (behavior)
- **Thiết kế từ brief cũng chung bộ với `--revert-design`.** Mọi thiết kế trong `docs/prototype/` là một bộ = một thiết kế = **một artifact**; không tạo artifact riêng nữa.
- Chỉ còn **một** file `docs/prototype/.artifact.json` cho cả bộ (`url`, `screens`, `updated`). Bỏ `docs/prototype/<slug>/.artifact.json` và trường `type`.
- `--publish` luôn publish **cả bộ** (trang tổng hợp `docs/prototype/index.html` + các màn hình qua `files`). Không còn hỏi chọn thư mục khi publish.
- Thêm màn hình mới (từ brief hay revert) thì cập nhật trang tổng hợp, thêm vào `screens`, và cập nhật cùng artifact.
- Màn hình dựng từ brief cũng cập nhật trang tổng hợp `docs/prototype/index.html`.

### Updated
- SKILL.md có mục mới "Bộ prototype = một thiết kế = một artifact"; README, EXAMPLES, USER_PROMPT, SYSTEM_PROMPT cập nhật theo.

### Migration
- Nếu đã có `docs/prototype/<slug>/.artifact.json`: gộp thành một `docs/prototype/.artifact.json` (giữ một URL, thêm `screens`), xoá các file riêng; các artifact cũ còn lại không dùng nữa tự xoá thủ công nếu muốn.

## [1.6.1] - 2026-10-21

### Fixed
- `--revert-design`: trước đây mỗi màn hình revert có thư mục và `.artifact.json` riêng. Nay **tất cả UI revert là cùng một thiết kế**, dùng **một** `.artifact.json` chung ở `docs/prototype/.artifact.json`.
- Cả bộ revert publish thành **một artifact** (trang tổng hợp `docs/prototype/index.html` + các trang màn hình qua `files`).
- Revert thêm màn hình ở lần sau: thêm vào `screens` và cập nhật cùng artifact, không tạo mới.
- `--publish` không kèm brief: nhận ra bộ revert (qua `docs/prototype/index.html` hoặc `.artifact.json`); có cả bộ revert và thiết kế thường thì hỏi chọn.

### Unchanged
- Thiết kế thường (từ brief) vẫn dùng `docs/prototype/<slug>/.artifact.json` riêng cho từng thiết kế.

### Migration
- Đã revert và publish theo cách cũ: gộp các `<slug>/.artifact.json` thành một `docs/prototype/.artifact.json` (giữ một URL, thêm `screens`).

## [1.6.0] - 2026-10-21

### Changed (behavior)
- Gọi skill mà **không truyền brief hay flag nào** (`/nqdev-design-to-artifact`) giờ tự kích hoạt `--help`: đọc `EXAMPLES.md`, hiển thị hướng dẫn rồi dừng, không tạo file, không publish.
- `--help` tự gõ vẫn chỉ có hiệu lực khi là đối số duy nhất; đi kèm đối số khác thì bị bỏ qua.

### Updated
- `description`, SKILL.md, README, EXAMPLES, USER_PROMPT, SYSTEM_PROMPT cập nhật theo.

## [1.5.1] - 2026-10-21

### Fixed
- `description` trong SKILL.md chứa `<name>` bị coi là thẻ XML, gây lỗi "description cannot contain XML tags". Đã đổi thành `--themes=NAME`. Mô tả không còn ký tự `<` hoặc `>`.

## [1.5.0] - 2026-10-21

### Added
- Flag `--themes=<name_theme>` (bí danh `--theme=`): design theo quy chuẩn của theme.
- Theme đã biết: `heroui`, `heroui-v3` (https://heroui.com/), `bootstrap` (https://getbootstrap.com/), `material-v3` (https://m3.material.io/).
- Ghi nhớ theme cho cả bộ prototype trong `docs/prototype/.theme.json`.
- Lần sau không truyền `--themes`: tự dùng theme đã lưu.
- Truyền theme khác theme đã lưu: hỏi người dùng có bỏ qua theme mới và design tiếp theo theme cũ không ([A] giữ theme cũ, [B] đổi theme của cả bộ).
- Tên theme chưa biết: hỏi chọn theme đã biết hoặc xin link tài liệu chính thức.
- Đọc tài liệu chính thức của theme (WebFetch/WebSearch) để lấy token; comment đầu file ghi theme.
- `--revert-design`: dò thư viện UI đang dùng và gợi ý `--themes` (không tự lưu).

### Changed
- `allowed-tools` thêm `WebFetch`, `WebSearch`; `argument-hint` và `description` bổ sung `--themes`.

## [1.4.0] - 2026-10-21

### Changed (behavior)
- **Mặc định dừng ở local**, không còn hỏi `[A] Publish / [B] Chỉnh / [C] Dừng` và không gọi `Artifact`.
- Publish chỉ khi có `--publish` (flag là sự đồng ý của user, không hỏi xác nhận lại).

### Added
- Flag `--publish`. Dùng không kèm brief để publish thiết kế đã có trong `docs/prototype/` (nhiều thư mục thì hỏi chọn).
- Lưu link artifact vào `docs/prototype/<slug>/.artifact.json` sau lần publish đầu; các lần `--publish` sau cập nhật đúng artifact đó, không tạo mới.
- Link đã lưu không còn truy cập được / mất quyền sửa: hỏi user có tạo mới không, không tự tạo.
- Báo rõ "tạo mới" hay "cập nhật artifact đã có" sau khi publish.

### Changed
- `--update=<url>` chỉ có tác dụng khi đi cùng `--publish`; khác URL đã lưu thì ghi đè `.artifact.json`.
- `argument-hint`, `description`, EXAMPLES, README, USER_PROMPT, SYSTEM_PROMPT cập nhật theo.

### Removed
- Flag `--no-publish` (đã là hành vi mặc định). Nếu vẫn gõ thì bị bỏ qua.

## [1.3.0] - 2026-10-21

### Added
- Flag `--help`: khi là đối số duy nhất, đọc `EXAMPLES.md` và hiển thị làm hướng dẫn sử dụng, không tạo file, không publish.
- Khi `--help` đi kèm brief hoặc flag khác thì bị bỏ qua, skill chạy bình thường.
- `EXAMPLES.md` có thêm bảng "Danh sách flag" và Ví dụ 5 (`--help`).

### Changed
- `argument-hint` và `description` bổ sung `--help`.

## [1.2.0] - 2026-10-21

### Changed
- Nơi lưu thiết kế đổi từ `design/<slug>/` sang `./docs/prototype/<slug>/` (áp dụng cho cả `--revert-design`).
- `.artifact.json` cũng nằm trong `docs/prototype/<slug>/`.

### Added
- Thư mục `docs/prototype/` chưa có thì tạo trước (`mkdir -p`) khi ghi file.
- Slug đã tồn tại thì hỏi user trước khi ghi đè.

### Migration
- Thiết kế cũ trong `design/<slug>/` cần chuyển thủ công sang `docs/prototype/<slug>/`; `--update` chỉ tìm `.artifact.json` ở vị trí mới.

## [1.1.0] - 2026-10-21

### Added
- Flag `--revert-design[=<path|feature>]`: đọc UI đã có trong project (chưa có thiết kế) và dựng lại bản thiết kế giống UI đó.
- Quy trình R1–R8 cho chế độ revert: xác định phạm vi, đọc nguồn, trích xuất, dựng lại, bảo mật dữ liệu, UI sạch, đối chiếu, review/publish.
- Comment nguồn ở đầu file thiết kế (đường dẫn UI gốc, phần đã đơn giản hóa).
- Ví dụ và edge case cho `--revert-design` trong README, USER_PROMPT, EXAMPLES.

### Changed
- `argument-hint` và `description` bổ sung `--revert-design`.
- Brief không bắt buộc khi dùng `--revert-design`.

## [1.0.0] - 2026-10-21

### Added
- Workflow design local → review → publish lên Artifact.
- Quy tắc "UI sạch": không hiển thị mô tả tính năng trên giao diện, mô tả đặt trong comment code.
- Bước tự kiểm tra UI sạch trước khi review.
- Cập nhật artifact cũ qua `--update=<url>` hoặc `.artifact.json`.
- Cờ `--no-publish`.
- Fallback khi không có `Artifact` tool.
- Bộ tài liệu: README, SYSTEM_PROMPT, USER_PROMPT, EXAMPLES, CHANGELOG.

### Assumptions
- Loại thiết kế mặc định: UI mockup / landing page (một file HTML).
- Cơ chế publish: `Artifact` tool; chưa dùng DesignSync.
- Artifact mặc định private.
- `disable-model-invocation: true`.
