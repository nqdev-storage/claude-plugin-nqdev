# Hướng dẫn cài đặt và sử dụng plugin `nqdev` từ Git repo

> Cập nhật: 2026-11-27 · Plugin `nqdev` v2.7.1
> Repo: https://github.com/nqdev-storage/claude-plugin-nqdev
> Áp dụng cho **Claude Code** (CLI và extension IDE). Skill cũng dùng được trên Codex CLI và Gemini CLI, xem mục 9. Plugin này chưa hỗ trợ riêng cho Claude Desktop.

## 1. Cách hoạt động

Repo này là một **marketplace** (xem [.claude-plugin/marketplace.json](../.claude-plugin/marketplace.json)); plugin `nqdev` nằm trong thư mục [nqdev/](../nqdev/README.md). Vì vậy việc cài gồm **hai bước**:

1. **Thêm marketplace** từ repo Git: Claude Code clone repo về máy và đọc danh sách plugin.
2. **Cài plugin** `nqdev` từ marketplace đó.

Hai tên cần phân biệt:

| Tên | Giá trị | Dùng ở đâu |
|---|---|---|
| Tên marketplace | `nqdev-marketplace` | Phần sau dấu `@` khi cài |
| Tên plugin | `nqdev` | Phần trước dấu `@` khi cài |

Cú pháp cài luôn là `nqdev@nqdev-marketplace`. Tên marketplace lấy từ trường `name` trong `marketplace.json`, **không phải tên repo**.

## 2. Yêu cầu

- Đã cài **Claude Code** và đăng nhập được.
- Máy có **Git**.
- Truy cập được repo. Nếu repo đang private, xem mục 6.

## 3. Cài đặt

### 3.1. Cách nhanh nhất: từ GitHub

Chạy trong terminal (CLI):

```bash
# Bước 1: thêm marketplace từ repo GitHub
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist

# Bước 2: cài plugin
claude plugin install nqdev@nqdev-marketplace
```

Hoặc gõ trực tiếp trong phiên Claude Code:

```
/plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist
/plugin install nqdev@nqdev-marketplace
```

Sau khi cài, chạy `/reload-plugins` để áp dụng ngay trong phiên đang mở (hoặc khởi động lại Claude Code).

> **Branch `dist` của repo này chứa gì?** Chỉ các file cần cài: `.claude-plugin/`, `nqdev/`, `vhs/`, `README.md`, `LICENSE` (không có `plans/`, `docs/`, `.claude/`, `CLAUDE.md`).
>
> CI ([publish-dist.yml](../.github/workflows/publish-dist.yml)) cập nhật nó từ repo phát triển mỗi khi có tag phát hành `vX.Y.Z`. Cùng tag đó có ở repo này, nên dùng được với `#vX.Y.Z`.
>
> Đã cài theo lệnh cũ (không có `#dist`, hoặc `#main`): chạy `claude plugin marketplace remove nqdev-marketplace` rồi add lại bằng lệnh ở Bước 1. Plugin đã cài vẫn giữ tên `<plugin>@nqdev-marketplace`.

### 3.2. Các dạng nguồn Git khác

Lệnh `marketplace add` nhận nhiều dạng nguồn:

| Nguồn | Ví dụ |
|---|---|
| GitHub `owner/repo` | `nqdev-storage/claude-plugin-nqdev` |
| Link git đầy đủ (https) | `https://github.com/nqdev-storage/claude-plugin-nqdev.git` |
| SSH | `git@github.com:nqdev-storage/claude-plugin-nqdev.git` |
| Thư mục local (đã clone) | `./claude-plugin-nqdev` hoặc `D:/path/to/claude-plugin-nqdev` |

Lưu ý:
- Link `https://` phải ghi **đủ tiền tố** `https://`. Nếu viết thiếu, Claude Code hiểu nhầm là dạng `owner/repo` của GitHub và báo lỗi.
- Thư mục local phải bắt đầu bằng `./`, `../`, `/` hoặc `~`, và chứa `.claude-plugin/marketplace.json`.

### 3.3. Cài một phiên bản cố định (tag hoặc branch)

