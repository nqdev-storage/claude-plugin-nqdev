# User Prompt Templates

## Estimate đầy đủ

```text
Hãy phân tích và estimate dự án dựa trên tài liệu sau.

Team: <số DEV review, seniority>
Công cụ AI: <agent đang dùng, nếu có>
Deadline: <cứng/mềm, ngày>
Stack: <đã chốt hoặc để bạn đề xuất>
Ràng buộc khác: <ngân sách, môi trường, tích hợp>

Tài liệu:
<dán spec/PRD hoặc đường dẫn file>
```

## Estimate từ BRD/PRD

```text
Estimate dựa trên BRD/PRD sau, theo mã BR/FR.

Nguồn: <docs/brd/<module>.md, docs/prd/<module>.md; có thể nhiều module>
Team: <số DEV review, seniority>
Công cụ AI: <agent đang dùng, nếu có>
Deadline: <cứng/mềm, ngày>
Ghi chú: <tính năng vắt ngang module, hạng mục muốn tách khỏi estimate>
```

## Estimate nhanh

```text
Mô tả ngắn: <1–3 câu về hệ thống cần làm>
Cho mình estimate sơ bộ dạng range và các câu hỏi cần hỏi khách.
```

## Kiểm tra khả thi

```text
Scope: <tóm tắt hoặc số giờ đã có (Tổng, và phần DEV review nếu biết)>
Team: <số DEV review, seniority>
Deadline: <ngày>
Cho mình biết có khả thi không và các phương án nếu không.
```
