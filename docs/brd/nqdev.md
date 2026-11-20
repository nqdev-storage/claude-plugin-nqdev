# BRD — NQDEV: Plugin Claude Code `nqdev` (skill, command, workflow, marketplace)

> **Dành cho:** owner plugin, người duyệt nghiệp vụ trước khi phát hành hoặc nộp Claude Plugin Directory, dev viết thêm skill/command cho plugin.
> **Đọc để:** biết plugin `nqdev` phải làm gì cho người dùng, thế nào là đúng, và phần nào còn ngoài phạm vi.
> **Nên đọc trước:** [nqdev/README.md](../../nqdev/README.md), [Hướng dẫn cài đặt và sử dụng](../huong-dan-cai-dat-va-su-dung.md), [Hướng dẫn nộp plugin](../huong-dan-nop-plugin.md).
> **Cập nhật:** 2026-11-20 · **Trạng thái:** Nháp
> **Nguồn:** viết ngược từ tài liệu của plugin v1.1.0, không có ghi chú họp hay file chốt nghiệp vụ riêng. Viết tắt trong cột Nguồn: `README` = [nqdev/README.md](../../nqdev/README.md); `README gốc` = [README.md](../../README.md); `HDCĐ` = [huong-dan-cai-dat-va-su-dung.md](../huong-dan-cai-dat-va-su-dung.md); `HDNP` = [huong-dan-nop-plugin.md](../huong-dan-nop-plugin.md).

## 1. Phạm vi

| | |
|---|---|
| **Trong phạm vi** | Phân phối plugin qua marketplace riêng `nqdev-marketplace` từ repo Git; 11 skill xếp theo flow coding; 7 slash command; 4 workflow dựng sẵn của `nqdev-task-flow` (`feature`, `bugfix`, `init`, `release`) có điểm duyệt; dữ liệu dùng chung giữa các skill trong repo đích (`docs/brd/`, `plans/`, `.claude/rules/code-rules.md`); tích hợp Jira Cloud và Google Sheet theo cấu hình người dùng; dùng skill trên Codex CLI và Gemini CLI; tài liệu dạng site Docsify; điều kiện để nộp Claude Plugin Directory. |
| **Ngoài phạm vi** | Skill riêng cho giai đoạn Lập kế hoạch và Test (chưa có; `nqdev-task-flow` tạm đảm nhận, README). Agent và MCP server (`agents/`, `.mcp.json` để trống, README). Hook của plugin (README). Hỗ trợ riêng cho Claude Desktop (HDCĐ). Skill viết tài liệu cho cả repo (README). Code và dữ liệu của repo đích: thuộc người dùng, plugin chỉ đọc/ghi theo lệnh của họ. Nội dung 4 trang URL cho Directory: viết trên `blogs.nhquydev.net`, không thuộc repo này (HDNP). |
| **Giai đoạn** | Bản hiện hành: v1.2.0 (README). Phân phối qua marketplace riêng: đã dùng được (HDNP). Nộp Directory chính thức: chưa có mốc `[cần xác nhận: có nộp không, khi nào]`. |

## 2. Thuật ngữ

| Thuật ngữ | Nghĩa trong hệ mới |
|---|---|
| Plugin | Gói `nqdev` chứa skill và command, cài một lần dùng mọi dự án. |
| Marketplace | Danh sách plugin để Claude Code tải về. Repo này vừa là plugin vừa là marketplace `nqdev-marketplace`. |
| Skill | Bộ hướng dẫn cho agent, nằm ở `nqdev/skills/<tên>/SKILL.md`. Chạy được khi tự kích hoạt hoặc khi gọi rõ. |
| Slash command | Lệnh dạng `/nqdev:<tên>`, chỉ chạy trên Claude Code. |
| Tên đầy đủ | Dạng `/nqdev:<tên>` để gọi skill hoặc command của plugin. |
| Tự kích hoạt | Agent tự nạp skill khi yêu cầu của người dùng khớp `description` của skill. |
| Chỉ gọi rõ | Skill không tự kích hoạt; người dùng phải gõ tên. Dùng cho skill sửa code hoặc canvas. |
| Workflow | Chuỗi bước dựng sẵn do `nqdev-task-flow` điều phối. |
| Điểm duyệt | Chỗ workflow dừng lại chờ người dùng đồng ý trước khi sang bước sau. |
| Bàn giao | Workflow không tự chạy bước, mà đưa đúng lệnh để người dùng tự gõ. |
| Repo đích | Repo của người dùng mà plugin đang làm việc trong đó, khác với repo plugin này. |
| Scope cài | Phạm vi hiệu lực của plugin: `user`, `project`, `local`. |

## 3. Tác nhân

