# Lĩnh vực `architecture` — thiết kế hệ thống / chọn phương án

**Đầu ra:** một quyết định có lập luận (hoặc bảng so sánh phương án), không phải code.

## Mục bắt buộc thêm vào mẫu full

- **Bài toán thật sự cần giải**: nêu vấn đề, không nêu sẵn giải pháp (tránh prompt kiểu "dùng Kafka thế nào" khi vấn đề chỉ là chậm).
- **Ràng buộc bắt buộc**: stack hiện có, nhân sự, thời gian, ngân sách, hệ thống không được đụng vào.
- **Quy mô & tăng trưởng**: lượng request/bản ghi hiện tại và dự kiến — thiếu con số này thì mọi lời khuyên đều vô nghĩa.
- **Số phương án cần so sánh** và tiêu chí so sánh.

## Checklist đặc thù

- [ ] **Hiện trạng đang làm thế nào và vướng ở đâu?** Thiết kế mới phải bắt đầu từ đây.
- [ ] **Điều gì là bất biến** (không được đổi DB, phải giữ API cũ, phải chạy on-premise...).
- [ ] **Ưu tiên khi đánh đổi**: đơn giản, chi phí, hiệu năng, hay tốc độ triển khai? Mỗi lựa chọn ra kết quả khác nhau.
- [ ] **Yêu cầu nêu rõ nhược điểm của phương án được chọn** — nếu không, câu trả lời sẽ chỉ là quảng cáo.
- [ ] **Có cần đường đi chuyển đổi (migration path)** từ hiện trạng sang đích không.
- [ ] **Đầu ra dừng ở mức nào**: khuyến nghị, hay kèm sơ đồ / ADR / kế hoạch triển khai.

## Bẫy hay gặp

- Prompt đã chọn sẵn công nghệ rồi hỏi cách dùng → refined nên tách làm 2: (1) vấn đề cần giải, (2) công nghệ đang cân nhắc, và cho phép phản biện lựa chọn đó.
- Nếu user muốn thiết kế **rồi** implement luôn: giữ lĩnh vực `architecture`, ghi rõ implement là bước sau khi chốt thiết kế.

## Ví dụ rút gọn

**Thô:** *"có nên tách service gửi tin ra riêng không"*

**Refined (trích):**

```
## Mục tiêu
Đưa ra khuyến nghị: có nên tách phần gửi tin thành service riêng, kèm lập luận và nhược điểm.

## Context
- Hiện trạng: <mô tả cách đang chạy, lấy từ repo>
- Vướng mắc đang gặp: <cụ thể>
- Quy mô: [cần xác nhận: số tin/ngày hiện tại và dự kiến 12 tháng tới]

## Yêu cầu cụ thể
1. Tóm tắt hiện trạng dựa trên source code, chỉ ra điểm nghẽn thật sự
2. So sánh 3 phương án: giữ nguyên + tối ưu / tách service / giải pháp trung gian
3. Với mỗi phương án: ưu, nhược, chi phí chuyển đổi, rủi ro vận hành
4. Khuyến nghị 1 phương án + đường đi chuyển đổi theo giai đoạn

## Output format
Bảng so sánh + phần khuyến nghị + phần "khi nào KHÔNG nên chọn phương án này"

## Ràng buộc
- Không đề xuất đổi DBMS hoặc viết lại từ đầu
- Bám vào stack repo đang dùng

## Tiêu chí hoàn thành
- Mỗi phương án có ít nhất 2 nhược điểm cụ thể, không chung chung
```
