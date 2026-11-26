---
name: nqdev-init-agents
description: "Khởi tạo hạ tầng hướng dẫn cho AI agent trong dự án: CLAUDE.md (gốc hoặc phân cấp), .claudeignore, .claude/rules/code-rules.md (quy tắc DB, git, workflow, comment), tùy chọn .rtk/, .opencode/ và settings. Dùng khi người dùng gõ /nqdev:nqdev-init-agents hoặc yêu cầu \"init agents\", \"tạo CLAUDE.md\", \"setup rule cho AI trong repo\". Không dùng khi người dùng chỉ muốn một CLAUDE.md tóm tắt codebase kiểu lệnh /init có sẵn, hay khi đang làm tính năng (nqdev-task-flow)."
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai (không có shell nên in nội dung các file ra chat để người dùng tự lưu)
version: '1.8.1'
author: QuyIT Platform
created_date: '2026-08-10'
updated_date: '2026-11-21'
metadata:
  author: QuyIT Platform
  version: "1.8.1"
  created_date: "2026-08-10"
  updated_date: "2026-11-21"
---

# nqdev-init-agents

## Mục tiêu
Phân tích dự án rồi tạo bộ file hướng dẫn cho AI agent, không ghi đè file đã có.

## Flag
| Flag | Tác dụng |
|---|---|
| `--sub-claude` / `--hierarchical-claude` | Tạo CLAUDE.md theo từng lớp (xem "Phân cấp") |
| `--no-hierarchical-claude` | Tắt chế độ phân cấp |
| `--claude-depth=N` | Độ sâu 1-15, mặc định 2 |
| `--claude-dirs=a,b` | Thư mục đích, mặc định tự dò (src, tests, db, docs) |
| `--rtk` / `--no-rtk` | Bật/tắt `.rtk/`, mặc định tự dò |
| `--opencode` | Tạo cấu hình OpenCode và `.env` (xem "Tùy chọn") |

## Việc phải làm
Thứ tự tự chọn, trừ các điểm đánh dấu BẮT BUỘC.
1. Kiểm tra thư mục dự án, phát hiện CLAUDE.md hiện có (giữ nguyên, không ghi đè). Dò cấu trúc và tech stack.
2. Tạo `CLAUDE.md` gốc: quy ước code, test, deploy, cùng callout "Database Safety", "Git Safety", "Workflow Safety" trỏ tới code-rules.md.
3. Tạo `.claudeignore` (build artifacts, secrets, vendor).
4. **BẮT BUỘC, không phụ thuộc flag:** tạo `.claude/rules/code-rules.md` bằng cách chép từ `templates/code-rules.md` của skill này (đường dẫn tính từ thư mục gốc của skill (dòng *Base directory for this skill* mà Claude Code hiện khi nạp skill)), gồm phần Testing (số điện thoại test mặc định `0909090909`, `0765418062`; không dùng số khác) và các policy ở mục "Nội dung code-rules.md" bên dưới, sao chép nguyên văn: Testing, Comment (có label dev), Database Execution Policy, Git Commit Policy, Development Workflow Policy, Task Execution Policy. Tạo `.claude/.gitignore` với `.env`, `*.share.json`, `dev.local.json`.
5. Thêm phần tùy chọn theo flag (hierarchical, `.rtk/`, `.opencode/`, settings) và `docs/Business-Document.md` nếu có thư mục docs (chép khuôn từ `templates/Business-Document.md` của skill này). File này chỉ ở cấp dự án (vision, KPI, budget, rủi ro), không thay BRD theo module trong `docs/brd/` (việc của `nqdev-brd-prd-writer`).
6. Tạo thư mục nháp `draft/` (xem "Thư mục draft"), không phụ thuộc flag.
7. Tóm tắt: file đã tạo, file bỏ qua vì đã tồn tại (gồm cả `draft/`).

## Ràng buộc cứng
- Không ghi đè file có sẵn. `.env` không được commit; không để dòng `!.env` trong `.gitignore`.
- Label comment của dev lấy từ `.claude/dev.local.json`; chưa có thì gợi ý từ `git config`, hỏi xác nhận một lần rồi lưu (không commit).
- Nội dung bốn policy (DB, Git, Workflow, Task Execution) phải đúng nguyên văn bên dưới, không rút gọn hay diễn đạt lại.

## Hoàn thành khi
CLAUDE.md và code-rules.md tồn tại, `draft/` và `draft/docs/` có `.gitkeep`, `.gitignore` đúng (gồm khối `draft/*`), báo cáo cuối liệt kê file tạo và file bỏ qua.

## Nội dung code-rules.md (nguyên văn)

## Comment Rule

1. Chỉ comment khi logic phức tạp, workaround tạm, hoặc edge case đặc biệt.
2. Comment giải thích WHY, không giải thích WHAT.
3. Sửa code → sửa/xóa comment cũ theo, không để lỗi thời.
4. Code tự rõ nghĩa (CRUD đơn giản, tên biến/hàm rõ ràng) → không comment.
5. Comment ngắn: mặc định một dòng (tối đa khoảng 100 ký tự); không viết nhiều đoạn, không kể lịch sử thay đổi (đã có git).

### Comment label (per developer)

1. Read `.claude/dev.local.json` → `label`; if present, use it without asking.
2. Otherwise suggest a label from `git config user.name` / `user.email`, ask the dev to confirm or override once, then save it to `.claude/dev.local.json` (not committed).
3. Format: `<comment-syntax> [<label>] <WHY explanation>`, e.g. `// [<label>] ...`, `# [<label>] ...`, `-- [<label>] ...`.

---

## Database Execution Policy

NOT run by Claude — cần DBA review

