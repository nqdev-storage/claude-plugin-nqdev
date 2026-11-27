# nqdev-brd-prd-writer

## Overview
Skill giúp AI viết **BRD theo từng module** vào `docs/brd/<module>.md`, tuân thủ khuôn và quy ước của repo (`docs/brd/README.md`, `docs/brd/_TEMPLATE.md`). PRD là tuỳ chọn, chỉ viết khi được yêu cầu.

## Purpose
Biến yêu cầu thô thành BRD cùng một khuôn giữa các module, truy vết được bằng mã `BR/AC/UC-<MODULE>-<số>`, để owner module viết song song, người duyệt nghiệp vụ soát nhanh và dev/QA dùng lại mã ở test và merge request.

## Target users
Owner module, Business Analyst, Product Manager, Tech Lead.

## Features
- Đọc khuôn và quy ước từ repo; repo chưa có thì dùng khuôn 13 mục đóng kèm
- Mỗi module một file; giữ nguyên thứ tự và đủ mục của khuôn
- Mã `BR-<MODULE>-<số>`, `AC-<MODULE>-<số>`, `UC-<MODULE>-<số>`; mã đã phát hành không đổi, không dùng lại
- Xử lý tính năng vắt ngang nhiều module (BR chính, BR trỏ, hợp đồng/sự kiện ở mục 9)
- Đánh dấu `[cần xác nhận: ...]` thay vì bịa; gom vào "Câu hỏi mở" kèm người cần hỏi
- Cập nhật tại chỗ file BRD đã có, ghi "Lịch sử thay đổi"
- PRD tuỳ chọn tại `docs/prd/<module>.md`, FR trỏ về BR

## Input format
Tên module và nguồn nghiệp vụ: mô tả, ghi chú họp, yêu cầu khách hàng, file chốt nghiệp vụ, tài liệu hệ cũ người dùng chỉ ra.

## Output format
Một file Markdown `docs/brd/<module>.md` theo khuôn, kèm tóm tắt ngắn (số BR/AC/UC, số mục chờ xác nhận, rủi ro phát hiện). Tuỳ chọn: `docs/prd/<module>.md`.

## Usage
- Claude Code / OpenCode / Gemini CLI / Codex CLI: `Dùng nqdev-brd-prd-writer viết BRD cho module billing từ <nguồn>`
- Claude.ai: import file `.skill`, nêu module và dán nguồn nghiệp vụ; kết quả trả về dạng file hoặc trong chat.

Xem thêm [EXAMPLES.md](EXAMPLES.md).

## Edge cases
Xem [references/edge-cases.md](https://github.com/nqdev-storage/claude-plugin-nqdev/blob/dist/nqdev/skills/nqdev-brd-prd-writer/references/edge-cases.md): không rõ module, file đã tồn tại, bỏ yêu cầu, tính năng nhiều module, yêu cầu mâu thuẫn hoặc không đo được.

## Limitations
- Không dựng ngược từ source code, không ước lượng thời gian/chi phí
- Không sửa `docs/brd/README.md` (bảng module, trạng thái) và không tự tạo `_TEMPLATE.md`
- Không tạo sơ đồ/ảnh thật
- Không thay bước soát của dự án (reviewer, người duyệt nghiệp vụ)
- Đầu vào mỏng cho ra nhiều mục `[cần xác nhận]`

## Best practices
- Đặt `docs/brd/README.md` và `_TEMPLATE.md` vào repo trước để mọi module cùng khuôn
- Chỉ rõ dòng/đoạn của file chốt nghiệp vụ làm nguồn cho từng BR
- Rà "Câu hỏi mở" với người duyệt trước khi chuyển trạng thái "Chờ duyệt"

## Supported tools
Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai. Không dùng tính năng riêng của công cụ nào; trên Claude.ai không có repo nên dùng khuôn đóng kèm trừ khi người dùng dán khuôn của họ.

## Related skills
- `nqdev-requirement-estimator`: estimate theo giờ (AI làm, DEV review), phase MVP
- `nqdev-system-design-diagram`: vẽ sơ đồ luồng cho UC

## Recommended improvements
- Script kiểm tra tự động: đủ 13 mục, BR nào cũng có AC, mã không trùng
- Chế độ soát chéo hai file BRD của tính năng vắt ngang module
- Sinh khung test case từ bảng AC
- Khuôn PRD theo module do repo quy định (`docs/prd/_TEMPLATE.md`)
