# Lĩnh vực `analyze` — đọc hiểu / phân tích hệ thống có sẵn

**Đầu ra:** hiểu biết được viết ra (mô tả luồng, sơ đồ, danh sách phụ thuộc, bảng tổng hợp) — **không sửa code**.

## Mục bắt buộc thêm vào mẫu full

- **Điểm bắt đầu trace**: entry point cụ thể (controller/action, hàm, queue consumer, job). Không có → hỏi hoặc `[cần xác nhận]`.
- **Độ sâu**: dừng ở tầng nào (chỉ service, hay xuống tới DB / hệ thống ngoài).
- **Góc nhìn**: luồng dữ liệu, luồng nghiệp vụ, hay quan hệ phụ thuộc giữa module.

## Checklist đặc thù

- [ ] **Phạm vi rõ**: 1 tính năng / 1 module / cả service? Đây là chỗ prompt hay quá rộng nhất.
- [ ] **Bắt buộc đọc source trước khi kết luận** — nêu thẳng trong prompt để tránh trả lời bằng phỏng đoán.
- [ ] **Mọi khẳng định phải kèm file:line** làm bằng chứng.
- [ ] **Định dạng đầu ra**: văn xuôi, bảng, sơ đồ mermaid, hay file markdown lưu lại.
- [ ] **Được phép nêu nhận xét cải tiến không**, hay chỉ mô tả hiện trạng (rất hay lẫn sang `review`).

## Bẫy hay gặp

- "phân tích giúp tôi module X" — không giới hạn độ sâu sẽ ra một bản trả lời dài vô ích. Refined phải chốt độ sâu + số mục tối đa.
- Nếu user thật ra muốn biết *nên sửa gì* → đó là `review`, không phải `analyze`.

## Ví dụ rút gọn

**Thô:** *"đọc giúp tôi luồng gửi tin nhắn chạy thế nào"*

**Refined (trích):**

```
## Mục tiêu
Mô tả luồng xử lý một tin nhắn từ lúc nhận request tới lúc có kết quả gửi.

## Yêu cầu cụ thể
1. Bắt đầu trace từ [entry point cụ thể]
2. Đi theo thứ tự thực thi, nêu rõ mỗi bước: file:line, việc làm, dữ liệu vào/ra
3. Đánh dấu các điểm bất đồng bộ (queue, job nền) và điều gì xảy ra nếu bước đó lỗi

## Output format
Danh sách các bước đánh số + sơ đồ mermaid tổng quan ở cuối

## Ràng buộc
- Chỉ mô tả hiện trạng, không đề xuất cải tiến
- Mọi bước phải kèm file:line, không suy đoán

## Tiêu chí hoàn thành
- Trace liền mạch từ entry point tới bước cuối, không đứt đoạn
- Nêu được các nhánh lỗi chính
```
