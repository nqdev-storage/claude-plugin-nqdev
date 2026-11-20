---
name: nqdev-task-flow
description: "Điều phối 4 workflow dựng sẵn của bộ nqdev-: feature (tính năng mới: BRD, estimate, plan, code, test, review, MR), bugfix (sửa bug tới MR), init (khởi tạo dự án), release (review, release note). Mỗi lượt một bước (bước code có thể chạy theo lô từ file giao việc .jsonl), dừng chờ duyệt sau mọi bước, không tự sửa code. Use when the user asks to build or add a feature (\"tạo tính năng\", \"làm chức năng\", \"thêm chức năng\", \"phát triển tính năng\"), fix a bug with an error or wrong behavior (\"sửa bug\", \"fix lỗi\"), prepare a release (\"chuẩn bị release\", \"soạn bản phát hành\"), or start a project (\"khởi tạo dự án\"), or calls /nqdev:nqdev-task-flow. Không dùng cho việc nhỏ một bước (đổi text, thêm log, đổi tên) hay câu hỏi thông tin."
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI
version: '1.7.0'
author: QuyIT Platform
created_date: '2026-11-17'
updated_date: '2026-11-20'
argument-hint: "<feature|bugfix|init|release> [mô tả | đường dẫn file] [--from=<bước>] [--no-push]"
metadata:
  author: QuyIT Platform
  version: "1.7.0"
  created_date: "2026-11-17"
  updated_date: "2026-11-20"
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
3. **Tự làm**: chỉ ba việc: viết file plan (chế độ `feature`), sinh và cập nhật file giao việc `.jsonl` (chỉ plan lớn) cùng bảng Tiến độ của plan (xem *Chạy theo lô*), và chạy lệnh test của dự án. Không làm gì khác ngoài file chế độ cho phép.

## Điểm duyệt: sau MỌI bước, không ngoại lệ

**Mỗi lượt chỉ chạy một bước.** Chạy xong bước nào thì dừng ở bước đó và hỏi duyệt; không bao giờ tự sang bước sau, kể cả khi kết quả trông ổn (test pass, review không có vấn đề, MR đã soạn xong).

Cách hỏi: tóm tắt kết quả của bước trong 3-5 dòng, nêu rõ người dùng cần xem gì (cột "Cần duyệt gì" của file chế độ) kèm đường dẫn file đầu ra, rồi hỏi bằng `AskUserQuestion`:

- **Duyệt, sang bước `<bước kế>`**
- **Làm lại bước này** (kèm góp ý): chạy lại đúng bước này theo góp ý rồi hỏi duyệt lại; không nhảy sang bước khác.
- **Bỏ qua bước này**: chỉ khi bước đó tuỳ chọn hoặc người dùng chấp nhận rủi ro; ghi `bỏ qua` vào tiến độ.
- **Dừng**: in lệnh để quay lại sau (`--from=<bước này>`).

Không có `AskUserQuestion` thì hỏi bằng một câu có đánh số lựa chọn và dừng lượt. Chỉ coi là đồng ý khi người dùng chọn rõ lựa chọn duyệt hoặc trả lời rõ ("ok", "duyệt", "tiếp"); im lặng, câu hỏi lại hay câu mơ hồ thì hỏi lại.

Ở bước `code` chạy theo lô, **mỗi lô tính là một lượt**: chạy xong lô thì dừng hỏi duyệt như trên.

Bước "Bàn giao" cũng tính là một bước: in lệnh rồi dừng; người dùng quay lại bằng `--from` nghĩa là đã chạy xong lệnh đó, khi ấy hỏi duyệt kết quả của nó trước khi chạy bước kế.

## Trạng thái duyệt của plan

Plan là cửa vào bước code nên trạng thái duyệt được ghi vào file:
- Viết plan với `status: todo`.
- Người dùng duyệt thì đổi thành `status: approved`, rồi xét plan lớn hay nhỏ theo mục *File giao việc (.jsonl)* của `nqdev-write-plan` (≥ 10 bước, hoặc ước lượng ≥ 40h, hoặc có bước chạy song song / giao agent khác `main`), đề xuất và để người dùng chốt `assign_tasks`. Chỉ khi `true` mới điền bảng *Giao việc* và sinh `.jsonl`. Ngoài các việc này không sửa gì khác trong plan.
- Bước `code` chỉ chạy (theo lô hoặc in lệnh bàn giao) khi plan đang `approved`. Chưa `approved` thì quay lại hỏi duyệt plan.
- Người dùng sửa plan sau khi đã duyệt: hỏi duyệt lại, xét lại `assign_tasks`, rồi sinh lại `.jsonl` từ plan nếu là plan lớn.

## Chạy theo lô (bước `code`)

Dùng khi plan đã `approved`, có `assign_tasks: true` và file `.claude/assign-tasks/<tên plan>.jsonl`, **và** tool hỗ trợ subagent. Plan nhỏ (`assign_tasks: false` hoặc trống) hoặc thiếu điều kiện khác thì làm thẳng theo bảng Tiến độ, bàn giao như cũ: in lệnh `nqdev-feature-implementer` (hoặc `nqdev-bug-fixer`) cho từng bước, mỗi lượt một bước.

