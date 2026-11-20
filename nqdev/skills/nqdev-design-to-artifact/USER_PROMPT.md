# User Prompt Templates — nqdev-design-to-artifact

## Mẫu cơ bản

```text
/nqdev:nqdev-design-to-artifact
Thiết kế màn hình <tên màn hình> cho <đối tượng dùng>.
Nội dung chính: <danh sách khối nội dung>.
Phong cách: <tuỳ chọn: tối giản / doanh nghiệp / ...>.
```

## Design local (mặc định, không publish)

```text
/nqdev:nqdev-design-to-artifact Dashboard quản lý đơn hàng, bảng đơn + bộ lọc trạng thái
```

## Publish lên Artifact

```text
/nqdev:nqdev-design-to-artifact --publish
/nqdev:nqdev-design-to-artifact Dashboard quản lý đơn hàng, bảng đơn + bộ lọc trạng thái --publish
```

Cả bộ prototype (thiết kế từ brief và từ `--revert-design`) là **một canvas**. Lần đầu tạo canvas và lưu link vào `docs/prototype/.artifact.json`; các lần `--publish` sau cập nhật đúng canvas đó, chỉ gửi các màn đã đổi.

## Design theo theme

```text
/nqdev:nqdev-design-to-artifact Dashboard đơn hàng --themes=material-v3
/nqdev:nqdev-design-to-artifact Trang đăng ký --themes=heroui-v3
/nqdev:nqdev-design-to-artifact Trang quản trị --themes=bootstrap
/nqdev:nqdev-design-to-artifact Trang chủ --themes="material v3"
```

Theme được ghi nhớ cho cả bộ prototype. Lần sau không truyền `--themes` thì dùng lại theme đã lưu; truyền theme khác thì skill hỏi có giữ theme cũ không.

## Xem hướng dẫn

```text
/nqdev:nqdev-design-to-artifact
/nqdev:nqdev-design-to-artifact --help
```

Gọi skill không kèm đối số nào sẽ tự hiển thị hướng dẫn. `--help` tự gõ chỉ hoạt động khi là đối số duy nhất; đi kèm đối số khác thì bị bỏ qua.

## Khôi phục UI có sẵn thành trang hoàn chỉnh

```text
/nqdev:nqdev-design-to-artifact --revert-design
/nqdev:nqdev-design-to-artifact --revert-design=src/pages/orders
/nqdev:nqdev-design-to-artifact --revert-design="màn hình danh sách khách hàng" --publish
```

Skill khôi phục các màn hoàn chỉnh có tương tác, liên kết với nhau như sản phẩm thật (nguồn trong `_gen/`, đầu ra trong `project/`). Chạy được sản phẩm ở local thì chạy và đối chiếu từng tính năng (UI, link giữa trang, click); các lệnh chạy sản phẩm và thao tác trình duyệt có thể hỏi bạn cấp quyền.

## Cập nhật artifact đã có

```text
/nqdev:nqdev-design-to-artifact Đổi bảng sang dạng thẻ, giữ nguyên bộ lọc --publish
/nqdev:nqdev-design-to-artifact --publish --update=<artifact-url>
```

Dòng đầu cập nhật canvas đã lưu trong `docs/prototype/.artifact.json`. Dòng sau trỏ sang canvas khác và ghi đè link đã lưu.

## Kiểm tra bộ prototype (chỉ đọc)

```text
/nqdev:nqdev-design-to-artifact --check
```

Báo cáo nút thiếu hành vi, màn thiếu trong `canvas.json`, đầu ra cũ, lệch theme, chữ mô tả lọt lên UI, trạng thái publish. Không sửa gì.

## Gỡ canvas đã publish

```text
/nqdev:nqdev-design-to-artifact --unpublish
```

Skill hỏi xác nhận, gỡ canvas, giữ nguyên nguồn để `--publish` lại sau.

## Đổi theme cho cả bộ

```text
/nqdev:nqdev-design-to-artifact --themes=heroui
```

Bộ đang dùng theme khác thì skill hỏi; chọn đổi sẽ re-theme toàn bộ nguồn và rà lệch theme.

## Bàn giao và đối chiếu với code thật

```text
/nqdev:nqdev-design-to-artifact Lập plan và Jira để cập nhật UI thật theo prototype
/nqdev:nqdev-design-to-artifact Kiểm tra UI app đã khớp prototype chưa
```

## Chỉnh nút và hành vi

```text
/nqdev:nqdev-design-to-artifact Nút "Xóa" ở bảng đơn hàng phải hỏi xác nhận, nút "Duyệt" báo thành công sau 1 giây
```

Hành vi nằm trong `_gen/actions.py`, gắn theo chữ trên nút. Đổi nhãn nút thì đổi khóa tương ứng; `interact.py` sẽ cảnh báo nếu lệch.

## Ô nhập kèm nút (i)

```text
/nqdev:nqdev-design-to-artifact Mỗi ô nhập có nút (i): di chuột hoặc focus bàn phím để hiện tooltip gợi ý nội dung. Nút (i) vẫn thấy khi thẻ tùy chọn đang gập.
```

## Nhắc quy tắc UI sạch (khi cần)

```text
Giữ UI sạch: không ghi mô tả tính năng trên giao diện, mô tả để trong comment code.
```

## Sau khi xem thiết kế local

- Muốn chỉnh: nêu phần cần sửa, skill sửa ở local.
- Hài lòng: chạy lại với `--publish`.