| Tác nhân | Là ai | Làm gì với module này |
|---|---|---|
| Người dùng (dev) | Dev dùng Claude Code trong repo của mình | Cài plugin, gọi skill/command, chạy workflow, duyệt từng bước, tự gõ lệnh sửa code và commit. |
| Thành viên nhóm | Dev cùng dự án với người dùng | Cài plugin theo scope `project` mà người dùng đã commit. |
| Owner plugin | Người giữ repo plugin | Thêm/sửa skill và command, tăng `version`, phát hành, nộp Directory. |
| Claude Code | Môi trường chạy chính | Tải marketplace, nạp skill/command, chặn tự gọi skill "chỉ gọi rõ". |
| Codex CLI, Gemini CLI | Môi trường chạy phụ | Đọc skill được copy thủ công; không đọc command, không đọc marketplace. |
| Jira Cloud | Hệ thống ngoài | Nhận truy vấn và cập nhật từ các command Jira, theo thông tin xác thực của người dùng. |
| Google Drive connector (claude.ai) | Hệ thống ngoài | Cho `tracker-gs-sync` đọc Google Sheet được share cho tài khoản người dùng. |
| Người duyệt Claude Plugin Directory | Anthropic | Quét tự động và duyệt listing lần đầu khi plugin được nộp. |

## 4. Yêu cầu nghiệp vụ

| Mã | Yêu cầu | Nguồn | Giai đoạn | Ghi chú |
|---|---|---|---|---|
| BR-NQDEV-001 | Người dùng cài được plugin bằng hai bước: thêm marketplace từ repo Git, rồi cài `nqdev@nqdev-marketplace`. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-002 | Lệnh thêm marketplace nhận bốn dạng nguồn: GitHub `owner/repo`, link `https://`, SSH, thư mục local. | HDCĐ | v1.1.0 | Hành vi của Claude Code, plugin chỉ cần đúng cấu trúc marketplace. |
| BR-NQDEV-003 | Người dùng chọn được scope cài `user`, `project` hoặc `local`. | HDCĐ | v1.1.0 | |
| BR-NQDEV-004 | Mỗi lần phát hành bản mới, `version` trong `plugin.json` phải tăng. | HDCĐ, HDNP | v1.1.0 | Người dùng chỉ nhận bản mới khi `version` tăng. |
| BR-NQDEV-005 | Plugin cung cấp 11 skill, mỗi skill gắn với một giai đoạn của flow coding hoặc vai trò điều phối. | README | v1.1.0 | |
| BR-NQDEV-006 | Plugin cung cấp 7 slash command cho quản lý plan, git, Jira và Google Sheet. | README | v1.1.0 | |
| BR-NQDEV-007 | Mọi skill và command gọi được bằng tên đầy đủ `/nqdev:<tên>`. | HDCĐ, README | v1.1.0 | Gọi tên ngắn chưa được tài liệu Claude Code xác nhận (HDCĐ). |
| BR-NQDEV-008 | Ba skill sửa code hoặc canvas (`nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-design-to-artifact`) chỉ chạy khi người dùng gọi rõ. | README, HDCĐ | v1.1.0 | Xem Câu hỏi mở #3 về `nqdev-init-agents`. |
| BR-NQDEV-009 | `nqdev-task-flow` cung cấp 4 workflow: `feature`, `bugfix`, `init`, `release`, với thứ tự bước như bảng ở README. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-010 | Mỗi lượt, workflow chạy đúng một bước rồi dừng chờ người dùng duyệt, kể cả khi test pass hay review không có vấn đề. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-011 | Workflow chỉ sang bước code khi file plan có `status: approved`. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-012 | Ở bước sửa code và bước commit, workflow không tự chạy mà đưa đúng lệnh để người dùng gõ. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-013 | Khi tự kích hoạt, `nqdev-task-flow` hỏi người dùng muốn chạy workflow hay làm trực tiếp trước khi làm bất cứ bước nào. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-014 | Người dùng quay lại workflow ở một bước cụ thể bằng `--from=<bước>`; không truyền `--from` thì workflow dò `docs/brd/`, `plans/`, `git status` để đề xuất bước bắt đầu. | README | v1.1.0 | |
| BR-NQDEV-015 | Các skill nối với nhau qua dữ liệu trong repo đích: `docs/brd/<module>.md` với mã `BR-`/`AC-`/`UC-`, `plans/<stt>-<YYYY-MM-DD>-<slug>.md`, `.claude/rules/code-rules.md` và `CLAUDE.md`. | README | v1.1.0 | Xem Câu hỏi mở #5. |
| BR-NQDEV-016 | `nqdev-init-agents` không ghi đè file đã có trong repo đích. | README | v1.1.0 | |
| BR-NQDEV-017 | Command có thể commit và push (`sync-git-ship`, `sync-status`) có cờ `--no-push` để người dùng kiểm tra trước khi đẩy code. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-018 | `sync-git-ship` chặn commit khi phát hiện secret trong thay đổi. | README | v1.1.0 | Cách phát hiện: Câu hỏi mở #8. |
| BR-NQDEV-019 | Command Jira dừng và báo đúng tên biến thiếu khi thiếu `JIRA_BASE_URL`, `JIRA_EMAIL` hoặc `JIRA_API_TOKEN`. | HDCĐ | v1.1.0 | |
| BR-NQDEV-020 | Command ghi lên Jira luôn hỏi người dùng trước khi ghi. | README | v1.1.0 | Áp dụng cho `sync-jira-status`, `tracker-jira-nqdev`. |
| BR-NQDEV-021 | Plugin không chứa sẵn thông tin đăng nhập, token hay domain riêng nào. | README, HDCĐ, HDNP | v1.1.0 | |
| BR-NQDEV-022 | `tracker-gs-sync` đọc Google Sheet qua connector Google Drive của claude.ai, chỉ với sheet đã được share cho tài khoản Google đó. | README | v1.1.0 | |
| BR-NQDEV-023 | Skill dùng được trên Codex CLI và Gemini CLI bằng cách copy thư mục skill; slash command không hỗ trợ trên hai CLI này. | README, HDCĐ | v1.1.0 | |
| BR-NQDEV-024 | Trên Codex CLI, skill "chỉ gọi rõ" kèm `agents/openai.yaml` đặt `allow_implicit_invocation: false`. | README | v1.1.0 | Xem Câu hỏi mở #4. |
| BR-NQDEV-025 | Tài liệu plugin xem được dạng web bằng Docsify khi phục vụ root repo. | README gốc | v1.1.0 | |
| BR-NQDEV-026 | `plugin.json` khai báo đủ trường Directory yêu cầu: `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, icon, và 4 URL `https://` (`documentationUrl`, `supportUrl`, `privacyPolicyUrl`, `termsOfServiceUrl`). | HDNP | Nộp Directory | |
| BR-NQDEV-027 | Bốn trang URL của Directory có nội dung thật và truy cập công khai trước khi nộp. | HDNP | Nộp Directory | Câu hỏi mở #2. |
| BR-NQDEV-028 | Tên plugin giữ cố định là `nqdev`; muốn đổi nhãn hiển thị thì sửa `displayName`. | HDNP | Nộp Directory | Directory không cho đổi tên sau khi publish. |

