# Lĩnh vực `docs` — tài liệu, BRD, mô tả task, hướng dẫn

**Đầu ra:** văn bản cho **người khác đọc**. Lĩnh vực này khác mọi lĩnh vực còn lại ở một điểm: đối tượng đọc quyết định tất cả.

## Mục bắt buộc thêm vào mẫu full

- **Ai đọc**: dev trong team / QA / PM / khách hàng / người dùng cuối / bản thân sau 6 tháng. Bắt buộc phải có.
- **Đọc để làm gì**: để làm theo, để duyệt, để ước lượng, để tra cứu.
- **Độ dài & nơi đăng**: Jira, Confluence, README trong repo, file markdown, slide.
- **Giọng văn & ngôn ngữ**: tiếng Việt hay Anh, có được dùng thuật ngữ kỹ thuật không.

## Checklist đặc thù

- [ ] **Dựa trên gì để viết?** Source code, BRD cũ, ghi chú họp — nêu rõ nguồn, cấm bịa nội dung nghiệp vụ.
- [ ] **Cấu trúc bắt buộc**: có template sẵn của công ty/dự án không (mục tiêu, phạm vi, AC, luồng...).
- [ ] **Mức chi tiết**: tóm tắt nửa trang hay tài liệu đầy đủ.
- [ ] **Có cần ảnh/sơ đồ không** — nếu có thì chèn placeholder ở đâu.
- [ ] **Phần nào KHÔNG viết** (VD: không viết phần ước lượng thời gian, không suy đoán roadmap).
- [ ] **Lưu ở đâu**: in ra chat, hay ghi thành file trong repo.

## Bẫy hay gặp

- Thiếu "ai đọc" → tài liệu viết cho dev nhưng gửi khách hàng, hoặc ngược lại. Đây là lỗi số một của lĩnh vực này.
- Với BRD/mô tả task dựng từ code: prompt phải ép **đọc code trước**, và ghi rõ chỉ mô tả cái code thật sự làm, không mô tả cái "đáng lẽ nên làm".

## Ví dụ rút gọn

**Thô:** *"viết mô tả cho task này để add vào Jira"*

**Refined (trích):**

```
## Mục tiêu
Viết mô tả ngắn gọn cho task <tên> để đưa vào Jira.

## Context
- Đối tượng đọc: PM, QA và dev trong team
- Nguồn tham chiếu: <các file/module liên quan trong repo, kèm đường dẫn>

## Yêu cầu cụ thể
1. Đọc code liên quan trước, mô tả đúng phạm vi đã/sẽ làm
2. Gồm 3 phần: Bối cảnh & vấn đề / Phạm vi công việc / Acceptance criteria
3. Phạm vi tách rõ theo từng service hoặc từng màn hình

## Output format
Markdown, tối đa 1 màn hình đọc, dùng bullet, có tiêu đề task đề xuất

## Ràng buộc
- Tiếng Việt, giữ nguyên thuật ngữ kỹ thuật
- Không ước lượng thời gian, không suy đoán tính năng chưa có trong code

## Tiêu chí hoàn thành
- Acceptance criteria kiểm chứng được bằng thao tác cụ thể
- Người đọc không cần mở source vẫn hiểu task làm gì
```
