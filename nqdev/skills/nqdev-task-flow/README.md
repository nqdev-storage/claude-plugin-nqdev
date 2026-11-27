# nqdev-task-flow

Điều phối 4 workflow dựng sẵn của bộ `nqdev`: gọi đúng skill ở đúng bước và **dừng chờ bạn duyệt sau mọi bước**. Phần việc chuyên môn do skill của từng bước làm; skill này không làm thay.

- **Phiên bản:** 1.8.0 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI

## Dùng khi nào

- Bạn yêu cầu làm tính năng ("tạo tính năng …", "thêm chức năng …"), sửa bug có lỗi hoặc hành vi sai, chuẩn bị release, hoặc khởi tạo dự án.
- Bạn muốn đi trọn một việc theo quy trình có kiểm soát thay vì tự nhớ thứ tự skill.

Không dùng cho việc nhỏ một bước (đổi text, thêm log, đổi tên) hoặc câu hỏi thông tin. Muốn chạy một bước lẻ thì gọi thẳng skill của bước đó.

## Bốn workflow

| Chế độ | Chuỗi bước | Đầu vào gợi ý |
|---|---|---|
| `feature` | BRD → estimate → thiết kế UI (tuỳ chọn) → plan → code → test → review → MR → chốt | mô tả tính năng, hoặc đường dẫn BRD/plan |
| `bugfix` | sửa bug → test → review → MR → chốt | thông báo lỗi hoặc stack trace |
| `init` | rule cho AI → BRD → estimate | mô tả dự án |
| `release` | review → release note → chốt | khoảng phát hành, ví dụ `v1.2.0..HEAD` |

Chi tiết từng chế độ nằm trong `references/<chế độ>.md`; skill chỉ đọc file của chế độ đang chạy.

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | `<feature\|bugfix\|init\|release> [mô tả \| đường dẫn file] [--from=<bước>] [--no-push]`. `--from` chạy tiếp từ một bước (dùng sau khi bạn tự chạy xong một bước bàn giao); không có thì skill dò repo (`docs/brd/`, `plans/`, `git status`) để đề xuất bước bắt đầu kèm bằng chứng |
| **Đầu ra** | Mỗi lượt một báo cáo: bảng tiến độ các bước (`đã duyệt` / `chờ duyệt` / `bỏ qua` / `chờ người dùng chạy lệnh` / `chưa làm`), tóm tắt bước vừa chạy, và việc tiếp theo (câu hỏi duyệt hoặc lệnh để bạn gõ). File sinh ra là của từng skill (BRD, plan, test, MR…) |

Ví dụ:

```text
/nqdev:nqdev-task-flow feature thêm chức năng xuất Excel danh sách khách hàng
/nqdev:nqdev-task-flow feature --from=review
/nqdev:nqdev-task-flow bugfix "NullReferenceException tại OrderService.cs:142 khi đơn không có địa chỉ"
/nqdev:nqdev-task-flow release v1.2.0..HEAD --no-push
```

Bạn cũng có thể chỉ nói yêu cầu. Khi skill tự kích hoạt, nó **chưa làm gì** mà hỏi một câu: chạy workflow, làm trực tiếp, hay chọn chế độ khác.

## Cách duyệt

- **Mỗi lượt chỉ chạy một bước.** Xong bước nào dừng ở đó, kể cả khi test pass hay review không có vấn đề. Bạn chọn: duyệt và sang bước kế, làm lại bước này (kèm góp ý), bỏ qua (chỉ bước tuỳ chọn hoặc bạn chấp nhận rủi ro), hoặc dừng.
- **Plan là cửa vào bước code.** Plan viết với `status: todo`; bạn duyệt thì đổi thành `status: approved`. Chưa `approved` thì bước code không chạy.
- **Bước bàn giao:** ở bước sửa code (`nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-design-to-artifact`) và bước chốt (`/nqdev:sync-status`), skill không tự chạy mà đưa đúng lệnh để bạn gõ, kèm lệnh quay lại (`--from=<bước kế>`).
- **Plan lớn chạy theo lô** (từ 10 bước, hoặc ước lượng từ 40h, hoặc có bước chạy song song): sau khi bạn duyệt plan và bảng giao việc, bước code chạy tối đa 3 bước một lô theo file `.claude/assign-tasks/<tên plan>.jsonl`, và dừng duyệt sau mỗi lô. Cần tool có subagent.

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây (workflow gọi các skill khác của bộ nên cài kèm chúng):

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-task-flow/` | `~/.claude/skills/nqdev-task-flow/` |
| OpenCode | `.opencode/skills/nqdev-task-flow/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-task-flow/` |
| Gemini CLI | `.gemini/skills/nqdev-task-flow/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-task-flow/` |
| Codex CLI | `.agents/skills/nqdev-task-flow/` | `~/.agents/skills/nqdev-task-flow/` |

## Hành vi theo tool

- **Claude Code:** gọi bằng `/nqdev:nqdev-task-flow`. Câu hỏi duyệt dùng `AskUserQuestion`; không có thì skill hỏi bằng một câu có đánh số lựa chọn.
- **Codex CLI:** gọi bằng `$nqdev-task-flow`. `agents/openai.yaml` đặt `allow_implicit_invocation: true` để tự kích hoạt như trên Claude Code.
- **Slash command** (`/nqdev:sync-status`…) chỉ có trên Claude Code; trên CLI khác bước chốt chỉ liệt kê việc cần làm tay.
- Skill không nạp được skill của bước (CLI không hỗ trợ, chưa cài, bị chặn) thì chuyển bước đó thành bàn giao.

## Giới hạn

- Không tự commit, push, tag hay tạo MR; bước chốt luôn là bàn giao. Không chạy lệnh ghi vào database.
- Không chạy liền một mạch: mỗi bước bàn giao cần bạn gõ lệnh rồi quay lại bằng `--from`.
- Dừng khi một bước lỗi hoặc thiếu đầu vào, không nhảy sang bước sau. Không đánh dấu xong khi chưa thấy bằng chứng.
- Jira là tuỳ chọn: thiếu `JIRA_BASE_URL`, `JIRA_EMAIL` hoặc `JIRA_API_TOKEN` thì bước chốt ghi "bỏ qua Jira", không hỏi token.
- Chưa nối `nqdev-write-plan`, `nqdev-test-case-writer`, `nqdev-unit-test-generator` vào các bước plan và test: workflow viết plan theo khuôn ngắn và chỉ chạy lệnh test sẵn có của dự án.

## Cấu trúc

```text
nqdev-task-flow/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
└── references/
    ├── feature.md
    ├── bugfix.md
    ├── init.md
    └── release.md
```
