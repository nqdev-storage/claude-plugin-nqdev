# Chế độ `release`: chuẩn bị phát hành

Đầu vào: khoảng phát hành, ví dụ `v1.2.0..HEAD`. Không có thì lấy từ tag gần nhất tới `HEAD` (`git describe --tags --abbrev=0`) và hỏi xác nhận; repo chưa có tag thì hỏi mốc bắt đầu.

## Các bước

Mỗi bước chạy xong đều dừng chờ duyệt (xem SKILL.md, mục "Điểm duyệt").

| Bước (`--from`) | Loại | Việc | Đầu ra | Cần duyệt gì |
|---|---|---|---|---|
| `review` | Gọi skill `nqdev-code-review` | Review toàn bộ thay đổi trong khoảng, ưu tiên DB, phân quyền, API công khai | Bảng vấn đề | Bảng vấn đề. Còn mức Chặn thì đề xuất dừng phát hành. Không tự sửa code |
| `notes` | Gọi skill `nqdev-release-note-writer` | Soạn release note và checklist deploy (migration, cấu hình, rollback) | Release note và checklist | Nội dung release note và checklist đủ chưa |
| `ship` | Bàn giao `/nqdev:sync-status` | In lệnh chốt và dừng | Commit | Sau khi người dùng quay lại: commit đã có, workflow kết thúc |

Lệnh bàn giao mẫu:

```
/nqdev:sync-status --no-push
```

Không tạo tag, không deploy. Kết thúc bằng danh sách việc người dùng tự làm: tạo tag, chạy migration (DBA), deploy theo checklist.

Diff quá lớn để review một lần: review theo module, phần rủi ro cao trước, ghi rõ phần chưa review vào báo cáo.
