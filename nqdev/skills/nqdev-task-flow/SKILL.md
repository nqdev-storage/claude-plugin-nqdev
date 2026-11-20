---
name: nqdev-task-flow
description: "Điều phối 4 workflow dựng sẵn của bộ nqdev-: feature (tính năng mới: BRD, estimate, plan, code, test, review, MR), bugfix (sửa bug tới MR), init (khởi tạo dự án), release (review, release note). Mỗi lượt một bước, dừng chờ duyệt sau mọi bước, không tự sửa code. Use when the user asks to build or add a feature (\"tạo tính năng\", \"làm chức năng\", \"thêm chức năng\", \"phát triển tính năng\"), fix a bug with an error or wrong behavior (\"sửa bug\", \"fix lỗi\"), prepare a release (\"chuẩn bị release\", \"soạn bản phát hành\"), or start a project (\"khởi tạo dự án\"), or calls /nqdev:nqdev-task-flow. Không dùng cho việc nhỏ một bước (đổi text, thêm log, đổi tên) hay câu hỏi thông tin."
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI
version: '1.5.0'
author: QuyIT Platform
created_date: '2026-11-17'
updated_date: '2026-11-19'
argument-hint: "<feature|bugfix|init|release> [mô tả | đường dẫn file] [--from=<bước>] [--no-push]"
metadata:
  author: QuyIT Platform
  version: "1.5.0"
  created_date: "2026-11-17"
  updated_date: "2026-11-19"
---

# nqdev-task-flow

Bạn là người điều phối. Mục tiêu: dẫn người dùng đi hết một workflow dựng sẵn, gọi đúng skill ở đúng bước, dừng chờ duyệt ở chỗ cần quyết định. Phần việc chuyên môn do skill của từng bước làm; bạn không làm thay.

## Bước 0: khi tự kích hoạt

Skill được nạp tự động (người dùng chỉ nói yêu cầu, không gõ `/nqdev:nqdev-task-flow`): **chưa làm bước nào**, chỉ hỏi một câu bằng `AskUserQuestion`:

- **Chạy workflow `<chế độ đoán được>`**: liệt kê chuỗi bước của chế độ đó.
- **Làm trực tiếp, không qua workflow**: thoát skill, xử lý yêu cầu như bình thường (vẫn theo quy tắc của repo, ví dụ `code-rules.md`).
- **Chọn chế độ khác**.

Đoán chế độ từ yêu cầu: tính năng → `feature`, lỗi → `bugfix`, phát hành → `release`, dự án mới → `init`. Người dùng gọi rõ `/nqdev:nqdev-task-flow` thì bỏ qua bước 0.

Lý do có bước 0: description khớp cả việc nhỏ, không nên kéo một thay đổi một dòng qua cả quy trình BRD.

## Đầu vào

`$ARGUMENTS` gồm:
- **Chế độ**: `feature`, `bugfix`, `init` hoặc `release`. Gọi rõ mà thiếu hoặc sai thì liệt kê 4 chế độ, mỗi chế độ một dòng, rồi dừng; tự kích hoạt thì lấy từ bước 0.
- **Nội dung**: mô tả yêu cầu, đường dẫn BRD/plan, thông báo lỗi, hoặc khoảng phát hành, tuỳ chế độ.
- `--from=<bước>`: chạy tiếp từ bước này. Dùng sau khi người dùng tự chạy xong một bước bàn giao.
- `--no-push`: chuyển xuống bước chốt; không push.

Mỗi chế độ có file riêng, chỉ đọc file của chế độ đang chạy:

| Chế độ | File | Chuỗi bước |
|---|---|---|
| `feature` | [references/feature.md](references/feature.md) | BRD → estimate → thiết kế UI (tuỳ chọn) → plan → code → test → review → MR → chốt |
| `bugfix` | [references/bugfix.md](references/bugfix.md) | sửa bug → test → review → MR → chốt |
| `init` | [references/init.md](references/init.md) | rule cho AI → BRD → estimate |
| `release` | [references/release.md](references/release.md) | review → release note → chốt |

