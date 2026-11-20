# Examples — nqdev-brd-prd-writer

Ví dụ minh hoạ (dự án giả định, không phải dữ liệu thật).

## Ví dụ 1 — Viết BRD cho một module

**Đầu vào:**
> Viết BRD cho module `orders`. Ghi chú họp 2026-11-10: cửa hàng ABC duyệt đơn sỉ qua chat, mỗi đơn mất vài giờ. Nhân viên bán hàng nhập đơn trên web, quản lý duyệt, kế toán xem đơn đã duyệt. Đơn trên 50 triệu cần giám đốc duyệt thêm.

**Kết quả:** file `docs/brd/orders.md`, đủ 13 mục theo khuôn. Trích:

Mục 4
| Mã | Yêu cầu | Nguồn | Giai đoạn | Ghi chú |
|---|---|---|---|---|
| BR-ORDERS-001 | Nhân viên bán hàng nhập đơn sỉ trên web | Ghi chú họp 2026-11-10 | `[cần xác nhận]` | |
| BR-ORDERS-002 | Quản lý duyệt hoặc từ chối đơn chờ duyệt | Ghi chú họp 2026-11-10 | `[cần xác nhận]` | |
| BR-ORDERS-003 | Đơn trên 50 triệu cần giám đốc duyệt thêm sau quản lý | Ghi chú họp 2026-11-10 | `[cần xác nhận]` | |

Mục 7
| Mã | Cho (Given) | Khi (When) | Thì (Then) | Thoả BR |
|---|---|---|---|---|
| AC-ORDERS-001 | Đơn 30 triệu ở trạng thái Chờ duyệt | Quản lý bấm Duyệt | Đơn chuyển sang Đã duyệt và có trong danh sách của kế toán | BR-ORDERS-002 |
| AC-ORDERS-002 | Đơn 60 triệu ở trạng thái Chờ duyệt | Quản lý bấm Duyệt | Đơn chuyển sang Chờ giám đốc duyệt | BR-ORDERS-003 |

Mục 10: "Không áp dụng — trước đây duyệt qua chat, không có hệ thống cũ."

Mục 12
| # | Câu hỏi | Hỏi ai | Chặn BR nào |
|---|---|---|---|
| 1 | Đơn đúng 50 triệu có cần giám đốc duyệt không? | Chủ cửa hàng | BR-ORDERS-003 |

Tóm tắt giao: `docs/brd/orders.md`, 3 BR, 3 AC, 2 UC, 5 mục `[cần xác nhận]`. Rủi ro: chưa có số liệu sản lượng cho mục 11.

## Ví dụ 2 — Không rõ module, đầu vào mỏng

**Đầu vào:** `Viết BRD cho phần đặt lịch khám.`

**Hành vi:** hỏi 1 lượt tối đa 4 câu (module nào, phạm vi chắc có/không, tác nhân chính, nguồn nghiệp vụ). Chạy tự động thì giữ đủ 13 mục, điền `[cần xác nhận]` và ghi "Độ đầy đủ: thấp" ở dòng Nguồn.

## Ví dụ 3 — Bỏ một yêu cầu đã phát hành

**Đầu vào:** `Bỏ BR-ORDERS-003, khách quyết định không cần giám đốc duyệt.`

**Hành vi:** giữ dòng BR-ORDERS-003, ghi "Đã bỏ — khách quyết định (nguồn, ngày)" ở Ghi chú; AC-ORDERS-002 ghi "Đã bỏ"; yêu cầu mới (nếu có) nhận mã BR-ORDERS-004; thêm dòng vào "Lịch sử thay đổi".

## Ví dụ 4 — Tính năng vắt ngang module

**Đầu vào:** `Thanh toán đơn nằm ở module billing (giữ logic chính), orders chỉ gọi sang. Viết phần của orders.`

**Hành vi:** `docs/brd/orders.md` thêm BR phần của orders, cột Ghi chú trỏ mã BR của billing (chưa có mã thì `[cần xác nhận: mã BR của billing]`); mục 9 thêm dòng "Dùng | billing | <hợp đồng> | … | Cần thêm". Không viết vào `docs/brd/billing.md`.

## Ví dụ 5 — Đòi ước lượng

**Đầu vào:** `Viết BRD xong ước lượng luôn mất bao nhiêu ngày.`

**Hành vi:** viết BRD, không ước lượng; gợi ý `nqdev-requirement-estimator`.
