# Changelog — nqdev-task-flow

Các phiên bản trước (khi skill còn tên `nqdev-flow`, tới 1.3.1) chưa có file này; xem mục "Lịch sử thay đổi" trong [nqdev/README.md](../../README.md).

## [1.5.0] - 2026-11-19

### Changed
- `references/feature.md`: tên file plan theo quy ước mới của `nqdev-write-plan`, `plans/<stt>-<YYYY-MM-DD>-<slug>.md` (`stt` là số 3 chữ số, lớn nhất đang có trong `plans/` cộng 1).

## [1.4.0] - 2026-11-19

### Changed
- **Breaking**: đổi tên skill `nqdev-flow` thành `nqdev-task-flow` (thư mục, `name`, tiêu đề, ví dụ lệnh). Lệnh gọi là `/nqdev:nqdev-task-flow` (Codex CLI: `$nqdev-task-flow`). Không giữ alias tên cũ.
- `references/bugfix.md`, `feature.md`, `init.md`: đổi lệnh quay lại bước (`--from=<bước kế>`) sang tên mới.
- Nội dung nghiệp vụ của 4 workflow không đổi.
