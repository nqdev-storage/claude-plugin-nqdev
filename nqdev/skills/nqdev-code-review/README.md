# nqdev-code-review

Review diff, merge request hoặc nhóm file theo bốn trục (đúng đắn, bảo mật, hiệu năng, quy tắc và yêu cầu), trả bảng vấn đề có bằng chứng, xếp theo mức độ, kèm kết luận.

- **Phiên bản:** 1.0.1 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- "Review giúp đoạn này", "kiểm tra trước khi merge", "code này ổn chưa", review MR/PR.
- Muốn đối chiếu thay đổi với quy tắc repo (`.claude/rules/code-rules.md`) và tiêu chí nghiệm thu (AC) trong `docs/brd/`.

Không dùng để sửa code (`nqdev-feature-implementer`, `nqdev-bug-fixer`) hay rà soát skill/prompt.

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Diff dán trực tiếp, danh sách file hoặc thư mục, hoặc mô tả phạm vi ("các file vừa đổi trong module billing"). Không xác định được phạm vi thì skill hỏi đúng một câu. Tuỳ chọn: `--focus` (chỉ soát một trục, mặc định đủ bốn), `--brd=MODULE` (đối chiếu `docs/brd/<module>.md`; không truyền thì tự tìm theo tên module hoặc mã BR/AC trong diff) |
| **Đầu ra** | Kết luận (`Đạt` / `Đạt sau khi sửa mức Chặn` / `Chưa đạt`), phạm vi đã review, bảng vấn đề `# \| Mức \| Trục \| Vị trí \| Vấn đề \| Cách sửa đề xuất`, đối chiếu AC (khi có BRD), tối đa 5 câu hỏi cho tác giả, tối đa 3 điểm làm tốt |

Mức độ: **Chặn** (phải sửa trước khi merge), **Cao**, **Trung bình**, **Gợi ý** (phong cách, không chặn merge).

Ví dụ:

```text
/nqdev:nqdev-code-review src/billing --brd=billing
/nqdev:nqdev-code-review src/auth/login.ts --focus=security
```

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-code-review/` | `~/.claude/skills/nqdev-code-review/` |
| OpenCode | `.opencode/skills/nqdev-code-review/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-code-review/` |
| Gemini CLI | `.gemini/skills/nqdev-code-review/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-code-review/` |
| Codex CLI | `.agents/skills/nqdev-code-review/` | `~/.agents/skills/nqdev-code-review/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- Skill chỉ đọc, không khai báo `allowed-tools`: quyền theo cấu hình của từng tool. Skill tự kích hoạt được khi yêu cầu khớp mô tả.
- **Chỉ có diff, không có repo** (ví dụ Claude.ai): review trên diff và ghi rõ giới hạn là không đọc được ngữ cảnh xung quanh.

## Giới hạn

- Chỉ đọc: không sửa file, không chạy lệnh ghi, không commit. Tác giả giữ quyền quyết định cách sửa.
- Mỗi vấn đề có `file:line` và trích đoạn ngắn; phần chưa đọc đủ để kết luận thì ghi `[cần xác nhận: ...]`, không khẳng định là lỗi. Không tìm thấy vấn đề thì nói thẳng, không thêm gợi ý cho đủ số.
- Thấy credential trong code thì báo vị trí, không chép giá trị.
- Không chạy test hay ứng dụng; kết luận dựa trên đọc code. Không thay thế kiểm thử bảo mật chuyên sâu.
- Diff quá lớn thì đề xuất chia theo module, review phần rủi ro cao trước (DB, phân quyền, thanh toán, API công khai). Code sinh tự động, file lock, vendor bị bỏ qua.
- Không có BRD thì bỏ mục đối chiếu yêu cầu và nói rõ.

## Cấu trúc

```text
nqdev-code-review/
├── SKILL.md
└── README.md
```
