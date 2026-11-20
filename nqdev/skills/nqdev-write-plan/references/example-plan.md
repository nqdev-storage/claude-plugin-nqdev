# Ví dụ tham khảo — file plan mẫu

Hai ví dụ hư cấu, không thuộc project cụ thể nào, minh hoạ đúng template trong `SKILL.md`: một plan **Pre** đang làm dở và một nhật ký **Post**. Dùng để hình dung mức chi tiết, không copy máy móc.

Tên file đặt tại `plans/<stt>-<YYYY-MM-DD>-<slug>.md` của repo đang làm việc; `stt` = số lớn nhất đang có trong `plans/` cộng 1. Hai ví dụ dưới tương ứng `plans/012-2026-01-20-login-rate-limit.md` và `plans/007-2026-01-15-deploy-scripts-refactor.md`.

---

## Ví dụ 1 — Pre (kế hoạch, đang làm)

```markdown
---
mode: pre
type: feature
status: in_progress
priority: high
complexity: medium
impact: high
related_issues: []
related_prs: []
estimated_hours: 6
time_spent_hours: 2.5
completed_date:
---

# Kế hoạch: Thêm rate limit cho API đăng nhập

> **Ngày lập:** 2026-01-20
> **Scope dự kiến:** `src/auth/login.controller.ts`, `src/middleware/`, `config/`

## 1. Bối cảnh

Log tuần trước có nhiều đợt thử mật khẩu hàng loạt vào `POST /auth/login` từ một số IP. API hiện không giới hạn số lần thử. Hệ thống đã có Redis cho session, chưa dùng cho mục đích khác.

## 2. Approach và quyết định đã chốt

- Đếm số lần thử theo cặp IP + username trong Redis (cửa sổ trượt 15 phút), vượt 5 lần thì trả `429` kèm `Retry-After`.
- Đã loại: giới hạn ở reverse proxy, vì cần đếm theo username, proxy không đọc body.
- **Đã chốt với người dùng:** không khoá tài khoản sau nhiều lần sai (tránh bị lợi dụng để khoá tài khoản người khác); ngưỡng 5 lần đặt trong config để đổi không cần deploy code.

## 3. Tiến độ

| # | Bước | Trạng thái | Bắt đầu | Kết thúc | Delta (phút) | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | Middleware đếm số lần thử bằng Redis | xong | 2026-01-20 09:00 | 2026-01-20 10:00 | 60 | |
| 2 | Gắn vào `POST /auth/login`, trả `429` + `Retry-After` | xong | 2026-01-20 10:00 | 2026-01-20 10:30 | 30 | |
| 3 | Đưa ngưỡng và cửa sổ thời gian vào config | đang làm | 2026-01-21 09:00 | 2026-01-21 09:30 | 30 | dừng chờ DEV chốt tên key config |
| 3 | (tiếp) | đang làm | 2026-01-21 14:00 | | | đang làm, chưa có mốc kết thúc |
| 4 | Test: vượt ngưỡng, hết cửa sổ, Redis mất kết nối | chưa làm | | | | |
| 5 | Ghi log khi chặn | bỏ | 2026-01-21 09:30 | 2026-01-21 10:00 | 30 | Đã có log chung ở middleware lỗi, không cần thêm |
| **Tổng** | | | | | **150** | = 2.5h · Ước lượng: 6 |

## 4. Risks và Unknowns

- **Risk:** Redis mất kết nối làm chặn toàn bộ đăng nhập → **Mitigation:** lỗi Redis thì cho qua (fail-open) và log cảnh báo.
- **Unknown:** người dùng sau NAT chung một IP có bị chặn oan không → **Plan:** đếm theo IP + username, không chỉ IP.

## 5. Tiêu chí hoàn thành

- Lần thử thứ 6 trong 15 phút trả `429` có `Retry-After`; hết cửa sổ thì đăng nhập lại được.
- Redis lỗi thì đăng nhập vẫn hoạt động.
- Test của bước 4 pass trên CI.

## Nhật ký thay đổi plan

- 2026-01-21: bỏ bước 5 (log khi chặn) — middleware lỗi đã ghi log `429`, thêm nữa là trùng.
```

---

## Ví dụ 2 — Post (nhật ký sau khi làm)

