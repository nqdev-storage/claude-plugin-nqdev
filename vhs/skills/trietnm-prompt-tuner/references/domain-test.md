# Lĩnh vực `test` — test case, test code, kế hoạch kiểm thử

**Đầu ra:** code test chạy được, hoặc bộ test case cho QA.

## Mục bắt buộc thêm vào mẫu full

- **Loại test**: unit / integration / e2e / test thủ công cho QA. Bốn thứ này viết hoàn toàn khác nhau.
- **Framework & quy ước**: lấy từ repo (xUnit/NUnit/MSTest, Jest/Vitest, Playwright/Cypress...) và thư mục test đang đặt ở đâu.
- **Đối tượng test**: hàm/class/endpoint/màn hình cụ thể.
- **Phụ thuộc bên ngoài**: DB, API ngoài, queue — mock hay dùng thật.

## Checklist đặc thù

- [ ] **Có repo test sẵn chưa?** Có thì bám theo mẫu đang có, đừng dựng khung mới.
- [ ] **Phạm vi case**: chỉ happy path, hay cả case biên và case lỗi.
- [ ] **Số lượng case mong muốn** — không nói thì AI viết 3 case qua loa hoặc 30 case thừa.
- [ ] **Dữ liệu test lấy đâu ra**: fixture, factory, hay dữ liệu thật đã ẩn danh.
- [ ] **Tiêu chí đậu**: coverage bao nhiêu, hay chỉ cần phủ các nhánh chính.
- [ ] **Có được sửa code sản phẩm để test được không** (thêm interface, tách hàm).

## Bẫy hay gặp

- Prompt "viết test cho file này" mà file có 15 hàm → refined phải chốt hàm nào, hoặc yêu cầu liệt kê rồi hỏi lại.
- Test case cho QA phải viết theo ngôn ngữ nghiệp vụ (thao tác + kết quả mong đợi), không phải ngôn ngữ code.

## Ví dụ rút gọn

**Thô:** *"viết unit test cho hàm tính giá"*

**Refined (trích):**

```
## Mục tiêu
Viết unit test cho hàm tính giá <tên hàm> tại [đường dẫn file].

## Context
- Framework test đang dùng: <lấy từ repo>, test đặt tại <thư mục>
- Phụ thuộc của hàm: <liệt kê từ code — DB, config, service khác>

## Yêu cầu cụ thể
1. Đọc hàm và các nhánh điều kiện bên trong trước khi viết
2. Viết test phủ: happy path, từng nhánh điều kiện, case biên (0, âm, null, vượt hạn mức)
3. Mock các phụ thuộc bên ngoài theo đúng cách repo đang mock

## Output format
File test theo đúng quy ước đặt tên trong repo

## Ràng buộc
- Không sửa code sản phẩm
- Mỗi test một khẳng định rõ ràng, tên test mô tả được tình huống

## Tiêu chí hoàn thành
- Phủ hết nhánh điều kiện của hàm
- Test chạy xanh, không phụ thuộc thứ tự chạy
- [cần xác nhận: có cần chạy thử bộ test không?]
```
