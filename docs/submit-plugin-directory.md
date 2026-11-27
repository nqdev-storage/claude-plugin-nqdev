# Thông tin submit plugin `nqdev` lên Claude Plugin Directory

> Soạn: 2026-11-20, cập nhật phiên bản: 2026-11-27 · Plugin `nqdev` v2.7.1 · Form: <https://claude.ai/directory/manage/new/plugin>\
> Các trường dưới đây đoán theo form tại thời điểm soạn (trang cần đăng nhập, chưa xem trực tiếp), cần đối chiếu form thật.
>
> Các bước, điều kiện và cách xử lý sau khi nộp: [Hướng dẫn nộp plugin](huong-dan-nop-plugin.md).

Theo [hướng dẫn nộp plugin](huong-dan-nop-plugin.md) (mục 3.4), phần **Listing details** của portal là chỉ đọc, lấy từ `nqdev/.claude-plugin/plugin.json` và `nqdev/README.md`.

Muốn đổi nội dung listing thì sửa hai file đó rồi validate lại. Mục 2 bên dưới dùng để đối chiếu, không phải gõ tay.

## 1. Source

| Trường | Giá trị |
|---|---|
| Submission type | Plugin bundle |
| Repository | `nqdev-storage/claude-plugin-nqdev` |
| Plugin path | `nqdev` |
| Branch or tag | `dist` (repo public chỉ có branch `dist` và `gh-pages`, không có `main`) |

## 2. Listing (đối chiếu với `plugin.json`)

| Trường | Giá trị |
|---|---|
| Name | `nqdev` (không đổi được sau khi publish) |
| Display name | NQDev Toolkit |
| Version | 2.7.1 |
| Author | Nguyễn Quý |
| License | Apache-2.0 |
| Repository / Homepage | https://github.com/nqdev-storage/claude-plugin-nqdev |
| Documentation URL | https://blogs.nhquydev.net/claude-plugin-nqdev/ |
| Support URL | https://blogs.nhquydev.net/claude-plugin-nqdev/support/ |
| Privacy policy URL | https://blogs.nhquydev.net/claude-plugin-nqdev/privacy-policy/ |
| Terms of service URL | https://blogs.nhquydev.net/claude-plugin-nqdev/terms-of-service/ |
| Icon | `nqdev/.claude-plugin/icon.png`, PNG 1024×1024, 185 KB (chỉ ghi nhận ở lần nộp đầu) |
| Keywords | nqdev, skills, commands, workflow, brd, estimation, code-review, release-notes, documentation, jira, git, vietnamese |

### Mô tả ngắn

**EN** (128 ký tự):

> Skills and slash commands covering the full coding flow, with 4 built-in workflows: new feature, bug fix, project init, release.

**VI** (117 ký tự):

> Bộ skill và slash command theo flow coding, kèm 4 workflow dựng sẵn: tính năng mới, sửa bug, khởi tạo dự án, release.

`description` hiện tại trong `plugin.json` chỉ có tiếng Việt (khoảng 300 ký tự). Nếu muốn listing có tiếng Anh, cần sửa `description` trong `plugin.json` (và `marketplace.json` cho khớp).

### Mô tả dài

**EN:**

> NQDev Toolkit packages 14 skills and 7 slash commands that follow a coding flow from requirements to release.
>
> - **Built-in workflows** (`/nqdev:nqdev-task-flow feature | bugfix | init | release`): each run does one step and stops for your approval. A plan must be marked `approved` before coding starts. For code edits and commits the workflow hands you the exact command to run instead of running it itself.
> - **Requirements and planning:** BRD writer with BR/AC/UC traceability, hour-based estimation, execution plans in `plans/`.
> - **Design and setup:** local UI screen design, `CLAUDE.md` and AI agent rules for a repository.
> - **Code and test:** feature implementer, bug fixer, test cases from acceptance criteria, unit/integration test generator.
> - **Review and release:** code review, commit and MR/PR description writer, release notes with deploy checklist, business-flow extraction from code.
> - **Sync commands:** update plan status, Jira and Google Sheet trackers, and git commit/push, all triggered only by the user.
>
> Skills are written in Vietnamese and also work on Codex CLI and Gemini CLI; slash commands are Claude Code only.

**VI:**

> NQDev Toolkit gồm 14 skill và 7 slash command theo flow coding, từ thu thập yêu cầu tới phát hành.
>
> - **Workflow dựng sẵn** (`/nqdev:nqdev-task-flow feature | bugfix | init | release`): mỗi lượt chạy một bước rồi dừng chờ bạn duyệt. Plan phải được đánh dấu `approved` mới tới bước code. Ở bước sửa code và commit, workflow đưa đúng lệnh để bạn tự gõ thay vì tự chạy.
> - **Yêu cầu và kế hoạch:** viết BRD có mã truy vết BR/AC/UC, ước lượng theo giờ, execution plan trong `plans/`.
> - **Thiết kế và setup:** thiết kế màn hình UI ở local, tạo `CLAUDE.md` và rule cho AI agent trong repo.
> - **Code và test:** code tính năng, sửa bug, sinh test case từ tiêu chí nghiệm thu, viết unit/integration test.
> - **Review và phát hành:** review code, soạn commit message và mô tả MR/PR, release note kèm checklist deploy, trích xuất luồng nghiệp vụ từ code.
> - **Command đồng bộ:** cập nhật trạng thái plan, tracker Jira và Google Sheet, commit/push git; tất cả chỉ chạy khi người dùng gọi.
>
> Skill viết bằng tiếng Việt, dùng được cả trên Codex CLI và Gemini CLI; slash command chỉ chạy trên Claude Code.

