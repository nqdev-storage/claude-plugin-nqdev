# Giới thiệu các skill của plugin `nqdev` và `vhs`

> Cập nhật: 2026-11-27 · Plugin `nqdev` v2.7.1 (14 skill) · Plugin `vhs` v1.0.0 (2 skill)\
> Dành cho người dùng mới cài plugin và muốn biết **nên dùng skill nào, vào lúc nào, nhận lại thứ gì**. Cách cài: [Hướng dẫn cài đặt và sử dụng](huong-dan-cai-dat-va-su-dung.md).

## 1. Cách đọc trang này

- Mục 2 giúp chọn skill theo tình huống. Mục 3 nói các skill nối nhau thế nào. Mục 4 và 5 mô tả từng skill.
- Gọi skill bằng tên đầy đủ có tiền tố plugin: `/nqdev:<tên-skill>` hoặc `/vhs:<tên-skill>`.
- Phần lớn skill còn **tự kích hoạt** khi yêu cầu của bạn khớp mô tả. Nhiều khi chỉ cần nói việc cần làm.
- Mọi skill đều **không tự commit, push hay chạy lệnh ghi vào database**. Kết quả là văn bản, file tài liệu, hoặc code để bạn xem lại.
- Chỗ nguồn không nói rõ, skill ghi `[cần xác nhận: ...]` thay vì tự bịa. Đó là chủ ý.

## 2. Chọn skill theo tình huống

