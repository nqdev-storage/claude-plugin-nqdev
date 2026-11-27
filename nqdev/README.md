# nqdev — Claude Code plugin

Bộ **skills** và **slash commands** của nqdev (QuyIT Platform) dành cho Claude Code, đóng gói thành một plugin để cài một lần dùng mọi nơi. Các skill xếp theo các giai đoạn của flow coding, từ thu thập yêu cầu tới deploy.

Phiên bản plugin: **2.7.1** (2026-11-26) · 14 skill (gồm skill điều phối `nqdev-task-flow` với 4 workflow dựng sẵn) · 7 slash command.

## Bắt đầu nhanh: workflow dựng sẵn

Cài xong là dùng được, không cần tự nối skill. Skill `nqdev-task-flow` dẫn bạn qua từng bước: **mỗi lượt chạy đúng một bước rồi dừng chờ bạn duyệt**, không tự đi tiếp. Ví dụ plan phải được duyệt (ghi `status: approved` vào file plan) thì mới tới bước code.

Không cần nhớ lệnh: chỉ cần nói *"tạo tính năng xuất Excel"*, *"sửa lỗi này: …"*, Claude tự nạp `nqdev-task-flow` và **hỏi trước** bạn muốn chạy workflow hay làm trực tiếp (việc nhỏ một dòng thì chọn làm trực tiếp). Gõ lệnh dưới đây thì bỏ qua câu hỏi đó.

| Lệnh | Workflow |
|---|---|
| `/nqdev:nqdev-task-flow feature <mô tả tính năng>` | BRD → estimate → thiết kế UI (tuỳ chọn) → plan → code → test → review → MR → chốt |
| `/nqdev:nqdev-task-flow bugfix <thông báo lỗi>` | sửa bug → test → review → MR → chốt |
| `/nqdev:nqdev-task-flow init [mô tả dự án]` | rule cho AI → BRD → estimate |
| `/nqdev:nqdev-task-flow release [v1.2.0..HEAD]` | review → release note → chốt |

Ở bước sửa code (`nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-design-to-artifact`) và bước commit (`/nqdev:sync-status`), workflow **không tự chạy** mà đưa đúng lệnh để bạn gõ. Đây là điểm duyệt có chủ đích: chỉ bạn mới cho phép sửa code và đưa code ra ngoài. Chạy xong lệnh đó, quay lại bằng `--from`:

```
/nqdev:nqdev-task-flow feature --from=test
```

Không truyền `--from` thì workflow tự dò repo (`docs/brd/`, `plans/`, `git status`) để đề xuất bước bắt đầu.