## 5. Luồng sử dụng

### UC-NQDEV-01 — Cài plugin từ GitHub

- **Tác nhân:** Người dùng (dev).
- **Điều kiện trước:** Đã cài và đăng nhập Claude Code, máy có Git, truy cập được repo (HDCĐ).
- **Luồng chính:** 1. Người dùng chạy `claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist`. 2. Claude Code clone branch `dist` của repo phát hành (chỉ chứa `.claude-plugin/`, `nqdev/`, `vhs/`, `README.md`, `LICENSE`) và đọc `marketplace.json`. 3. Người dùng chạy `claude plugin install nqdev@nqdev-marketplace`, có thể kèm `--scope project`. 4. Người dùng chạy `/reload-plugins`. 5. Người dùng kiểm tra bằng `claude plugin list`.
- **Ngoại lệ:** Gõ sai nguồn: Claude Code báo `Invalid marketplace source format`. Thiếu `@nqdev-marketplace`: báo `Plugin "nqdev" not found in any marketplace`. Repo private mà Git không xác thực được: báo `SSH/HTTPS authentication failed` (HDCĐ).
- **Kết quả:** `nqdev` xuất hiện trong danh sách plugin đã cài, gọi được `/nqdev:<tên>`.
- **Thoả BR:** BR-NQDEV-001, BR-NQDEV-002, BR-NQDEV-003, BR-NQDEV-007

### UC-NQDEV-02 — Làm tính năng mới bằng workflow `feature`

- **Tác nhân:** Người dùng (dev), Claude Code.
- **Điều kiện trước:** Plugin đã cài.
- **Luồng chính:** 1. Người dùng nói "tạo tính năng …" hoặc gõ `/nqdev:nqdev-task-flow feature <mô tả>`. 2. Nếu tự kích hoạt, workflow hỏi chạy workflow hay làm trực tiếp. 3. Workflow viết BRD rồi dừng chờ duyệt. 4. Sau khi duyệt, workflow ước lượng rồi dừng. 5. Workflow viết plan `status: todo` rồi dừng. 6. Người dùng duyệt, plan thành `status: approved`. 7. Workflow đưa lệnh `/nqdev:nqdev-feature-implementer plans/....md`, người dùng tự gõ. 8. Người dùng gõ `/nqdev:nqdev-task-flow feature --from=test`. Workflow chạy test, review, soạn mô tả MR, dừng sau mỗi bước. 9. Workflow đưa lệnh `/nqdev:sync-status --no-push` để người dùng tự chốt commit.
- **Ngoại lệ:** Người dùng chọn "Làm lại" ở bước plan: workflow sửa plan và hỏi lại, không sang bước code. Người dùng chọn làm trực tiếp ở bước 2: workflow không chạy. Không truyền `--from` khi quay lại: workflow dò `docs/brd/`, `plans/`, `git status` rồi đề xuất bước.
- **Kết quả:** Có BRD, plan `approved`, code do người dùng tự cho phép sửa, mô tả MR; chưa có commit nào nếu người dùng chưa gõ lệnh commit.
- **Thoả BR:** BR-NQDEV-009, BR-NQDEV-010, BR-NQDEV-011, BR-NQDEV-012, BR-NQDEV-013, BR-NQDEV-014, BR-NQDEV-015

