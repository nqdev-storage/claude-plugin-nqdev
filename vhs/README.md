# vhs — ViHAT Toolkit

Plugin Claude Code chứa các skill của ViHAT, nằm trong marketplace `nqdev-marketplace`. Phiên bản hiện tại: **1.0.0**.

Skill trong plugin này **không** theo quy tắc đặt tên `nqdev-*` của plugin `nqdev`; tên skill giữ nguyên như bản gốc.

## Cài đặt

```bash
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist   # một lần
claude plugin install vhs@nqdev-marketplace
```

Trong phiên đang mở, chạy `/reload-plugins` để áp dụng. Cập nhật: `claude plugin marketplace update nqdev-marketplace` rồi `claude plugin update vhs@nqdev-marketplace`.

## Skills (2)

| Skill | Phiên bản | Gọi | Công dụng |
|---|---|---|---|
| [trietnm-prompt-tuner](skills/trietnm-prompt-tuner/SKILL.md) | 1.0.0 | `/vhs:trietnm-prompt-tuner <prompt thô>` | Nhận diện lĩnh vực của prompt (code, debug, review, kiến trúc, database, devops, test, tài liệu, ngoài IT), dò context từ workspace rồi viết lại prompt theo mẫu của lĩnh vực đó. Luôn dừng chờ xác nhận [A] chạy / [B] chỉnh / [C] huỷ / [D] lưu file, không tự chạy. |
| [trietnm-user-doc-writer](skills/trietnm-user-doc-writer/SKILL.md) | 1.0.0 | `/vhs:trietnm-user-doc-writer help \| plan \| full \| module <tên>` | Quét source code, viết tài liệu hướng dẫn sử dụng tiếng Việt cho người dùng cuối vào `docs/user-guide/`, có DOC-PLAN và style guide để các đợt viết nhất quán, kèm placeholder chèn ảnh chụp màn hình. |

Skill cũng tự kích hoạt theo `description` khi yêu cầu khớp, ví dụ "prompt này ok chưa", "viết tài liệu hướng dẫn sử dụng".

## Dùng trên Codex CLI và Gemini CLI

Copy thư mục skill vào `~/.agents/skills/<tên>/` (Codex CLI) hoặc `~/.gemini/skills/<tên>/` (Gemini CLI), gọi bằng tên skill không có tiền tố `vhs:`. Chi tiết: [Hướng dẫn cài đặt và sử dụng](../docs/huong-dan-cai-dat-va-su-dung.md).

## Cấu trúc

```
vhs/
├── .claude-plugin/
│   ├── plugin.json
│   ├── icon.png          # Biểu tượng ViHAT, 1024×1024
│   └── icon.svg
├── skills/
│   ├── trietnm-prompt-tuner/      # SKILL.md, CHANGELOG.md, references/
│   └── trietnm-user-doc-writer/   # SKILL.md, CHANGELOG.md, templates/
└── README.md
```

## Lịch sử thay đổi

- **1.0.0** (2026-11-18): Phát hành đầu tiên với 2 skill `trietnm-prompt-tuner`, `trietnm-user-doc-writer`.

## Giấy phép

MIT. Tác giả: ViHAT.
