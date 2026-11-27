# nqdev-bug-fixer

Sửa một bug theo trình tự: tái hiện, khoanh vùng, tìm nguyên nhân gốc, sửa tối thiểu, và để lại một test chứng minh bug không quay lại.

- **Phiên bản:** 1.0.1 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- Bạn có thông báo lỗi, stack trace, log, hoặc mô tả "mong đợi gì, thực tế ra gì".
- Muốn tìm nguyên nhân gốc chứ không vá triệu chứng.

**Skill chỉ chạy khi bạn gọi rõ** (`/nqdev:nqdev-bug-fixer` hoặc yêu cầu thẳng "sửa bug này", "fix lỗi"), vì nó sửa code.

Không dùng để thêm tính năng (`nqdev-feature-implementer`), chỉ review (`nqdev-code-review`), hay thay quy trình xử lý sự cố production. Yêu cầu của người dùng thực ra là đổi nghiệp vụ, không phải lỗi code: skill dừng và chuyển sang `nqdev-brd-prd-writer`.

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Ít nhất một trong: thông báo lỗi, stack trace, log, mô tả hành vi sai. Thiếu hết thì skill hỏi tối đa 2 câu rồi dừng. Tuỳ chọn: `--diagnose-only` (chỉ tìm nguyên nhân, không ghi file), `--brd=MODULE` (đối chiếu hành vi đúng với `docs/brd/<module>.md`) |
| **Đầu ra** | Bản sửa trong repo kèm test tái hiện, và báo cáo: triệu chứng, nguyên nhân gốc (câu "Vì X nên khi Y thì Z", kèm `file:line`), cách sửa, kết quả kiểm chứng, phạm vi ảnh hưởng, việc bạn cần làm, ghi nhận ngoài phạm vi |

Ví dụ:

```text
/nqdev:nqdev-bug-fixer "NullReferenceException tại OrderService.Calculate khi đơn không có mã giảm giá"
/nqdev:nqdev-bug-fixer "tổng tiền hoá đơn lệch 1 đồng khi có thuế" --brd=billing --diagnose-only
```

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-bug-fixer/` | `~/.claude/skills/nqdev-bug-fixer/` |
| OpenCode | `.opencode/skills/nqdev-bug-fixer/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-bug-fixer/` |
| Gemini CLI | `.gemini/skills/nqdev-bug-fixer/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-bug-fixer/` |
| Codex CLI | `.agents/skills/nqdev-bug-fixer/` | `~/.agents/skills/nqdev-bug-fixer/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- **Claude Code:** `disable-model-invocation: true`, nên Claude không tự nạp skill này.
- **Codex CLI:** `agents/openai.yaml` đặt `allow_implicit_invocation: false`, chỉ chạy khi gọi `$nqdev-bug-fixer`.
- **OpenCode / Gemini CLI:** quyền theo cấu hình của tool.
- **Claude.ai:** không có shell, nên skill phân tích trên code và log bạn dán, trả bản sửa theo từng file và ghi rõ chưa chạy test.

## Giới hạn

- Mỗi lần một bug; nhiều bug không liên quan thì xử lý lần lượt.
- Không tái hiện được thì chỉ dừng ở mức giả thuyết, không sửa mò.
- Không sửa khi chưa kiểm chứng được nguyên nhân gốc, không sửa test cho khớp code sai, không tự commit hay push.
- Không chạy lệnh sửa schema hoặc dữ liệu database khi chưa được đồng ý rõ; không bao giờ ngoài local/dev.
- Quy tắc repo (`.claude/rules/code-rules.md`, `CLAUDE.md`) thắng skill khi hai bên khác nhau.

## Cấu trúc

```text
nqdev-bug-fixer/
├── SKILL.md
├── README.md
└── agents/
    └── openai.yaml
```
