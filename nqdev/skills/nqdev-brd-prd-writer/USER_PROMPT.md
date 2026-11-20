# User Prompt Templates — nqdev-brd-prd-writer

## 1. Viết BRD cho một module
```
Dùng nqdev-brd-prd-writer viết BRD cho module <module>.
Nguồn: <mô tả / ghi chú họp / file chốt nghiệp vụ (dòng …) / tài liệu hệ cũ (đường dẫn)>
```
Kết quả lưu ở `docs/brd/<module>.md` theo khuôn `docs/brd/_TEMPLATE.md` của repo.

## 2. Cập nhật BRD đã có
```
Yêu cầu của module <module> thay đổi: <nội dung thay đổi, nguồn>.
Cập nhật docs/brd/<module>.md: giữ mã cũ, cấp mã mới cho yêu cầu thêm, ghi Lịch sử thay đổi.
```

## 3. Bỏ một yêu cầu
```
Bỏ BR-<MODULE>-<số> vì <lý do>. Cập nhật docs/brd/<module>.md, giữ mã và ghi "Đã bỏ".
```

## 4. Tính năng vắt ngang nhiều module
```
Tính năng <tên> nằm ở module <A> (giữ logic chính) và <B>.
Viết phần BR của module <B>, trỏ mã BR của <A>, ghi hợp đồng/sự kiện ở mục 9.
```

## 5. Viết thêm PRD (tuỳ chọn)
```
Dùng nqdev-brd-prd-writer viết PRD cho module <module> dựa trên docs/brd/<module>.md.
```
