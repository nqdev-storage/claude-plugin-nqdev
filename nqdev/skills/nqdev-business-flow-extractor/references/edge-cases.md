# Trường hợp khó khi trích xuất luồng

| Tình huống | Cách xử lý |
|---|---|
| Không tìm thấy entry point | Liệt kê tối đa 5 ứng viên gần nhất kèm `file:line`, hỏi người dùng chọn. Không tự chọn rồi viết như thể chắc chắn. |
| Logic nằm ngoài source (stored procedure, trigger, cấu hình, rule engine, dịch vụ bên thứ ba) | Mô tả tới chỗ gọi ra ngoài; phần bên trong ghi `[cần xác nhận với BA/dev]` và đưa vào "Câu hỏi còn mở". Có file `.sql` trong repo thì đọc và truy vết như code. |
| Feature flag, cấu hình theo môi trường | Ghi điều kiện bật/tắt thành nhánh trong sơ đồ; giá trị thật theo môi trường là câu hỏi còn mở. |
| Code chết hoặc nhánh không ai gọi | Không đưa vào luồng chính. Ghi riêng ở Phụ lục với ghi chú "không thấy nơi gọi". |
| Nhiều phiên bản cùng tồn tại (v1/v2, controller cũ và mới) | Hỏi phiên bản cần mô tả; không gộp hai phiên bản vào một luồng. |
| Luồng đi qua nhiều service hoặc queue | Mỗi service là một làn trong sơ đồ (`subgraph`). Với `--depth=external`, đi tiếp qua queue tới consumer; thiếu source của service bên kia thì dừng ở ranh giới và ghi câu hỏi. |
| Xử lý bất đồng bộ, retry, timeout | Ghi rõ trong luồng lỗi: số lần thử, thời gian chờ, trạng thái dữ liệu khi hết lượt thử (theo code, không theo giả định). |
| Tài liệu cũ mâu thuẫn với code | Mô tả theo code; ghi mâu thuẫn vào "Câu hỏi còn mở" để BA quyết định. |
| Yêu cầu quá rộng ("toàn bộ module đơn hàng") | Đề xuất danh sách luồng con, hỏi chọn một luồng chạy trước. |