### UC-NQDEV-03 — Chốt công việc và cập nhật Jira

- **Tác nhân:** Người dùng (dev), Jira Cloud.
- **Điều kiện trước:** Đã đặt `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` trước khi mở Claude Code (HDCĐ).
- **Luồng chính:** 1. Người dùng gõ `/nqdev:sync-status --no-push`. 2. Command cập nhật plan. 3. Command hỏi trước rồi mới ghi trạng thái hoặc comment lên Jira. 4. Command kiểm tra thay đổi, chặn nếu có secret, rồi commit. 5. Không push vì có `--no-push`.
- **Ngoại lệ:** Thiếu biến Jira: command dừng và báo tên biến thiếu. Phát hiện secret: không commit. Người dùng từ chối ghi Jira: không ghi.
- **Kết quả:** Plan và Jira khớp việc đã làm, có commit cục bộ, chưa push.
- **Thoả BR:** BR-NQDEV-017, BR-NQDEV-018, BR-NQDEV-019, BR-NQDEV-020, BR-NQDEV-021

### UC-NQDEV-04 — Nhận bản cập nhật

- **Tác nhân:** Người dùng (dev), Owner plugin.
- **Điều kiện trước:** Plugin đã cài từ marketplace.
- **Luồng chính:** 1. Owner tăng `version` trong `plugin.json` và push. 2. Người dùng chạy `claude plugin marketplace update nqdev-marketplace`. 3. Người dùng chạy `claude plugin update nqdev@nqdev-marketplace` rồi khởi động lại hoặc `/reload-plugins`.
- **Ngoại lệ:** Owner push mà không tăng `version`: người dùng không nhận bản mới. Repo private và credential helper cần hỏi mật khẩu: tự cập nhật chạy nền thất bại, bản cũ được giữ (HDCĐ).
- **Kết quả:** Người dùng chạy bản có `version` mới.
- **Thoả BR:** BR-NQDEV-004

### UC-NQDEV-05 — Dùng skill trên Codex CLI hoặc Gemini CLI

- **Tác nhân:** Người dùng (dev), Codex CLI hoặc Gemini CLI.
- **Điều kiện trước:** Đã clone repo plugin.
- **Luồng chính:** 1. Người dùng copy `nqdev/skills/*` vào `~/.agents/skills/` (Codex) hoặc `~/.gemini/skills/` (Gemini). 2. Mở lại CLI. 3. Gọi skill bằng `$<tên-skill>` (Codex), hoặc kiểm tra bằng `/skills list` (Gemini).
- **Ngoại lệ:** Người dùng thử gọi slash command: không chạy, vì command chỉ dành cho Claude Code. Skill không hiện: đường dẫn thư mục khác theo phiên bản CLI (HDCĐ).
- **Kết quả:** Skill chạy trên CLI đích; skill "chỉ gọi rõ" không tự kích hoạt trên Codex.
- **Thoả BR:** BR-NQDEV-023, BR-NQDEV-024

### UC-NQDEV-06 — Nộp plugin vào Claude Plugin Directory

- **Tác nhân:** Owner plugin, Người duyệt Claude Plugin Directory.
- **Điều kiện trước:** Tài khoản Claude trả phí, repo sẽ public trước khi publish (HDNP).
- **Luồng chính:** 1. Owner hoàn tất checklist trong HDNP. 2. Chạy `claude plugin validate . --strict`. 3. Vào portal, chọn Plugin bundle, nhập repo, bấm Validate. 4. Trả lời Data handling, Compliance. 5. Bấm Submit for review.
- **Ngoại lệ:** Validate lỗi: sửa rồi validate lại. Bị từ chối: đọc Requested changes, sửa, Resubmit (HDNP).
- **Kết quả:** Plugin có listing trên Directory.
- **Thoả BR:** BR-NQDEV-004, BR-NQDEV-026, BR-NQDEV-027, BR-NQDEV-028

## 6. Quy tắc nghiệp vụ