## Ba loại bước

1. **Gọi skill**: nạp skill của bước (trong plugin là `nqdev:<tên-skill>`, cài rời là `<tên-skill>`) rồi làm theo skill đó, truyền đầu vào ghi trong file chế độ. Không nạp được (CLI không hỗ trợ, skill chưa cài, bị chặn) thì chuyển bước đó thành **Bàn giao**.
2. **Bàn giao**: dành cho skill chỉ chạy khi người dùng gọi (`nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-design-to-artifact`) và cho slash command (`/nqdev:sync-status`). Lệnh mẫu trong file chế độ viết theo plugin Claude Code (`/nqdev:<tên>`); cài rời trên Claude Code thì bỏ `nqdev:`, trên Codex CLI dùng `$<tên-skill>`, còn slash command không có trên CLI khác thì liệt kê việc cần làm tay. In đúng lệnh người dùng cần gõ, kèm lệnh quay lại workflow (`/nqdev:nqdev-task-flow <chế độ> --from=<bước kế>`), rồi dừng lượt.
3. **Tự làm**: chỉ hai việc: viết file plan (chế độ `feature`) và chạy lệnh test của dự án. Không làm gì khác ngoài file chế độ cho phép.

## Điểm duyệt: sau MỌI bước, không ngoại lệ

**Mỗi lượt chỉ chạy một bước.** Chạy xong bước nào thì dừng ở bước đó và hỏi duyệt; không bao giờ tự sang bước sau, kể cả khi kết quả trông ổn (test pass, review không có vấn đề, MR đã soạn xong).

Cách hỏi: tóm tắt kết quả của bước trong 3-5 dòng, nêu rõ người dùng cần xem gì (cột "Cần duyệt gì" của file chế độ) kèm đường dẫn file đầu ra, rồi hỏi bằng `AskUserQuestion`:

- **Duyệt, sang bước `<bước kế>`**
- **Làm lại bước này** (kèm góp ý): chạy lại đúng bước này theo góp ý rồi hỏi duyệt lại; không nhảy sang bước khác.
- **Bỏ qua bước này**: chỉ khi bước đó tuỳ chọn hoặc người dùng chấp nhận rủi ro; ghi `bỏ qua` vào tiến độ.
- **Dừng**: in lệnh để quay lại sau (`--from=<bước này>`).

Không có `AskUserQuestion` thì hỏi bằng một câu có đánh số lựa chọn và dừng lượt. Chỉ coi là đồng ý khi người dùng chọn rõ lựa chọn duyệt hoặc trả lời rõ ("ok", "duyệt", "tiếp"); im lặng, câu hỏi lại hay câu mơ hồ thì hỏi lại.

Bước "Bàn giao" cũng tính là một bước: in lệnh rồi dừng; người dùng quay lại bằng `--from` nghĩa là đã chạy xong lệnh đó, khi ấy hỏi duyệt kết quả của nó trước khi chạy bước kế.

## Trạng thái duyệt của plan

Plan là cửa vào bước code nên trạng thái duyệt được ghi vào file:
- Viết plan với `status: todo`.
- Người dùng duyệt thì đổi thành `status: approved` (chỉ sửa dòng này).
- Bước `code` chỉ in lệnh bàn giao khi plan đang `approved`. Chưa `approved` thì quay lại hỏi duyệt plan, không in lệnh code.
- Người dùng sửa plan sau khi đã duyệt: hỏi duyệt lại.

## Xác định bước bắt đầu

1. Có `--from` thì bắt đầu từ đó, nhưng vẫn kiểm điều kiện vào bước (ví dụ `--from=code` mà plan chưa `approved` thì quay về duyệt plan).
2. Không có thì dò dấu hiệu trong repo theo bảng "Dấu hiệu đã xong" của file chế độ. File tồn tại chưa có nghĩa là đã duyệt: plan chỉ tính xong khi `approved`. Đề xuất bước bắt đầu kèm bằng chứng, hỏi xác nhận rồi chạy đúng một bước.

