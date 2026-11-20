---
description: "Chạy trọn quy trình chốt công việc, theo thứ tự: cập nhật plan, cập nhật Jira, git commit và push"
argument-hint: "[EPIC-KEY hoặc KEY | --no-push | trống]"
allowed-tools: Bash(git:*), Bash(curl:*), Bash(date:*), Bash(python3:*), Bash(ls:*), Bash(grep:*), Bash(sleep:*), Bash(printenv:*), Read, Edit, Write, Grep, Glob
model: haiku
---

# Chốt công việc: plan, Jira, git

Đầu vào (có thể trống): `$ARGUMENTS`

Chạy lần lượt ba bước, mỗi bước theo đúng hướng dẫn của lệnh tương ứng; dừng và báo nếu một bước lỗi hoặc thiếu bằng chứng, **không** làm tiếp bước sau khi chưa xử lý được.

Trước mỗi bước, **đọc toàn bộ file hướng dẫn của lệnh đó** rồi làm đúng theo, kể cả các quy tắc an toàn và điểm hỏi xác nhận (quét secret, không commit lên nhánh mặc định, duyệt trước khi ghi Jira). Không tự chế các bước. File nằm cạnh file này: `${CLAUDE_PLUGIN_ROOT}/commands/sync-plan-status.md`, `sync-jira-status.md`, `sync-git-ship.md` (cài rời thì tìm trong thư mục `commands/` chứa lệnh này). Không đọc được thì dừng và báo.

1. **Plan** theo `/nqdev:sync-plan-status` (không truyền đối số, trừ khi người dùng chỉ định file).
2. **Jira** theo `/nqdev:sync-jira-status` (truyền mã epic/issue nếu `$ARGUMENTS` có; thiếu biến môi trường Jira thì bỏ qua bước này, nói rõ và vẫn làm bước 3).
3. **Git** theo `/nqdev:sync-git-ship` (truyền `--no-push` nếu có). Thay đổi của bước 1 nằm trong cùng lần commit; thông điệp commit nêu cả phần việc chính lẫn việc cập nhật plan.

Thứ tự này có lý do: plan cần ghi mã Jira và kết quả kiểm thử trước khi commit, còn Jira nên ghi mã commit sau khi push (nếu cần ghi hash thì comment Jira bổ sung sau bước 3, nhưng hỏi người dùng trước khi comment).

Báo cáo cuối: ba dòng (plan, Jira, git) mỗi dòng nêu kết quả và việc còn mở, kèm danh sách việc người dùng phải tự làm.
