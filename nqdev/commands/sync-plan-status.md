---
description: Cập nhật trạng thái các file plan trong thư mục plans/ theo công việc đã làm (frontmatter status, dòng Trạng thái, mục "Cập nhật" có ngày)
argument-hint: "[tên file plan hoặc từ khóa | trống = tất cả plan trong plans/]"
allowed-tools: Bash(git:*), Bash(ls:*), Bash(date:*), Read, Edit, Write, Grep, Glob
model: haiku
---

# Cập nhật trạng thái plan

Đầu vào (có thể trống): `$ARGUMENTS`

Mục tiêu: để mỗi file plan phản ánh đúng hiện trạng công việc, dựa trên **bằng chứng** (commit, code, kết quả test, Jira), không đoán.

## Bước 1. Tìm plan
1. Gốc repo: `git rev-parse --show-toplevel`. Plan nằm ở `plans/*.md` (không có thì `docs/plans/`; không thấy thì dừng và nói rõ).
2. Có `$ARGUMENTS` thì chỉ lấy file có tên hoặc nội dung khớp; trống thì lấy mọi plan.
3. Với mỗi plan, đọc đầu file: frontmatter `status` (các giá trị đang dùng: `in_progress`, `completed`), dòng `> **Trạng thái:** ...` nếu có, và các mục việc còn mở (`- [ ]`, "Còn mở", "Chưa làm").

## Bước 2. Thu thập bằng chứng
- `git log --oneline` từ lần cuối sửa file plan đó (`git log -1 --format=%H -- <file>` rồi `<hash>..HEAD`), `git status --short`.
- Đối chiếu từng việc còn mở với code/test thực tế (Grep/Read). Việc nào đã có commit hoặc file tương ứng thì coi là xong; chỉ khi thấy bằng chứng.
- Đọc lại kết quả kiểm thử đã chạy trong phiên (nếu có). Không chạy lại test nặng chỉ để cập nhật plan.

## Bước 3. Quyết định trạng thái
| Tình huống | Cập nhật |
|---|---|
| Mọi việc xong, không còn mục mở thuộc plan này | `status: completed` |
| Còn việc mở thuộc plan này | giữ `in_progress`, đánh `- [x]` đúng các việc đã xong |
| Việc còn mở thuộc task/plan khác | `completed`, ghi rõ việc còn lại nằm ở đâu (mã Jira nếu có) |
| Không có bằng chứng | giữ nguyên và ghi "chưa xác nhận" |

Việc cần người dùng tự làm (thu hồi token, publish, chạy thử ở máy khác) chỉ tick khi **người dùng đã xác nhận**; ghi "theo xác nhận của ... ngày YYYY-MM-DD".

## Bước 4. Ghi vào file
- Sửa frontmatter `status`, dòng `> **Trạng thái:**` (nếu có) và các checkbox.
- Thêm cuối file mục `## Cập nhật YYYY-MM-DD (<chủ đề ngắn>)` (lấy ngày bằng `date +%F`), 3 đến 8 gạch đầu dòng: đã làm gì, quyết định, kết quả kiểm thử, **việc còn lại** và **hạn chế đã biết**. Giữ giọng văn và ngôn ngữ của file (thường là tiếng Việt).
- Không xóa lịch sử cũ, không viết lại các mục trước. Không thêm mã bí mật, token, dữ liệu thật.

## Bước 5. Báo cáo
Bảng `File | Trạng thái cũ -> mới | Việc đã tick | Việc còn mở`. Nhắc: chưa commit (dùng `/nqdev:sync-git-ship` hoặc `/nqdev:sync-status`).
