# Chế độ `feature`: tính năng mới

Đầu vào: mô tả tính năng, ghi chú họp, hoặc đường dẫn BRD có sẵn (`docs/brd/<module>.md`).

## Các bước

Mỗi bước chạy xong đều dừng chờ duyệt (xem SKILL.md, mục "Điểm duyệt").

| Bước (`--from`) | Loại | Việc | Đầu ra | Cần duyệt gì |
|---|---|---|---|---|
| `brd` | Gọi skill `nqdev-brd-prd-writer` | Viết hoặc cập nhật BRD của module từ đầu vào | `docs/brd/<module>.md` | BRD đúng ý chưa: BR, AC, phạm vi |
| `estimate` | Gọi skill `nqdev-requirement-estimator` | Ước lượng từ BRD đã duyệt | Bảng estimate trong hội thoại | Chốt scope, phần MVP |
| `design` | Bàn giao `nqdev-design-to-artifact` | Hỏi trước có cần thiết kế UI không; cần thì in lệnh và dừng | `docs/prototype/` | Trước: có làm bước này không. Sau khi người dùng quay lại: màn hình đúng ý chưa |
| `plan` | Tự làm | Viết plan theo khuôn bên dưới, giới hạn trong scope đã chốt, `status: todo`. Tên file theo quy ước của `nqdev-write-plan`: `stt` là số 3 chữ số, lớn nhất đang có trong `plans/` cộng 1 | `plans/<stt>-<YYYY-MM-DD>-<slug>.md` | Plan đúng ý chưa: phạm vi, file sẽ đổi, các bước, plan lớn hay nhỏ. Duyệt thì đổi `status: approved` và chốt `assign_tasks`; plan lớn thì điền bảng Giao việc (agent, lô, phụ thuộc) và sinh `.claude/assign-tasks/<tên plan>.jsonl` |
| `code` | Chạy theo lô, hoặc Bàn giao `nqdev-feature-implementer` | Kiểm plan đã `approved`. Plan lớn (`assign_tasks: true`), có `.jsonl` và tool có subagent → chạy từng lô theo SKILL.md mục *Chạy theo lô*, dừng duyệt sau mỗi lô. Plan nhỏ hoặc thiếu điều kiện → in lệnh code và dừng | Thay đổi trong repo; `.jsonl` và bảng Tiến độ có mốc thời gian | Sau mỗi lô hoặc khi người dùng quay lại: kết quả từng bước, `git diff --stat` có đúng phạm vi plan không |
| `test` | Tự làm | Chạy lệnh test của dự án | Kết quả test | Kết quả test. Có test lỗi thì đề xuất quay lại `code` |
| `review` | Gọi skill `nqdev-code-review` | Review thay đổi, đối chiếu BRD (và màn trong mục `## Màn hình` của plan, nếu có) | Bảng vấn đề | Bảng vấn đề. Còn mức Chặn thì đề xuất quay lại `code`. Không tự sửa code |
| `mr` | Gọi skill `nqdev-merge-request-writer` | Soạn commit message và mô tả MR | Văn bản trong hội thoại | Commit message và mô tả MR đúng chưa |
| `ship` | Bàn giao `/nqdev:sync-status` | In lệnh chốt và dừng | Commit | Sau khi người dùng quay lại: commit đã có, workflow kết thúc |

Lệnh bàn giao mẫu:

```
/nqdev:nqdev-design-to-artifact <màn hình cần thiết kế, theo docs/brd/<module>.md>
/nqdev:nqdev-feature-implementer plans/<stt>-<YYYY-MM-DD>-<slug>.md
/nqdev:sync-status --no-push
```

Sau mỗi lệnh, người dùng quay lại bằng `/nqdev:nqdev-task-flow feature --from=<bước kế>`.

## Dấu hiệu đã xong

| Bước | Dấu hiệu |
|---|---|
| `brd` | Có `docs/brd/<module>.md` khớp tính năng |
| `design` | Có màn trong `docs/prototype/_gen/` ghi `<!--traces: ...-->` trỏ tới mã UC/AC của module, hoặc bảng "Truy vết màn ↔ UC/AC" trong `docs/specs/ui-ux.md` có module này. Bộ prototype cũ chưa có `traces` thì hỏi |
| `plan` | Có file trong `plans/` nhắc tới tính năng **và** `status: approved`. File có mà còn `todo` nghĩa là chờ duyệt, không phải xong |
| `code` | Plan lớn có `.jsonl`: mọi dòng `done` hoặc `skipped`, trừ dòng bàn giao (dòng cuối). Không có: `git status` hoặc `git diff <nhánh gốc>` có thay đổi ngoài `docs/` và `plans/` |
| `ship` | Không còn thay đổi chưa commit và nhánh đã có commit mới |

`estimate`, `test`, `review`, `mr` không để lại file; khi không chắc thì hỏi.

Vào bước `code` (kể cả qua `--from=code`) mà plan chưa `approved`: không chạy lô, không in lệnh code, quay lại hỏi duyệt plan.

## Khuôn plan (bước `plan`)

Dùng skill `nqdev-write-plan` (đi kèm plugin `nqdev`), nhưng file plan vẫn phải có `status: todo` trong frontmatter để ghi trạng thái duyệt, và có mục `## Màn hình` như khuôn dưới. Không nạp được skill (cài rời, hoặc CLI không cho skill gọi skill) thì viết theo khuôn:

```markdown
---
title: <tên tính năng>
status: todo
created: YYYY-MM-DD
brd: docs/brd/<module>.md
---

# <tên tính năng>

## Mục tiêu
<1-2 câu, kèm mã BR liên quan>

## Phạm vi
- Làm: ...
- Không làm: ...

## Màn hình
- `docs/prototype/project/<màn>.dc.html`: UC-<MODULE>-01, AC-<MODULE>-003

## File dự kiến thay đổi
- `<đường dẫn>`: <việc>

## Các bước
1. ...

## Kiểm thử
- <AC-xxx>: <cách kiểm>

## Rủi ro và câu hỏi mở
- ...
```

Chỉ ghi file dự kiến thay đổi khi đã đọc code để biết chúng tồn tại; chưa biết thì ghi `[cần xác nhận]`.

Mục `## Màn hình`: lấy từ dòng `<!--traces: ...-->` của nguồn màn (hoặc bảng "Truy vết màn ↔ UC/AC" trong `docs/specs/ui-ux.md`), chỉ các màn thuộc scope đã chốt. Bỏ qua bước `design` hoặc không có prototype thì ghi "Không có". Màn có nhưng chưa ghi `traces` thì liệt kê đường dẫn và ghi `[cần xác nhận: UC/AC]`.

## Bước `test`

Lấy lệnh test từ `.claude/rules/code-rules.md`, `CLAUDE.md`, `AGENTS.md`, rồi tới file cấu hình dự án (`package.json` scripts, `*.sln`, `pyproject.toml`...). Không xác định được thì hỏi lệnh. Không tự cài dependency, không chạy test cần database thật.