| Tôi đang muốn… | Dùng skill |
|---|---|
| Biến ý tưởng, ghi chú họp, yêu cầu khách hàng thành tài liệu yêu cầu | [`nqdev-brd-prd-writer`](#nqdev-brd-prd-writer) |
| Biết một việc mất bao lâu, cần mấy người, nên làm gì trước | [`nqdev-requirement-estimator`](#nqdev-requirement-estimator) |
| Dựng thử giao diện màn hình, bấm được | [`nqdev-design-to-artifact`](#nqdev-design-to-artifact) |
| Thiết lập repo mới để AI làm đúng quy tắc của đội | [`nqdev-init-agents`](#nqdev-init-agents) |
| Lập kế hoạch trước khi code, hoặc ghi lại việc vừa làm | [`nqdev-write-plan`](#nqdev-write-plan) |
| Đi trọn một tính năng, bug hoặc đợt release, duyệt từng bước | [`nqdev-task-flow`](#nqdev-task-flow) |
| Code một tính năng theo plan đã duyệt | [`nqdev-feature-implementer`](#nqdev-feature-implementer) |
| Sửa một bug đã có thông báo lỗi hoặc stack trace | [`nqdev-bug-fixer`](#nqdev-bug-fixer) |
| Có kịch bản kiểm thử thủ công cho QA từ BRD | [`nqdev-test-case-writer`](#nqdev-test-case-writer) |
| Có unit test, integration test tự động cho code sẵn có | [`nqdev-unit-test-generator`](#nqdev-unit-test-generator) |
| Soát thay đổi trước khi merge | [`nqdev-code-review`](#nqdev-code-review) |
| Soạn commit message hoặc mô tả merge request | [`nqdev-merge-request-writer`](#nqdev-merge-request-writer) |
| Chuẩn bị release note và checklist deploy | [`nqdev-release-note-writer`](#nqdev-release-note-writer) |
| Ghi lại một luồng nghiệp vụ của ứng dụng có sẵn cho PM/BA/QA | [`nqdev-business-flow-extractor`](#nqdev-business-flow-extractor) |
| Tinh chỉnh một prompt thô trước khi chạy | [`trietnm-prompt-tuner`](#trietnm-prompt-tuner) |
| Viết hướng dẫn sử dụng phần mềm cho người dùng cuối | [`trietnm-user-doc-writer`](#trietnm-user-doc-writer) |

Việc nhỏ một bước (đổi text, thêm log, đổi tên biến): làm trực tiếp, không cần qua skill nào.

## 3. Các skill nối nhau thế nào

Các skill của `nqdev` không gọi nhau tự động. Chúng nối với nhau qua **file và mã trong repo của bạn**:

| Thứ dùng chung | Do skill nào tạo | Skill nào đọc lại |
|---|---|---|
| `docs/brd/<module>.md`, mã `BR-`, `AC-`, `UC-` | `nqdev-brd-prd-writer` | estimate, thiết kế, code, review, test case, MR, release note |
| `plans/<stt>-<YYYY-MM-DD>-<slug>.md` | `nqdev-write-plan` | code, review, MR, release note |
| `.claude/rules/code-rules.md`, `CLAUDE.md` | `nqdev-init-agents` | mọi skill ở giai đoạn code, review, deploy |
| `docs/business-flows/<slug>.md` | `nqdev-business-flow-extractor` | `nqdev-test-case-writer` và người đọc PM/BA/QA |

Chuỗi điển hình cho một tính năng mới: BRD → estimate → thiết kế → plan → code → review → MR → release note.

`nqdev-task-flow` dẫn bạn đi hết chuỗi này, mỗi lượt một bước. Bản đồ đầy đủ các giai đoạn: [nqdev/README.md](../nqdev/README.md#skills-14).

## 4. Skill của plugin `nqdev`

### Thu thập yêu cầu và ước lượng

#### `nqdev-brd-prd-writer`

- **Dùng khi:** có ý tưởng, ghi chú họp hoặc yêu cầu khách hàng cần thành BRD; cập nhật một BRD đã có.
- **Không dùng khi:** muốn dựng yêu cầu ngược từ source code (dùng `nqdev-business-flow-extractor`), hoặc cần ước lượng (dùng `nqdev-requirement-estimator`).
- **Gọi:** `/nqdev:nqdev-brd-prd-writer`, hoặc nói "viết BRD cho module billing từ ghi chú họp này".
- **Vào:** tên module và nguồn nghiệp vụ.
- **Ra:** file `docs/brd/<module>.md` theo khuôn của repo, có mã `BR-/AC-/UC-<MODULE>-<số>`. PRD ở `docs/prd/` chỉ viết khi bạn yêu cầu rõ.
- **Lưu ý:**
  - Mỗi module một file. Mã đã phát hành không đổi và không dùng lại.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-brd-prd-writer/README.md), [EXAMPLES](../nqdev/skills/nqdev-brd-prd-writer/EXAMPLES.md).

#### `nqdev-requirement-estimator`

- **Dùng khi:** hỏi "mất bao lâu", "cần mấy người", "nên làm gì trước", hoặc cần rà soát phạm vi.
- **Không dùng khi:** cần viết hay sửa BRD/PRD (dùng `nqdev-brd-prd-writer`), cần plan thực thi hoặc code.
- **Gọi:** `/nqdev:nqdev-requirement-estimator <file spec/BRD hoặc mô tả yêu cầu>`
- **Vào:** mô tả, spec, hoặc BRD/PRD.
- **Ra:** giả định, bảng module (khoảng giờ theo ba cột AI | DEV review | Tổng), phase MVP, tổng, rủi ro, tối đa 5 câu hỏi cần làm rõ, phần loại trừ. Kết quả trả trong chat.
- **Lưu ý:**
  - Mô hình là AI làm, DEV review.
  - Nguồn mơ hồ vẫn estimate với khoảng rộng kèm giả định, không chờ trả lời.
  - Chỉ đọc, không ghi file.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-requirement-estimator/README.md).

### Thiết kế và thiết lập

#### `nqdev-design-to-artifact`

- **Dùng khi:** cần thiết kế màn hình UI và dựng trang bấm thử được để cho khách hoặc đội xem.
- **Chỉ chạy khi bạn gọi rõ**, vì có ghi file và có thể publish.
- **Gọi:** `/nqdev:nqdev-design-to-artifact <mô tả màn hình> [--themes=<tên>] [--check] [--publish] [--help]`
- **Vào:** mô tả màn hình, và UC/AC trong `docs/brd/` nếu có.
- **Ra:** nguồn thiết kế trong `docs/prototype/_gen/`, màn dựng sẵn trong `docs/prototype/project/`, kèm bộ quy ước giao diện.
- **Lưu ý:**
  - Mặc định dừng ở local. Chỉ khi có `--publish` mới đưa lên Artifact.
  - Mỗi màn ghi `<!--traces: UC-..., AC-...-->` để truy vết về BRD. `--check` báo màn thiếu hoặc lệch mã.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-design-to-artifact/README.md), [EXAMPLES](../nqdev/skills/nqdev-design-to-artifact/EXAMPLES.md).

#### `nqdev-init-agents`

- **Dùng khi:** bắt đầu một repo và muốn AI làm theo quy tắc của đội ("init agents", "tạo CLAUDE.md", "setup rule cho AI").
- **Không dùng khi:** chỉ cần một `CLAUDE.md` tóm tắt codebase kiểu lệnh `/init` có sẵn, hoặc đang làm tính năng (dùng `nqdev-task-flow`).
- **Gọi:** `/nqdev:nqdev-init-agents [--sub-claude] [--claude-depth=N] [--rtk|--no-rtk] [--opencode]`
- **Vào:** dự án đang mở, skill tự phân tích.
- **Ra:** `CLAUDE.md`, `.claudeignore`, `.claude/rules/code-rules.md` (quy tắc về database, git, workflow, comment, testing), thư mục `draft/`. Tuỳ chọn thêm `CLAUDE.md` theo từng lớp, `.rtk/`, `.opencode/`.
- **Lưu ý:**
  - Không bao giờ ghi đè file đã có.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-init-agents/README.md).

### Lập kế hoạch và điều phối

#### `nqdev-write-plan`

- **Dùng khi:** "viết execution plan", "lên kế hoạch rồi ghi vào plans", "cập nhật trạng thái plan", "log công việc vừa làm".
- **Không dùng khi:** chỉ bàn kế hoạch trong chat, viết BRD/PRD hoặc estimate.
- **Gọi:** `/nqdev:nqdev-write-plan`, hoặc nói yêu cầu bằng lời.
- **Vào:** mô tả công việc, sắp làm hoặc vừa làm.
- **Ra:** file `plans/<stt>-<YYYY-MM-DD>-<slug>.md` có ước lượng giờ và bảng Tiến độ ghi mốc bắt đầu/kết thúc từng bước. Plan lớn có thêm file giao việc `.claude/assign-tasks/<tên plan>.jsonl`.
- **Lưu ý:**
  - Chỉ ghi file khi bạn đồng ý hoặc quy trình yêu cầu. Không tự commit file plan.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-write-plan/README.md).

#### `nqdev-task-flow`

- **Dùng khi:** muốn đi trọn một việc theo workflow có duyệt từng bước: "tạo tính năng …", "sửa lỗi …", "chuẩn bị release", "khởi tạo dự án".
- **Không dùng khi:** việc nhỏ một bước, hoặc chỉ hỏi thông tin.
- **Gọi:** `/nqdev:nqdev-task-flow <feature|bugfix|init|release> [mô tả] [--from=<bước>] [--no-push]`
- **Khi chỉ nói yêu cầu:** skill tự nạp nhưng **hỏi trước** bạn muốn chạy workflow hay làm trực tiếp.
- **Vào:** yêu cầu, thông báo lỗi, hoặc khoảng phát hành, tuỳ chế độ.
- **Ra:** báo cáo tiến độ từng lượt. Chế độ `feature` đi qua: BRD → estimate → thiết kế UI (tuỳ chọn) → plan → code → test → review → MR → chốt. Ba chế độ còn lại là `bugfix`, `init`, `release`.
- **Lưu ý:**
  - Mỗi lượt chạy **đúng một bước rồi dừng chờ duyệt**.
  - Plan phải `status: approved` mới tới bước code.
  - Ở bước sửa code và bước commit, skill đưa đúng lệnh để bạn tự gõ.
  - Plan lớn chạy bước code theo lô, tối đa 3 bước một lô, cần tool có subagent.
  - Chưa nối `nqdev-write-plan`, `nqdev-test-case-writer`, `nqdev-unit-test-generator` vào các bước plan và test.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-task-flow/README.md).

### Code và test

#### `nqdev-feature-implementer`

- **Dùng khi:** đã có plan (hoặc mô tả rõ) và muốn code tính năng theo plan và BRD.
- **Chỉ chạy khi bạn gọi rõ**, vì sửa code.
- **Không dùng khi:** sửa bug (dùng `nqdev-bug-fixer`), review, hoặc lập plan.
- **Gọi:** `/nqdev:nqdev-feature-implementer plans/<file>.md [--brd=<MODULE>] [--scope=<mã BR>] [--dry-run]`
- **Vào:** plan và BRD.
- **Ra:** code kèm test, và bảng truy vết `Mã BR/AC | Màn | File thay đổi | Test kiểm | Trạng thái`.
- **Lưu ý:**
  - Làm đúng phạm vi BR. Yêu cầu mơ hồ thì dừng và hỏi, không tự chọn.
  - Không tự commit, push, không chạy lệnh thay đổi database.
  - `--dry-run` chỉ trình bày danh sách file sẽ đổi.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-feature-implementer/README.md).

#### `nqdev-bug-fixer`

- **Dùng khi:** có thông báo lỗi, stack trace, log hoặc mô tả "mong đợi gì, thực tế ra gì".
- **Chỉ chạy khi bạn gọi rõ**, vì sửa code.
- **Không dùng khi:** thêm tính năng (dùng `nqdev-feature-implementer`) hoặc chỉ review.
- **Gọi:** `/nqdev:nqdev-bug-fixer "<thông báo lỗi hoặc mô tả>" [--brd=<MODULE>] [--diagnose-only]`
- **Vào:** triệu chứng của bug.
- **Ra:** triệu chứng, nguyên nhân gốc (kèm `file:line` và bằng chứng), cách sửa, test chống tái phát, phạm vi ảnh hưởng.
- **Lưu ý:**
  - Không sửa khi chưa kiểm chứng được nguyên nhân gốc. Không sửa test cho khớp code sai.
  - `--diagnose-only` dừng sau khi tìm nguyên nhân, không ghi file.
  - Mỗi lần một bug.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-bug-fixer/README.md).

#### `nqdev-test-case-writer`

- **Dùng khi:** QA cần test case thủ công từ BRD hoặc từ tài liệu luồng nghiệp vụ ("viết test case cho module billing").
- **Không dùng khi:** cần code test tự động (dùng `nqdev-unit-test-generator`), hoặc viết, sửa BRD.
- **Gọi:** `/nqdev:nqdev-test-case-writer <module hoặc đường dẫn BRD> [--scope=<mã BR,...>] [--type=<loại>]`
- **Vào:** `docs/brd/<module>.md`, hoặc `docs/business-flows/<slug>.md`.
- **Ra:** bảng test case mã `TC-<MODULE>-<số>`, mỗi test ghi mã AC/BR nó kiểm, ma trận phủ AC, danh sách AC chưa phủ.
- **Lưu ý:**
  - Chỉ đọc, kết quả trả trong chat.
  - Kết quả mong đợi lấy đúng từ phần "Thì" của AC, không tự nghĩ ra giá trị.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-test-case-writer/README.md).

#### `nqdev-unit-test-generator`

- **Dùng khi:** cần viết unit test hoặc integration test cho code có sẵn ("viết test cho hàm này", "bổ sung test").
- **Chỉ chạy khi bạn gọi rõ.**
- **Không dùng khi:** cần test case thủ công cho QA (dùng `nqdev-test-case-writer`) hoặc sửa bug mà test phát hiện (dùng `nqdev-bug-fixer`).
- **Gọi:** `/nqdev:nqdev-unit-test-generator <file | class | hàm | thư mục> [--type=unit|integration] [--brd=<MODULE>] [--plan-only]`
- **Vào:** code mục tiêu.
- **Ra:** file test theo đúng framework và quy ước test của repo, kèm bảng phủ, kết quả chạy, danh sách nghi bug.
- **Lưu ý:**
  - Chỉ ghi file test và file hỗ trợ test, không sửa code ứng dụng.
  - Code có vẻ sai thì test viết theo hành vi đúng và để thất bại, rồi báo nghi bug.
  - `--plan-only` chỉ liệt kê các ca sẽ viết.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-unit-test-generator/README.md).

### Review và phát hành

#### `nqdev-code-review`

- **Dùng khi:** "review giúp đoạn này", "kiểm tra trước khi merge", "code này ổn chưa".
- **Không dùng khi:** muốn sửa code (dùng `nqdev-feature-implementer` hoặc `nqdev-bug-fixer`), hoặc rà soát skill/prompt.
- **Gọi:** `/nqdev:nqdev-code-review <file | thư mục | dán diff> [--focus=<trục>] [--brd=<MODULE>]`
- **Vào:** diff hoặc danh sách file.
- **Ra:** kết luận (`Đạt` / `Đạt sau khi sửa mức Chặn` / `Chưa đạt`), bảng vấn đề theo mức Chặn, Cao, Trung bình, Gợi ý, đối chiếu AC nếu có BRD, tối đa 5 câu hỏi cho tác giả.
- **Lưu ý:**
  - Soát bốn trục: đúng đắn, bảo mật, hiệu năng, quy tắc và yêu cầu.
  - Chỉ đọc. Mỗi vấn đề có `file:line` làm bằng chứng.
  - Không chạy test hay ứng dụng.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-code-review/README.md).

#### `nqdev-merge-request-writer`

- **Dùng khi:** "soạn commit message", "viết mô tả merge request", "tóm tắt thay đổi để tạo PR".
- **Không dùng khi:** muốn review code (dùng `nqdev-code-review`) hoặc viết release note (dùng `nqdev-release-note-writer`).
- **Gọi:** `/nqdev:nqdev-merge-request-writer <commit|mr> [--base=<nhánh>] [--brd=<MODULE>] [--plan=<file>]`
- **Vào:** diff và lịch sử commit, đọc bằng lệnh git chỉ đọc.
- **Ra:** văn bản trong khối code để chép nguyên văn, theo template và kiểu commit của repo, kèm mã BR/AC và cách kiểm thử.
- **Lưu ý:**
  - Chỉ soạn văn bản. Commit, push và tạo MR do bạn làm.
  - Chỉ mô tả điều có trong diff, không ghi "đã test" khi không có bằng chứng.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-merge-request-writer/README.md).

#### `nqdev-release-note-writer`

- **Dùng khi:** "soạn release note", "chuẩn bị checklist deploy", "bản này có gì thay đổi".
- **Không dùng khi:** viết mô tả MR (dùng `nqdev-merge-request-writer`) hoặc nhật ký công việc (dùng `nqdev-write-plan`).
- **Gọi:** `/nqdev:nqdev-release-note-writer [--from=<mốc>] [--to=<mốc>] [--version=<số>] [--audience=internal|customer] [--no-checklist]`
- **Vào:** commit, `plans/`, mã BR giữa hai mốc.
- **Ra:** release note chia nhóm (phá tương thích, tính năng mới, cải tiến, sửa lỗi, bảo mật…) và checklist deploy gồm trước deploy, deploy, kiểm tra sau deploy, rollback.
- **Lưu ý:**
  - Chỉ đọc. Không tag, push hay deploy. Không tự tăng số phiên bản.
  - Migration không lùi được thì ghi rõ là không lùi được bằng cách hạ phiên bản code.
  - Bản `customer` dùng ngôn ngữ nghiệp vụ, không có chi tiết nội bộ.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-release-note-writer/README.md).

#### `nqdev-business-flow-extractor`

- **Dùng khi:** cần ghi lại hoặc reverse engineer luồng nghiệp vụ của một tính năng từ source ("trích xuất luồng nghiệp vụ", "BA cần hiểu luồng này").
- **Không dùng khi:** viết BRD từ ý tưởng, ghi chú họp hay yêu cầu khách hàng (dùng `nqdev-brd-prd-writer`).
- **Gọi:** `/nqdev:nqdev-business-flow-extractor <tính năng | entry point> [--out=<thư mục>] [--depth=service|data|external]`
- **Vào:** tên tính năng hoặc entry point (màn hình, endpoint, job, consumer…).
- **Ra:** tài liệu `docs/business-flows/<slug>.md` bằng ngôn ngữ nghiệp vụ. Gồm sơ đồ Mermaid, luồng chính, luồng thay thế, luồng lỗi, mục cho QA/QC, phụ lục `file:line`.
- **Lưu ý:**
  - Mỗi lần một luồng.
  - Chỉ đọc source, chỉ ghi file tài liệu.
  - Không chạy ứng dụng nên không xác minh được hành vi lúc chạy thật.
  - Tài liệu riêng: [README](../nqdev/skills/nqdev-business-flow-extractor/README.md).

## 5. Skill của plugin `vhs`

Plugin `vhs` (ViHAT) cài độc lập với `nqdev`, tên skill giữ nguyên bản gốc: `claude plugin install vhs@nqdev-marketplace`. Chi tiết: [vhs/README.md](../vhs/README.md).

#### `trietnm-prompt-tuner`

- **Dùng khi:** muốn hỏi "prompt này ok chưa", cần refine hoặc tối ưu một prompt thô.
- **Gọi:** `/vhs:trietnm-prompt-tuner <prompt thô>`
- **Vào:** prompt thô.
- **Ra:** ba phần:
  - Lĩnh vực nhận diện được: `code`, `analyze`, `debug`, `review`, `architecture`, `data`, `devops`, `test`, `docs`, `general`.
  - Danh sách điểm thiếu của prompt gốc.
  - Prompt đã viết lại theo mẫu của lĩnh vực, với context lấy từ workspace.
- **Lưu ý:**
  - Luôn dừng chờ bạn chọn: chạy luôn, chỉnh lại, huỷ, hoặc lưu ra file. Không tự chạy prompt đã refine.
  - Lĩnh vực mơ hồ thì hỏi trước khi refine.
  - Tài liệu riêng: [README](../vhs/skills/trietnm-prompt-tuner/README.md).

#### `trietnm-user-doc-writer`

- **Dùng khi:** cần viết tài liệu hướng dẫn sử dụng (HDSD, user guide) cho người dùng cuối từ source code của phần mềm.
- **Gọi:** `/vhs:trietnm-user-doc-writer help | plan | full | module <tên>`. Không truyền tham số thì skill in phần hướng dẫn rồi hỏi bạn chọn chế độ.
- **Vào:** source code của dự án đang mở.
- **Ra:** thư mục `docs/user-guide/` gồm:
  - Mục lục, và mỗi module một file (có bước thao tác, ví dụ minh hoạ, vị trí gợi ý chèn ảnh).
  - `_style-guide.md`: quy ước format và bảng thuật ngữ.
  - `DOC-PLAN.md`: kế hoạch và nhật ký các đợt viết.
- **Lưu ý:**
  - `plan` khảo sát và lập kế hoạch. `full` viết toàn bộ. `module <tên>` viết một module.
  - Mỗi đợt viết đọc lại style guide và kế hoạch để các đợt nối nhau nhất quán.
  - Ảnh chụp màn hình do bạn bổ sung theo chỗ gợi ý.
  - Tài liệu riêng: [README](../vhs/skills/trietnm-user-doc-writer/README.md).

## 6. Tài liệu liên quan

- [nqdev/README.md](../nqdev/README.md): bảng skill, phiên bản, slash command, lịch sử thay đổi
- [vhs/README.md](../vhs/README.md): plugin `vhs`
- [Hướng dẫn cài đặt và sử dụng](huong-dan-cai-dat-va-su-dung.md): cài, cập nhật, workflow dựng sẵn, slash command, biến môi trường Jira