Thêm `#<ref>` vào sau nguồn để ghim vào tag hoặc branch. Mỗi bản phát hành có tag `vX.Y.Z` ở repo `nqdev-storage/claude-plugin-nqdev`:

```bash
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#vX.Y.Z
```

Repo `nqdev-storage/claude-plugin-nqdev` phát hành plugin qua branch `dist` (site tài liệu ở `gh-pages`).

Cần bản chưa phát hành thì dùng repo phát triển, nếu bạn có quyền truy cập: `nqdev-storage/claude-plugin-nqdev-develop#main`. Cách này tải cả repo, gồm `plans/`, `docs/`, `.claude/`.

> Không dùng cờ `--ref`: tài liệu của Claude Code không mô tả cờ này. Hãy dùng dạng `#<ref>` ở trên.

### 3.4. Cài từ bản clone local (phù hợp khi phát triển hoặc thử nghiệm)

```bash
git clone -b dist https://github.com/nqdev-storage/claude-plugin-nqdev.git
cd claude-plugin-nqdev

claude plugin marketplace add ./
claude plugin install nqdev@nqdev-marketplace
```

Với marketplace local, sau khi sửa file chỉ cần chạy `/reload-plugins`, không cần đổi `version`.

### 3.5. Thêm và cài trong một bước

Bản Claude Code mới có cờ `--marketplace` để gộp hai bước:

```bash
claude plugin install nqdev --marketplace nqdev-storage/claude-plugin-nqdev#dist
```

Cờ này cần Claude Code đủ mới (CLI từ v2.1.292, trong phiên từ v2.1.275). Nếu lệnh báo lỗi, dùng cách hai bước ở mục 3.1.

### 3.6. Chọn phạm vi cài (scope)

| Scope | Lưu ở | Dùng khi |
|---|---|---|
| `user` (mặc định) | `~/.claude/settings.json` | Dùng cho cá nhân, mọi dự án |
| `project` | `.claude/settings.json` (commit vào repo) | Cả nhóm cùng dùng trong một dự án |
| `local` | `.claude/settings.local.json` | Chỉ máy bạn, chỉ dự án này |

```bash
# Cài cho cả dự án
claude plugin install nqdev@nqdev-marketplace --scope project
```

Thứ tự ưu tiên: `local` ghi đè `project`, `project` ghi đè `user`. Khi chia sẻ cho nhóm, mỗi thành viên vẫn cần tự chạy lệnh cài trên máy mình.

### 3.7. Kiểm tra đã cài thành công

```bash
claude plugin list
claude plugin details nqdev
```

Trong phiên Claude Code, mở `/plugin` rồi chọn tab **Installed**. Nếu có lỗi nạp, xem tab **Errors**.

## 4. Sử dụng

### 4.1. Cách gọi

Skill và slash command của plugin có **tên đầy đủ** dạng `/<plugin>:<tên>`. Gõ `/` rồi tìm theo tên plugin:

```
/nqdev:sync-status
/nqdev:nqdev-code-review
```

Tài liệu chỉ ghi rõ dạng có tiền tố plugin. Việc gõ tên ngắn (không có `nqdev:`) có chạy hay không chưa được tài liệu xác nhận, nên hãy dùng dạng đầy đủ để chắc chắn.

Skill còn **tự kích hoạt** khi yêu cầu của bạn khớp phần `description` của skill. Nhiều khi chỉ cần mô tả công việc bằng lời, ví dụ: "estimate tài liệu này mất bao lâu", "review giúp đoạn này".

Bốn skill `nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-unit-test-generator`, `nqdev-design-to-artifact` **không tự kích hoạt** vì có sửa code, thêm file test hoặc ghi canvas. Phải gọi rõ bằng tên.

`nqdev-task-flow` tự kích hoạt khi bạn yêu cầu tính năng mới, sửa bug, chuẩn bị release hay khởi tạo dự án. Ví dụ, chỉ cần gõ "tạo tính năng xuất Excel". Skill luôn hỏi trước bạn muốn chạy workflow hay làm trực tiếp.

Để chắc chắn hơn, chạy `/nqdev:nqdev-task-flow init` một lần trong repo. File `code-rules.md` sinh ra có quy tắc nhắc Claude đề xuất workflow.

