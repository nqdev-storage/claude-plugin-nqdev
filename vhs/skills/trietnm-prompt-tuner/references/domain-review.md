# Lĩnh vực `review` — đánh giá chất lượng / bảo mật code có sẵn

**Đầu ra:** danh sách vấn đề có mức độ ưu tiên, kèm vị trí cụ thể.

## Mục bắt buộc thêm vào mẫu full

- **Đối tượng review**: diff hiện tại, 1 PR/branch, 1 file, hay 1 module. Rất hay bị bỏ sót.
- **Trục đánh giá**: chọn rõ trong số — đúng/sai logic, bảo mật, hiệu năng, khả năng bảo trì, tuân thủ quy ước repo.
- **Chuẩn đối chiếu**: quy ước trong `CLAUDE.md`/`AGENTS.md` của repo, KHÔNG áp chuẩn ngoài nếu repo không dùng.

## Checklist đặc thù

- [ ] **Chỉ review hay sửa luôn?** Mặc định nên là chỉ review.
- [ ] **Ngưỡng báo cáo**: chỉ vấn đề thật sự, hay cả gợi ý nhỏ về style.
- [ ] **Bắt buộc có mức độ**: Cao / Trung bình / Thấp — không có thì danh sách vô dụng để quyết định.
- [ ] **Mỗi vấn đề phải có file:line + kịch bản hỏng cụ thể**, không nhận xét chung chung kiểu "nên tách hàm".
- [ ] **Số lượng tối đa** để tránh báo cáo 40 mục không ai đọc.
- [ ] **Loại trừ**: bỏ qua code sinh tự động, thư viện bên thứ ba, file migration cũ.

## Bẫy hay gặp

- Không nói rõ trục đánh giá → AI rải đều mọi thứ, loãng.
- Không nói "chỉ nhận xét" → AI sửa code ngoài ý muốn.
- Đừng để AI bịa vi phạm quy ước: nếu repo không có tài liệu quy ước, prompt phải ghi "suy quy ước từ code xung quanh".

## Ví dụ rút gọn

**Thô:** *"review giúp tôi code này xem ổn chưa"*

**Refined (trích):**

```
## Mục tiêu
Review <đối tượng: diff hiện tại / file X> và liệt kê các vấn đề đáng sửa.

## Yêu cầu cụ thể
1. Đọc toàn bộ đối tượng review trước khi kết luận
2. Đánh giá theo 4 trục: đúng/sai logic, bảo mật, hiệu năng, khả năng bảo trì
3. Đối chiếu quy ước với code xung quanh trong cùng module

## Output format
Bảng: | # | Trục | Vấn đề | file:line | Mức độ | Cách sửa gợi ý |

## Ràng buộc
- Chỉ nhận xét, KHÔNG sửa code
- Mỗi vấn đề phải kèm kịch bản hỏng cụ thể, bỏ qua góp ý thuần style
- Tối đa 10 mục, ưu tiên mức Cao trước

## Tiêu chí hoàn thành
- Không có mục nào thiếu file:line
- Có phần kết luận: có nên merge hay không
```