1. **Cú pháp cài:** luôn là `<tên plugin>@<tên marketplace>` = `nqdev@nqdev-marketplace`. Tên marketplace lấy từ trường `name` trong `marketplace.json`, không phải tên repo (HDCĐ).
2. **Thứ tự ưu tiên scope:** `local` ghi đè `project`, `project` ghi đè `user` (HDCĐ).
3. **Nhận bản mới:** plugin có đặt `version` chỉ được cập nhật khi `version` tăng. Riêng marketplace local thì chỉ cần `/reload-plugins` (HDCĐ).
4. **Chuyển trạng thái plan trong workflow:** `todo` → (người dùng chọn Duyệt) → `approved`. Chọn Làm lại thì plan vẫn ở `todo` và được sửa. Chỉ `approved` mới mở bước code (HDCĐ).
5. **Phân loại cách gọi skill:**
   - Chỉ gọi rõ: `nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-design-to-artifact`.
   - Tự kích hoạt có hỏi trước: `nqdev-task-flow`.
   - Còn lại: tự kích hoạt theo `description` hoặc gọi rõ (README).
6. **Những việc chỉ người dùng được làm:** sửa code ứng dụng, commit, push. Workflow chỉ bàn giao lệnh cho người dùng (HDCĐ).
7. **Tên plugin:** dạng kebab-case, không bắt đầu bằng `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-` (HDNP).
8. **Icon cho Directory:** PNG hoặc JPEG vuông, 512–2048 px mỗi cạnh, dưới 2 MB, không nhận SVG hay WebP. Chỉ được ghi nhận ở lần nộp đầu (HDNP).
9. **Giới hạn nộp Directory:** tối đa 10 submission trong 24 giờ cho mỗi tổ chức; mỗi cặp repo + thư mục chỉ có một submission (HDNP).

## 7. Tiêu chí nghiệm thu