### 4.2. Workflow dựng sẵn (nên bắt đầu từ đây)

Skill `nqdev-task-flow` nối các skill thành 4 workflow. **Mỗi lượt chạy đúng một bước rồi dừng chờ bạn duyệt**; không bước nào tự đi tiếp, kể cả khi test pass hay review không có vấn đề:

| Lệnh | Workflow |
|---|---|
| `/nqdev:nqdev-task-flow feature <mô tả tính năng>` | BRD → estimate → thiết kế UI (tuỳ chọn) → plan → code → test → review → MR → chốt |
| `/nqdev:nqdev-task-flow bugfix <thông báo lỗi>` | sửa bug → test → review → MR → chốt |
| `/nqdev:nqdev-task-flow init [mô tả dự án]` | rule cho AI → BRD → estimate |
| `/nqdev:nqdev-task-flow release [v1.2.0..HEAD]` | review → release note → chốt |

Ví dụ một vòng `feature`:

1. `/nqdev:nqdev-task-flow feature thêm xuất Excel danh sách khách hàng`: workflow viết BRD rồi dừng, hỏi bạn duyệt. Duyệt xong mới chạy estimate, rồi lại dừng hỏi chốt scope.
2. Workflow viết plan (`status: todo`) rồi dừng. Bạn đọc plan: chọn **Duyệt** thì plan đổi thành `status: approved`; chọn **Làm lại** kèm góp ý thì workflow sửa plan và hỏi lại.
3. Chỉ khi plan đã `approved`, workflow mới đưa lệnh `/nqdev:nqdev-feature-implementer plans/....md`. Bạn gõ lệnh đó.
4. Code xong, gõ `/nqdev:nqdev-task-flow feature --from=test`. Workflow cho bạn xem lại phần code đã đổi, rồi chạy test, review, soạn mô tả MR; mỗi bước đều dừng chờ duyệt.
5. Cuối cùng workflow đưa lệnh `/nqdev:sync-status --no-push` để bạn tự chốt commit.

Workflow không tự commit hay push, và mặc định không tự sửa code ứng dụng: các bước đó do bạn gõ lệnh.

Ngoại lệ là **plan lớn**: từ 10 bước, hoặc ước lượng từ 40h, hoặc có bước chạy song song. Sau khi bạn duyệt plan và bảng giao việc, bước `code` chạy **theo lô**:

- Tối đa 3 bước một lô, giao cho các agent khai báo trong `.claude/assign-tasks/<tên plan>.jsonl`.
- Workflow dừng chờ bạn duyệt sau mỗi lô.
- Cần tool có subagent (như Claude Code). Không có thì workflow bàn giao từng bước như trên.

### 4.3. Skills (14)

| Skill | Dùng khi bạn muốn | Ví dụ yêu cầu |
|---|---|---|
| `nqdev-brd-prd-writer` | Viết BRD theo module vào `docs/brd/` | "Viết BRD cho module đặt hàng từ ghi chú họp này" |
| `nqdev-requirement-estimator` | Ước lượng theo giờ (AI làm, DEV review), chia module, rủi ro | "Estimate tài liệu yêu cầu này mất bao lâu?" |
| `nqdev-design-to-artifact` | Thiết kế màn hình UI, dựng prototype bấm thử được | `/nqdev:nqdev-design-to-artifact màn hình đăng nhập` |
| `nqdev-init-agents` | Khởi tạo CLAUDE.md, `.claudeignore`, rules cho dự án | "Init agents cho repo này" |
| `nqdev-feature-implementer` | Code tính năng theo plan và BRD | `/nqdev:nqdev-feature-implementer plans/001-2026-11-17-dat-hang.md` |
| `nqdev-bug-fixer` | Sửa bug có thông báo lỗi hoặc stack trace | `/nqdev:nqdev-bug-fixer <dán stack trace>` |
| `nqdev-write-plan` | Ghi execution plan hoặc nhật ký công việc vào `plans/` | "Viết plan cho tính năng xuất Excel" |
| `nqdev-test-case-writer` | Sinh test case thủ công từ AC trong BRD | "Viết test case cho module billing" |
| `nqdev-unit-test-generator` | Viết unit/integration test cho code có sẵn | `/nqdev:nqdev-unit-test-generator src/billing/InvoiceCalculator.cs` |
| `nqdev-code-review` | Review diff, MR hoặc nhóm file | "Review giúp thay đổi trên nhánh này" |
| `nqdev-merge-request-writer` | Soạn commit message, mô tả MR/PR | "Soạn mô tả merge request cho nhánh này" |
| `nqdev-release-note-writer` | Soạn release note và checklist deploy | "Soạn release note từ v1.2.0 đến v1.3.0" |
| `nqdev-business-flow-extractor` | Trích xuất luồng nghiệp vụ từ code | "Trích xuất luồng nghiệp vụ thanh toán" |
| `nqdev-task-flow` | Chạy một workflow dựng sẵn (mục 4.2) | `/nqdev:nqdev-task-flow bugfix <thông báo lỗi>` |

