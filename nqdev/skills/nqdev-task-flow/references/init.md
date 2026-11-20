# Chế độ `init`: khởi tạo dự án

Đầu vào (tuỳ chọn): mô tả dự án, ghi chú họp hoặc tài liệu yêu cầu ban đầu.

## Các bước

Mỗi bước chạy xong đều dừng chờ duyệt (xem SKILL.md, mục "Điểm duyệt").

| Bước (`--from`) | Loại | Việc | Đầu ra | Cần duyệt gì |
|---|---|---|---|---|
| `rules` | Gọi skill `nqdev-init-agents` | Tạo `CLAUDE.md`, `.claudeignore`, `.claude/rules/code-rules.md`; không ghi đè file đã có | Các file hướng dẫn cho AI | Quy tắc đúng với dự án chưa: tech stack, lệnh build/test, quy tắc DB và git |
| `brd` | Gọi skill `nqdev-brd-prd-writer` | Viết BRD từng module một. Không có đầu vào thì hỏi có làm bước này không | `docs/brd/<module>.md` | Từng BRD: duyệt xong module này mới viết module kế |
| `estimate` | Gọi skill `nqdev-requirement-estimator` | Ước lượng toàn dự án từ các BRD đã duyệt | Bảng estimate trong hội thoại | Chốt phase MVP |

## Dấu hiệu đã xong

| Bước | Dấu hiệu |
|---|---|
| `rules` | Có `.claude/rules/code-rules.md` hoặc `CLAUDE.md` |
| `brd` | Có file trong `docs/brd/` |

Kết thúc: gợi ý bắt đầu tính năng đầu tiên trong MVP bằng `/nqdev:nqdev-task-flow feature docs/brd/<module>.md --from=plan`.
