# Lĩnh vực `debug` — truy nguyên nhân một lỗi cụ thể

**Đầu ra:** nguyên nhân gốc + cách sửa. Đây là lĩnh vực **dễ hỏng nhất vì thiếu dữ kiện**.

## Mục bắt buộc thêm vào mẫu full

- **Triệu chứng**: điều gì đang xảy ra (nguyên văn thông báo lỗi / hành vi sai).
- **Kỳ vọng**: đáng lẽ phải ra sao.
- **Cách tái hiện**: thao tác nào, input nào, tần suất (luôn luôn / ngẫu nhiên).
- **Môi trường**: local / dev / production, phiên bản, mới xảy ra từ khi nào.
- **Đã loại trừ những gì**: tránh AI lặp lại việc user đã thử.

## Checklist đặc thù

- [ ] **Có log / stacktrace thật chưa?** Không có → HỎI TRƯỚC, đây là thông tin cốt tử.
- [ ] **Mới phát sinh hay có từ đầu?** Nếu mới → hỏi thay đổi gần nhất (commit/deploy/đổi config).
- [ ] **Xảy ra với mọi trường hợp hay chỉ một số dữ liệu?**
- [ ] **Yêu cầu tìm nguyên nhân gốc trước khi vá** — cấm sửa triệu chứng bằng try/catch nuốt lỗi.
- [ ] **Được sửa luôn hay chỉ chẩn đoán?** Hai đầu ra khác nhau.
- [ ] **Có được chạy lệnh / query DB để kiểm chứng không.**

## Quy tắc riêng

Nếu prompt thô không có **triệu chứng cụ thể** hoặc **thông báo lỗi**, dừng lại hỏi tối đa 2 câu trước khi refine — refine một prompt debug rỗng dữ kiện chỉ tạo ra phỏng đoán.

## Ví dụ rút gọn

**Thô:** *"api báo lỗi 500 sửa giúp tôi"*

**Hỏi trước:** *"Bạn cho tôi (1) nguyên văn log/stacktrace lỗi, (2) endpoint nào và môi trường nào?"*

**Refined (trích):**

```
## Mục tiêu
Tìm nguyên nhân gốc của lỗi 500 tại endpoint <X> và đề xuất cách sửa.

## Triệu chứng
- Nguyên văn lỗi: <paste>
- Kỳ vọng: trả về 200 kèm <dữ liệu>
- Tái hiện: <thao tác>, xảy ra <luôn/ngẫu nhiên>
- Môi trường: <dev/prod>, bắt đầu từ <thời điểm>

## Yêu cầu cụ thể
1. Đọc code theo stacktrace, xác định dòng ném lỗi
2. Truy ngược nguyên nhân gốc, phân biệt rõ với triệu chứng
3. Đề xuất cách sửa + cách kiểm chứng đã hết lỗi

## Ràng buộc
- Không vá bằng cách nuốt exception
- Chẩn đoán trước, chỉ sửa code khi tôi đồng ý

## Tiêu chí hoàn thành
- Chỉ ra được file:line gây lỗi và giải thích vì sao dữ liệu đi tới đó lại sai
```