| Mã | Cho (Given) | Khi (When) | Thì (Then) | Thoả BR |
|---|---|---|---|---|
| AC-NQDEV-001 | Máy có Claude Code và Git, chưa cài `nqdev` | Chạy `claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist` rồi `claude plugin install nqdev@nqdev-marketplace` | `claude plugin list` có dòng `nqdev`, cả hai lệnh kết thúc không lỗi | BR-NQDEV-001 |
| AC-NQDEV-002 | Một bản clone local của repo | Chạy `claude plugin marketplace add ./` trong thư mục clone | Marketplace `nqdev-marketplace` được thêm, không báo `Invalid marketplace source format` | BR-NQDEV-002 |
| AC-NQDEV-003 | Một repo dự án chưa có `.claude/settings.json` | Chạy `claude plugin install nqdev@nqdev-marketplace --scope project` | `.claude/settings.json` của dự án có khai báo bật plugin `nqdev` | BR-NQDEV-003 |
| AC-NQDEV-004 | Một commit phát hành có sửa skill hoặc command | Soát `nqdev/.claude-plugin/plugin.json` trước khi phát hành | `version` lớn hơn `version` của bản phát hành trước theo SemVer | BR-NQDEV-004 |
| AC-NQDEV-005 | Plugin v1.1.0 đã cài | Mở `/plugin`, tab Installed, xem chi tiết `nqdev` | Đếm được đúng 11 skill, khớp bảng ở README | BR-NQDEV-005 |
| AC-NQDEV-006 | Plugin v1.1.0 đã cài | Gõ `/nqdev:` trong phiên Claude Code | Gợi ý có đủ 7 command trong bảng ở README | BR-NQDEV-006 |
| AC-NQDEV-007 | Plugin đã cài | Gõ `/nqdev:nqdev-code-review` và `/nqdev:sync-status --no-push` | Cả hai được nạp và chạy, không báo không tìm thấy lệnh | BR-NQDEV-007 |
| AC-NQDEV-008 | Plugin đã cài, chưa gõ tên skill nào | Người dùng viết "sửa lỗi NullReferenceException ở hàm X" | `nqdev-bug-fixer` không được nạp tự động; chỉ chạy khi gõ `/nqdev:nqdev-bug-fixer` | BR-NQDEV-008 |
| AC-NQDEV-009 | Plugin đã cài | Gõ lần lượt `/nqdev:nqdev-task-flow feature …`, `bugfix …`, `init`, `release` | Mỗi lệnh khởi động đúng workflow; bước đầu tiên lần lượt là BRD, sửa bug, rule cho AI, review | BR-NQDEV-009 |
| AC-NQDEV-010 | Workflow `feature` đang chạy, bước BRD vừa xong | Lượt hiện tại kết thúc | Workflow dừng và hỏi duyệt; bước estimate chưa chạy | BR-NQDEV-010 |
| AC-NQDEV-011 | File plan có `status: todo` | Người dùng yêu cầu workflow sang bước code | Workflow không đưa lệnh `nqdev-feature-implementer`, và yêu cầu duyệt plan trước | BR-NQDEV-011 |
| AC-NQDEV-012 | Plan có `status: approved` | Workflow tới bước code | Workflow in lệnh `/nqdev:nqdev-feature-implementer plans/<file>.md`; `git status` của repo đích không đổi sau lượt đó | BR-NQDEV-012 |
| AC-NQDEV-013 | Plugin đã cài, không gõ lệnh workflow | Người dùng viết "tạo tính năng xuất Excel" | Câu trả lời đầu tiên là câu hỏi chọn chạy workflow hay làm trực tiếp; chưa có file nào được tạo | BR-NQDEV-013 |
| AC-NQDEV-014 | Repo đích có plan `approved` và đã có thay đổi code | Gõ `/nqdev:nqdev-task-flow feature` không kèm `--from` | Workflow đề xuất bước bắt đầu dựa trên `docs/brd/`, `plans/`, `git status`, và hỏi xác nhận trước khi chạy | BR-NQDEV-014 |
| AC-NQDEV-015 | Repo đích có `docs/brd/<module>.md` chứa `BR-<MODULE>-001` | Chạy `nqdev-merge-request-writer` cho một thay đổi thoả yêu cầu đó | Mô tả MR có mã `BR-<MODULE>-001` | BR-NQDEV-015 |
| AC-NQDEV-016 | Repo đích đã có `CLAUDE.md` | Chạy `/nqdev:nqdev-init-agents` | Nội dung `CLAUDE.md` giữ nguyên từng byte (so bằng `git diff`) | BR-NQDEV-016 |
| AC-NQDEV-017 | Repo đích có thay đổi chưa commit, có remote | Chạy `/nqdev:sync-git-ship --no-push` | Có commit cục bộ mới; nhánh trên remote không đổi | BR-NQDEV-017 |
| AC-NQDEV-018 | Thay đổi chưa commit có một file chứa token mẫu `[cần xác nhận: mẫu secret dùng để kiểm thử]` | Chạy `/nqdev:sync-git-ship --no-push` | Không có commit mới; command báo file chứa secret | BR-NQDEV-018 |
| AC-NQDEV-019 | Không đặt `JIRA_API_TOKEN`, hai biến còn lại có | Chạy `/nqdev:tracker-jira-nqdev menu` | Command dừng, thông báo có chuỗi `JIRA_API_TOKEN`; không gọi Jira | BR-NQDEV-019 |
| AC-NQDEV-020 | Đủ biến Jira, có một task cần chuyển trạng thái | Chạy `/nqdev:sync-jira-status` và trả lời "không" ở câu hỏi xác nhận | Trạng thái và comment của task trên Jira không đổi | BR-NQDEV-020 |
| AC-NQDEV-021 | Mã nguồn plugin ở bản phát hành | Quét `nqdev/skills/` và `nqdev/commands/` tìm token, mật khẩu, domain Atlassian thật, đường dẫn máy cá nhân | 0 kết quả | BR-NQDEV-021 |
| AC-NQDEV-022 | Connector Google Drive đã bật, có một sheet **chưa** share cho tài khoản đó | Chạy `/nqdev:tracker-gs-sync` với link sheet đó | Command báo không đọc được sheet; không tạo dữ liệu issue nào | BR-NQDEV-022 |
| AC-NQDEV-023 | Đã copy `nqdev/skills/*` vào `~/.agents/skills/` | Gọi `$nqdev-code-review` trên Codex CLI | Skill chạy; gọi `/nqdev:sync-status` trên Codex CLI không chạy | BR-NQDEV-023 |
| AC-NQDEV-024 | Đã copy `nqdev/skills/*` vào thư mục skill của Codex | Kiểm tra `nqdev-feature-implementer/agents/openai.yaml` | File tồn tại và có `allow_implicit_invocation: false` | BR-NQDEV-024 |
| AC-NQDEV-025 | Static server phục vụ root repo | Mở `/docs/` trên trình duyệt | Trang chủ hiện nội dung README.md; menu có 3 mục như `docs/_sidebar.md` | BR-NQDEV-025 |
| AC-NQDEV-026 | `plugin.json` ở bản định nộp | Chạy `claude plugin validate . --strict` và soát danh sách trường ở BR-NQDEV-026 | Lệnh không báo lỗi hay cảnh báo; có đủ các trường, 4 URL bắt đầu bằng `https://` | BR-NQDEV-026 |
| AC-NQDEV-027 | Trước ngày nộp | Mở 4 URL trong `plugin.json` bằng trình duyệt chưa đăng nhập | Cả 4 trả HTTP 200, có nội dung theo bảng ở HDNP | BR-NQDEV-027 |
| AC-NQDEV-028 | Một bản phát hành sau khi đã publish | So `name` trong `plugin.json` với bản đã publish | `name` vẫn là `nqdev` | BR-NQDEV-028 |

