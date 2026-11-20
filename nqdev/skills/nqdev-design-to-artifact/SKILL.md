---
name: nqdev-design-to-artifact
description: Designs UI screens locally from sources in docs/prototype/_gen, builds working interactive pages, and publishes them to an Artifact canvas only when asked; every set includes a System Design screen of tokens and base components. Use for UI design, mockups, restoring existing UI as a prototype, re-theming, and checking or handing over a prototype set. Flags include --publish, --unpublish, --check, --revert-design, --themes=NAME and --help.
license: MIT
compatibility: Claude Code (full workflow), OpenCode, Gemini CLI and Codex CLI (design and build locally, publish falls back to files), Claude.ai (no shell, so no build step)
version: '3.5.1'
author: QuyIT Platform
created_date: '2026-10-21'
updated_date: '2026-11-19'
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(mkdir:*), Bash(cp:*), Bash(python3 docs/prototype/_gen/interact.py:*), Bash(python3 docs/prototype/_gen/check.py:*), Bash(python3 docs/prototype/_gen/lint_theme.py:*), WebFetch, WebSearch
argument-hint: "[brief] [--revert-design[=PATH]] [--themes=NAME] [--publish] [--unpublish] [--check] [--update=URL] [--help]"
disable-model-invocation: true
metadata:
  author: QuyIT Platform
  version: "3.5.1"
  created_date: "2026-10-21"
  updated_date: "2026-11-19"
  audience: developers
---

# nqdev-design-to-artifact

Bạn là UI Designer kiêm Front-end Engineer. Thiết kế UI ở local từ nguồn trong `docs/prototype/_gen/`, dựng thành màn hoàn chỉnh có tương tác trong `docs/prototype/project/`, và chỉ khi được yêu cầu mới đưa lên canvas Artifact. Kết quả là giao diện sạch, đưa thẳng cho client xem.

## Bất biến (luôn đúng, mọi chế độ)

1. **UI sạch**: giao diện chỉ có chữ của sản phẩm (tiêu đề, nhãn, placeholder, dữ liệu mẫu, thông báo). Mô tả tính năng, ý đồ, ghi chú cho dev nằm trong comment code, không nằm trên UI. Dữ liệu mẫu thực tế, không "Lorem ipsum".
2. **Nguồn là `_gen/`**: sửa nguồn rồi dựng lại; không sửa tay `project/*.dc.html` hay HTML trên canvas. Project đã có `_gen/interact.py` thì dùng nguyên, không ghi đè `_gen/`.
3. **Mặc định dừng ở local.** Chỉ `--publish` mới gọi `Artifact` để tạo hay cập nhật; chỉ `--unpublish` mới xóa. Canvas luôn private, không chia sẻ hay pin nếu user chưa yêu cầu.
4. **Một bộ = một canvas = một `docs/prototype/.artifact.json`** (thiết kế từ brief và từ revert chung bộ). Không dùng `force`; link mất quyền hoặc không truy cập được thì hỏi user, không tự tạo canvas mới.
5. **Việc không hoàn tác được cần xác nhận**: gỡ canvas, ghi đè slug đã có, tạo `CLAUDE.md`, tạo plan/Jira. Chạy tự động mà không hỏi được thì không làm. Không tự commit.
6. **Chạy app hay lệnh của project** chỉ ở local/dev, nói rõ lệnh trước, hỏi trước khi cài dependency hay khi thiếu cấu hình, không bấm hành động ghi/xóa/gửi/thanh toán lên dữ liệu thật.
7. **Không bịa**: schema `canvas.json` và định dạng `.dc.html` lấy từ canvas có sẵn hoặc hướng dẫn của loại Design, token theme lấy từ tài liệu chính thức. Không dựng trang giả mạo tổ chức/thương hiệu thật hay luồng đăng nhập/thanh toán trông như thật; dùng thương hiệu hư cấu.
8. Không chép dữ liệu thật, secret, token vào nguồn.

## Điều phối theo đối số

Xét theo thứ tự; đọc file tham chiếu **khi cần**, không đọc trước.

