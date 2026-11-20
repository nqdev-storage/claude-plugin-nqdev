# Edge cases

| Tình huống | Xử lý |
|---|---|
| Không rõ module | Hỏi trước khi viết. Repo có bảng module trong `docs/brd/README.md` thì đưa danh sách đó làm lựa chọn |
| Module không có trong bảng của README | Không tự thêm vào bảng. Hỏi người dùng tên file, rồi nhắc owner bổ sung bảng |
| File `docs/brd/<module>.md` đã tồn tại | Cập nhật tại chỗ, giữ mã cũ, cấp số tiếp theo, thêm dòng "Lịch sử thay đổi". Không viết đè từ đầu |
| Bỏ một yêu cầu đã phát hành | Giữ dòng và mã, ghi "Đã bỏ" + lý do ở cột Ghi chú; AC liên quan ghi "Đã bỏ" tương ứng |
| Tính năng vắt ngang nhiều module | Module giữ logic chính viết BR đầy đủ; module kia viết phần của mình, trỏ mã BR module chính; ghi hợp đồng/sự kiện ở mục 9 cả hai file. Chỉ được giao một module thì viết module đó và liệt kê phần cần owner kia viết vào "Câu hỏi mở" |
| Đầu vào quá mỏng (1–2 câu) | Hỏi 1 lượt tối đa 4 câu; không có người trả lời thì giữ đủ 13 mục, điền `[cần xác nhận]`, ghi "Độ đầy đủ: thấp" ở dòng Nguồn |
| Hai yêu cầu mâu thuẫn | Không tự chọn. Ghi cả hai vào "Câu hỏi mở" kèm nguồn và người quyết định; BR liên quan gắn `[cần xác nhận]` |
| Yêu cầu là giải pháp kỹ thuật ("dùng Redis") | BR nêu nhu cầu nghiệp vụ gốc; giải pháp ghi ở Ghi chú kèm `[cần xác nhận: lý do nghiệp vụ]` |
| Yêu cầu không đo được ("nhanh", "dễ dùng") | Không đưa vào AC. Ghi `[cần xác nhận: ngưỡng đo được]` và thêm vào "Câu hỏi mở" |
| Số liệu chỉ có ở hệ cũ, chưa ai chốt | Ghi ở mục 10 với nguồn; không chép sang mục 6 hay 11 như quy tắc mới khi chưa có căn cứ độc lập |
| Dự án không có hệ cũ | Mục 10 giữ tiêu đề, ghi "Không áp dụng" + lý do |
| Khuôn repo khác khuôn đóng kèm | Theo khuôn repo, không "sửa cho giống" khuôn đóng kèm |
| Người dùng muốn PRD | Viết BRD trước (hoặc dùng BRD đã có), rồi PRD theo `prd-template.md`, FR trỏ về BR |
| Đòi ước lượng | Không làm trong skill này; gợi ý `nqdev-requirement-estimator` |
| Đưa source code | Nói rõ skill không dựng yêu cầu từ code; đề nghị người dùng đưa tài liệu hệ cũ hoặc mô tả hành vi cần giữ. Chỉ dùng code khi người dùng nói rõ là bối cảnh phụ: hành vi đọc từ code chỉ ghi ở mục 10 kèm nguồn (file) và `[cần xác nhận]`, không tính là căn cứ để "Giữ". Người dùng muốn tài liệu luồng nghiệp vụ dựng từ code thì gợi ý skill `nqdev-business-flow-extractor` (không tự chuyển) |
