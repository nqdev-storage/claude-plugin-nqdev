# BRD — <module>: <tên nghiệp vụ>

> **Dành cho:** <ai đọc: owner module, người duyệt nghiệp vụ, dev module liên quan>.
> **Đọc để:** biết module <module> phải làm gì, đúng thế nào là đúng, và phạm vi từng giai đoạn.
> **Nên đọc trước:** <tài liệu mô tả module, tài liệu kiến trúc, `docs/Business-Document.md` nếu có (bối cảnh cấp dự án) — đường dẫn tương đối>.
> **Cập nhật:** YYYY-MM-DD · **Trạng thái:** Nháp | Chờ duyệt | Đã duyệt (người duyệt, ngày)
> **Nguồn:** <file chốt nghiệp vụ (dòng …), ghi chú họp (ngày), tài liệu hệ cũ (đường dẫn), quyết định đã chốt>

<!-- Xoá các chú thích <!-- … --> khi viết xong. Mục không áp dụng: giữ tiêu đề, ghi "Không áp dụng" + lý do. -->

## 1. Phạm vi

| | |
|---|---|
| **Trong phạm vi** | <!-- liệt kê theo tính năng của module --> |
| **Ngoài phạm vi** | <!-- thứ người đọc dễ tưởng là thuộc module này nhưng không phải; ghi module nào giữ --> |
| **Giai đoạn** | <!-- chỉ ghi theo nguồn, vd MVP: … · GĐ2: … --> |

## 2. Thuật ngữ

<!-- Chỉ thuật ngữ riêng của module. Thuật ngữ chung: trỏ tới bảng thuật ngữ của dự án nếu có. -->

| Thuật ngữ | Nghĩa trong hệ mới |
|---|---|

## 3. Tác nhân

| Tác nhân | Là ai | Làm gì với module này |
|---|---|---|
<!-- vd: người dùng cuối, hệ thống tích hợp qua API, nhân viên vận hành, service khác -->

## 4. Yêu cầu nghiệp vụ

| Mã | Yêu cầu | Nguồn | Giai đoạn | Ghi chú |
|---|---|---|---|---|
| BR-<MODULE>-001 | <!-- một câu, một yêu cầu, kiểm được --> | <!-- file/dòng, ghi chú họp, quyết định, tài liệu hệ cũ --> | | |

## 5. Luồng sử dụng

### UC-<MODULE>-01 — <tên luồng>

- **Tác nhân:** …
- **Điều kiện trước:** …
- **Luồng chính:** 1. … 2. …
- **Ngoại lệ:** <!-- mỗi ngoại lệ: hệ thống làm gì, người dùng thấy gì -->
- **Kết quả:** …
- **Thoả BR:** BR-<MODULE>-001, …

## 6. Quy tắc nghiệp vụ

<!-- Công thức, giới hạn, thứ tự ưu tiên, trạng thái và chuyển trạng thái. Số liệu phải có nguồn, không có thì [cần xác nhận]. -->

## 7. Tiêu chí nghiệm thu

| Mã | Cho (Given) | Khi (When) | Thì (Then) | Thoả BR |
|---|---|---|---|---|
| AC-<MODULE>-001 | | | <!-- kết quả đo được: số, trạng thái, mã lỗi. Không dùng "nhanh", "thân thiện" --> | BR-<MODULE>-001 |

<!-- Dữ liệu cá nhân trong ví dụ / tiêu chí: chỉ dùng dữ liệu mẫu dự án cho phép, không dùng dữ liệu thật. -->

## 8. Dữ liệu

| Thực thể | Trường chính | Chứa PII? | Giữ bao lâu | Ghi chú |
|---|---|---|---|---|

<!-- Chỉ mức nghiệp vụ. Thiết kế bảng làm ở bước thiết kế CSDL. Không dùng tên bảng / cột của hệ cũ. -->

## 9. Tích hợp với module khác

| Hướng | Module | Hợp đồng / sự kiện | Dùng để | Trạng thái |
|---|---|---|---|---|
| Cung cấp | | | | Đã có / Cần thêm |
| Dùng | | | | |
| Phát sự kiện | | `topic` | | |
| Nghe sự kiện | | `topic` | | |

<!-- Cần hợp đồng mới ⇒ ghi "Cần thêm", chốt với owner module kia trước khi code. -->

## 10. Đối chiếu hệ cũ

| Hành vi của hệ cũ | Nguồn | Hệ mới | Căn cứ |
|---|---|---|---|
| | | Giữ / Đổi / Bỏ | <!-- giữ phải có căn cứ độc lập: quyết định đã chốt, tài liệu bên thứ ba --> |

<!-- Dự án không có hệ cũ: ghi "Không áp dụng" + lý do. -->

## 11. Yêu cầu phi chức năng

| Hạng mục | Yêu cầu | Nguồn |
|---|---|---|
| Sản lượng / độ trễ | `[cần xác nhận: số liệu đo được]` | |
| Tiền | <!-- nếu module chạm tiền: độ chính xác, chống ghi trùng, đối soát --> | |
| Thông báo / gửi tin | <!-- nếu module gửi tin: không gửi trùng, timeout không tính là thành công --> | |
| Bảo mật / PII | | |

## 12. Câu hỏi mở

| # | Câu hỏi | Hỏi ai | Chặn BR nào |
|---|---|---|---|

## 13. Lịch sử thay đổi

- YYYY-MM-DD — Bản đầu.