### 4.4. Slash commands (7)

| Slash command | Công dụng | Ví dụ |
|---|---|---|
| `/nqdev:nqdev-cmd-plans-cleanup` | Dọn nội dung trùng lặp và frontmatter mâu thuẫn trong `plans/` | `/nqdev:nqdev-cmd-plans-cleanup` |
| `/nqdev:sync-plan-status` | Cập nhật trạng thái các file plan theo việc đã làm | `/nqdev:sync-plan-status` |
| `/nqdev:sync-git-ship` | Kiểm tra thay đổi, commit kiểu conventional và push; chặn commit secret | `/nqdev:sync-git-ship --no-push` |
| `/nqdev:sync-jira-status` | Cập nhật trạng thái Jira theo công việc đã làm | `/nqdev:sync-jira-status` |
| `/nqdev:sync-status` | Chốt công việc: cập nhật plan, Jira, commit và push | `/nqdev:sync-status --no-push` |
| `/nqdev:tracker-jira-nqdev` | Truy vấn Jira Cloud qua REST API | `/nqdev:tracker-jira-nqdev menu` |
| `/nqdev:tracker-gs-sync` | Đồng bộ và lọc issue từ Google Sheet theo sprint | `/nqdev:tracker-gs-sync menu` |

Mỗi slash command có `argument-hint` riêng. Gõ slash command để xem gợi ý tham số.

> **Cẩn thận:** `/nqdev:sync-git-ship` và `/nqdev:sync-status` có thể **commit và push** code. Dùng cờ `--no-push` khi muốn kiểm tra trước, và đọc kỹ danh sách thay đổi trước khi xác nhận.

### 4.5. Cấu hình bắt buộc cho các slash command Jira

Ba slash command `tracker-jira-nqdev`, `sync-jira-status`, `sync-status` cần ba biến môi trường. Plugin **không** chứa sẵn thông tin đăng nhập hay domain nào.

| Biến | Ý nghĩa |
|---|---|
| `JIRA_BASE_URL` | Ví dụ `https://<your-domain>.atlassian.net` |
| `JIRA_EMAIL` | Email tài khoản Atlassian |
| `JIRA_API_TOKEN` | API token tạo tại https://id.atlassian.com/manage-profile/security/api-tokens |

Đặt biến trước khi mở Claude Code.

PowerShell (Windows), cho phiên hiện tại:

```powershell
$env:JIRA_BASE_URL = "https://<your-domain>.atlassian.net"
$env:JIRA_EMAIL = "you@example.com"
$env:JIRA_API_TOKEN = "<token>"
```

Bash (macOS/Linux):

```bash
export JIRA_BASE_URL="https://<your-domain>.atlassian.net"
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="<token>"
```

Thiếu biến nào, slash command sẽ dừng và báo rõ biến thiếu. Không commit token vào repo.

### 4.6. Plugin `vhs` (cài thêm, tuỳ chọn)

Cùng marketplace còn có plugin `vhs` (ViHAT) với 2 skill, cài độc lập với `nqdev`:

```bash
claude plugin install vhs@nqdev-marketplace
```

