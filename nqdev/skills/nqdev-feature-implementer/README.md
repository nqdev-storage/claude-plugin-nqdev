# nqdev-feature-implementer

Code một tính năng theo plan trong `plans/` và yêu cầu trong `docs/brd/`, đúng cách repo đang làm, kèm test và bảng truy vết BR/AC.

- **Phiên bản:** 1.1.1 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- Đã có plan (do `nqdev-write-plan` tạo hoặc viết tay) và muốn triển khai: "implement tính năng theo plan", "code theo BRD", "triển khai plan này".
- Muốn code bám yêu cầu đã chốt và truy vết được về mã BR/AC.

**Skill chỉ chạy khi bạn gọi rõ** (`/nqdev:nqdev-feature-implementer`), vì nó sửa code. Trong workflow `nqdev-task-flow`, bước code luôn là bước bàn giao: workflow đưa lệnh để bạn tự gõ.

Không dùng để sửa bug (`nqdev-bug-fixer`), review (`nqdev-code-review`) hay lập plan (`nqdev-write-plan`).

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Plan trong `plans/` hoặc mô tả tính năng; yêu cầu từ `docs/brd/<module>.md` (qua `--brd`, hoặc tự tìm theo mã BR/AC trong plan); prototype nếu plan có mục `## Màn hình` (đọc làm mẫu, không chép). Tuỳ chọn: `--scope=<mã BR>`, `--dry-run` (chỉ trình bày file sẽ đổi và cách làm) |
| **Đầu ra** | Code và test trong repo, cùng báo cáo: tóm tắt, bảng truy vết `Mã BR / AC \| Màn \| File thay đổi \| Test kiểm \| Trạng thái`, file đã đổi, kết quả build/test, việc bạn cần làm (migration, biến môi trường), phần chưa làm |

Ví dụ:

```text
/nqdev:nqdev-feature-implementer plans/001-2026-11-17-refund-flow-planning.md --brd=billing
/nqdev:nqdev-feature-implementer "thêm bộ lọc theo trạng thái cho danh sách đơn" --scope=BR-ORDER-007 --dry-run
```

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-feature-implementer/` | `~/.claude/skills/nqdev-feature-implementer/` |
| OpenCode | `.opencode/skills/nqdev-feature-implementer/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-feature-implementer/` |
| Gemini CLI | `.gemini/skills/nqdev-feature-implementer/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-feature-implementer/` |
| Codex CLI | `.agents/skills/nqdev-feature-implementer/` | `~/.agents/skills/nqdev-feature-implementer/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- **Claude Code:** `disable-model-invocation: true`, nên Claude không tự nạp skill này.
- **Codex CLI:** `agents/openai.yaml` đặt `allow_implicit_invocation: false`, chỉ chạy khi gọi `$nqdev-feature-implementer`.
- **OpenCode / Gemini CLI:** quyền theo cấu hình của tool.
- **Claude.ai:** không có shell, nên skill trả code đầy đủ theo từng file kèm đường dẫn và ghi rõ chưa build, chưa chạy test.

## Giới hạn

- Làm đúng phạm vi BR; không thêm tính năng ngoài BR, không refactor phần không liên quan (ghi vào "Ghi nhận ngoài phạm vi").
- BR hoặc AC mơ hồ, mang `[cần xác nhận]`, hoặc mâu thuẫn plan thì dừng ở phần đó và hỏi, không tự chọn ngưỡng hay quy tắc nghiệp vụ.
- Không tự commit, push, tạo MR; không chạy lệnh thay đổi schema hay dữ liệu database; hỏi trước khi thêm thư viện mới.
- Mỗi AC trong phạm vi có ít nhất một test tự động, trừ khi repo không có hạ tầng test.
- Không deploy, không thay thế review của con người; nên luôn qua `nqdev-code-review`.
- Chất lượng phụ thuộc plan và BRD; yêu cầu mơ hồ sẽ dẫn tới câu hỏi thay vì code.

## Cấu trúc

```text
nqdev-feature-implementer/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── agents/
    └── openai.yaml
```
