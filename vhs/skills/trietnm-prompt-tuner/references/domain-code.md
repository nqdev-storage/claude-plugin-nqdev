# Lĩnh vực `code` — viết / sửa / refactor code

**Đầu ra:** thay đổi thật trong repo (file mới, hàm mới, tính năng mới, code đã dọn lại).

## Mục bắt buộc thêm vào mẫu full

- **Điểm xuất phát**: file/hàm/module sẽ sửa, hoặc nơi hợp lý để đặt code mới (lấy từ context probe, không đoán).
- **Quy ước phải tuân theo**: lấy từ `CLAUDE.md`/`AGENTS.md` nếu có; không có thì ghi "bám theo code xung quanh" thay vì áp chuẩn ngoài.
- **Phạm vi được phép đụng**: chỉ file nào, có được sửa file chung / migration / config không.

## Checklist đặc thù (prompt lĩnh vực này hay thiếu)

- [ ] **Sửa hay viết mới?** Sửa code có sẵn và viết từ đầu cho ra kết quả rất khác.
- [ ] **Hành vi mong muốn cụ thể** — input gì, output gì, case biên nào phải xử lý.
- [ ] **Có được đổi API/interface hiện tại không** (breaking change) hay phải giữ tương thích.
- [ ] **Có cần test kèm không** — viết test, hay chỉ code.
- [ ] **Có cần chạy thử / build không**, hay chỉ cần code trên file.
- [ ] **Ranh giới không được vượt**: không refactor lan man, không đổi format file khác, không thêm dependency mới nếu chưa cho phép.

## Bẫy hay gặp

- Prompt kiểu "làm giúp tôi tính năng X" mà không nói X hành xử thế nào → refined phải liệt kê câu hỏi hành vi dưới dạng `[cần xác nhận: ...]`, đừng tự thiết kế hộ.
- User nói "refactor" nhưng thực ra muốn "sửa bug" → nếu có dấu hiệu lỗi, quay lại `detect.md` cân nhắc `debug`.

## Ví dụ rút gọn

**Thô:** *"thêm nút export excel cho màn hình danh sách khách hàng"*

**Refined (trích):**

```
## Mục tiêu
Thêm chức năng export Excel cho màn hình danh sách khách hàng.

## Context
- Repo <root>, branch <branch>; web ASP.NET MVC, grid dùng Kendo
- Màn hình liên quan: [CustomerList.cshtml](...) + action `CustomerList_Read`

## Yêu cầu cụ thể
1. Đọc code màn hình hiện tại trước khi sửa
2. Thêm nút Export cạnh thanh filter, dùng đúng thư viện export đang có trong repo
3. File xuất giữ nguyên bộ lọc đang áp dụng trên grid

## Ràng buộc
- Không thêm thư viện mới nếu repo đã có sẵn giải pháp export
- Chỉ sửa file thuộc màn hình này

## Tiêu chí hoàn thành
- Export ra đúng số dòng đang hiển thị theo filter
- [cần xác nhận: xuất toàn bộ kết quả hay chỉ trang hiện tại?]
- [cần xác nhận: cần cột nào, có giới hạn số dòng tối đa không?]
```