| Skill | Gọi | Dùng khi |
|---|---|---|
| `trietnm-prompt-tuner` | `/vhs:trietnm-prompt-tuner <prompt thô>` | Muốn tinh chỉnh một prompt thô theo đúng lĩnh vực trước khi chạy |
| `trietnm-user-doc-writer` | `/vhs:trietnm-user-doc-writer help \| plan \| full \| module <tên>` | Viết tài liệu hướng dẫn sử dụng cho người dùng cuối từ source code |

Chi tiết: [vhs/README.md](../vhs/README.md). Cập nhật và gỡ giống mục 5, thay `nqdev` bằng `vhs`.

## 5. Cập nhật, tắt, gỡ

### 5.1. Cập nhật lên bản mới

```bash
# Làm mới danh sách từ Git
claude plugin marketplace update nqdev-marketplace

# Cập nhật plugin (cần khởi động lại để áp dụng)
claude plugin update nqdev@nqdev-marketplace
```

Trong phiên: mở `/plugin`, vào tab **Installed**, chọn plugin rồi **Update now**. Sau đó chạy `/reload-plugins`.

Chi tiết cần biết:
- Với marketplace của bên thứ ba như repo này, **tự cập nhật mặc định đang tắt**. Bạn có thể bật trong `/plugin` → **Marketplaces** → chọn marketplace → **Enable auto-update**.
- Không có lệnh cập nhật tất cả plugin cùng lúc.
- Plugin có đặt `version` thì **chỉ cập nhật khi `version` được tăng**. Nếu bạn là người phát hành bản mới, hãy tăng `version` trong `plugin.json` ở mỗi lần release.

### 5.2. Tắt và bật

```bash
claude plugin disable nqdev@nqdev-marketplace
claude plugin enable nqdev@nqdev-marketplace
```

### 5.3. Gỡ plugin và marketplace

```bash
# Gỡ plugin
claude plugin uninstall nqdev@nqdev-marketplace

# Gỡ plugin ở scope project
claude plugin uninstall nqdev@nqdev-marketplace --scope project

# Gỡ cả marketplace (sẽ gỡ luôn mọi plugin cài từ nó)
claude plugin marketplace remove nqdev-marketplace
```

## 6. Repo private

Nếu repo `nqdev-storage/claude-plugin-nqdev` chưa public hoặc bạn dùng bản fork private, Claude Code dùng **thông tin xác thực Git sẵn có của máy**:

- **HTTPS:** credential helper của Git phải hoạt động, ví dụ `gh auth login` rồi `gh auth setup-git`. Lệnh Git không được hỏi mật khẩu tương tác.
- **SSH:** host phải có trong `known_hosts` và khoá phải dùng được mà **không hỏi passphrase** (ví dụ khoá đã nạp vào `ssh-agent`).
- **Chỉ đặt biến `GITHUB_TOKEN`:** không đủ để xác thực. Token chỉ có tác dụng khi đi qua credential helper như helper của `gh` CLI.
- Tự cập nhật chạy nền sẽ **thất bại âm thầm** nếu helper cần hỏi mật khẩu. Khi đó bản cũ vẫn được giữ.

Có thể kiểm tra nhanh quyền truy cập:

```bash
git ls-remote https://github.com/nqdev-storage/claude-plugin-nqdev.git
```

## 7. Chia sẻ cho cả nhóm trong một dự án

Chạy một lần trong thư mục dự án, rồi commit file `.claude/settings.json` được tạo ra:

```bash
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist --scope project
claude plugin install nqdev@nqdev-marketplace --scope project
```

- Marketplace sẽ được đăng ký cho các thành viên khi họ tin cậy thư mục dự án.
- Plugin chỉ bật trong `.claude/settings.json` **không tự tải về** máy thành viên. Tab **Errors** sẽ báo `Plugin "nqdev" is enabled in project settings but isn't installed here`.
- Mỗi người cần chạy `claude plugin install nqdev@nqdev-marketplace --scope project`.

## 8. Xử lý sự cố