Để Claude luôn nhớ đề xuất workflow, chạy `/nqdev:nqdev-task-flow init` (hoặc `/nqdev:nqdev-init-agents`) một lần trong repo: `.claude/rules/code-rules.md` sinh ra có sẵn quy tắc "tính năng, bug, release thì đề xuất `nqdev-task-flow` trước". Repo đã có `code-rules.md` từ trước sẽ không bị ghi đè; tự thêm quy tắc số 0 trong mục "Development Workflow Policy" của [template](https://github.com/nqdev-storage/claude-plugin-nqdev/blob/dist/nqdev/skills/nqdev-init-agents/templates/code-rules.md).

## Cài đặt

```bash
# Thêm marketplace từ GitHub (branch phát hành dist, chỉ chứa file cần cài)
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist
# hoặc từ bản clone local khi phát triển: claude plugin marketplace add ./

# Cài plugin
claude plugin install nqdev@nqdev-marketplace
```

Trong phiên Claude Code có thể dùng `/plugin marketplace add ...` và `/plugin install nqdev@nqdev-marketplace`. Sau khi sửa file cục bộ, chạy `/reload-plugins`.

Skill cũng dùng được trên Codex CLI và Gemini CLI bằng cách copy thư mục skill. Slash command chỉ dùng được trên Claude Code. Chi tiết: [mục 9 của hướng dẫn cài đặt](../docs/huong-dan-cai-dat-va-su-dung.md).

## Skills (14)

### Flow coding và skill tương ứng

| Giai đoạn | Skill |
|---|---|
| 1. Thu thập yêu cầu | `nqdev-brd-prd-writer` |
| 2. Phân tích / Estimate | `nqdev-requirement-estimator` |
| 3. Thiết kế | `nqdev-design-to-artifact` |
| 4. Setup môi trường AI | `nqdev-init-agents` |
| 5. Lập kế hoạch | `nqdev-write-plan` |
| 6. Code | `nqdev-feature-implementer`, `nqdev-bug-fixer` |
| 7. Test | `nqdev-test-case-writer`, `nqdev-unit-test-generator` |
| 8. Review / Refactor | `nqdev-code-review`, `nqdev-merge-request-writer` |
| 9. Deploy | `nqdev-release-note-writer` |
| 10. Tài liệu hoá | `nqdev-business-flow-extractor` |
| Điều phối cả flow | `nqdev-task-flow` |

Giai đoạn Lập kế hoạch và Test đã có skill riêng, nhưng `nqdev-task-flow` chưa gọi chúng: bước plan vẫn viết theo khuôn ngắn vào `plans/` và bước test chạy lệnh test sẵn có của dự án; command `/nqdev:sync-plan-status` và `/nqdev:nqdev-cmd-plans-cleanup` dùng để cập nhật và dọn plan.

### Danh sách skill

| Skill | Phiên bản | Công dụng chính | Vai trò trong flow |
|---|---|---|---|
| `nqdev-brd-prd-writer` | 2.1.4 | Biến ý tưởng, ghi chú họp, yêu cầu khách hàng thành BRD, mỗi module một file trong `docs/brd/`, có mã BR/AC/UC. PRD chỉ viết khi được yêu cầu rõ. | Thu thập yêu cầu |
| `nqdev-requirement-estimator` | 5.0.0 | Ước lượng theo giờ, bước 0.5 (dạng khoảng; AI làm, DEV review và góp ý) từ mô tả, spec hoặc BRD/PRD; chia module, phase MVP/sau MVP, rủi ro, câu hỏi cần làm rõ. Chỉ đọc. | Phân tích / Estimate |
| `nqdev-design-to-artifact` | 3.5.1 | Thiết kế màn hình UI ở local từ `docs/prototype/_gen/`, dựng trang bấm thử được, kèm màn System Design. Chỉ publish khi có `--publish`. | Thiết kế (UI/UX) |
| `nqdev-init-agents` | 1.8.2 | Tạo `CLAUDE.md`, `.claudeignore`, `.claude/rules/code-rules.md` (quy tắc DB, Git, Workflow, Comment, Testing; có quy tắc đề xuất `nqdev-task-flow`) và thư mục `draft/` cho repo. Không ghi đè file đã có. | Setup môi trường AI |
| `nqdev-feature-implementer` | 1.1.1 | Code một tính năng theo plan và BRD, tuân thủ quy tắc repo, kèm test và bảng truy vết BR/AC. Không tự commit, push hay chạy lệnh DB. | Code |
| `nqdev-bug-fixer` | 1.0.1 | Sửa bug theo trình tự: tái hiện, khoanh vùng, nguyên nhân gốc, sửa tối thiểu, test chống tái phát. | Code |
| `nqdev-write-plan` | 1.10.0 | Viết execution plan (trước khi làm) hoặc nhật ký công việc (sau khi làm) vào `plans/<stt>-<YYYY-MM-DD>-<slug>.md`, có ước lượng, bảng Tiến độ ghi mốc bắt đầu/kết thúc từng task, cập nhật trạng thái khi làm tiếp hoặc xong. Plan lớn có file giao việc `.claude/assign-tasks/*.jsonl` để chạy theo lô. | Lập kế hoạch |
| `nqdev-test-case-writer` | 1.0.0 | Sinh test case thủ công từ AC (Cho/Khi/Thì) trong BRD hoặc tài liệu luồng nghiệp vụ; mỗi test case có mã `TC-` và ghi mã AC/BR, kèm ma trận phủ. Chỉ đọc. | Test |
| `nqdev-unit-test-generator` | 1.0.0 | Viết unit test và integration test cho code có sẵn theo đúng framework và quy ước test của repo; chỉ ghi file test, không sửa code ứng dụng. | Test |
| `nqdev-code-review` | 1.0.1 | Review diff, MR hoặc nhóm file theo bốn trục: đúng đắn, bảo mật, hiệu năng, quy tắc và yêu cầu. Trả bảng vấn đề theo mức độ. Chỉ đọc. | Review / Refactor |
| `nqdev-merge-request-writer` | 1.0.2 | Soạn commit message và mô tả MR/PR từ diff, theo quy ước và template của repo, kèm mã BR/AC. Không tự commit, push hay tạo MR. | Review / Refactor |
| `nqdev-release-note-writer` | 1.0.1 | Tổng hợp release note và checklist deploy (migration, cấu hình, rollback) giữa hai bản phát hành. Không tự tag, push hay deploy. | Deploy |
| `nqdev-business-flow-extractor` | 1.1.2 | Đọc code để rút ra một luồng nghiệp vụ thành tài liệu cho PM/BA/QA/QC, có sơ đồ Mermaid và phụ lục `file:line`. | Tài liệu hoá |
| `nqdev-task-flow` | 1.8.0 | Điều phối 4 workflow dựng sẵn (`feature`, `bugfix`, `init`, `release`): tự kích hoạt khi bạn yêu cầu tính năng, sửa bug, release (hỏi trước có chạy workflow không), mỗi lượt một bước, dừng chờ duyệt sau mọi bước, plan phải `approved` mới tới bước code (plan lớn chạy theo lô từ file giao việc, duyệt sau mỗi lô), đưa lệnh cho người dùng gõ ở bước sửa code và commit. Không tự commit hay push. | Điều phối |

### Cách gọi skill

- Phần lớn skill tự kích hoạt khi yêu cầu khớp với `description`, hoặc gọi bằng `/nqdev:<tên-skill>`.
- Bốn skill **chỉ chạy khi gọi rõ** (`disable-model-invocation: true`) vì có tác động lên code, file test hoặc canvas: `nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-unit-test-generator`, `nqdev-design-to-artifact`. Claude Code chặn mọi cách gọi tự động các skill này (kể cả từ skill khác hay subagent), nên `nqdev-task-flow` chỉ đưa lệnh cho bạn gõ.
- `nqdev-task-flow` tự kích hoạt được, nhưng luôn hỏi trước (bước 0) và không tự sửa code.
- Trên Codex CLI, `nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-unit-test-generator` và `nqdev-design-to-artifact` có kèm `agents/openai.yaml` với `policy.allow_implicit_invocation: false` để chỉ chạy khi được gọi rõ; `nqdev-task-flow` đặt `true` để tự kích hoạt như trên Claude Code.

### Các skill nối với nhau thế nào

Các skill chia sẻ một số thư mục và mã định danh trong repo đích:

| Thứ dùng chung | Nguồn tạo ra | Skill dùng lại |
|---|---|---|
| `docs/brd/<module>.md`, mã `BR-`, `AC-`, `UC-` | `nqdev-brd-prd-writer` | `nqdev-requirement-estimator`, `nqdev-design-to-artifact`, `nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-code-review`, `nqdev-merge-request-writer`, `nqdev-release-note-writer` |
| `docs/prototype/` (màn ghi `<!--traces: UC-..., AC-...-->`), bảng "Truy vết màn ↔ UC/AC" trong `docs/specs/ui-ux.md` | `nqdev-design-to-artifact` | `nqdev-task-flow` (mục `## Màn hình` trong plan), `nqdev-feature-implementer` (cột "Màn" trong bảng truy vết) |
| `plans/<stt>-<YYYY-MM-DD>-<slug>.md` | `nqdev-write-plan`, `nqdev-task-flow` (bước `plan`) hoặc viết tay | `nqdev-feature-implementer`, `nqdev-code-review`, `nqdev-merge-request-writer`, `nqdev-release-note-writer` |
| `.claude/rules/code-rules.md`, `CLAUDE.md` | `nqdev-init-agents` | Mọi skill ở giai đoạn Code, Review, Deploy |
| `docs/business-flows/<slug>.md` | `nqdev-business-flow-extractor` | Người đọc PM/BA/QA/QC |

Chuỗi điển hình cho một tính năng mới (chính là workflow `/nqdev:nqdev-task-flow feature`):

1. `nqdev-brd-prd-writer` viết BRD.
2. `nqdev-requirement-estimator` ước lượng từ BRD.
3. `nqdev-design-to-artifact` thiết kế màn hình.
4. `nqdev-write-plan` viết plan thực thi vào `plans/`.
5. `nqdev-feature-implementer` code theo plan và BRD.
6. `nqdev-code-review` soát, `nqdev-merge-request-writer` soạn mô tả MR.
7. `nqdev-release-note-writer` soạn release note và checklist deploy.
8. `/nqdev:sync-status` cập nhật plan, Jira, commit và push.

## Slash commands (7)

| Command                    | Công dụng                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------- |
| `/nqdev-cmd-plans-cleanup` | Dọn nội dung trùng lặp và frontmatter mâu thuẫn trong `plans/`                        |
| `/sync-plan-status`        | Cập nhật trạng thái các file plan theo công việc đã làm                               |
| `/sync-git-ship`           | Kiểm tra thay đổi, commit kiểu conventional và push; chặn commit secret               |
| `/sync-jira-status`        | Cập nhật trạng thái Jira theo công việc đã làm (chuyển trạng thái, comment, tạo task) |
| `/sync-status`             | Chốt công việc: cập nhật plan, Jira, commit và push                                   |
| `/tracker-jira-nqdev`      | Truy vấn Jira Cloud qua REST API                                                      |
| `/tracker-gs-sync`         | Đồng bộ và lọc issue từ Google Sheet theo sprint                                      |

Trong plugin, gọi command bằng tên đầy đủ, ví dụ `/nqdev:sync-status`. `/sync-git-ship` và `/sync-status` có thể **commit và push**; dùng `--no-push` khi muốn kiểm tra trước.

## Biến môi trường

Các command liên quan Jira (`/nqdev:tracker-jira-nqdev`, `/nqdev:sync-jira-status`, `/nqdev:sync-status`) cần 3 biến: `JIRA_BASE_URL` (ví dụ `https://<your-domain>.atlassian.net`), `JIRA_EMAIL`, `JIRA_API_TOKEN`. Plugin không chứa sẵn thông tin đăng nhập hay domain nào.

`/nqdev:tracker-gs-sync` cần bật connector **Google Drive** của claude.ai (Settings → Connectors) và sheet phải được share cho tài khoản Google đó.

## Cấu trúc plugin

Cấu trúc chuẩn của một Claude plugin:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata (required)
├── .mcp.json            # MCP server configuration (optional)
├── commands/            # Slash commands (optional)
├── agents/              # Agent definitions (optional)
├── skills/              # Skill definitions (optional)
└── README.md            # Documentation
```

Plugin `nqdev` nằm trong thư mục `nqdev/` của repo marketplace (`marketplace.json` khai báo `"source": "./nqdev"`):

```
nqdev/
├── .claude-plugin/
│   ├── plugin.json         # Metadata plugin (name, version, author, URL directory...)
│   ├── icon.png            # Icon 1024x1024 cho listing (render từ icon.svg)
│   └── icon.svg            # Bản gốc của icon, sửa file này rồi render lại PNG
├── .mcp.json               # Cấu hình MCP server (hiện để trống)
├── commands/               # 7 slash command (*.md)
├── agents/                 # Định nghĩa agent (hiện để trống, giữ chỗ bằng .gitkeep)
├── skills/                 # 14 skill, mỗi skill một thư mục có SKILL.md
│   ├── nqdev-task-flow/references/     # Các bước của 4 workflow: feature, bugfix, init, release
│   └── <skill>/agents/openai.yaml # Chỉ có ở feature-implementer, bug-fixer, unit-test-generator, design-to-artifact, flow (cấu hình cho Codex CLI)
├── LICENSE
└── README.md               # File này
```

Plugin này chưa có agent và MCP server nào (`agents/` và `.mcp.json` đang để trống), cũng chưa dùng `hooks/`. Trong `.claude-plugin/` chỉ có `plugin.json` và icon. Khi cài, Claude Code chỉ copy thư mục `nqdev/`, nên mọi file plugin cần lúc chạy phải nằm trong thư mục này.

Cấu trúc của cả repo (marketplace, `docs/`, CI) xem ở [README của repo](../README.md).

## Việc còn dở

- Cả 14 skill đã có README. Mười một skill chưa có SYSTEM_PROMPT, USER_PROMPT, EXAMPLES: `nqdev-bug-fixer`, `nqdev-business-flow-extractor`, `nqdev-code-review`, `nqdev-feature-implementer`, `nqdev-init-agents`, `nqdev-merge-request-writer`, `nqdev-release-note-writer`, `nqdev-task-flow`, `nqdev-test-case-writer`, `nqdev-unit-test-generator`, `nqdev-write-plan`. Bốn skill trong số đó còn thiếu cả CHANGELOG: `nqdev-bug-fixer`, `nqdev-business-flow-extractor`, `nqdev-code-review`, `nqdev-release-note-writer`.
- `nqdev-task-flow` chưa nối `nqdev-write-plan`, `nqdev-test-case-writer`, `nqdev-unit-test-generator` vào các bước plan và test (hiện viết plan theo khuôn ngắn, chạy lệnh test sẵn có).
- `nqdev-task-flow` chưa chạy thử trên Claude Code thật: tài liệu Claude Code không nói rõ một skill có nạp được skill khác không. Nếu không được, bước "Gọi skill" tự chuyển thành "Bàn giao" (đưa lệnh cho người dùng gõ).
- Chưa có skill viết tài liệu cho cả repo (trước đây là `nqdev-codebase-analyst`, đã bỏ).

## Lịch sử thay đổi

| Ngày | Thay đổi |
|---|---|
| 2026-11-26 | Plugin v2.7.1: `nqdev-init-agents` 1.8.2, sửa khối `.gitignore` của `draft/`: `draft/*` ignore luôn thư mục `draft/docs/` nên `!draft/docs/.gitkeep` không có tác dụng; khối mới thêm `!draft/docs/` và `draft/docs/*` trước dòng `!draft/docs/.gitkeep`. Repo đích đã có khối `draft/*` cũ thì skill thay cả khối, không chèn thêm từng dòng; kiểm tra bằng file thử chưa track. |
| 2026-11-26 | Plugin v2.7.0: `nqdev-write-plan` 1.10.0, quy đổi giờ sang MD (1 MD = 8h, bước 0.125 MD, trường `estimated_md` / `time_spent_md` và hàng Tổng); bảng Tiến độ luôn có dòng `0` "Phân tích và lập plan" (mốc ghi từ đầu phiên) và dòng cuối "Bàn giao: commit, push, MR, tracker"; quy tắc mốc suy ra, không chồng mốc, phần chênh với worklog Jira ghi ở hàng Tổng; `estimated_hours` tính end-to-end. `nqdev-task-flow` 1.8.0, chạy theo lô không bốc bước 0 và bước bàn giao, ghi mốc cho 2 bước này. `nqdev-init-agents` 1.8.1 và `nqdev-brd-prd-writer` 2.1.4, làm rõ ranh giới `docs/Business-Document.md` (cấp dự án) với BRD từng module. Plan cũ không bắt buộc sửa. |
| 2026-11-20 | Plugin v2.6.0: `nqdev-write-plan` 1.8.0, bảng Tiến độ có cột `Bắt đầu \| Kết thúc \| Delta (phút)` cho từng lần làm task, bỏ mục Nhật ký thời gian, `time_spent_hours` = tổng Delta làm tròn 0.25h ở hàng Tổng; thêm trạng thái `approved`, trường `assign_tasks` và file giao việc `.claude/assign-tasks/<plan>.jsonl` cho plan lớn (≥ 10 bước, hoặc ≥ 40h, hoặc có bước chạy song song). `nqdev-task-flow` 1.7.0, plan lớn chạy bước `code` theo lô (tối đa 3 bước, giao agent theo `.jsonl`, duyệt sau mỗi lô). `nqdev-init-agents` 1.8.0, tạo thư mục `draft/`. |
| 2026-11-19 | Plugin v2.5.0: `nqdev-write-plan` 1.5.0 đổi Template Pre thành Bối cảnh / Approach và quyết định đã chốt / Tiến độ (bảng `# | Bước | Trạng thái | Ghi chú`, trạng thái `chưa làm` / `đang làm` / `xong` / `bỏ`, thay checklist Todo) / Risks và Unknowns / Tiêu chí hoàn thành / Câu hỏi và Phụ thuộc; `references/example-plan.md` có thêm ví dụ Pre đang làm. Command `/nqdev:nqdev-cmd-plans-cleanup` nhận diện cả tên mục mới lẫn cũ. |
| 2026-11-19 | Plugin v2.4.0: đổi mô hình estimate sang **AI là người làm, DEV là người review và góp ý**, đơn vị **giờ, bước 0.5**. `nqdev-requirement-estimator` 5.0.0 (**breaking**: bỏ person-day; mỗi dòng có 3 cột AI | DEV review | Tổng; Tổng = Dev + QA/UAT; bỏ PM và timeline theo tuần; kiểm tra khả thi so giờ DEV với quỹ giờ DEV; baseline viết lại, dựa trên kinh nghiệm, chưa đo). `nqdev-write-plan` 1.4.0 (`estimated_hours` bước 0.5, thời gian thực tế vẫn 0.25), `nqdev-design-to-artifact` 3.5.1 (chỉnh câu ước lượng giờ), `nqdev-brd-prd-writer` 2.1.3 (sửa mô tả trong README). |
| 2026-11-19 | Plugin v2.3.0: đổi quy ước tên file plan từ `plans/YYYY-MM-DD-<slug>.md` thành `plans/<stt>-<YYYY-MM-DD>-<slug>.md` (`stt` là số thứ tự 3 chữ số, bộ đếm chung cho cả `plans/`). `nqdev-write-plan` 1.3.0 (thêm cách tính `stt`), `nqdev-task-flow` 1.5.0, `nqdev-feature-implementer` 1.1.1 và `nqdev-merge-request-writer` 1.0.2 (cập nhật ví dụ). Đã đổi tên 8 file trong `plans/` của repo này (`001-` đến `008-`). Repo đích có plan cũ không bắt buộc đổi tên; bộ đếm bỏ qua file chưa có `stt`. |
| 2026-11-19 | Plugin v2.2.1: bỏ nhãn cố định `[nqdev]` khỏi ví dụ comment; dùng placeholder `[<label>]` (nhãn của từng dev, lưu ở `.claude/dev.local.json`). `nqdev-init-agents` 1.7.1, template `code-rules` 2.2.2. Repo đích đã sinh `code-rules.md` từ bản cũ không bị ảnh hưởng. |
| 2026-11-19 | Plugin v2.2.0: đổi tên skill `nqdev-flow` thành `nqdev-task-flow` (1.4.0), **breaking**: lệnh gọi đổi từ `/nqdev:nqdev-flow` thành `/nqdev:nqdev-task-flow` (Codex CLI: `$nqdev-task-flow`), không giữ alias. Cập nhật tham chiếu ở `nqdev-init-agents` 1.7.0 (rule số 0 trong `code-rules.md` v2.2.1), `nqdev-design-to-artifact` 3.5.0, command `/nqdev:nqdev-cmd-plans-cleanup` và tài liệu. Repo đích đã sinh `code-rules.md` từ bản cũ cần sửa tay rule số 0. |
| 2026-11-18 | Plugin v2.1.0: thêm 3 skill `nqdev-write-plan` (1.2.1), `nqdev-test-case-writer` (1.0.0), `nqdev-unit-test-generator` (1.0.0). Hai skill test được chuẩn hoá frontmatter; `nqdev-unit-test-generator` chỉ chạy khi gọi rõ (`disable-model-invocation: true`, `agents/openai.yaml` đặt `false`). `nqdev-flow` 1.3.1 và `nqdev-design-to-artifact` 3.4.1 bỏ cách nói `nqdev-write-plan` là skill tuỳ chọn; command `/nqdev:nqdev-cmd-plans-cleanup` cũng vậy. Chưa nối skill mới vào `nqdev-flow`. |
| 2026-11-18 | Plugin v1.3.0: nối nhánh thiết kế UI vào chuỗi truy vết BR/AC/UC. `nqdev-design-to-artifact` 3.4.0 đọc UC/AC từ `docs/brd/<module>.md`, ghi `<!--traces: ...-->` vào nguồn từng màn và bảng "Truy vết màn ↔ UC/AC" trong `docs/specs/ui-ux.md`; `--check` báo màn thiếu hoặc lệch mã. `nqdev-flow` 1.3.0: khuôn plan có mục `## Màn hình`, bước `review` đối chiếu cả màn. `nqdev-feature-implementer` 1.1.0 đọc prototype mà plan trỏ tới, bảng truy vết thêm cột "Màn". Không có BRD hay prototype thì các skill chạy như cũ. |
| 2026-11-18 | Plugin v1.2.0: dời plugin vào thư mục `nqdev/` (`marketplace.json` đổi `source` từ `./` thành `./nqdev`) để repo marketplace chứa được nhiều plugin. Không đổi skill hay command nào; lệnh cài vẫn là `nqdev@nqdev-marketplace`. Đã cài bản cũ: chạy `claude plugin marketplace update nqdev-marketplace` rồi `claude plugin update nqdev@nqdev-marketplace`. Tác giả hiển thị đổi thành "Nguyễn Quý". |
| 2026-11-17 | Plugin v1.1.0: thêm skill `nqdev-flow` (1.2.0) với 4 workflow dựng sẵn (`feature`, `bugfix`, `init`, `release`): tự kích hoạt có hỏi trước, duyệt sau mọi bước, plan phải `approved` mới tới code. `nqdev-init-agents` 1.6.3 thêm quy tắc đề xuất `nqdev-flow` vào `code-rules.md`. Rà soát trước phát hành: bỏ Sheet ID thật khỏi ví dụ `tracker-gs-sync`; `sync-jira-status` và `tracker-jira-nqdev` luôn hỏi trước khi ghi Jira; thêm 3 file `references/` còn thiếu của `nqdev-business-flow-extractor`; `design-to-artifact` dùng `${CLAUDE_PLUGIN_ROOT}` và có `openai.yaml`; ví dụ trong skill và command dùng tên đầy đủ `/nqdev:<tên>`. Rà soát lần hai: bỏ `${CLAUDE_PLUGIN_ROOT}` khỏi file tham chiếu của skill, thêm kiểm tra biến Jira bằng `printenv` cho `sync-jira-status` và `sync-status`, sửa đường dẫn home trên Windows trong `tracker-gs-sync`. |
| 2026-11-17 | Plugin v1.0.2: chuẩn hoá frontmatter 10 skill (bỏ nháy ở `name`, thêm metadata, `compatibility` có Gemini CLI và Codex CLI), thêm `agents/openai.yaml`, `nqdev-requirement-estimator` 4.0.2 sửa tiêu đề. Bỏ khỏi danh sách 6 skill chưa đưa vào plugin: `nqdev-system-design-diagram`, `nqdev-write-plan`, `nqdev-test-case-writer`, `nqdev-unit-test-generator`, `nqdev-skill-refactor`, `nqdev-slash-command-builder`. Gộp `docs/readme.md` vào README này. |
| 2026-11-17 | Thêm 7 skill cho các giai đoạn Code, Test, Review/Refactor, Deploy. |
| 2026-11-16 | Đổi tên `nqdev-client-requirement-insight` thành `nqdev-requirement-estimator`. Gộp `nqdev-drawio-diagram-creator` vào `nqdev-system-design-diagram`. Bỏ `nqdev-codebase-analyst`. |

## Tài liệu

- [Hướng dẫn cài đặt và sử dụng từ Git repo](../docs/huong-dan-cai-dat-va-su-dung.md)
- [Giới thiệu các skill: chọn skill theo tình huống, đầu vào và đầu ra](../docs/gioi-thieu-cac-skill.md)
- [Hướng dẫn nộp plugin lên Claude Plugin Directory](../docs/huong-dan-nop-plugin.md)

## Tài liệu tham khảo

Các nguồn dùng để xây dựng plugin này:

- [Claude Code: Plugins](https://code.claude.com/docs/en/plugins): tạo và cài plugin
- [Claude Code: Plugins reference](https://code.claude.com/docs/en/plugins-reference): schema `plugin.json`, cấu trúc thư mục, biến `${CLAUDE_PLUGIN_ROOT}`
- [Claude Code: Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces): schema `marketplace.json`, các loại `source`
- [Claude Code: Publish plugins](https://code.claude.com/docs/en/plugins/publish): quy trình phát hành
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official): repo mẫu, cấu trúc plugin của Anthropic
- [ivan-magda/claude-code-plugin-template](https://github.com/ivan-magda/claude-code-plugin-template)
- [Claude Marketplace: Plugins](https://claude.com/marketplace/plugins): nơi duyệt và nộp plugin
- [Hướng dẫn nộp plugin (Anthropic)](https://claude.com/docs/plugins/submit): các bước nộp qua developer portal

## Giấy phép

Apache-2.0 — xem [LICENSE](https://github.com/nqdev-storage/claude-plugin-nqdev/blob/dist/nqdev/LICENSE).
