# nqdev-merge-request-writer

Viết commit message và mô tả merge request/pull request từ diff và lịch sử commit, theo quy ước và template của repo, kèm mã BR/AC liên quan và cách kiểm thử.

- **Phiên bản:** 1.0.2 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- "Soạn commit message", "viết mô tả merge request", "tóm tắt thay đổi để tạo PR".
- Muốn người review hiểu thay đổi làm gì, vì sao, kiểm thế nào và rủi ro ở đâu mà không cần hỏi lại.

Không dùng để review code (`nqdev-code-review`) hay viết release note (`nqdev-release-note-writer`).

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Chế độ `commit` (thay đổi đang staged, hoặc chưa commit nếu chưa stage gì) hoặc `mr` (toàn bộ nhánh so với nhánh gốc). Skill đọc thay đổi bằng lệnh git chỉ đọc (`git status`, `git diff`, `git log`). Tuỳ chọn: `--base=<nhánh gốc>` (không truyền thì dò nhánh mặc định), `--brd`, `--plan` (nguồn lấy mã BR/AC và lý do; không truyền thì tự tìm mã `BR-`/`AC-` trong commit, tên nhánh, `plans/`) |
| **Đầu ra** | Văn bản hoàn chỉnh trong khối code để chép nguyên văn: tiêu đề và thân MR (hoặc commit message), kèm tối đa 5 dòng nêu quy ước đã áp dụng, các chỗ `[cần xác nhận]` và cảnh báo (diff lẫn việc không liên quan, file có vẻ commit nhầm, thiếu test cho hành vi mới) |

Repo có template MR/PR thì skill giữ nguyên các mục và thứ tự của template, và theo kiểu của 10-20 commit gần nhất. Repo không có quy ước thì dùng mẫu mặc định và nói rõ.

Ví dụ:

```text
/nqdev:nqdev-merge-request-writer commit
/nqdev:nqdev-merge-request-writer mr --base=develop --brd=billing
```

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-merge-request-writer/` | `~/.claude/skills/nqdev-merge-request-writer/` |
| OpenCode | `.opencode/skills/nqdev-merge-request-writer/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-merge-request-writer/` |
| Gemini CLI | `.gemini/skills/nqdev-merge-request-writer/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-merge-request-writer/` |
| Codex CLI | `.agents/skills/nqdev-merge-request-writer/` | `~/.agents/skills/nqdev-merge-request-writer/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- Skill chỉ đọc, không khai báo `allowed-tools`: quyền theo cấu hình của từng tool. Skill tự kích hoạt được khi yêu cầu khớp mô tả.
- **Không có shell** (ví dụ Claude.ai): skill dùng diff bạn dán vào; không có diff thì không viết được.

## Giới hạn

- Chỉ soạn văn bản: không `git add`, `commit`, `push`, không tạo hay sửa MR. Bạn là người commit và tạo MR.
- Chỉ mô tả điều có trong diff; không ghi "đã test" khi không có bằng chứng. Mã BR/AC và ticket chỉ ghi khi tìm thấy trong nguồn, không thì để `[cần xác nhận: mã BR/ticket]`.
- Luôn nêu điều người review và người deploy phải biết: thay đổi phá tương thích, migration, cấu hình mới, phụ thuộc mới, việc làm tay.
- Diff có credential thì cảnh báo trước và không chép giá trị. Không thêm dòng ký tên hay đồng tác giả trừ khi quy ước repo yêu cầu.
- Không đánh giá chất lượng code, không gọi API GitLab/GitHub.
- Repo viết commit bằng ngôn ngữ khác thì skill viết theo ngôn ngữ đó dù bạn đang chat bằng tiếng Việt, và nói rõ.

## Cấu trúc

```text
nqdev-merge-request-writer/
├── SKILL.md
├── README.md
└── CHANGELOG.md
```
