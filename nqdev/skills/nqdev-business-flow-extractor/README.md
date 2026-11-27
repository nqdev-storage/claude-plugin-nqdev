# nqdev-business-flow-extractor

Đọc ứng dụng có sẵn, trích xuất **một** luồng nghiệp vụ và viết thành tài liệu để PM/BA/QA/QC hiểu mà không cần mở source.

- **Phiên bản:** 1.1.2 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- "Trích xuất luồng nghiệp vụ", "viết tài liệu nghiệp vụ từ code", "BA cần hiểu luồng này".
- Cần ghi lại (reverse engineer) cách một tính năng đang chạy thật.

Không dùng để viết BRD từ ý tưởng, ghi chú họp hay yêu cầu khách hàng (`nqdev-brd-prd-writer`).

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Bắt buộc: tên tính năng hoặc entry point (màn hình, endpoint, job, consumer, stored procedure); thiếu thì skill hỏi đúng một câu. Tuỳ chọn: `--depth=service\|data\|external` (mặc định `data`: xuống tới đọc/ghi dữ liệu; `external`: đi tiếp tới hệ thống ngoài, queue, job nền), `--out=<thư mục>` (mặc định `docs/business-flows/`) |
| **Đầu ra** | File `<slug>.md` trong thư mục đầu ra, viết bằng ngôn ngữ nghiệp vụ theo `references/output-template.md`: sơ đồ Mermaid (nhãn node bằng ngôn ngữ nghiệp vụ), luồng chính, luồng thay thế, luồng lỗi, mục cho QA/QC (điểm quyết định và nhánh lỗi), câu hỏi còn mở, phụ lục truy vết `file:line`. Kèm bản tóm tắt tối đa 10 dòng |

Ví dụ:

```text
/nqdev:nqdev-business-flow-extractor "thanh toán đơn hàng"
/nqdev:nqdev-business-flow-extractor POST /api/refunds --depth=external --out=docs/business-flows
```

Tài liệu sinh ra là đầu vào cho `nqdev-test-case-writer` (kịch bản kiểm thử từ điểm quyết định và nhánh lỗi).

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-business-flow-extractor/` | `~/.claude/skills/nqdev-business-flow-extractor/` |
| OpenCode | `.opencode/skills/nqdev-business-flow-extractor/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-business-flow-extractor/` |
| Gemini CLI | `.gemini/skills/nqdev-business-flow-extractor/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-business-flow-extractor/` |
| Codex CLI | `.agents/skills/nqdev-business-flow-extractor/` | `~/.agents/skills/nqdev-business-flow-extractor/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- **Claude Code:** `allowed-tools` cho phép `Read, Grep, Glob, Write` mà không phải hỏi.
- **OpenCode / Gemini CLI / Codex CLI:** bỏ qua `allowed-tools`; quyền theo cấu hình của tool.
- **Không ghi được file** (ví dụ Claude.ai, không có repo): skill trả tài liệu trong chat hoặc artifact.

## Giới hạn

- Chỉ mô tả điều code thật sự làm; code là nguồn sự thật, tài liệu cũ chỉ để lấy từ ngữ nghiệp vụ. Chỗ chưa chắc ghi `[cần xác nhận với BA/dev]` và đưa vào "Câu hỏi còn mở".
- Thân tài liệu không có tên hàm, class, bảng; những thứ đó chỉ ở phụ lục kèm `file:line`.
- Chỉ đọc, không sửa code ứng dụng; chỉ ghi file tài liệu đầu ra.
- Mỗi lần một luồng. Yêu cầu quá rộng thì skill đề xuất danh sách luồng và hỏi chọn luồng chạy trước.
- Không chạy ứng dụng nên không xác minh được hành vi lúc chạy thật hay dữ liệu thật; không thay xác nhận của BA.

## Cấu trúc

```text
nqdev-business-flow-extractor/
├── SKILL.md
├── README.md
└── references/
    ├── output-template.md    # khuôn tài liệu đầu ra
    ├── stack-hints.md        # cách tìm entry point theo framework
    └── edge-cases.md         # không thấy entry point, feature flag, code chết, đa service
```
