# nqdev-requirement-estimator

**Version**: 5.0.0 · **Author**: QuyIT Platform · **Created**: 2026-10-27 · **Updated**: 2026-11-19

## Overview

Phân tích yêu cầu phần mềm và tạo bản estimate dự án: module, ưu tiên, effort dạng range theo giờ (bước 0.5; AI làm, DEV review và góp ý; 3 cột AI | DEV review | Tổng), phase MVP/post-MVP, rủi ro, câu hỏi clarify, exclusions. Đầu vào là mô tả/spec do người dùng đưa, hoặc BRD/PRD do `nqdev-brd-prd-writer` tạo (`docs/brd/<module>.md`, `docs/prd/<module>.md`).

## Purpose

Giúp BA / Tech Lead / PM trả lời nhanh và nhất quán các câu hỏi "mất bao lâu", "cần mấy người", "nên làm gì trước" mà vẫn nêu rõ assumption và giới hạn của con số. Khi nguồn là BRD/PRD, estimate truy vết được về mã BR/FR.

## Target users

BA, Tech Lead, PM, pre-sales và dev lead cần estimate hoặc review scope trước khi báo giá hoặc lên kế hoạch.

## Input format

- Văn bản dán trực tiếp (kể cả chỉ vài dòng) hoặc file spec (đọc bằng `Read`).
- BRD/PRD: đường dẫn `docs/brd/<module>.md` hoặc `docs/prd/<module>.md`, một hoặc nhiều module. Không rõ module thì skill hỏi một câu.
- Tùy chọn: số DEV review và seniority, công cụ AI, deadline, stack, ràng buộc ngân sách.

## Output format

Trả trong chat, Markdown mặc định: Assumptions, bảng Modules (range theo giờ, 3 cột AI | DEV review | Tổng, kèm mã BR/FR nếu có), Phases, Tổng (không quy ra số tuần), Rủi ro, Câu hỏi clarify (tối đa 5), Exclusions. Widget trực quan nếu môi trường có `show_widget` (xem `references/output-widget.md`). Skill không ghi file vào `docs/brd`, `docs/prd`.

## Quan hệ với nqdev-brd-prd-writer

- `nqdev-brd-prd-writer` viết BRD/PRD (không ước lượng); skill này đọc và estimate (không viết BRD/PRD).
- Giai đoạn lấy từ cột "Giai đoạn" của BRD; đề xuất khác chỉ gắn nhãn "đề xuất đổi".
- Câu hỏi clarify ưu tiên lấy từ mục "Câu hỏi mở" của BRD.

## Cấu trúc

```text
nqdev-requirement-estimator/
├── SKILL.md                   # Metadata + hướng dẫn cốt lõi (nạp khi skill được gọi)
├── README.md
├── SYSTEM_PROMPT.md           # Bản prompt dùng ngoài cơ chế skill
├── USER_PROMPT.md             # Mẫu prompt người dùng
├── EXAMPLES.md                # 4 gold examples để eval
├── CHANGELOG.md
└── references/                # Nạp theo nhu cầu (progressive disclosure)
    ├── baselines.md
    ├── risk-catalog.md
    ├── brd-prd-input.md       # Chỉ khi đầu vào là BRD/PRD
    └── output-widget.md
```

## Edge cases

- Input quá ngắn hoặc mơ hồ: vẫn estimate bằng range rộng kèm assumption, đồng thời nêu câu hỏi.
- BR còn `[cần xác nhận]`: range rộng, ghi câu hỏi chặn nó.
- BRD và mô tả người dùng mâu thuẫn: không tự chọn, hỏi, tạm theo BRD và nói rõ.
- Tính năng vắt ngang nhiều module: tính một lần ở module giữ logic chính.
- Deadline/team mâu thuẫn với scope: tính khả thi và đề xuất phương án.
- Spec rất dài: nên chạy ở subagent (`context: fork`) để tóm tắt trước, rồi estimate.
- Task không có trong baseline: suy từ task gần nhất và ghi rõ.
- Dự án AI/ML: không có baseline, estimate riêng bằng range rộng.

## Limitations

- Baseline là điểm xuất phát dựa trên kinh nghiệm cho mô hình AI làm, DEV review; cần hiệu chỉnh theo dữ liệu thực tế (so `estimated_hours` với `time_spent_hours` của `nqdev-write-plan`).
- Không tính chi phí tiền, hạ tầng hay license (chỉ giờ).
- Không quy ra số tuần, không có dòng PM; kiểm tra khả thi chỉ so giờ DEV cần với quỹ giờ DEV.
- Không thay thế discovery với khách hàng khi yêu cầu chưa ổn định.
- Không viết, sửa BRD/PRD và không lưu estimate thành file.

## Best practices

- Luôn gửi kèm thông tin team và deadline nếu có.
- Dùng range để thảo luận scope với khách hàng, không chốt một con số.
- Giải quyết "Câu hỏi mở" của BRD trước khi báo giá.

## Supported tools

| Tool | Hành vi |
|---|---|
| Claude Code | Đọc file spec/BRD/PRD bằng `Read`; xuất Markdown |
| OpenCode | Giống Claude Code; field riêng của Claude Code bị bỏ qua |
| Gemini CLI | Đọc `SKILL.md` natively; không có `allowed-tools` |
| Codex CLI | Đọc `SKILL.md` natively; gọi bằng `$nqdev-requirement-estimator` hoặc tự động theo mô tả |
| Claude.ai | Có thể render widget qua `show_widget` nếu muốn |

## Future enhancements

- Xuất sang `.xlsx` (bảng module + công thức) và `.docx` để gửi khách hàng.
- Lưu estimate thành file theo module khi có quy ước thư mục.
- Hiệu chỉnh baseline từ dữ liệu dự án đã hoàn thành.
- Ước lượng theo ba điểm (optimistic/likely/pessimistic) và mức độ tin cậy.
- Quy đổi chi phí theo rate card.