## 8. Dữ liệu

| Thực thể | Trường chính | Chứa PII? | Giữ bao lâu | Ghi chú |
|---|---|---|---|---|
| Thông tin xác thực Jira | Base URL, email, API token | Có (email); token là secret | Do người dùng giữ trong biến môi trường; plugin không lưu | Nguồn: HDCĐ. |
| Plan | Tiêu đề, `status` (`todo`, `approved`, …), các bước, trạng thái từng bước | Không | Theo repo đích | Nằm trong `plans/` của repo đích. |
| Tài liệu yêu cầu (BRD) | Module, mã BR/AC/UC, nguồn, trạng thái duyệt | Tuỳ nội dung người dùng đưa vào | Theo repo đích | Nằm trong `docs/brd/` của repo đích. |
| Ánh xạ sprint → link Google Sheet | Tên sprint, link sheet | Không | `[cần xác nhận: nơi lưu và thời hạn]` | Mô tả command `tracker-gs-sync` nói có lưu ánh xạ để dùng lại; README không nêu nơi lưu. |
| Thông tin listing Directory | Tên, mô tả, icon, 4 URL, email liên hệ | Có (email liên hệ ở bước Compliance) | Theo Anthropic | Nguồn: HDNP. |

## 9. Tích hợp với module khác

| Hướng | Module | Hợp đồng / sự kiện | Dùng để | Trạng thái |
|---|---|---|---|---|
| Cung cấp | Claude Code | `nqdev/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` (`source: "./nqdev"`) | Claude Code tải và nạp plugin | Đã có |
| Cung cấp | Codex CLI | `nqdev/skills/<tên>/agents/openai.yaml` | Đặt cách gọi skill trên Codex | Đã có |
| Cung cấp | Claude Plugin Directory | Các trường trong `plugin.json` và `README.md` (listing chỉ đọc từ hai file này, HDNP) | Hiện plugin trên Directory | Cần thêm: 4 trang URL chưa có nội dung |
| Dùng | Jira Cloud | REST API, xác thực bằng email và API token | Truy vấn và cập nhật issue | Đã có |
| Dùng | Google Drive connector (claude.ai) | Connector của claude.ai | Đọc Google Sheet tracker | Đã có |
| Dùng | Git remote của repo đích | `git commit`, `git push` | Chốt và đẩy thay đổi | Đã có |
| Phát sự kiện | | | | Không áp dụng: plugin không có hook hay hàng đợi sự kiện |
| Nghe sự kiện | | | | Không áp dụng: plugin không có hook (README) |

## 10. Đối chiếu hệ cũ

Plugin không thay thế một hệ thống khác. Phần dưới đây đối chiếu với các bản trước của chính plugin, theo các quyết định đã ghi trong lịch sử thay đổi.

| Hành vi của hệ cũ | Nguồn | Hệ mới | Căn cứ |
|---|---|---|---|
| Có skill `nqdev-codebase-analyst` viết tài liệu cho cả repo | README | Bỏ | Quyết định ngày 2026-11-16 ghi ở README |
| Liệt kê 6 skill chưa đưa vào plugin (`nqdev-system-design-diagram`, `nqdev-write-plan`, `nqdev-test-case-writer`, `nqdev-unit-test-generator`, `nqdev-skill-refactor`, `nqdev-slash-command-builder`) | README | Bỏ | Quyết định ở bản v1.0.2, README |
| `nqdev-client-requirement-insight` | README | Đổi: thành `nqdev-requirement-estimator` | Quyết định ngày 2026-11-16, README |
| `nqdev-drawio-diagram-creator` là skill riêng | README | Đổi: gộp vào `nqdev-system-design-diagram` (skill này hiện không có trong plugin) | README |
| `docs/readme.md` riêng | README | Đổi: gộp vào README.md | README |
| Không có workflow dựng sẵn | README | Đổi: thêm `nqdev-task-flow` với 4 workflow | Bản v1.1.0, README |

## 11. Yêu cầu phi chức năng

