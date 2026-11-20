# Changelog — nqdev-write-plan

Định dạng theo [Keep a Changelog](https://keepachangelog.com/), phiên bản theo Semantic Versioning.

## [1.5.0] — 2026-11-19

### Changed
- Template Pre: mục 1 là "Bối cảnh"; mục 2 thành "Approach và quyết định đã chốt" (ghi cả quyết định đã chốt với người dùng); mục 3 "Tiến độ" là bảng `# | Bước | Trạng thái | Ghi chú` với trạng thái `chưa làm` / `đang làm` / `xong` / `bỏ`, thay checklist Todo `[x]/[~]/[ ]`; mục 4 "Risks và Unknowns". Mục "Vòng đời một plan" cập nhật theo.
- `references/example-plan.md`: thêm ví dụ Pre (đang làm, có quyết định đã chốt, bảng Tiến độ đủ 4 trạng thái, Nhật ký thay đổi plan); rút gọn ví dụ Post và mục "Vì sao đúng chuẩn".

## [1.4.0] — 2026-11-19

### Changed
- `estimated_hours` làm tròn đến 0.5 giờ và là tổng end-to-end theo mô hình AI làm, DEV review và góp ý (khớp `nqdev-requirement-estimator` 5.0.0). Thời gian thực tế (`time_spent_hours`, bảng nhật ký) vẫn làm tròn đến 0.25.
- `README.md`: cập nhật quy tắc ước lượng.

## [1.3.0] — 2026-11-19

### Changed
- Quy ước tên file đổi từ `plans/<YYYY-MM-DD>-<slug>.md` thành `plans/<stt>-<YYYY-MM-DD>-<slug>.md`. `stt` là số thứ tự 3 chữ số, bộ đếm chung cho cả `plans/`: lấy số lớn nhất đang có cộng 1, bắt đầu từ `001`, vượt `999` thì dùng 4 chữ số.
- Bước "Tìm plan liên quan" lấy luôn `stt` từ danh sách `plans/` vừa liệt kê; bỏ qua file chưa có `stt` (file cũ, `cleanup-report-*.md`).
- `README.md`, `references/example-plan.md`: cập nhật quy ước và ví dụ tên file.

## [1.2.1] — 2026-11-18

### Changed
- Frontmatter: bỏ nháy ở `name` theo quy ước tên skill của repo.

## [1.2.0] — 2026-11-17

### Added
- Mục **Ghi nhận thời gian**: đơn vị giờ làm tròn 0.25; định nghĩa một lần làm; quy trình cuối mỗi lần làm (đề xuất số giờ từ mốc thời gian → người dùng xác nhận → thêm dòng và cộng dồn); xử lý khi không có người xác nhận, khi vượt ước lượng, và với plan cũ.
- Mục bắt buộc **Nhật ký thời gian** (bảng Ngày / Số giờ / Việc đã làm / Ghi chú, có hàng Tổng) trong cả Template Pre và Template Post.
- Bước "Ghi nhận thời gian" trong Quy trình và trong Vòng đời một plan.
- Ví dụ có Nhật ký thời gian với 2 lần làm cộng dồn thành `time_spent_hours: 3`.

### Changed
- `estimated_hours` bắt buộc với plan Pre (nhật ký Post vẫn tuỳ chọn).
- `time_spent_hours` là tổng cộng dồn, khởi tạo `0` và cập nhật sau mỗi lần làm thay vì chỉ điền khi xong.
- Số giờ ghi dạng số (`1.5`), bỏ dạng `~X`; plan cũ được chuyển khi cập nhật lần đầu.
- Description thêm phần ước lượng và cộng dồn thời gian, thêm trigger "ghi nhận thời gian làm vào plan".

## [1.1.0] — 2026-11-17

Bản đầu tiên có metadata theo chuẩn NQDev. Bản trước không ghi version, được coi là 1.0.0.

### Added
- Frontmatter đầy đủ: `license`, `compatibility`, `version`, `author`, `created_date`, `updated_date`, `allowed-tools` và `metadata` sao chép các trường NQDev.
- Mục **Quy trình** 6 bước: tìm repo root, tìm plan liên quan, chọn ngôn ngữ, soạn, xin phép trước khi ghi, báo lại.
- Cách xử lý khi không phải git repo hoặc không có filesystem (Claude.ai): trả plan trong chat, không nói là đã ghi.
- Mục **Vòng đời một plan**: `planning → in_progress → completed / blocked / paused`, ký hiệu Todo `[x]` `[~]` `[ ]` (khớp Development Workflow Policy của `nqdev-init-agents`), mục `## Kết quả` khi xong, *Nhật ký thay đổi plan*.
- Frontmatter chung cho cả hai chế độ, có thêm `mode`, `priority`, `paused`, `completed_date`.
- `README.md`, `CHANGELOG.md`.

### Changed
- Description: bỏ "PHẢI dùng" / "LUÔN chủ động gọi", thu hẹp trigger, thêm phần khi nào **không** dùng. Skill vẫn được tự đề xuất nhưng chỉ ghi file khi người dùng đồng ý.
- Quy tắc gộp file: cập nhật plan **cùng chủ đề, chưa `completed`**, không còn phụ thuộc "cùng ngày".
- Quy tắc ngày: ngày trong tên file là ngày tạo file và không đổi; bỏ mâu thuẫn giữa "ngày thực hiện" và "ngày lập kế hoạch".
- Không cần hậu tố `-planning` / `-roadmap` trong slug nữa (file cũ vẫn hợp lệ).
- H1 của chế độ Post đổi thành `# Nhật ký:`.
- Quy tắc mục trống: mục bắt buộc ghi "Không có", mục tùy chọn thì bỏ hẳn.
- Tín hiệu tự đề xuất: dùng tiêu chí cụ thể thay cho "tần suất git commits".
- `references/example-plan.md`: thêm frontmatter, H1 `# Nhật ký:`, link tương đối trong bảng file, giải thích thêm.

### Fixed
- Lỗi chính tả "dự trên" và chữ "machine để tối ưu".

### Lưu ý tương thích
- File plan cũ (không có `mode`, `priority`, `completed_date`, H1 `# Kế hoạch:` cho nhật ký) vẫn đọc và cập nhật được; agent bổ sung trường còn thiếu khi cập nhật.
