# Chế độ `bugfix`: sửa bug

Đầu vào: thông báo lỗi, stack trace, mô tả hành vi sai, hoặc mã issue. Thiếu cả ba thứ đầu thì hỏi đúng một câu: lỗi xảy ra thế nào và ở đâu.

## Các bước

Mỗi bước chạy xong đều dừng chờ duyệt (xem SKILL.md, mục "Điểm duyệt").

| Bước (`--from`) | Loại | Việc | Đầu ra | Cần duyệt gì |
|---|---|---|---|---|
| `fix` | Bàn giao `nqdev-bug-fixer` | In lệnh sửa bug và dừng | Thay đổi trong repo | Sau khi người dùng quay lại: nguyên nhân gốc và `git diff --stat`, bản sửa có gọn không |
| `test` | Tự làm | Chạy lệnh test của dự án (cách lấy lệnh như chế độ `feature`) | Kết quả test | Kết quả test. Có test lỗi thì đề xuất quay lại `fix` |
| `review` | Gọi skill `nqdev-code-review` | Review riêng phần thay đổi của bản sửa | Bảng vấn đề | Bảng vấn đề. Còn mức Chặn thì đề xuất quay lại `fix`. Không tự sửa code |
| `mr` | Gọi skill `nqdev-merge-request-writer` | Soạn commit message và mô tả MR, nêu nguyên nhân gốc | Văn bản trong hội thoại | Commit message và mô tả MR đúng chưa |
| `ship` | Bàn giao `/nqdev:sync-status` | In lệnh chốt và dừng | Commit | Sau khi người dùng quay lại: commit đã có, workflow kết thúc |

Lệnh bàn giao mẫu:

```
/nqdev:nqdev-bug-fixer <dán nguyên thông báo lỗi hoặc stack trace>
/nqdev:sync-status --no-push
```

Sau mỗi lệnh, người dùng quay lại bằng `/nqdev:nqdev-task-flow bugfix --from=<bước kế>`.

## Dấu hiệu đã xong

| Bước | Dấu hiệu |
|---|---|
| `fix` | `git status` có thay đổi, trong đó có file test mới hoặc sửa |
| `ship` | Không còn thay đổi chưa commit |

Bug nghiêm trọng hoặc sửa nhiều chỗ: gợi ý chạy `feature` từ bước `plan` thay vì `bugfix`.