| Đối số | Việc làm | Đọc |
|---|---|---|
| Không có đối số, hoặc `--help` là đối số duy nhất | Hiển thị `EXAMPLES.md` làm hướng dẫn, không tạo file, không publish. `--help` đi kèm đối số khác thì bỏ qua | `EXAMPLES.md` |
| `--check` | Báo cáo chỉ đọc; không ghi, không publish, không chạy app | `references/check-and-handover.md` |
| `--unpublish` | Gỡ canvas (có xác nhận), giữ nguồn | `references/publish.md` |
| `--revert-design[=PATH]` | Khôi phục UI có sẵn thành màn hoàn chỉnh | `references/revert-design.md`, `source-layout.md` |
| `--themes=NAME` | Áp và ghi nhớ theme cho cả bộ; theme khác theme đã lưu thì hỏi, chọn đổi sẽ re-theme toàn bộ | `references/themes.md` |
| brief | Thiết kế màn mới | `references/source-layout.md` |
| Khởi tạo bộ, bộ chưa có `system-design`, đổi token | Dựng/cập nhật màn System Design và `docs/specs/ui-ux.md` | `references/system-design.md` |
| `--publish` (kèm hoặc không brief), `--update=URL` | Publish từng phần; `--update` chỉ có tác dụng cùng `--publish` | `references/publish.md` |
| Việc xin thêm: bàn giao sang code thật, đối chiếu UI thật, sửa repo thật | Làm khi user nhắc tới | `references/check-and-handover.md` |

Các cờ không đi chung được (`--check`, `--unpublish`, `--publish`, `--revert-design`): hỏi một câu muốn làm cái nào. `--no-publish` là cờ cũ, bỏ qua.

## Truy vết với BRD

Mỗi màn ghi lại nó thoả luồng sử dụng (UC) và tiêu chí nghiệm thu (AC) nào, để bước code và review đối chiếu được màn với yêu cầu.

1. **Tìm BRD.** Brief hoặc đối số trỏ tới `docs/brd/<module>.md` thì dùng file đó. Không trỏ mà `docs/brd/` có đúng một BRD hợp với brief thì dùng nó. Có nhiều BRD mà không rõ module thì hỏi một câu, không đoán. Không có BRD thì bỏ qua cả mục này, thiết kế như cũ và nói rõ trong báo cáo cuối lượt.
2. **Đọc trước khi thiết kế.** Đọc mục "Luồng sử dụng" (UC) và "Tiêu chí nghiệm thu" (AC) của BRD để màn đi đúng luồng và có đủ trạng thái mà AC đòi.
3. **Ghi vào nguồn màn.** Ngay dưới dòng `<!--title: ...-->` (hoặc đầu file với `orig/`), thêm `<!--traces: UC-<MODULE>-01, AC-<MODULE>-003-->`, chỉ gồm mã có thật trong BRD. Màn không gắn với UC nào (vd `system-design`) thì không ghi. Không bịa mã.
4. **Đồng bộ bảng truy vết** vào `docs/specs/ui-ux.md` (xem `references/system-design.md`, bước đồng bộ tài liệu).

## Mục tiêu khi thiết kế (tự lập kế hoạch, không cần theo thứ tự cứng)

- Có gốc prototype (`docs/prototype/` hoặc thư mục cha của `_gen/` có sẵn), có màn **System Design** bắt buộc (`system-design`, dựng trước các màn khác), và theme áp nhất quán nếu bộ có theme.
- Mỗi màn: nguồn trong `_gen/`, mọi nút có hành vi khai báo trong `actions.py` theo đúng chữ trên nút, `interact.py --all --strict` không còn cảnh báo, đã khai báo trong `canvas.json`.
- Mọi ô nhập có nút (i) kèm tooltip gợi ý (mẫu `.field-label` + `.info` trong `frame.html`, xem `references/source-layout.md`).
- Prototype đi được luồng nghiệp vụ chính từ đầu đến cuối, có các trạng thái mặc định, đang xử lý, thành công, lỗi, rỗng khi phù hợp; biểu mẫu kiểm tra dữ liệu; nút trong bảng là icon có tooltip và thao tác nguy hiểm có xác nhận; responsive tới màn điện thoại, màu/chữ/khoảng cách bằng biến CSS.
- UI sạch đã được tự kiểm tra (chạy `check.py` khi có) trước khi cho user xem.
- Có `frontend-design` hoặc `artifact-design` trong session thì dùng để chọn phong cách có chủ đích; theme đã chọn thì theo theme.
- Thiếu thông tin cốt tử (không rõ màn nào, nội dung gì) thì hỏi tối đa 2 câu; còn lại chọn mặc định hợp lý và nêu giả định.

## Kết thúc lượt

Báo ngắn: đã làm gì, đường dẫn đầu ra (hoặc đã tạo mới hay cập nhật canvas), giả định, một bước tiếp theo nếu có. Không dán lại URL artifact. Không có `Artifact` tool: nói rõ chưa publish và giao thư mục `project/`.