```markdown
---
mode: post
type: refactor
status: in_progress
priority: medium
complexity: medium
impact: high
related_issues: []
related_prs: []
estimated_hours:
time_spent_hours: 2.75
completed_date:
---

# Nhật ký: Gộp 2 script deploy trùng lặp thành 1 script dùng chung

> **Ngày:** 2026-01-15
> **Phạm vi:** `scripts/deploy-staging.sh`, `scripts/deploy-production.sh`, `scripts/lib/`

## 1. Bối cảnh

Hai script deploy được copy từ nhau rồi sửa tay nên lệch nhau: staging thiếu health-check, production thiếu rollback tự động. Phát hiện khi một lần deploy staging fail mà không báo lỗi.

## 2. Công việc đã thực hiện

1. Staging: thêm health-check (lấy từ production). **Giữ nguyên** bước seed dữ liệu mẫu, vì staging cố ý cần dữ liệu demo, không phải điểm lệch.
2. Production: thêm rollback tự động khi health-check fail.
3. Gộp thành `scripts/lib/deploy-common.sh` nhận `--env=staging|production`, thay vì đồng bộ tay 2 file: hai file đã lệch nhau một lần, đồng bộ tay dễ lặp lại lỗi.

## 3. Files đã thay đổi

| File | Thay đổi |
|---|---|
| [scripts/deploy-staging.sh](../scripts/deploy-staging.sh) | Chỉ còn gọi `deploy-common.sh --env=staging` |
| [scripts/deploy-production.sh](../scripts/deploy-production.sh) | Chỉ còn gọi `deploy-common.sh --env=production` |
| [scripts/lib/deploy-common.sh](../scripts/lib/deploy-common.sh) (**Mới**) | Logic deploy dùng chung, tham số hoá phần khác biệt |

## 4. Trạng thái hiện tại

Đã commit `a1b2c3d`, deploy thử staging thành công. **Chưa** chạy thử production, đang chờ cửa sổ bảo trì.

## 5. Việc còn mở

- [ ] Chạy thử deploy production trong cửa sổ bảo trì tiếp theo.
- [ ] Cân nhắc gửi thông báo (Slack/email) khi rollback tự động kích hoạt; hiện chỉ log ra console.

## Tiến độ

| # | Bước | Trạng thái | Bắt đầu | Kết thúc | Delta (phút) | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | So sánh 2 script, thêm health-check và rollback | xong | 2026-01-15 09:00 | 2026-01-15 10:40 | 100 | |
| 2 | Tách `deploy-common.sh`, chạy thử staging | xong | 2026-01-15 13:30 | 2026-01-15 14:40 | 70 | |
| **Tổng** | | | | | **170** | = 2.75h (170 ÷ 60 = 2.83, làm tròn 0.25) · Không có ước lượng (nhật ký Post) |
```

---

## Vì sao hai ví dụ "đúng chuẩn"

**Chung**
- Frontmatter đủ mọi trường; trường chưa có giá trị để trống, không xoá. Cả hai `status: in_progress` nên `completed_date` trống.
- Delta ghi phút thô; chỉ hàng Tổng được đổi ra giờ và làm tròn 0.25, và số đó bằng `time_spent_hours`. Khoảng nghỉ giữa các mốc (nghỉ trưa, chờ review) không được tính.
- Mục **(Tùy chọn)** không có nội dung thì bỏ hẳn (ví dụ 1 bỏ mục 6, ví dụ 2 bỏ mục 6–7).

**Ví dụ 1 (Pre)**
- H1 `# Kế hoạch:`; `estimated_hours: 6` làm tròn 0.5, là tổng end-to-end theo mô hình AI làm, DEV review; hàng Tổng ghi "Ước lượng: 6".
- Mục 2 tách rõ phương án đã loại và **quyết định đã chốt với người dùng**, để phiên sau không đề xuất lại việc khoá tài khoản.
- Bảng Tiến độ dùng đủ 4 trạng thái; bước `bỏ` có lý do, có dòng tương ứng trong Nhật ký thay đổi plan, và 30 phút đã làm vẫn tính vào Tổng.
- Bước 3 làm qua 2 lần: dòng thứ hai cùng `#`, cột Bước ghi "(tiếp)". Dòng đang làm chưa có mốc kết thúc nên chưa có Delta; thời gian chờ DEV từ 09:30 đến 14:00 không được tính.

**Ví dụ 2 (Post)**
- H1 `# Nhật ký:`; `estimated_hours` trống vì việc đã làm xong mới ghi.
- Mục 2 nêu cả "làm gì" lẫn "tại sao", kể cả lý do **giữ nguyên** bước seed dữ liệu.
- Mục 3 có link tương đối tới từng file, file mới đánh dấu **Mới**; mục 4 nói rõ phần chưa làm; mục 5 chỉ gồm việc cố ý để sau.
