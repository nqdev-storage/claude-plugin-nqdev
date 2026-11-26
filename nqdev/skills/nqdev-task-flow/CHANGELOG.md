# Changelog — nqdev-task-flow

Các phiên bản trước (khi skill còn tên `nqdev-flow`, tới 1.3.1) chưa có file này; xem mục "Lịch sử thay đổi" trong [nqdev/README.md](../../README.md).

## [1.8.0] - 2026-11-26

### Added
- Mục *Mốc bước 0 và bước bàn giao*: ghi mốc giờ hệ thống ở lượt đầu tiên làm Bắt đầu dòng 0 của plan, kết thúc lúc duyệt plan; dòng bàn giao bắt đầu ở bước `mr` (hoặc bước chốt), kết thúc khi người dùng xác nhận đã chốt. Khớp `nqdev-write-plan` 1.10.0.

### Changed
- *Chạy theo lô* không bốc bước 0 và bước bàn giao; bước `code` xong khi hết `todo` trừ dòng bàn giao (cả dấu hiệu "đã xong" trong `references/feature.md`). Lý do: dòng bàn giao chứa commit/push, không được giao cho agent, và chỉ xong sau bước chốt.

## [1.7.1] - 2026-11-26

### Changed
- Bước nhận kết quả cập nhật cả `time_spent_md` cùng `time_spent_hours`, khớp `nqdev-write-plan` 1.9.0.

## [1.7.0] - 2026-11-20

### Changed
- Chạy theo lô chỉ áp dụng cho plan lớn (`assign_tasks: true`, theo ngưỡng của `nqdev-write-plan` 1.8.0). Lúc duyệt plan, đề xuất lớn/nhỏ để người dùng chốt; plan nhỏ không sinh `.jsonl`, bước `code` bàn giao từng bước như cũ.
- `references/feature.md`: bước `plan`, `code` và "Dấu hiệu đã xong" cập nhật theo.

## [1.6.0] - 2026-11-20

### Added
- Mục *Chạy theo lô* ở bước `code`: plan `approved` có file giao việc `.claude/assign-tasks/<tên plan>.jsonl` (sinh bởi `nqdev-write-plan` 1.7.0) và tool có subagent thì bốc lô theo `batch` và `depends_on` (tối đa 3 bước), giao cho `agent` ghi trong file, cập nhật `status` / `started_at` / `ended_at` ở `.jsonl` và mốc thời gian ở bảng Tiến độ của plan, dừng duyệt sau mỗi lô. Thiếu điều kiện thì bàn giao từng bước như cũ.

### Changed
- Duyệt plan: ngoài đổi `status: approved` còn điền bảng Giao việc và sinh `.jsonl`; sửa plan sau khi duyệt thì sinh lại `.jsonl`.
- Ràng buộc 2 và 7: thêm ngoại lệ chạy theo lô (mỗi lượt một lô; luồng điều phối vẫn không tự sửa code).
- `references/feature.md`: bước `plan`, `code` và bảng "Dấu hiệu đã xong" cập nhật theo.

## [1.5.0] - 2026-11-19

### Changed
- `references/feature.md`: tên file plan theo quy ước mới của `nqdev-write-plan`, `plans/<stt>-<YYYY-MM-DD>-<slug>.md` (`stt` là số 3 chữ số, lớn nhất đang có trong `plans/` cộng 1).

## [1.4.0] - 2026-11-19

### Changed
- **Breaking**: đổi tên skill `nqdev-flow` thành `nqdev-task-flow` (thư mục, `name`, tiêu đề, ví dụ lệnh). Lệnh gọi là `/nqdev:nqdev-task-flow` (Codex CLI: `$nqdev-task-flow`). Không giữ alias tên cũ.
- `references/bugfix.md`, `feature.md`, `init.md`: đổi lệnh quay lại bước (`--from=<bước kế>`) sang tên mới.
- Nội dung nghiệp vụ của 4 workflow không đổi.
