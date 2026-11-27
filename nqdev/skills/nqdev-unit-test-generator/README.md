# nqdev-unit-test-generator

Viết unit test và integration test tự động cho code có sẵn, theo đúng framework và quy ước test của repo, phủ luồng chính, nhánh lỗi và giá trị biên.

- **Phiên bản:** 1.0.0 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- "Viết test cho hàm/class/module này", "bổ sung test", "tăng coverage".
- Muốn test viết theo cách repo đang viết test, không đưa framework mới vào.

**Skill chỉ chạy khi bạn gọi rõ** (`/nqdev:nqdev-unit-test-generator`), vì nó ghi file vào repo.

Không dùng để viết test case thủ công cho QA (`nqdev-test-case-writer`) hay sửa bug mà test phát hiện (`nqdev-bug-fixer`).

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Mục tiêu cần test: file, class, hàm hoặc thư mục (thiếu thì skill hỏi đúng một câu). Tuỳ chọn: `--type=unit\|integration` (mặc định `unit`), `--brd=MODULE` (lấy hành vi kỳ vọng từ AC trong `docs/brd/<module>.md`, ghi mã AC vào tên hoặc chú thích test), `--plan-only` (chỉ liệt kê các ca sẽ viết) |
| **Đầu ra** | File test và file hỗ trợ test (fixture, factory) trong repo, cùng báo cáo: số file và số test, bảng phủ `Hành vi / nhánh \| Test \| Mã AC / TC \| Kết quả chạy`, lệnh đã chạy, mục "Nghi bug" và "Chưa phủ" |

Ví dụ:

```text
/nqdev:nqdev-unit-test-generator src/billing/InvoiceCalculator.cs --brd=billing
/nqdev:nqdev-unit-test-generator src/orders --type=integration --plan-only
```

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-unit-test-generator/` | `~/.claude/skills/nqdev-unit-test-generator/` |
| OpenCode | `.opencode/skills/nqdev-unit-test-generator/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-unit-test-generator/` |
| Gemini CLI | `.gemini/skills/nqdev-unit-test-generator/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-unit-test-generator/` |
| Codex CLI | `.agents/skills/nqdev-unit-test-generator/` | `~/.agents/skills/nqdev-unit-test-generator/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- **Claude Code:** `disable-model-invocation: true`, nên Claude không tự nạp skill này.
- **Codex CLI:** `agents/openai.yaml` đặt `allow_implicit_invocation: false`, chỉ chạy khi gọi `$nqdev-unit-test-generator`.
- **OpenCode / Gemini CLI:** quyền theo cấu hình của tool.
- **Claude.ai:** không có shell, nên skill trả code test theo từng file kèm đường dẫn và ghi rõ chưa chạy.

## Giới hạn

- Chỉ ghi file test và file hỗ trợ test, không sửa code ứng dụng; code khó test thì nêu đề xuất trong báo cáo.
- Code có vẻ sai so với BRD hoặc ý đồ rõ ràng: test viết theo hành vi đúng và để thất bại, rồi báo là nghi bug thay vì khoá hành vi sai.
- Repo chưa có hạ tầng test: skill không tự cài mà đề xuất framework và chờ đồng ý.
- Không hạ ngưỡng coverage, không bỏ qua hay sửa test có sẵn trừ khi bạn yêu cầu. Con số coverage chỉ báo khi đo được bằng công cụ của repo.
- Không viết test giao diện đầu-cuối, test tải, test bảo mật. Test chỉ phủ hành vi suy ra được từ code và yêu cầu, không đảm bảo hết bug.

## Cấu trúc

```text
nqdev-unit-test-generator/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── agents/
    └── openai.yaml
```
