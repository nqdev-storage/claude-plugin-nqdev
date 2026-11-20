# Changelog

Định dạng theo [Semantic Versioning](https://semver.org/). Ngày theo ISO 8601.

## [5.0.0] - 2026-11-19

### Changed
- **Breaking**: đổi mô hình estimate từ person-day của 1 senior dev sang **giờ (bước 0.5)** với **AI là người làm, DEV là người review và góp ý**. Mỗi dòng có 3 cột AI | DEV review | Tổng (end-to-end tới khi sẵn sàng merge, gồm các vòng sửa theo góp ý).
- `references/baselines.md`: viết lại toàn bộ baseline theo mô hình mới, có giả định chuẩn, hệ số context áp lên từng cột, mục Hiệu chỉnh (so `estimated_hours` với `time_spent_hours` của `nqdev-write-plan`). Số liệu dựa trên kinh nghiệm, chưa đo.
- Công thức: Tổng = Dev + QA/UAT (15–20% Dev, một dòng). Bỏ dòng PM và bỏ timeline theo tuần. Kiểm tra khả thi so giờ DEV cần với quỹ giờ DEV (số DEV × 24 giờ/tuần × số tuần).
- `SKILL.md`, `SYSTEM_PROMPT.md`, `USER_PROMPT.md`, `README.md`, `references/output-widget.md`: cập nhật đơn vị, mô hình, đầu vào (số DEV review, công cụ AI).
- `EXAMPLES.md`: TC2 tính lại theo giờ (Dev 19–33, Tổng 22–39.5); TC3 viết lại theo giờ DEV so với quỹ giờ DEV.

## [4.0.2] - 2026-11-17

### Fixed
- `SKILL.md`: đổi tiêu đề cũ "Client Requirement Insight" thành "Requirement Estimator" cho khớp tên skill.

## [4.0.1] - 2026-11-16

### Fixed
- `references/brd-prd-input.md`: bỏ tham chiếu tới `nqdev-codebase-analyst` (không có trong bộ nqdev-).
- Mục Migration của 4.0.0 đã xong: `nqdev-brd-prd-writer` 2.1.0 trỏ đúng tên `nqdev-requirement-estimator`.

## [4.0.0] - 2026-11-16

Đổi tên skill từ `nqdev-client-requirement-insight` thành `nqdev-requirement-estimator`. Nội dung và hành vi giữ nguyên như 3.1.0.

### Changed
- `name`, thư mục skill và thư mục gốc trong gói `.skill` đổi sang `nqdev-requirement-estimator`.
- README: tiêu đề, cấu trúc thư mục và lệnh gọi Codex CLI (`$nqdev-requirement-estimator`).

### Migration
- Lệnh `/nqdev-client-requirement-insight` không còn dùng được; gỡ skill tên cũ trước khi cài để tránh hai skill trùng chức năng.
- `nqdev-brd-prd-writer` vẫn trỏ về tên cũ (description, rule 9, edge-cases); cập nhật skill đó riêng.

## [3.1.0] - 2026-11-16

Thêm đầu vào BRD/PRD từ `nqdev-brd-prd-writer`; cách dùng cũ (mô tả/spec trực tiếp) giữ nguyên.

### Added
- Mục "Nguồn đầu vào" trong `SKILL.md` và `references/brd-prd-input.md`: đọc `docs/brd/<module>.md`, `docs/prd/<module>.md`, estimate theo BR/FR, ghi mã truy vết, gom "Câu hỏi mở" thành câu hỏi clarify, dedupe tính năng vắt ngang module, xử lý nguồn lệch nhau.
- Bất biến "Giai đoạn theo nguồn": không ghi đè cột "Giai đoạn"; đề xuất khác gắn nhãn "đề xuất đổi".
- Ranh giới với `nqdev-brd-prd-writer`: skill chỉ đọc và estimate, không viết hay ghi file vào `docs/brd`, `docs/prd`; kết quả trả trong chat.
- Mẫu prompt "Estimate từ BRD/PRD" trong `USER_PROMPT.md`; gold case TC4 (BRD mẫu module `INVOICE`) trong `EXAMPLES.md`.
- Gemini CLI và Codex CLI trong `compatibility` và bảng Supported tools.

### Changed
- `description` nêu đầu vào BRD/PRD và ranh giới không viết BRD/PRD.
- `risk-catalog.md` và `output-widget.md` tham chiếu mã BR/FR và tín hiệu "Cần thêm" của BRD mục 9.
- Frontmatter lấy bản đồng bộ làm gốc: `version`, `created_date`, `updated_date` quote chuỗi, `metadata` mirror.

### Fixed
- Estimate không truy vết về mã BR/FR.
- Skill có thể xếp phase trái với cột "Giai đoạn" của BRD.
- Câu hỏi clarify có thể trùng hoặc bỏ sót "Câu hỏi mở" của BRD.

## [3.0.0] - 2026-10-27

Refactor lớn theo Single-Agent Loop và Progressive Disclosure. Bản trước chưa có metadata phiên bản; từ bản này đánh số 3.0.0.

### Changed
- Thay luồng 6 bước tuần tự bằng "đầu ra bắt buộc + bất biến", để model tự lập kế hoạch.
- `description` thu gọn, chỉ nêu việc skill làm và khi nào dùng; loại bỏ cụm gây over-trigger.
- Thống nhất công thức: QA/UAT một dòng (15–20% Dev), PM 10%, timeline = Tổng ÷ (số dev × 4) tuần.
- Trả lời theo ngôn ngữ người dùng (mặc định tiếng Việt).
- Hình thức trình bày mặc định là Markdown; widget chuyển thành tùy chọn.

### Added
- Metadata NQDev đầy đủ (version, author, created_date, updated_date, `metadata` mirror) và `license`, `compatibility`, `allowed-tools`, `argument-hint`.
- Quy tắc kiểm tra khả thi (deadline/team so với timeline tính được).
- `references/risk-catalog.md` theo loại dự án (thay checklist thiên về một dự án cũ).
- `README.md`, `SYSTEM_PROMPT.md`, `USER_PROMPT.md`, `EXAMPLES.md` (3 gold cases), `CHANGELOG.md`.

### Fixed
- `estimation-cheatsheet.md` không được link: gộp vào `references/baselines.md`, một nguồn số duy nhất.
- Mâu thuẫn baseline (full-text search, auth, hệ số junior, số môi trường) và công thức (QA, timeline).
- Mâu thuẫn "luôn hỏi 5 câu" với "vẫn estimate khi spec mơ hồ".
- Template widget: bỏ class thiếu định nghĩa, bổ sung assumptions/exclusions/câu hỏi, hỗ trợ dark mode.

### Removed
- Bảng baseline trùng trong SKILL.md, exclusions trùng, CSS widget dài (~5KB).
- `references/estimation-cheatsheet.md` và `references/widget-template.md` (thay bằng `baselines.md` và `output-widget.md`).
