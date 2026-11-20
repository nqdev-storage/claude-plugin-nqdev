# Lĩnh vực `data` — schema, SQL, migration, tối ưu truy vấn

**Đầu ra:** DDL / câu query / kế hoạch migration / phương án tối ưu.

## Mục bắt buộc thêm vào mẫu full

- **DBMS + phiên bản**: Postgres/SQL Server/MySQL/Mongo... Cú pháp và khả năng khác nhau hoàn toàn — thiếu là không làm được.
- **Khối lượng dữ liệu**: số bản ghi hiện tại, tốc độ tăng. Quyết định việc có cần index/partition hay không.
- **Bảng liên quan**: lấy tên bảng và cột THẬT từ repo (model/entity/migration), không bịa tên.
- **Ràng buộc tương thích**: có được đổi bảng đang chạy không, có downtime không, có code cũ đang đọc bảng đó không.

## Checklist đặc thù

- [ ] **Đọc schema thật trước khi viết SQL** — nêu thẳng yêu cầu này trong prompt.
- [ ] **Quy ước đặt tên của repo** (snake_case, tiền tố `tbl_`, kiểu cột ngày giờ...) — suy từ các bảng có sẵn.
- [ ] **Migration phải có kịch bản rollback** và chạy được trên dữ liệu đang có.
- [ ] **Với tối ưu query**: có execution plan chưa? Không có thì yêu cầu phân tích trước, đừng đoán index.
- [ ] **Múi giờ / kiểu dữ liệu ngày giờ** — nguồn lỗi kinh điển.
- [ ] **Dữ liệu nhạy cảm**: có cột nào cần mã hoá / che khi trả ra không.

## Bẫy hay gặp

- Prompt "tối ưu câu query này" mà không có số lượng bản ghi và plan → câu trả lời chỉ là mẹo chung. Refined phải yêu cầu đọc plan hoặc ghi `[cần xác nhận]`.
- AI rất hay bịa tên cột. Prompt refined bắt buộc có câu: *"chỉ dùng tên bảng/cột có thật trong repo, trích dẫn file định nghĩa"*.

## Ví dụ rút gọn

**Thô:** *"thiết kế bảng lưu lịch sử gửi tin"*

**Refined (trích):**

```
## Mục tiêu
Thiết kế bảng lưu lịch sử gửi tin + DDL chạy được.

## Context
- DBMS: [cần xác nhận: SQL Server hay PostgreSQL, phiên bản nào]
- Bảng liên quan đang có: <lấy từ model/entity trong repo, kèm đường dẫn file>
- Khối lượng dự kiến: [cần xác nhận: số bản ghi/ngày và thời gian lưu trữ]

## Yêu cầu cụ thể
1. Đọc các entity/bảng liên quan trong repo trước khi thiết kế
2. Đề xuất cấu trúc bảng: cột, kiểu, khoá chính, khoá ngoại, index
3. Viết DDL theo đúng quy ước đặt tên đang dùng trong repo
4. Nêu phương án lưu trữ dài hạn (xoá theo hạn / phân vùng) nếu dữ liệu lớn

## Ràng buộc
- Chỉ dùng tên bảng/cột có thật, trích dẫn file định nghĩa cho từng bảng tham chiếu
- Không đổi cấu trúc bảng đang chạy
- Kèm script rollback

## Tiêu chí hoàn thành
- DDL chạy được không sửa tay
- Mỗi index có giải thích phục vụ truy vấn nào
```