### Lệnh cài đặt

```bash
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist
claude plugin install nqdev@nqdev-marketplace
```

### Danh sách skill và slash command

Skill (14): `nqdev-brd-prd-writer`, `nqdev-requirement-estimator`, `nqdev-design-to-artifact`, `nqdev-init-agents`, `nqdev-write-plan`, `nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-test-case-writer`, `nqdev-unit-test-generator`, `nqdev-code-review`, `nqdev-merge-request-writer`, `nqdev-release-note-writer`, `nqdev-business-flow-extractor`, `nqdev-task-flow`.

Slash command (7): `nqdev-cmd-plans-cleanup`, `sync-git-ship`, `sync-jira-status`, `sync-plan-status`, `sync-status`, `tracker-gs-sync`, `tracker-jira-nqdev`.

Chi tiết từng skill: [nqdev/README.md](../nqdev/README.md).

## 3. Data handling

Plugin chỉ gồm skill và slash command dạng Markdown: không có MCP server (`nqdev/.mcp.json` rỗng), không có hook, không có agent. Một số slash command gọi dịch vụ ngoài bằng thông tin người dùng tự cấu hình.

| Tích hợp | Dùng ở | Cấu hình | Hành vi |
|---|---|---|---|
| Jira (REST API) | `tracker-jira-nqdev`, `sync-jira-status`, `sync-status` | `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` | Đọc issue, chuyển trạng thái, comment, tạo issue |
| Google Sheet | `tracker-gs-sync` | Link sheet theo sprint do người dùng cung cấp | Đọc và lọc issue |
| Git remote | `sync-git-ship`, `sync-status` | Remote của repo người dùng | `git add`, commit, push |

**Plugin có đọc hoặc lưu dữ liệu cá nhân không? / Does the plugin read or store personal data?**

- EN: No data is collected by the plugin author. The Jira and Google Sheet commands read issue data (which may include assignee names) from services the user configures, only when the user runs them. Nothing is stored outside the user's own repository and services.
- VI: Tác giả plugin không thu thập dữ liệu nào. Command Jira và Google Sheet đọc dữ liệu issue (có thể gồm tên người được giao việc) từ dịch vụ do người dùng cấu hình, chỉ khi người dùng chạy. Không lưu dữ liệu ra ngoài repo và dịch vụ của chính người dùng.

**Có gửi dữ liệu tới dịch vụ khác ngoài connector đã khai báo không? / Is data sent to services other than declared connectors?**

- EN: Yes, only on explicit user commands: Jira REST API at the user's `JIRA_BASE_URL`, the user's Google Sheet, and the user's git remote. No other endpoints, no telemetry.
- VI: Có, chỉ khi người dùng gọi command: Jira REST API tại `JIRA_BASE_URL` của người dùng, Google Sheet của người dùng và git remote của repo. Không có endpoint nào khác, không có telemetry.

**Giữ dữ liệu bao lâu? / Data retention?**

- EN: The plugin keeps no data. Files it writes (`docs/brd/`, `plans/`, test files, etc.) live in the user's repository under the user's control.
- VI: Plugin không giữ dữ liệu. File được ghi ra (`docs/brd/`, `plans/`, file test...) nằm trong repo của người dùng, người dùng toàn quyền quản lý.

**Có dành cho người dưới 18 tuổi không? / Directed at users under 18?**

- EN/VI: No / Không. Plugin dành cho lập trình viên.

## 4. Compliance

| Trường | Giá trị |
|---|---|
| Contact email | [cần xác nhận: email liên hệ công khai, không dùng email cá nhân nếu không muốn lộ] |
| Bốn mục xác nhận | Đọc kỹ Anthropic Software Directory Terms và Software Directory Policy trước khi tick |

## 5. Review and submit

| Trường | Gợi ý |
|---|---|
| Auto-publish passing versions | [cần xác nhận: bật nếu muốn bản qua kiểm tra tự động lên luôn] |
| How new versions reach the directory | GitHub push webhook: workflow `publish-dist.yml` push branch `dist` mỗi lần đẩy tag `v*`, nên mỗi lần phát hành sẽ tự được nhận |

## 6. Checklist trước khi submit

Kiểm tra ngày 2026-11-20. Đây là ảnh chụp tại thời điểm đó, chưa kiểm lại: các dòng về HTTP 404, version trên `dist` và tag ở repo public có thể đã đổi, cần kiểm lại trước khi nộp.

- [x] `claude plugin validate ./nqdev --strict` pass (portal còn quét bảo mật và duyệt policy riêng)
- [x] Icon PNG vuông 1024×1024, 185 KB (yêu cầu 512–2048 px, dưới 2 MB)
- [x] Branch `dist` ở repo public có `nqdev/.claude-plugin/plugin.json` version 2.5.0, đủ 4 URL
- [ ] ❌ 4 URL Directory đều trả **HTTP 404**: documentation, support, privacy-policy, terms-of-service trên `blogs.nhquydev.net`. Phải publish đủ 4 trang trước khi nộp
- [ ] `plugin.json` đã lên `2.6.0` (lớn hơn tag `v2.5.1` đang có ở repo public); cần đẩy tag `v2.6.0` để `dist` có bản mới trước khi nộp
- [ ] `description` trong `plugin.json` chỉ có tiếng Việt. Quyết định có thêm tiếng Anh không (xem mục 2)
- [ ] Email liên hệ (mục 4)
- [ ] Đối chiếu các trường trong file này với form thật trên portal
