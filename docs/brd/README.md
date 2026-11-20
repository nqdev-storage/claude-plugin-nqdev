# Tài liệu yêu cầu nghiệp vụ (BRD)

Thư mục này chứa BRD của plugin `nqdev`, **mỗi module một file**. BRD nói module phải làm gì và thế nào là đúng. BRD không mô tả cách code.

## Danh sách module

| Module | File | Owner | Trạng thái | Cập nhật |
|---|---|---|---|---|
| `NQDEV`: plugin `nqdev` (skill, command, workflow, marketplace) | [nqdev.md](nqdev.md) | Nguyễn Quý | Nháp | 2026-11-18 |

Thêm module mới, đổi trạng thái hay ngày cập nhật của file BRD nào thì cập nhật dòng tương ứng trong bảng này.

## Viết BRD mới

1. Copy [_TEMPLATE.md](_TEMPLATE.md) thành `<module>.md`. Tên file viết thường, dạng kebab-case.
2. Hoặc gọi skill: `/nqdev:nqdev-brd-prd-writer`. Skill tự đọc file này và khuôn.
3. Thêm một dòng vào bảng "Danh sách module" ở trên.

## Quy ước

### Khuôn

- Giữ đủ 13 mục của khuôn, đúng tên và thứ tự. Mục không áp dụng thì giữ tiêu đề và ghi "Không áp dụng" kèm lý do.
- Viết xong thì xoá hết chú thích `<!-- … -->`.
- Viết tiếng Việt, giữ nguyên thuật ngữ kỹ thuật.

### Mã định danh

| Loại | Dạng | Ví dụ |
|---|---|---|
| Yêu cầu | `BR-<MODULE>-<3 chữ số>` | `BR-NQDEV-011` |
| Tiêu chí nghiệm thu | `AC-<MODULE>-<3 chữ số>` | `AC-NQDEV-011` |
| Luồng sử dụng | `UC-<MODULE>-<2 chữ số>` | `UC-NQDEV-02` |

- `<MODULE>` là tên module viết hoa, trùng cột Module ở bảng trên.
- Mỗi BR có ít nhất một AC. Mỗi UC có dòng "Thoả BR".
- Mã đã phát hành thì không đổi và không dùng lại. Bỏ một yêu cầu thì giữ mã, ghi "Đã bỏ" kèm lý do.
- Mã BR/AC được các skill khác dùng lại: `nqdev-feature-implementer`, `nqdev-code-review`, `nqdev-merge-request-writer`, `nqdev-release-note-writer`. Đổi mã sẽ làm hỏng truy vết.

### Nội dung

- **Không bịa.** Số liệu, tên, ngày, quy tắc không có nguồn thì ghi `[cần xác nhận: …]` và đưa vào mục "Câu hỏi mở".
- **Mỗi BR có nguồn.** Nguồn hợp lệ: ghi chú họp, quyết định đã chốt, tài liệu sản phẩm (README, `docs/`) kèm số dòng. Không dựng ngược yêu cầu từ code.
- **AC đo được.** Viết dạng Cho / Khi / Thì, kết quả là số, trạng thái, mã lỗi hoặc nội dung file. Không dùng "nhanh", "thân thiện".
- **Không ước lượng.** Thời gian và chi phí làm bằng `nqdev-requirement-estimator`, không ghi trong BRD.

### Dữ liệu mẫu

- Không dùng dữ liệu thật: email, token, domain công ty, đường dẫn máy cá nhân. Thư mục này nằm trên site công khai.
- Domain Jira mẫu: `https://<your-domain>.atlassian.net`. Email mẫu: `you@example.com`.
- Số điện thoại mẫu: chỉ dùng `0909090909` hoặc `0765418062`.

## Trạng thái và duyệt

```
Nháp → Chờ duyệt → Đã duyệt (người duyệt, ngày)
```

- Trạng thái ghi ở dòng đầu file BRD và ở bảng trên. Hai chỗ phải khớp nhau.
- Mọi thay đổi sau khi duyệt đều ghi một dòng vào mục "Lịch sử thay đổi" của file. Thay đổi làm thêm, bỏ hay đổi nghĩa một BR thì đưa về "Chờ duyệt".

## Lưu ý

- `docs/` là site Docsify công khai. File trong thư mục này không có trên menu (`docs/_sidebar.md`) nhưng ai biết URL vẫn mở được.
- `nqdev-task-flow` tìm `docs/brd/` để đoán bước bắt đầu. Ở repo plugin này, thư mục này mô tả chính plugin, không phải tính năng của repo đích.
