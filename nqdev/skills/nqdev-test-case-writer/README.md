# nqdev-test-case-writer

Sinh test case thủ công từ tiêu chí nghiệm thu (AC dạng Cho/Khi/Thì) trong BRD hoặc từ tài liệu luồng nghiệp vụ. Mỗi test case có mã `TC` và ghi mã AC/BR mà nó kiểm.

- **Phiên bản:** 1.0.0 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- QA cần kịch bản kiểm thử từ yêu cầu đã duyệt: "viết test case cho module billing", "QA cần test case từ BRD".
- Muốn mỗi test case truy ngược được về yêu cầu sinh ra nó.

Không dùng để viết code test tự động (`nqdev-unit-test-generator`) hay viết, sửa BRD (`nqdev-brd-prd-writer`).

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Theo thứ tự ưu tiên: BRD `docs/brd/<module>.md` (mã `BR-/AC-/UC-<MODULE>-<số>`), tài liệu luồng `docs/business-flows/<slug>.md` của `nqdev-business-flow-extractor`, hoặc văn bản yêu cầu bạn dán vào. Tuỳ chọn: `--scope=<mã BR,...>` (giới hạn theo BR), `--type=<loại>` (mặc định `all`) |
| **Đầu ra** | Trả trong chat: phạm vi, bảng test case (mã `TC-<MODULE>-<số>`, tiêu đề, AC/BR, loại, ưu tiên, điều kiện trước, dữ liệu test, bước thực hiện, kết quả mong đợi), ma trận phủ AC, danh sách AC chưa phủ, câu hỏi còn mở |

Ví dụ:

```text
/nqdev:nqdev-test-case-writer billing
/nqdev:nqdev-test-case-writer docs/brd/order.md --scope=BR-ORDER-003,BR-ORDER-004 --type=negative
```

Các loại test case được suy ra khi nguồn có căn cứ: luồng chính, tiêu cực, giá trị biên, phân quyền, chuyển trạng thái.

## Cài đặt

Cài cả bộ qua plugin: `claude plugin install nqdev@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-test-case-writer/` | `~/.claude/skills/nqdev-test-case-writer/` |
| OpenCode | `.opencode/skills/nqdev-test-case-writer/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-test-case-writer/` |
| Gemini CLI | `.gemini/skills/nqdev-test-case-writer/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-test-case-writer/` |
| Codex CLI | `.agents/skills/nqdev-test-case-writer/` | `~/.agents/skills/nqdev-test-case-writer/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- Skill chỉ đọc, không khai báo `allowed-tools`: quyền theo cấu hình của từng tool. Skill tự kích hoạt được khi yêu cầu khớp mô tả.
- **Claude.ai:** thường không có repo, nên bạn dán nội dung BRD hoặc yêu cầu vào chat.

## Giới hạn

- Chỉ đọc: không sửa BRD, không sửa code. Muốn lưu file thì skill đề xuất `docs/test-cases/<module>.md` và để bạn quyết định.
- Kết quả mong đợi lấy đúng từ phần "Thì" của AC hoặc tài liệu nguồn. Nguồn không nêu giá trị, ngưỡng hay thông báo lỗi thì ghi `[cần xác nhận: ...]`, không tự nghĩ ra số.
- Mỗi AC có ít nhất một test case; AC không viết được thì nêu lý do ở "AC chưa phủ". BR ghi "Đã bỏ" thì không viết test case.
- Mã `TC-` không đổi và không dùng lại; bổ sung vào bộ đã có thì tiếp số.
- Không chạy test, không viết code test. Không kiểm hiệu năng, tải, bảo mật trừ khi nguồn có yêu cầu đo được.
- Chất lượng phụ thuộc chất lượng AC; AC mơ hồ thì test case mang nhãn cần xác nhận.

## Cấu trúc

```text
nqdev-test-case-writer/
├── SKILL.md
├── README.md
└── CHANGELOG.md
```
