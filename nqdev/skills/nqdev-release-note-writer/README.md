# nqdev-release-note-writer

Tổng hợp release note và checklist deploy (migration, cấu hình, việc làm tay, rollback) từ commit, `plans/` và mã BR giữa hai bản phát hành.

- **Phiên bản:** 1.0.1 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- "Soạn release note", "changelog cho bản phát hành", "chuẩn bị checklist deploy", "bản này có gì thay đổi".
- Muốn người vận hành có checklist làm theo được, kể cả cách lùi lại.

Không dùng để viết mô tả MR (`nqdev-merge-request-writer`) hay nhật ký công việc (`nqdev-write-plan`).

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Khoảng thay đổi `--from` và `--to` (mặc định: tag phát hành gần nhất tới `HEAD`; repo không có tag và bạn không nêu mốc thì skill hỏi một câu). Tuỳ chọn: `--version=<số>` (không truyền thì để `[cần xác nhận: số phiên bản]`, không tự tăng số), `--audience=internal\|customer` (mặc định `internal`), `--no-checklist` |
| **Đầu ra** | Release note trong khối code (nhóm: thay đổi phá tương thích, tính năng mới, cải tiến, sửa lỗi, bảo mật, nội bộ, vấn đề đã biết), checklist deploy gồm trước deploy / deploy / kiểm tra sau deploy / rollback (mỗi dòng một ô `- [ ]`), danh sách cần xác nhận, phạm vi đã đọc |

Nguồn đọc khi có: lịch sử git trong khoảng, `plans/`, `docs/brd/`, file migration và cấu hình mẫu, `CHANGELOG.md` và release note cũ (định dạng của repo thắng mẫu mặc định).

Ví dụ:

```text
/nqdev:nqdev-release-note-writer --from=v1.4.0 --version=1.5.0
/nqdev:nqdev-release-note-writer --audience=customer --no-checklist
```

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-release-note-writer/` | `~/.claude/skills/nqdev-release-note-writer/` |
| OpenCode | `.opencode/skills/nqdev-release-note-writer/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-release-note-writer/` |
| Gemini CLI | `.gemini/skills/nqdev-release-note-writer/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-release-note-writer/` |
| Codex CLI | `.agents/skills/nqdev-release-note-writer/` | `~/.agents/skills/nqdev-release-note-writer/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- Skill chỉ đọc, không khai báo `allowed-tools`: quyền theo cấu hình của từng tool. Skill tự kích hoạt được khi yêu cầu khớp mô tả.
- **Không có shell** (ví dụ Claude.ai): skill dùng danh sách commit hoặc diff bạn dán vào và nói rõ giới hạn.

## Giới hạn

- Chỉ đọc: không tag, không push, không sửa `CHANGELOG.md`, không chạy migration, không deploy. Muốn ghi vào file thì skill đưa nội dung và đường dẫn đề xuất để bạn quyết định.
- Chỉ ghi điều truy được về commit, plan hoặc file thay đổi. Ngày phát hành, số phiên bản, thời gian downtime, mức cải thiện hiệu năng chỉ ghi khi nguồn có, không thì `[cần xác nhận: ...]`.
- Luôn soát riêng các thay đổi cần hành động: migration và schema, biến môi trường hoặc cấu hình, phụ thuộc, thay đổi phá tương thích, job mới, quyền.
- Lệnh deploy, migrate, rollback lấy từ tài liệu hoặc script của repo; không có thì ghi mức việc cần làm kèm `[cần xác nhận: lệnh cụ thể]`. Migration không lùi được thì ghi rõ là không lùi được bằng cách hạ phiên bản code.
- Bản `customer` không có tên hàm, bảng, nhánh, ticket nội bộ, tên người, và không nhắc lỗ hổng ở mức khai thác được.
- Chất lượng phụ thuộc commit message và `plans/`; lịch sử nghèo thông tin thì nhiều mục cần xác nhận. Không thay quy trình phê duyệt phát hành của đội.

## Cấu trúc

```text
nqdev-release-note-writer/
├── SKILL.md
└── README.md
```
