# Đầu vào là BRD/PRD (từ nqdev-brd-prd-writer)

Chỉ đọc file, không sửa. Khuôn BRD của repo (`docs/brd/_TEMPLATE.md`) thắng khuôn đóng kèm; nếu tên mục khác thì tra theo nghĩa.

## Đọc gì, ở đâu

| Cần biết | Tra ở (BRD) |
|---|---|
| Phạm vi, giai đoạn | Mục 1 và cột "Giai đoạn" của mục 4 |
| Tác nhân, ai dùng | Mục 3 |
| Đơn vị estimate | Mục 4 (BR); PRD mục 5 (FR, trỏ về BR) |
| Tiêu chí nghiệm thu | Mục 7 (AC) |
| Dữ liệu, PII, thời gian lưu | Mục 8 |
| Tích hợp module khác | Mục 9 |
| Hệ cũ cần đối chiếu/migrate | Mục 10 |
| Sản lượng, độ trễ, bảo mật | Mục 11 |
| Điểm còn mở | Mục 12 "Câu hỏi mở" (cột "Hỏi ai", "Chặn BR nào") |

Tra các mục trên trước, chỉ hỏi người dùng phần BRD/PRD không trả lời được.

## Quy tắc estimate

1. **Đơn vị là BR (PRD: FR).** Mỗi dòng estimate ghi mã phủ, ví dụ `BR-INVOICE-001, 002`. Được gom BR nhỏ cùng một tính năng thành một dòng nhưng phải liệt kê mã. BR không có dòng nào thì liệt kê riêng ở cuối. BR "Đã bỏ" không estimate, chỉ ghi chú đã bỏ qua.
2. **Giai đoạn theo nguồn.** Dùng nguyên cột "Giai đoạn". BR không ghi giai đoạn thì xếp tạm theo ưu tiên và ghi "chưa có trong nguồn". Muốn đề xuất khác: gắn nhãn "đề xuất đổi" kèm lý do, không ghi đè.
3. **`[cần xác nhận]` và "Câu hỏi mở".** BR bị chặn thì dùng range rộng và ghi câu hỏi chặn nó (số `#` trong mục 12). Câu hỏi clarify lấy từ "Câu hỏi mở" trước, tối đa 5, ưu tiên câu làm đổi estimate nhiều nhất; phần còn lại chỉ tham chiếu số `#`, không viết lại. NFR còn `[cần xác nhận]` (mục 11) thì không estimate như đã rõ.
4. **Tích hợp.** Dòng "Cần thêm" ở mục 9 là rủi ro tích hợp: nêu trong Rủi ro và cộng hệ số tích hợp nếu hợp đồng chưa có docs/test env.
5. **Hệ cũ.** Mục 10 có hành vi "Giữ/Đổi" kèm dữ liệu cần migrate thì nêu trong Exclusions hoặc estimate riêng nếu nguồn yêu cầu rõ; không tự cộng migrate.

## Nhiều file, nhiều module

- Mỗi module một file BRD. Đọc từng file, estimate theo BR, tổng hợp một lần.
- Tính năng vắt ngang module: module giữ logic chính tính đầy đủ; module kia chỉ tính phần của mình (BR trỏ mã BR của module chính). Không cộng hai lần.
- Hợp đồng/sự kiện giữa hai module ghi ở mục 9 của cả hai file: tính một lần, nêu ở module cung cấp.

## Khi nguồn lệch nhau

BRD/PRD và mô tả của người dùng nói khác nhau: không tự chọn. Ghi mâu thuẫn vào câu hỏi clarify, estimate tạm theo BRD/PRD và nói rõ đã chọn như vậy.

## Không làm

- Không ghi vào `docs/brd`, `docs/prd`; không sửa mã BR/AC/UC/FR.
- Không viết thêm yêu cầu mới; yêu cầu thiếu thì nêu thành câu hỏi và gợi ý `nqdev-brd-prd-writer` cập nhật.
- Không dựng ngược yêu cầu từ source code.
