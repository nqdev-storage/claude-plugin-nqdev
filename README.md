# nqdev-marketplace — Claude Code plugins

Marketplace Claude Code của nqdev (QuyIT Platform). Mỗi plugin nằm trong một thư mục riêng, khai báo trong [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json).

## Plugin

| Plugin | Phiên bản | Mô tả | Tài liệu |
|---|---|---|---|
| `nqdev` | 2.5.0 | Bộ 14 skill và 7 slash command theo flow coding, kèm 4 workflow dựng sẵn (tính năng mới, sửa bug, khởi tạo dự án, release): viết BRD, ước lượng, thiết kế UI, khởi tạo rule cho AI, viết plan, code và sửa bug, sinh test case, viết unit test, review, soạn MR và release note; đồng bộ plan, git, Jira, Google Sheet. | [nqdev/README.md](nqdev/README.md) |
| `vhs` | 1.0.0 | Bộ 2 skill của ViHAT: tinh chỉnh prompt thô theo lĩnh vực, viết tài liệu hướng dẫn sử dụng từ source code. | [vhs/README.md](vhs/README.md) |

## Cài đặt

```bash
# Thêm marketplace (một lần)
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist

# Cài plugin
claude plugin install nqdev@nqdev-marketplace
claude plugin install vhs@nqdev-marketplace   # tuỳ chọn
```

Trong phiên Claude Code có thể dùng `/plugin marketplace add ...` và `/plugin install ...`. Cú pháp cài luôn là `<plugin>@nqdev-marketplace`.

Repo `nqdev-storage/claude-plugin-nqdev` là bản phát hành: CI cập nhật branch `dist` của nó từ repo phát triển mỗi khi có tag phát hành `vX.Y.Z`, chỉ chứa `.claude-plugin/`, `nqdev/`, `vhs/`, `README.md`, `LICENSE`. Đã cài theo lệnh cũ (không có `#dist`, hoặc `#main`)? Chạy `claude plugin marketplace remove nqdev-marketplace` rồi add lại bằng lệnh trên.

Chi tiết (scope, repo private, cập nhật, xử lý sự cố, dùng skill trên Codex CLI và Gemini CLI): [Hướng dẫn cài đặt và sử dụng](docs/huong-dan-cai-dat-va-su-dung.md).

## Cấu trúc repo

```
claude-plugin-nqdev/
├── .claude-plugin/
│   └── marketplace.json    # Danh sách plugin, mỗi plugin có "source" trỏ tới thư mục của nó
├── nqdev/                  # Plugin nqdev ("source": "./nqdev"), xem nqdev/README.md
├── vhs/                    # Plugin vhs ("source": "./vhs"), xem vhs/README.md
├── docs/                   # Site Docsify
│   ├── index.html                     # Trang chủ là README.md này
│   ├── _sidebar.md                    # Menu
│   ├── huong-dan-cai-dat-va-su-dung.md
│   └── huong-dan-nop-plugin.md
├── .github/
│   └── workflows/
│       └── validate-plugins.yml   # CI kiểm tra marketplace và từng plugin theo "source"
├── .editorconfig
├── .gitignore
├── .nojekyll               # Để GitHub Pages không bỏ qua file bắt đầu bằng "_" (như _sidebar.md)
├── claude-plugin-nqdev.code-workspace
├── LICENSE
└── README.md
```

## Thêm plugin mới

1. Tạo thư mục `<tên-plugin>/` cùng cấp với `nqdev/`, có `<tên-plugin>/.claude-plugin/plugin.json` và `README.md`.
2. Thêm một entry vào `plugins` trong [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) với `"source": "./<tên-plugin>"`.
3. Kiểm tra:

   ```bash
   claude plugin validate . --strict                # marketplace
   claude plugin validate ./<tên-plugin> --strict   # plugin
   ```

4. Thêm dòng vào bảng "Plugin" ở trên. CI tự kiểm tra plugin mới theo `source`, không cần sửa workflow.

## Xem tài liệu dạng web

Phục vụ **root repo** bằng một static server rồi mở `/docs/`. `docs/index.html` dùng `basePath: '../'` nên đọc file md tính từ root.

## Tài liệu

- [Hướng dẫn cài đặt và sử dụng từ Git repo](docs/huong-dan-cai-dat-va-su-dung.md)
- [Hướng dẫn nộp plugin lên Claude Plugin Directory](docs/huong-dan-nop-plugin.md)
- [Plugin nqdev: skill, command, workflow](nqdev/README.md)
- [Plugin vhs: skill của ViHAT](vhs/README.md)

## Giấy phép

Apache-2.0 — xem [LICENSE](LICENSE).
