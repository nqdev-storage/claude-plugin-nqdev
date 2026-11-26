# Changelog — nqdev-write-plan

Định dạng theo [Keep a Changelog](https://keepachangelog.com/), phiên bản theo Semantic Versioning.

## [1.10.0] — 2026-11-26

### Added
- Bảng Tiến độ của plan Pre luôn có dòng `0 | Phân tích và lập plan` và dòng cuối `Bàn giao: commit, push, MR, tracker`; template Post có dòng 0 "Điều tra/phân tích" (khi có) và dòng bàn giao (nếu đã làm). Lý do: case thực tế plan ghi 19 phút trong khi worklog Jira 2h 5m, vì phân tích trước khi có plan và bàn giao sau khi code không có chỗ ghi.
- Ghi mốc bắt đầu ngay từ đầu phiên (lệnh lấy giờ hệ thống ở lần gọi tool đầu tiên, hoặc thời điểm tin nhắn giao việc). Bước 0 kết thúc lúc plan được duyệt hoặc lúc bắt đầu bước 1, mốc nào đến trước.
- Quy tắc mốc suy ra (hỏi người dùng, ghi chú "mốc suy ra, chưa xác nhận"), không chồng mốc (cắt tại mốc bắt đầu của bước kế tiếp), và đồng bộ worklog bên ngoài (plan là nguồn đúng, phần chênh ghi ở hàng Tổng).
- `.jsonl`: bước 0 và bước bàn giao là `step` hợp lệ, `agent: main`; bước bàn giao ở lô cuối, phụ thuộc mọi bước, không giao cho agent.

### Changed
- `estimated_hours` là end-to-end gồm cả phân tích và bàn giao.
- Ngưỡng plan lớn "≥ 10 bước" không đếm bước 0 và bước bàn giao.
- Plan lập trước 1.10.0 thiếu 2 dòng mới: không tự thêm, chỉ đề xuất.

## [1.9.0] — 2026-11-26

### Added
- Quy đổi giờ sang MD (ngày làm việc, 1 MD = 8h): trường frontmatter `estimated_md` và `time_spent_md`, hàng Tổng ghi kèm MD (`= Xh (Y MD) · Ước lượng: Xh (Y MD)`). MD = số giờ đã làm tròn ÷ 8, làm tròn 0.125 MD gần nhất, đúng nửa bước thì làm tròn lên, giờ > 0 thì tối thiểu 0.125. Giờ vẫn là đơn vị gốc, bước làm tròn giờ (0.5 / 0.25) không đổi. Plan cũ thêm 2 trường ở lần cập nhật đầu.

## [1.8.0] — 2026-11-20

### Changed
- File giao việc `.jsonl` chỉ dùng cho **plan lớn**: thoả ít nhất một trong ≥ 10 bước, `estimated_hours` ≥ 40, hoặc có ≥ 2 bước chạy song song / giao agent khác `main`. Lúc duyệt plan, skill đề xuất, người dùng chốt. Plan nhỏ làm thẳng theo bảng Tiến độ, không có bảng Giao việc.

### Added
- Trường frontmatter `assign_tasks` (`true` = plan lớn, dùng file giao việc; `false` hoặc trống = không). Plan cũ không có trường này: có bảng Giao việc thì coi như `true`.

## [1.7.0] — 2026-11-20

### Added
- Trạng thái `approved` trong vòng đời plan (`planning → approved → in_progress → completed`), khớp với `status: approved` mà `nqdev-task-flow` dùng.
- Bảng *Giao việc* (`# | Agent | Lô | Phụ thuộc`) trong template Pre, điền khi plan được duyệt.
- Mục *File giao việc (.jsonl)*: khi plan `approved`, sinh `.claude/assign-tasks/<tên plan>.jsonl`, mỗi bước một dòng gồm `plan`, `step`, `agent`, `batch`, `depends_on`, `status`, `started_at`, `ended_at`. Plan là nguồn đúng, lệch hoặc mất file thì sinh lại; chỉ agent điều phối được ghi; thư mục không commit.
- `references/example-plan.md`: ví dụ Pre có bảng Giao việc và file `.jsonl` khớp bảng Tiến độ.

## [1.6.1] — 2026-11-20

### Changed
- Cột `Delta (h)` đổi thành `Delta (phút)`, ghi số phút thô, không làm tròn từng dòng. Chỉ hàng **Tổng** được đổi ra giờ và làm tròn 0.25h (tổng > 0 mà dưới 0.25 thì ghi 0.25), và số đó là `time_spent_hours`. Lý do: ở 1.6.0, mức tối thiểu 0.25h được áp cho từng dòng nên tổng bị đẩy lên khi có nhiều lần làm ngắn (4 dòng × 3 phút thành 1h).
- `references/example-plan.md` và README cập nhật theo.

## [1.6.0] — 2026-11-20

### Changed
- Bảng *Tiến độ* (template Pre và Post) thêm cột `Bắt đầu | Kết thúc | Delta (h)` và hàng **Tổng**. Mỗi lần làm một task là một dòng; task làm qua nhiều lần thì thêm dòng cùng `#` với Bước "(tiếp)", thời gian chờ giữa các lần không được tính. Task `bỏ` vẫn tính Delta đã làm vào Tổng.
- `time_spent_hours` = hàng Tổng (tổng cột Delta) của bảng Tiến độ. Mốc ghi theo dạng `YYYY-MM-DD HH:mm`, Delta làm tròn 0.25h.
- Mục "Ghi nhận thời gian", "Vòng đời một plan" và quy tắc chuyển đổi plan cũ cập nhật theo; `references/example-plan.md` minh hoạ một task làm qua 2 lần và một task `bỏ`.

### Removed
- Mục *Nhật ký thời gian* (ghi theo phiên) ở cả hai template. Plan cũ được chuyển đổi khi cập nhật lần đầu: số giờ cũ được ghi thành dòng `0 | Trước khi có mốc thời gian`.

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
