# Changelog

Định dạng theo Semantic Versioning (`MAJOR.MINOR.PATCH`).

## [2.1.4] - 2026-11-21
### Changed
- `references/brd-template.md`: dòng "Nên đọc trước" gợi ý `docs/Business-Document.md` (bối cảnh cấp dự án do `nqdev-init-agents` tạo) nếu repo có.

## [2.1.3] - 2026-11-19
### Changed
- `README.md`: mô tả `nqdev-requirement-estimator` theo giờ (AI làm, DEV review) thay cho person-days, khớp estimator 5.0.0.

## [2.1.2] - 2026-11-17
### Changed
- `references/edge-cases.md`: khi người dùng đưa source code và muốn tài liệu luồng nghiệp vụ, gợi ý `nqdev-business-flow-extractor` (không tự chuyển).

## [2.1.1] - 2026-11-17
### Changed
- Description: yêu cầu trích xuất luồng nghiệp vụ từ source code trỏ sang `nqdev-business-flow-extractor`, để hai skill không cùng kích hoạt cho "viết tài liệu nghiệp vụ".

## [2.1.0] - 2026-11-16
### Changed
- Bỏ tham chiếu tới `nqdev-codebase-analyst` (không có trong bộ nqdev-) ở description, ràng buộc 8, README và `references/edge-cases.md`
- Người dùng đưa source code: không chuyển sang skill khác nữa; đề nghị đưa tài liệu hệ cũ, hoặc chỉ dùng code làm bối cảnh phụ cho mục 10 kèm `[cần xác nhận]`
- Đổi tên tham chiếu `nqdev-client-requirement-insight` thành `nqdev-requirement-estimator` (description, ràng buộc 9, README, EXAMPLES, edge-cases)

## [2.0.0] - 2026-11-16
### Changed (phá vỡ tương thích)
- Đầu ra mặc định: BRD theo module tại `docs/brd/<module>.md` (trước đây là 2 file `BRD-<ten-du-an>.md` + `PRD-<ten-du-an>.md`)
- Khuôn và quy ước đọc từ repo (`docs/brd/README.md`, `docs/brd/_TEMPLATE.md`); khuôn của repo thắng khuôn đóng kèm
- Khuôn BRD đóng kèm đổi sang 13 mục: Phạm vi, Thuật ngữ, Tác nhân, Yêu cầu nghiệp vụ, Luồng sử dụng, Quy tắc nghiệp vụ, Tiêu chí nghiệm thu, Dữ liệu, Tích hợp, Đối chiếu hệ cũ, Phi chức năng, Câu hỏi mở, Lịch sử thay đổi
- Hệ mã mới `BR-<MODULE>-<số>`, `AC-<MODULE>-<số>`, `UC-<MODULE>-<số>`; bỏ `RULE-`, `NFR-` trong BRD
- Không còn cho phép gộp mục; mục không áp dụng giữ tiêu đề và ghi lý do
- PRD thành tuỳ chọn, lưu `docs/prd/<module>.md`, mã `FR-<MODULE>-<số>` trỏ về BR và dùng lại mã AC của BRD
### Added
- Quy tắc cho tính năng vắt ngang nhiều module, bỏ yêu cầu đã phát hành ("Đã bỏ", giữ mã), cập nhật tại chỗ file đã có
- Ràng buộc cho mục Dữ liệu (mức nghiệp vụ) và Đối chiếu hệ cũ (Giữ cần căn cứ độc lập)

## [1.1.0] - 2026-11-12
### Changed
- Tách template BRD/PRD và bảng edge case ra `references/` (nạp khi cần), `SKILL.md` giảm từ 9,4 KB xuống 4,6 KB
- Sửa mâu thuẫn số câu hỏi làm rõ: một trần duy nhất là 4 câu (khớp giới hạn AskUserQuestion)
- Viết lại quy trình thành mục tiêu + ràng buộc cứng (kèm lý do) + tiêu chí hoàn thành
- Làm rõ `[cần xác nhận]` chỉ áp dụng cho giá trị/ngưỡng/tên chưa có nguồn, không gắn cho mã tự đặt
- Cho phép gộp BRD §9–§11 với dự án nhỏ; bỏ đường dẫn mặc định `docs/requirements/`
- `compatibility` thêm Gemini CLI và Codex CLI theo Project Instructions mới
- Description thêm "SRS nghiệp vụ"

## [1.0.0] - 2026-11-12
### Added
- Phát hành đầu tiên của `nqdev-brd-prd-writer`
- Quy trình 6 bước: thu thập → hỏi làm rõ → dàn ý và mã → viết BRD/PRD → tự kiểm tra → giao
- Template BRD (14 mục) và PRD (13 mục) với placeholder sơ đồ/ảnh
- Hệ thống mã truy vết `BR` / `FR` / `NFR` / `AC` / `RULE` và ma trận truy vết
- Bảng edge case và ranh giới với `nqdev-codebase-analyst`, `nqdev-client-requirement-insight`
- Bộ tài liệu: README, SYSTEM_PROMPT, USER_PROMPT, EXAMPLES, CHANGELOG
