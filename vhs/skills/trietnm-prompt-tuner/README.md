# trietnm-prompt-tuner

Tự nhận diện lĩnh vực của một prompt thô, rồi viết lại thành prompt rõ ràng, có cấu trúc, đúng mẫu của lĩnh vực đó, với context lấy từ workspace đang mở. Luôn dừng hỏi xác nhận, không tự chạy.

- **Phiên bản:** 1.0.0 · **Tác giả:** ViHAT · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- Bạn hỏi "prompt này ok chưa", "prompt vậy đủ ý chưa", hoặc muốn refine, tối ưu, chuẩn hoá một prompt.
- Bạn paste một yêu cầu thô và muốn biết nó đã rõ chưa trước khi giao cho AI chạy.

Khác một bộ refine prompt cố định: skill không bắt bạn chọn lĩnh vực bằng tay, và không gắn cứng đường dẫn hay tech stack của repo nào; context lấy từ workspace thật.

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Prompt thô: đoạn trong nháy, đoạn sau dấu hai chấm, hoặc đoạn paste nguyên văn. Không rõ đoạn nào thì skill hỏi lại |
| **Đầu ra** | Lĩnh vực nhận diện được và lý do, tối đa 5 điểm thiếu của prompt gốc, prompt đã viết lại, và bảng xác nhận **[A] Chạy luôn / [B] Chỉnh lại / [C] Huỷ / [D] Lưu ra file** (mặc định `.claude/prompts/YYYY-MM-DD-<slug>.md`) |

Ví dụ:

```text
/vhs:trietnm-prompt-tuner viết lại tài liệu docs
/vhs:trietnm-prompt-tuner "sao API trả về 500 khi đơn không có địa chỉ"
```

### Mười lĩnh vực

`code` · `analyze` · `debug` · `review` · `architecture` · `data` · `devops` · `test` · `docs` · `general`

Lĩnh vực được xác định theo **đầu ra bạn muốn**, không theo chủ đề ("viết tài liệu về kiến trúc" là `docs`, không phải `architecture`). Hai lĩnh vực quá sát nhau thì skill hỏi trước khi refine.

### Ba mức refine

| Mức | Khi nào | Cách xử lý |
|---|---|---|
| Bỏ qua | Prompt đạt ít nhất 5/6 tiêu chí (mục tiêu, context, phạm vi, định dạng đầu ra, ràng buộc, tiêu chí thành công) | Báo prompt đã ổn và hỏi có chạy luôn không |
| Gọn | Một nhiệm vụ đơn và thiếu tối đa 2 tiêu chí | Mẫu 3 mục: Mục tiêu / Yêu cầu / Output format |
| Đầy đủ | Các trường hợp còn lại | Mẫu đầy đủ kèm mục bắt buộc riêng của lĩnh vực |

## Cài đặt

Cài qua plugin: `claude plugin install vhs@nqdev-marketplace`. Hoặc copy thư mục skill vào chỗ dưới đây:

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/trietnm-prompt-tuner/` | `~/.claude/skills/trietnm-prompt-tuner/` |
| OpenCode | `.opencode/skills/trietnm-prompt-tuner/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/trietnm-prompt-tuner/` |
| Gemini CLI | `.gemini/skills/trietnm-prompt-tuner/` (hoặc `.agents/skills/`) | `~/.gemini/skills/trietnm-prompt-tuner/` |
| Codex CLI | `.agents/skills/trietnm-prompt-tuner/` | `~/.agents/skills/trietnm-prompt-tuner/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- Skill không khai báo `allowed-tools`: quyền theo cấu hình của từng tool. Tự kích hoạt được khi yêu cầu khớp mô tả.
- Khi hỏi làm rõ lĩnh vực, skill dùng `AskUserQuestion` nếu tool có; không có thì hỏi bằng một câu ngắn.
- Bước dò context (mọi lĩnh vực trừ `general`) chạy tối đa 5 lệnh shell và chỉ lấy thông tin có thật. **Claude.ai** thường không có repo nên phần này ít dữ liệu hơn.

## Giới hạn

- Không tự chạy prompt đã refine; chỉ chạy khi bạn chọn [A] hoặc đồng ý rõ ràng ("ok", "chạy đi").
- Không bịa ràng buộc, tiêu chí hay con số: thứ chưa biết được đánh dấu `[cần xác nhận: ...]`.
- Giữ nguyên ý gốc của prompt, chỉ bổ sung cấu trúc và context có thật. Chọn [B] thì skill sửa theo góp ý rồi hỏi xác nhận lại.
- Không đọc file quá 200 dòng khi dò context; không quét toàn repo.
- Lĩnh vực mơ hồ thì phải hỏi, không đoán.

## Cấu trúc

```text
trietnm-prompt-tuner/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    ├── detect.md             # bảng tín hiệu nhận diện lĩnh vực
    ├── context-probe.md      # cách dò context từ workspace
    └── domain-<lĩnh vực>.md  # 10 file, mỗi lĩnh vực một file: mục bắt buộc và checklist đặc thù
```
