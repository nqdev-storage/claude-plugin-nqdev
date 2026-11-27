# Examples (Gold Cases cho eval)

Dùng để so sánh bản cũ và bản mới. Chấm cứng pass/fail từng mục; đo thêm số token phần luôn nạp và độ lệch estimate giữa 3 lần chạy.

## TC1: Input mơ hồ, nhiều red flag

**Input**: "Làm app giống Grab để giao hàng nội bộ công ty, có theo dõi real-time, đơn giản thôi."

**Pass khi**
- Ra estimate dạng range kèm assumption, không chặn chờ trả lời, không chỉ một con số.
- Gắn cờ cả ba cụm "giống Grab", "real-time", "đơn giản thôi".
- Có tối đa 5 câu hỏi, ưu tiên: số tài xế/đơn đồng thời, mobile hay web, bản đồ/bên thứ ba.
- Exclusions có mobile native; MVP tách khỏi real-time.

**Fail khi**: chỉ hỏi lại mà không estimate, hoặc đưa một số duy nhất.

## TC2: Spec rõ, kiểm tra số học

**Input**: Web app kho nội bộ gồm login JWT, CRUD sản phẩm có validation, import CSV, dashboard stats cards. Team 2 DEV senior review, greenfield.

**Kỳ vọng (sai số ±10%)**
- Dev 19–33 giờ: AI 9.5–18, DEV review 9.5–15 (setup đã gồm JWT, không tính đôi auth).
- Tổng khoảng 22–39.5 giờ (đã gồm QA/UAT 15–20%); không có dòng PM và không quy ra số tuần.

**Pass khi**: mỗi module có 3 cột AI | DEV review | Tổng, bước 0.5 giờ; QA xuất hiện đúng một dòng; tổng khớp công thức; có exclusions; MVP hợp lý.

## TC3: Ràng buộc mâu thuẫn

**Input**: "Scope khoảng 80 giờ (Tổng), trong đó khoảng 40 giờ DEV review; deadline 1 tuần; team gồm 1 DEV review là junior."

**Pass khi**
- Áp hệ số junior × 1.4 lên cột DEV review (40 giờ thành khoảng 56 giờ) và so với quỹ giờ DEV 1 × 24 × 1 tuần = 24 giờ.
- Kết luận **không khả thi** và đưa ít nhất 2 phương án (cắt scope về MVP, thêm DEV review hoặc DEV senior, dời deadline) kèm số liệu (VD 1 DEV cần khoảng 2.3 tuần: 56 ÷ 24).

**Fail khi**: chỉ báo "80 giờ, 1 tuần" mà không kiểm tra khả thi, hoặc quy ra số tuần cho cột AI.

## TC4: Đầu vào là BRD (từ nqdev-brd-prd-writer)

BRD mẫu dựng cho eval, module `INVOICE`. Team: 2 DEV senior review, greenfield, chưa có deadline.

**Mục 1. Phạm vi**: Trong phạm vi: tạo, xuất, gửi, đồng bộ hóa đơn. Giai đoạn: MVP: BR-001, 002, 004 · GĐ2: BR-003.

**Mục 4. Yêu cầu nghiệp vụ**

| Mã | Yêu cầu | Nguồn | Giai đoạn |
|---|---|---|---|
| BR-INVOICE-001 | Hệ thống tạo hóa đơn từ đơn hàng đã xác nhận | Họp 2026-11-05 | MVP |
| BR-INVOICE-002 | Người dùng xuất hóa đơn ra PDF | Họp 2026-11-05 | MVP |
| BR-INVOICE-003 | Hệ thống gửi hóa đơn qua email cho khách | Họp 2026-11-05 | GĐ2 |
| BR-INVOICE-004 | Đồng bộ hóa đơn sang phần mềm kế toán `[cần xác nhận: tên phần mềm, có API và môi trường test không]` | Họp 2026-11-05 | MVP |
| BR-INVOICE-005 | Đã bỏ: in hóa đơn nhiều liên | Họp 2026-11-12 | |

**Mục 7. Tiêu chí nghiệm thu**: AC-INVOICE-001 đến 004, mỗi AC thoả một BR tương ứng (BR-005 đã bỏ nên không có AC).

**Mục 9. Tích hợp**: Dùng module ORDER, sự kiện `order.confirmed`, trạng thái **Cần thêm**.

**Mục 11. Phi chức năng**: số hóa đơn mỗi tháng `[cần xác nhận: số liệu đo được]`.

**Mục 12. Câu hỏi mở**

| # | Câu hỏi | Hỏi ai | Chặn BR nào |
|---|---|---|---|
| 1 | Phần mềm kế toán nào, có API và môi trường test? | Kế toán trưởng | BR-INVOICE-004 |
| 2 | Số hóa đơn mỗi tháng? | Owner module | Mục 11 |

**Input**: "Estimate module INVOICE theo BRD này, team 2 DEV senior review."

**Pass khi**
- Mỗi dòng estimate ghi mã BR phủ; BR-INVOICE-005 không có estimate, chỉ ghi chú đã bỏ.
- BR-INVOICE-003 ở GĐ2 theo nguồn; nếu đề xuất đổi thì có nhãn "đề xuất đổi" kèm lý do.
- BR-INVOICE-004 có range rộng (tích hợp bên thứ ba không có docs/test env) và ghi bị chặn bởi câu hỏi #1.
- Câu hỏi clarify lấy từ "Câu hỏi mở" (#1, #2), không hỏi lại tác nhân hay phạm vi đã có; tối đa 5 câu.
- `order.confirmed` ở trạng thái "Cần thêm" được nêu trong Rủi ro.
- Mỗi dòng có 3 cột AI | DEV review | Tổng (giờ, bước 0.5); QA đúng một dòng; tổng khớp công thức, không có PM và số tuần; kết quả trả trong chat, không ghi file vào `docs/brd`.

**Fail khi**: tự đặt module không có mã BR; estimate BR-INVOICE-005; đẩy BR-INVOICE-003 vào MVP không nhãn; estimate một số duy nhất cho BR-INVOICE-004; hỏi lại thứ BRD đã trả lời.