1. Claude/agents never execute SQL directly against any database (dev, staging, production), by any means (CLI, ORM migration tool, MCP DB connector).
2. Applies to all DDL (`CREATE`/`ALTER`/`DROP`/`TRUNCATE`), DML (`INSERT`/`UPDATE`/`DELETE`) and schema migrations.
3. Write the statement into the chat session only, prefix it with `-- NOT run by Claude — cần DBA review`, then stop. A human DBA reviews and executes it.
4. Read-only `SELECT` for diagnostics/inspection is the only exemption.

---

## Git Commit Policy

1. KHÔNG tự ý `git commit` (kể cả `--amend`) — luôn hỏi và chờ dev xác nhận rõ ràng trước khi commit.
2. Khi hỏi, nêu rõ: danh sách file sẽ commit + message dự kiến.
3. Xác nhận cho 1 lần commit không áp dụng cho các lần sau — mỗi lần commit hỏi lại.
4. Không tự `git push`, `git push --force`, `git reset --hard`, tạo/xóa branch, tag nếu dev chưa yêu cầu.

---

## Development Workflow Policy

0. Yêu cầu tính năng mới, sửa bug hoặc chuẩn bị release: nếu plugin `nqdev` đã cài, đề xuất chạy `/nqdev:nqdev-task-flow <feature|bugfix|release>` trước khi phân tích hay code; người dùng từ chối thì làm theo các mục dưới.
1. Trong session trao đổi: chỉ phân tích yêu cầu mới và hỏi làm rõ — KHÔNG viết/sửa code.
2. Sau khi phân tích xong: viết plan (phạm vi, file sẽ đổi, các bước) rồi dừng lại chờ duyệt. Ưu tiên dùng skill `/nqdev-write-plan` để viết plan (nếu có); không có thì tự viết theo cấu trúc trên.
3. Chỉ bắt đầu code sau khi dev duyệt plan rõ ràng. Im lặng hoặc trả lời mơ hồ = chưa duyệt.
4. Tuyệt đối không viết code khi đang trao đổi mà chưa có sự cho phép.
5. Plan thay đổi đáng kể trong lúc làm → dừng lại, cập nhật plan, xin duyệt lại.
6. Viết code xong (từng bước hoặc toàn bộ) → cập nhật trạng thái vào plan (bước nào xong / đang làm / còn lại) rồi báo dev.

## Task Execution Policy

1. Mỗi lần chỉ làm một task trong plan đã duyệt; không tự mở rộng phạm vi.
2. Làm trên nhánh riêng; mỗi task một commit nhỏ, đúng phạm vi. Tạo nhánh và commit theo Git Commit Policy (hỏi và chờ dev xác nhận).
3. Trước khi code: nêu file sẽ sửa. Cần sửa file ngoài danh sách đó hoặc thêm thư viện mới → dừng và hỏi; chưa được duyệt thì không làm.
4. Sau mỗi task: báo những gì đã đổi và task tiếp theo trong plan (cập nhật trạng thái plan theo mục 6 của Development Workflow Policy).
5. Gặp mơ hồ hoặc xung đột với plan: dừng và hỏi, không tự quyết.

## Thư mục draft
`draft/` là nơi chứa file nháp tạm, không commit. Cấu trúc:

```
draft/
├── .gitkeep
└── docs/
    └── .gitkeep      # nháp tài liệu
```

- Tạo `draft/.gitkeep` và `draft/docs/.gitkeep` (file rỗng). File nào đã có thì bỏ qua, không ghi đè.
- Thêm vào `.gitignore` gốc của dự án các dòng sau nếu chưa có (kiểm tra từng dòng, không thêm trùng):
  ```
  # draft/ là thư mục tạm để lưu các file draft, không commit các file trong đó trừ .gitkeep
  draft/*
  !draft/.gitkeep
  !draft/docs/.gitkeep
  ```
  Chưa có `.gitignore` thì tạo mới chỉ với khối trên.
- Ghi một dòng vào `CLAUDE.md` gốc: `draft/` chứa file nháp tạm (không commit), `draft/docs/` chứa nháp tài liệu.
- Mặc định luôn tạo, không có flag bật/tắt.

## Phân cấp (`--sub-claude`)
Tạo thêm `src/CLAUDE.md`, `tests/CLAUDE.md`, `db/CLAUDE.md`, `docs/CLAUDE.md` (hoặc theo `--claude-dirs`). Khi truy cập file, dùng CLAUDE.md gần nhất, rồi gộp với CLAUDE.md cha và gốc (cụ thể nhất thắng).

## Tùy chọn
- **`--rtk`:** tạo `.rtk/`, `.rtk/.gitignore` (`*.tmp`, `*.cache`, `*.log`, `.env.local`, `node_modules/`, `*.rtk`), `.rtk-usage.md`, và ghi mục .rtk vào CLAUDE.md gốc.
- **`--opencode`:** tạo `.opencode/opencode.jsonc` (`$schema` https://opencode.ai/config.json; điền `mcp` từ `.mcp.json` nếu có), `.opencode/.gitignore` (`.env.local`, `*.env`, `build/`, `dist/`), mẫu `.env` ở gốc; sửa `.gitignore` gốc (bỏ `!.env`, thêm `.env`, `.env.local`, `.env.*.local`); ghi chú vào CLAUDE.md.
- **Settings (khi dev yêu cầu):** `.claude/settings.share.json` theo từng máy, không commit; chỉ sinh `{"permissions": {"allow": []}}` hoặc giá trị dev cung cấp, không tự bịa pattern.
- **`.claude/dev.local.json`:** `{"label": "...", "name": "..."}` theo từng dev, không commit.