| Hạng mục | Yêu cầu | Nguồn |
|---|---|---|
| Sản lượng / độ trễ | Không áp dụng: plugin là văn bản hướng dẫn chạy trong Claude Code, không có server. | README |
| Tiền | Không áp dụng: plugin không xử lý thanh toán. | |
| Thông báo / gửi tin | Comment và chuyển trạng thái trên Jira chỉ diễn ra sau khi người dùng xác nhận (BR-NQDEV-020). Chống ghi trùng khi chạy lại command: `[cần xác nhận]`. | README |
| Bảo mật / PII | Không nhúng secret, token, domain riêng hay đường dẫn máy cá nhân vào skill/command. Quét lại trước mỗi lần nộp. Token Jira chỉ đọc từ biến môi trường. | README, HDNP |
| Kiểm soát của người dùng | Sửa code, commit, push luôn do người dùng tự gõ lệnh. Workflow dừng sau mọi bước. | README, HDCĐ |
| Tương thích | Claude Code (CLI và extension IDE) đầy đủ; Codex CLI và Gemini CLI chỉ skill; Claude Desktop chưa hỗ trợ riêng. | HDCĐ |
| Khai báo dữ liệu với Directory | Trả lời Data handling đúng sự thật: plugin không có server hay hook, nhưng command Jira và Google Sheet gọi dịch vụ ngoài theo cấu hình người dùng. | HDNP |
| Ngôn ngữ tài liệu | Tiếng Việt, giữ nguyên thuật ngữ kỹ thuật. | README, HDNP |

## 12. Câu hỏi mở

| # | Câu hỏi | Hỏi ai | Chặn BR nào |
|---|---|---|---|
| 1 | Có nộp Directory chính thức không, và mốc nào? | Owner plugin | BR-NQDEV-026, BR-NQDEV-027, BR-NQDEV-028 |
| 2 | Bốn trang trên `blogs.nhquydev.net` đã có nội dung và truy cập công khai chưa? | Owner plugin | BR-NQDEV-027 |
| 3 | `nqdev-init-agents` tạo file trong repo đích nhưng vẫn tự kích hoạt được, không có `openai.yaml`. Có xếp nó vào nhóm "chỉ gọi rõ" như BR-NQDEV-008 không? | Owner plugin | BR-NQDEV-008, BR-NQDEV-024 |
| 4 | README nói 4 skill có `openai.yaml` (gồm `design-to-artifact`, `nqdev-task-flow`), còn HDCĐ chỉ nêu 2 skill. Danh sách nào đúng để làm AC? | Owner plugin | BR-NQDEV-024 |
| 5 | `code-rules.md` do `nqdev-init-agents` sinh ra gợi ý dùng `/nqdev-write-plan`, nhưng skill này không có trong plugin (README). Plan trong repo đích lấy khuôn từ đâu? | Owner plugin | BR-NQDEV-015 |
| 6 | `nqdev-task-flow` chưa chạy thử trên Claude Code thật; chưa rõ một skill có nạp được skill khác không (README). Nếu không, bước "Gọi skill" thành "Bàn giao": có chấp nhận cho nghiệm thu không? | Owner plugin | BR-NQDEV-009, BR-NQDEV-010, BR-NQDEV-012 |
| 7 | `tracker-gs-sync` lưu ánh xạ sprint → link ở đâu và giữ bao lâu? | Owner plugin | BR-NQDEV-022 |
| 8 | `sync-git-ship` nhận diện secret theo quy tắc nào? Cần một mẫu secret giả để dùng trong AC-NQDEV-018. | Owner plugin | BR-NQDEV-018 |
| 9 | Chạy lại `sync-jira-status` cho cùng một việc có tạo comment trùng không? Có cần chống trùng? | Owner plugin | BR-NQDEV-020 |
| 10 | Quy tắc tạo skill (`.claude/rules/skill-authoring.md`) liệt kê Claude.ai là môi trường hỗ trợ, còn HDCĐ nói chưa hỗ trợ Claude Desktop. Claude.ai có thuộc phạm vi không? | Owner plugin | BR-NQDEV-023 |

## 13. Lịch sử thay đổi

- 2026-11-18 — Bản đầu, viết từ README.md và docs/ của plugin v1.1.0.
- 2026-11-18 — Cập nhật đường dẫn theo cấu trúc v1.2.0: plugin nằm trong `nqdev/`, `source: "./nqdev"`. Số dòng `README:<dòng>` đã dời theo `nqdev/README.md`. Không đổi BR nào.
- 2026-11-20 — UC cài plugin và AC-NQDEV-001 dùng `nqdev-storage/claude-plugin-nqdev#dist` (branch phát hành do `publish-dist.yml` đồng bộ từ `main`). Không đổi BR nào.
- 2026-11-20 — Đổi lệnh cài sang `nqdev-storage/claude-plugin-nqdev#dist`: `publish-dist.yml` đẩy bản phát hành vào `main` của repo public. Không đổi BR nào.
- 2026-11-20 — Đổi lại lệnh cài về `nqdev-storage/claude-plugin-nqdev#dist`: `publish-dist.yml` phát hành vào `dist` của repo public. Không đổi BR nào.
- 2026-11-20 — `dist` chỉ cập nhật khi có tag phát hành `vX.Y.Z` (không còn theo mỗi push `main`). Không đổi BR nào.
- 2026-11-20 — Làm gọn: bỏ số dòng trong mọi tham chiếu nguồn (đã lệch so với tài liệu hiện tại), chỉ giữ tên file. Không đổi BR/AC/UC nào.