| Triệu chứng | Nguyên nhân và cách xử lý |
|---|---|
| `Plugin "nqdev" not found in marketplace "nqdev-marketplace"` | Danh sách cũ hoặc gõ sai tên. Chạy `claude plugin marketplace update nqdev-marketplace` rồi thử lại. Kiểm tra đúng cú pháp `nqdev@nqdev-marketplace`. |
| `Plugin "nqdev" not found in any marketplace` | Thiếu phần `@nqdev-marketplace`, hoặc chưa thêm marketplace. |
| `Marketplace 'nqdev-marketplace' not found` | Chưa chạy `marketplace add`. Thêm marketplace trước. |
| `Invalid marketplace source format. Try: owner/repo, https://..., or ./path` | Viết sai nguồn. Link `https://` phải đủ tiền tố. |
| `SSH authentication failed` / `HTTPS authentication failed` | Lỗi xác thực Git. Xem mục 6. Thử `ssh -T git@github.com` hoặc `git ls-remote <url>`. |
| Cài xong nhưng không thấy skill/slash command | Chạy `/reload-plugins`. Mở `/plugin` → tab **Errors** để xem lỗi nạp. |
| Slash command Jira báo thiếu biến | Đặt đủ `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (mục 4.5), rồi mở lại Claude Code. |
| Gõ `claude plugin add` bị lỗi | Không có lệnh này. Dùng `claude plugin marketplace add` hoặc `claude plugin install`. |
| Gõ `--project` bị lỗi | Đúng cờ là `--scope project`. |

Chạy lại `/reload-plugins` sau mỗi lần sửa cấu hình. Nếu tải về bị hỏng, gỡ marketplace rồi thêm lại.

## 9. Dùng skill trên Codex CLI và Gemini CLI

Hai CLI này không đọc được marketplace của Claude Code, nên cần copy thư mục skill vào nơi mỗi CLI tìm skill. **Chỉ skill dùng được.**

7 slash command trong `nqdev/commands/` là định dạng riêng của Claude Code, không chạy trên hai CLI này.

Bước chung: clone repo.

```bash
git clone -b dist https://github.com/nqdev-storage/claude-plugin-nqdev.git
```

### 9.1. Codex CLI

Copy từng thư mục skill vào thư mục skill của Codex, cấp user (dùng mọi dự án) hoặc cấp dự án:

```bash
# Cấp user
mkdir -p ~/.agents/skills
cp -r claude-plugin-nqdev/nqdev/skills/* ~/.agents/skills/

# Hoặc cấp dự án (chạy ở root dự án)
mkdir -p .agents/skills
cp -r /path/to/claude-plugin-nqdev/nqdev/skills/* .agents/skills/
```

Gọi skill bằng `$<tên-skill>`, ví dụ `$nqdev-code-review`.

Bốn skill `nqdev-feature-implementer`, `nqdev-bug-fixer`, `nqdev-unit-test-generator` và `nqdev-design-to-artifact` có `agents/openai.yaml` đặt `allow_implicit_invocation: false`.

Vì vậy Codex chỉ chạy bốn skill này khi bạn gọi rõ.

### 9.2. Gemini CLI

```bash
# Cấp user
mkdir -p ~/.gemini/skills
cp -r claude-plugin-nqdev/nqdev/skills/* ~/.gemini/skills/

# Hoặc cấp dự án
mkdir -p .gemini/skills
cp -r /path/to/claude-plugin-nqdev/nqdev/skills/* .gemini/skills/
```

Mở lại Gemini CLI, chạy `/skills list` để kiểm tra.

### 9.3. Lưu ý

- Đường dẫn thư mục skill có thể khác giữa các phiên bản CLI. Nếu skill không hiện ra, kiểm tra tài liệu của phiên bản bạn đang dùng.
- Khi repo có bản mới, `git pull` rồi copy lại. Copy không tự cập nhật như marketplace của Claude Code.
- Trên Windows (PowerShell), thay `~` bằng `$HOME` và dùng `Copy-Item -Recurse`.
- `nqdev-design-to-artifact` trên hai CLI này chỉ dựng file ở local, không publish lên Artifact.

## 10. Tài liệu liên quan

- [README.md](../README.md): tổng quan plugin
- [docs/huong-dan-nop-plugin.md](huong-dan-nop-plugin.md): hướng dẫn nộp plugin lên Directory
- Claude Code: [Discover plugins](https://code.claude.com/docs/en/discover-plugins), [Plugins](https://code.claude.com/docs/en/plugins), [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