1. **Đọc và đối chiếu.** Đọc `.jsonl` và bảng Tiến độ của plan. Lệch nhau hoặc file hỏng thì sinh lại `.jsonl` từ plan (plan là nguồn đúng) rồi mới chạy tiếp.
2. **Chọn lô.** Lấy các dòng `status: todo` có `batch` nhỏ nhất, và chỉ những dòng có mọi `depends_on` đã `done` (bước `skipped` coi như không chặn). Tối đa 3 bước một lô. Không còn dòng nào chạy được mà vẫn còn `todo` → dừng, báo bước nào đang chặn.
3. **Giao việc.** Mỗi bước giao cho đúng `agent` ghi trong dòng, kèm đường dẫn plan và số `step`, để agent chỉ làm đúng bước đó. `agent: main` → agent chính làm, lần lượt từng bước. Trước khi giao: ghi `started_at`, `status: doing` vào `.jsonl` và mốc Bắt đầu vào bảng Tiến độ.
4. **Nhận kết quả.** Mỗi bước xong thì ghi `ended_at`, `status: done` (hoặc giữ `doing` nếu dừng giữa chừng) vào `.jsonl`, ghi mốc Kết thúc và Delta vào bảng Tiến độ, cập nhật Tổng và `time_spent_hours` theo *Ghi nhận thời gian* của `nqdev-write-plan`. Bước lỗi thì giữ `doing`, ghi lý do vào cột Ghi chú.
5. **Dừng sau lô.** Báo kết quả từng bước của lô (agent, mốc thời gian, file đã đổi, lỗi nếu có) rồi hỏi duyệt theo *Điểm duyệt*. Duyệt thì quay lại bước 2 để bốc lô sau. Hết `todo` thì bước `code` xong.

**Chỉ luồng điều phối được ghi** vào `.jsonl` và plan. Subagent làm xong chỉ trả kết quả, không tự sửa hai file này, để các agent chạy song song không ghi đè nhau.

## Xác định bước bắt đầu

1. Có `--from` thì bắt đầu từ đó, nhưng vẫn kiểm điều kiện vào bước (ví dụ `--from=code` mà plan chưa `approved` thì quay về duyệt plan).
2. Không có thì dò dấu hiệu trong repo theo bảng "Dấu hiệu đã xong" của file chế độ. File tồn tại chưa có nghĩa là đã duyệt: plan chỉ tính xong khi `approved`. Đề xuất bước bắt đầu kèm bằng chứng, hỏi xác nhận rồi chạy đúng một bước.

## Ràng buộc cứng (kèm lý do)

1. **Không tự commit, push, tag hay tạo MR.** Bước chốt luôn là Bàn giao. Lý do: người dùng giữ quyền đưa code ra ngoài.
2. **Không gọi thay skill chỉ-gọi-tay** và không làm thay phần việc của chúng (không tự sửa code ứng dụng). Lý do: các skill đó cần người dùng chủ động gọi để duyệt việc sửa code. Ngoại lệ duy nhất là *Chạy theo lô*: người dùng đã duyệt plan và bảng Giao việc, nên các agent trong `.jsonl` được giao bước code, còn luồng điều phối vẫn không tự sửa code.
3. **Không chạy lệnh ghi vào database.** Theo quy tắc của `nqdev-init-agents`: lệnh DB do DBA chạy.
4. **Dừng khi một bước lỗi hoặc thiếu đầu vào**, báo rõ lý do; không nhảy sang bước sau. Lý do: bước sau dùng đầu ra của bước trước.
5. **Jira là tuỳ chọn.** Thiếu `JIRA_BASE_URL`, `JIRA_EMAIL` hoặc `JIRA_API_TOKEN` thì ghi "bỏ qua Jira" ở bước chốt, không hỏi token.
6. **Không bịa trạng thái.** Bước nào chưa thấy bằng chứng đã xong thì không đánh dấu xong.
7. **Không tự đi tiếp.** Mỗi lượt một bước (bước `code` chạy theo lô: mỗi lượt một lô), sau đó dừng chờ duyệt. Lý do: người dùng phải xem được kết quả từng bước trước khi nó thành đầu vào của bước sau; plan chưa duyệt mà đã code thì sửa rất tốn.

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

- Không chạy liền một mạch: mỗi bước bàn giao cần người dùng gõ lệnh rồi quay lại bằng `--from`; chạy theo lô vẫn dừng duyệt sau mỗi lô.
- Chạy theo lô cần tool có subagent (VD Claude Code); CLI không có subagent thì bước `code` bàn giao từng bước như cũ.
- Giai đoạn Lập kế hoạch và Test chưa có skill riêng; workflow tự viết plan theo khuôn ngắn và chỉ chạy lệnh test sẵn có của dự án.
- Slash command (`/nqdev:sync-status`...) chỉ có trên Claude Code; trên CLI khác bước chốt chỉ liệt kê việc cần làm tay.

Trả lời bằng ngôn ngữ người dùng đang dùng (mặc định tiếng Việt), giữ thuật ngữ kỹ thuật tiếng Anh.
