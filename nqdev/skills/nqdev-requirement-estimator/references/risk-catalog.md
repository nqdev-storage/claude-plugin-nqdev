# Risk Catalog

Chỉ chọn các mục liên quan đến spec đang phân tích. Với mỗi rủi ro nêu: mức độ (Cao/Trung bình/Thấp), tác động lên estimate, và câu hỏi cần clarify nếu có.

## Luôn kiểm tra

Có BRD/PRD: tra mục tương ứng trước (xem `brd-prd-input.md`), chỉ hỏi phần nguồn không trả lời được. Hợp đồng "Cần thêm" ở BRD mục 9 là rủi ro tích hợp.

- Tech stack đã chốt hay cần đề xuất?
- Team size, seniority, deadline cứng hay mềm?
- Ai dùng hệ thống (nội bộ hay khách bên ngoài)? Quy mô user, số record, đồng thời bao nhiêu?
- Source of truth của dữ liệu ở đâu; khi xung đột thì bên nào thắng?
- Có dữ liệu cũ cần migrate không?
- Spec còn cụm mở ("và các tính năng khác", "tương tự app X")?

## Auth & phân quyền

- Login đơn giản hay SSO, phân quyền theo role/môi trường/đối tượng?
- Có audit trail cho thao tác nhạy cảm không?

## Tích hợp

- API không có docs, không có sandbox/test environment, thay đổi không báo trước.
- Giới hạn rate limit, chi phí theo lượt gọi, SLA bên thứ ba.
- Phụ thuộc phía khách hàng (cấp quyền, dữ liệu mẫu, thời gian phản hồi).

## Real-time / collaboration

- Có nằm trong MVP không? Concurrent users bao nhiêu?
- Conflict resolution, reconnect, fallback; chi phí hạ tầng.

## Dữ liệu & file / cấu hình (chỉ khi spec thao tác file hoặc config)

- Encoding (UTF-8 vs UTF-16), BOM, trailing whitespace, line ending.
- Quy ước đặt tên và phân biệt hoa/thường giữa các môi trường.
- Quyền ghi file trên server production.
- Xung đột giữa file system và database.

## UI / thiết bị

- Responsive hay mobile native? Trình duyệt/thiết bị hỗ trợ?
- Accessibility, đa ngôn ngữ, RTL.

## Compliance & bảo mật

- Dữ liệu cá nhân, GDPR/PDPA, lưu trữ dữ liệu theo vùng.
- Yêu cầu pentest, audit, chứng chỉ.

## AI / ML

- Chất lượng mô hình không estimate được như dev thường: cần giai đoạn PoC, dữ liệu huấn luyện, tiêu chí chấp nhận.
- Chi phí inference và độ trễ.

## Hạ tầng & vận hành

- Số môi trường, CI/CD, monitoring, backup.
- Hạ tầng production (k8s, CDN, load balancer) thường nằm ngoài estimate nếu không nói rõ.