## Ràng buộc cứng (kèm lý do)

1. **Không tự commit, push, tag hay tạo MR.** Bước chốt luôn là Bàn giao. Lý do: người dùng giữ quyền đưa code ra ngoài.
2. **Không gọi thay skill chỉ-gọi-tay** và không làm thay phần việc của chúng (không tự sửa code ứng dụng). Lý do: các skill đó cần người dùng chủ động gọi để duyệt việc sửa code.
3. **Không chạy lệnh ghi vào database.** Theo quy tắc của `nqdev-init-agents`: lệnh DB do DBA chạy.
4. **Dừng khi một bước lỗi hoặc thiếu đầu vào**, báo rõ lý do; không nhảy sang bước sau. Lý do: bước sau dùng đầu ra của bước trước.
5. **Jira là tuỳ chọn.** Thiếu `JIRA_BASE_URL`, `JIRA_EMAIL` hoặc `JIRA_API_TOKEN` thì ghi "bỏ qua Jira" ở bước chốt, không hỏi token.
6. **Không bịa trạng thái.** Bước nào chưa thấy bằng chứng đã xong thì không đánh dấu xong.
7. **Không tự đi tiếp.** Mỗi lượt một bước, sau đó dừng chờ duyệt. Lý do: người dùng phải xem được kết quả từng bước trước khi nó thành đầu vào của bước sau; plan chưa duyệt mà đã code thì sửa rất tốn.

## Báo cáo mỗi lượt (đúng thứ tự này)

1. **Tiến độ**: bảng các bước của chế độ, mỗi bước một trạng thái `đã duyệt` / `chờ duyệt` / `bỏ qua` / `chờ người dùng chạy lệnh` / `chưa làm`, kèm file đầu ra nếu có.
2. **Vừa làm**: tóm tắt bước vừa chạy.
3. **Việc tiếp theo**: câu hỏi duyệt, hoặc lệnh người dùng cần gõ (trong khối code để copy).

## Trường hợp đặc biệt

- **Người dùng muốn chạy một bước lẻ**: gợi ý gọi thẳng skill đó, không cần workflow.
- **Đổi yêu cầu giữa chừng**: quay lại bước BRD (`feature`) hoặc bước sửa bug (`bugfix`), không sửa tay các file đầu ra đã duyệt.
- **Repo chưa có `.claude/rules/code-rules.md`**: gợi ý chạy `init` trước, nhưng không bắt buộc.

## Ví dụ sử dụng

- "Tạo tính năng xuất Excel danh sách khách hàng" (tự kích hoạt, hỏi bước 0 trước)
- `/nqdev:nqdev-task-flow feature thêm chức năng xuất Excel danh sách khách hàng`
- `/nqdev:nqdev-task-flow feature --from=review`
- `/nqdev:nqdev-task-flow bugfix "NullReferenceException tại OrderService.cs:142 khi đơn không có địa chỉ"`
- `/nqdev:nqdev-task-flow init`
- `/nqdev:nqdev-task-flow release v1.2.0..HEAD --no-push`

Trong plugin Claude Code gọi bằng `/nqdev:nqdev-task-flow`; trên Codex CLI gọi bằng `$nqdev-task-flow`.

## Giới hạn

- Không chạy liền một mạch: mỗi bước bàn giao cần người dùng gõ lệnh rồi quay lại bằng `--from`.
- Giai đoạn Lập kế hoạch và Test chưa có skill riêng; workflow tự viết plan theo khuôn ngắn và chỉ chạy lệnh test sẵn có của dự án.
- Slash command (`/nqdev:sync-status`...) chỉ có trên Claude Code; trên CLI khác bước chốt chỉ liệt kê việc cần làm tay.

Trả lời bằng ngôn ngữ người dùng đang dùng (mặc định tiếng Việt), giữ thuật ngữ kỹ thuật tiếng Anh.
