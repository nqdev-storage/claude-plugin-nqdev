# Style Guide — Tài liệu hướng dẫn sử dụng

> File này là **nguồn sự thật** về format của toàn bộ user guide. Mọi đợt viết phải đọc file
> này trước. Muốn đổi quy ước → sửa ở đây trước, ghi lý do vào "Nhật ký" trong `DOC-PLAN.md`,
> rồi mới áp dụng và rà lại các file đã viết.

Cập nhật lần cuối: _(điền ngày)_

---

## 1. Ngôn ngữ & giọng văn

- Viết bằng **tiếng Việt**, xưng hô trung tính ("bạn" cho người dùng, hoặc câu mệnh lệnh: "Nhấn nút…").
- Viết cho **người dùng cuối**: chỉ nói về thao tác trên giao diện. Không nhắc tên hàm, class, bảng DB, API endpoint, tên file mã nguồn.
- Câu ngắn, chủ động. Mỗi bước = 1 hành động.
- Nhãn trên giao diện (nút, menu, trường) in **đậm**: nhấn **Lưu**, mở menu **Báo cáo**.
- Đường dẫn thao tác nhiều cấp dùng `→`: **Cấu hình → Người dùng → Thêm mới**.

## 2. Cấu trúc heading

| Cấp | Dùng cho |
|-----|----------|
| `#` (H1) | Tên module — mỗi file module đúng 1 H1 |
| `##` (H2) | Tên một tính năng / chức năng |
| `###` (H3) | Các phần trong tính năng: Mục đích, Tiền điều kiện, Các bước, Ví dụ, Lỗi thường gặp… |
| `####` (H4) | Chỉ khi thật cần chia nhỏ một phần |

Thứ tự các phần trong mỗi tính năng (H3) — giữ cố định:
1. Mục đích
2. Đối tượng sử dụng / Khi nào dùng
3. Tiền điều kiện
4. Các bước thực hiện
5. Ví dụ minh họa
6. Lỗi thường gặp & lưu ý

## 3. Đánh số các bước

- Dùng danh sách đánh số `1.` `2.` `3.` cho "Các bước thực hiện".
- Mỗi bước một hành động. Kết quả của bước (nếu cần) viết ngay sau, cùng dòng hoặc xuống dòng thụt lề.
- Bước có nhánh điều kiện: dùng gạch đầu dòng con.
  ```
  3. Chọn hình thức thanh toán:
     - **Tiền mặt**: nhập số tiền khách đưa.
     - **Chuyển khoản**: chọn ngân hàng và nhập mã giao dịch.
  ```

## 4. Placeholder ảnh (BẮT BUỘC đúng format này)

```md
<!-- SCREENSHOT: [mô tả cảnh cần chụp] | Gợi ý: [trạng thái màn hình, phần tử cần làm nổi bật] -->
![<caption ngắn>](./images/<module-slug>-<NN>-<mo-ta-ngan>.png)
```

- `<NN>`: số thứ tự 2 chữ số trong phạm vi module, tăng dần theo thứ tự xuất hiện (`01`, `02`…).
- Đặt ảnh đúng chỗ trong luồng, nơi người đọc cần nhìn màn hình (thường ngay sau bước mở màn hình, và sau bước điền form).
- Tối thiểu 1 ảnh cho mỗi màn hình chính. Không chèn ảnh cho thao tác hiển nhiên.
- Tên file ảnh: viết thường, bỏ dấu, nối bằng `-`.

## 5. Ví dụ minh họa

- Luôn có **dữ liệu mẫu cụ thể** (tên, số, ngày thật sự) — không viết chung chung "nhập thông tin".
- Nêu rõ **kết quả mong đợi** sau khi làm xong ví dụ.
- Trình bày dạng khối:
  > **Tình huống:** …
  > **Nhập:** …
  > **Kết quả:** …

## 6. Đặt tên file

- File module: `<module-slug>.md` — slug viết thường, bỏ dấu, thay khoảng trắng bằng `-`.
- Ảnh: `images/<module-slug>-<NN>-<mo-ta>.png`.

## 7. Liên kết chéo

- Link tới module khác bằng đường dẫn tương đối: `[Quản lý khách hàng](./quan-ly-khach-hang.md)`.
- Link tới một tính năng cụ thể: `[Tạo đơn hàng](./quan-ly-don-hang.md#tạo-đơn-hàng)`.
- Ở đầu mỗi file module, nếu phụ thuộc module khác → ghi ở phần "Liên quan".

## 8. Bảng thuật ngữ thống nhất

> Điền dần khi phát hiện thuật ngữ mới. Mỗi khái niệm chỉ dùng **một** từ duy nhất trong toàn tài liệu.

| Thuật ngữ chuẩn dùng trong tài liệu | Nghĩa / ngữ cảnh | Không dùng (biến thể cần tránh) |
|---|---|---|
| _(ví dụ)_ Đơn hàng | Phiếu ghi nhận yêu cầu mua của khách | order, phiếu đặt hàng, PO |
| | | |
| | | |

## 9. Từ viết tắt

| Viết tắt | Nghĩa đầy đủ |
|---|---|
| | |
