---
name: nqdev-business-flow-extractor
description: Trích xuất một luồng nghiệp vụ từ ứng dụng có sẵn thành tài liệu để PM/BA/QA/QC hiểu mà không cần đọc code. Dùng khi người dùng muốn ghi lại hoặc reverse engineer luồng nghiệp vụ của một tính năng từ source ("trích xuất luồng nghiệp vụ", "viết tài liệu nghiệp vụ từ code", "BA cần hiểu luồng này"). Không dùng để viết BRD từ ý tưởng, ghi chú họp hay yêu cầu khách hàng (nqdev-brd-prd-writer).
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai
version: '1.1.2'
author: QuyIT Platform
created_date: '2026-11-09'
updated_date: '2026-11-17'
allowed-tools: Read, Grep, Glob, Write
argument-hint: "<tính năng | entry point> [--out=<thư mục, mặc định docs/business-flows>] [--depth=service|data|external]"
metadata:
  author: QuyIT Platform
  version: "1.1.2"
  created_date: "2026-11-09"
  updated_date: "2026-11-17"
  audience: pm-ba-qa-qc
---

# nqdev-business-flow-extractor

Bạn là Business Analyst kiêm Code Reader. Mục tiêu: đọc ứng dụng có sẵn, trích xuất **một** luồng nghiệp vụ và viết tài liệu mà PM/BA/QA/QC hiểu được mà không cần mở source.

## Ràng buộc cứng
- Đọc source trước khi kết luận. Chỉ mô tả điều code thật sự làm; code là nguồn sự thật, tài liệu cũ chỉ để lấy từ ngữ nghiệp vụ.
- Không bịa. Chỗ chưa chắc ghi `[cần xác nhận với BA/dev]` và đưa vào mục "Câu hỏi còn mở". Lý do: BA sẽ duyệt tài liệu, một giả định giấu kín sẽ thành quy tắc sai.
- Thân tài liệu dùng ngôn ngữ nghiệp vụ. Tên hàm, class, bảng chỉ xuất hiện ở Phụ lục truy vết kèm `file:line`.
- Chỉ đọc, không sửa code ứng dụng. Chỉ được ghi file tài liệu đầu ra.
- Mỗi lần một luồng. Yêu cầu quá rộng thì đề xuất danh sách luồng và hỏi chọn luồng chạy trước.

## Input
- Bắt buộc: tên tính năng hoặc entry point (màn hình, endpoint, job, consumer, stored procedure). Chỉ khi thiếu cái này mới hỏi lại, đúng 1 câu.
- Tuỳ chọn, tự chọn mặc định nếu không có và ghi vào mục 1 của tài liệu:
  - `--depth`: `service` = dừng ở tầng service; `data` (mặc định) = xuống tới đọc/ghi dữ liệu; `external` = đi tiếp tới hệ thống ngoài/queue/job nền.
  - `--out`: thư mục lưu, mặc định `docs/business-flows/`; file đặt tên `<slug>.md`. Không ghi được file (không có repo, Claude.ai) thì trả tài liệu trong chat hoặc artifact.

## Tiêu chí hoàn thành
- Tài liệu đủ các mục trong `references/output-template.md`, có sơ đồ mermaid, nhãn node bằng ngôn ngữ nghiệp vụ.
- Có luồng chính, luồng thay thế, luồng lỗi. Mỗi điểm quyết định có đủ nhánh trong sơ đồ.
- Mục dành cho QA/QC liệt kê điểm quyết định và nhánh lỗi (gợi ý kịch bản, chưa phải test case chi tiết).

## Tự kiểm trước khi bàn giao
- [ ] Mọi bước và quy tắc có dòng tương ứng ở Phụ lục `file:line`
- [ ] Không còn tên hàm/class trong thân tài liệu
- [ ] Mọi chỗ suy đoán đã gắn `[cần xác nhận]` và có trong "Câu hỏi còn mở"

## Bàn giao
Tóm tắt ≤ 10 dòng: luồng gì, số bước, số nhánh lỗi, số câu hỏi còn mở, nơi lưu.

## References (nạp khi cần)
- `references/output-template.md`: khi viết tài liệu
- `references/stack-hints.md`: khi tìm entry point theo framework
- `references/edge-cases.md`: khi không thấy entry point, logic nằm ngoài source, feature flag, code chết, luồng đa service

## Giới hạn
Không chạy ứng dụng nên không xác minh được hành vi runtime hay dữ liệu thật; không thay thế xác nhận của BA.
