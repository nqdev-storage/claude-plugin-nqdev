"""Khai báo hành vi cho các nút của prototype.

Hành vi được gắn vào nút theo CHỮ HIỂN THỊ của nút (đã chuẩn hóa: chữ thường, gộp khoảng trắng).
Đổi nhãn nút trên giao diện thì phải đổi khóa tương ứng ở đây. interact.py sẽ cảnh báo:
  - nút trong nguồn chưa có hành vi,
  - hành vi khai báo cho màn nhưng không khớp nút nào.

Cấu trúc:
    ACTIONS = {
        "*":       { "<nhãn nút>": {spec}, ... },   # dùng cho mọi màn
        "<tên màn>": { "<nhãn nút>": {spec}, ... }, # chỉ màn đó, ghi đè khóa chung
    }

Các loại hành vi (spec["type"]):
    modal    Hộp thoại có ô nhập.   title, body?, fields?, confirm?, cancel?, toast?, delay?, outcome?, error?
    confirm  Hộp thoại xác nhận (nút nguy hiểm).  title, body?, confirm?, cancel?, toast?, delay?, outcome?, error?
    toggle   Bật/tắt một vùng.      region   (vùng khai báo trong nguồn bằng <!--region:tên--> ... <!--/region-->)
    toast    Hiện thông báo.        message, delay? (có delay thì nút chuyển sang "đang xử lý" rồi mới báo), outcome?
    goto     Chuyển sang màn khác.  screen   (tên màn; phát sự kiện "proto:goto" để nơi nhúng có thể xử lý thay)
    close    Đóng hộp thoại đang mở.

Trường nhập (fields): {"label": "...", "type": "text|number|date|email|textarea|select",
                       "required": True, "placeholder": "...", "options": [...] (select), "value": "..."}
    outcome: "success" (mặc định) hoặc "error" để minh họa trạng thái lỗi.

Hành vi phức tạp hơn (sắp xếp, lọc, phân trang...): viết thẳng <script> trong nguồn orig/frag.
"""

# Chuỗi giao diện của phần hộp thoại/thông báo do bộ dựng chèn vào. Đổi theo ngôn ngữ của sản phẩm.
STRINGS = {
    "required": "Vui lòng nhập {label}",
    "processing": "Đang xử lý…",
    "saved": "Đã lưu",
    "cancel": "Hủy",
    "confirm": "Lưu",
    "confirm_danger": "Xóa",
    "error": "Không thực hiện được. Vui lòng thử lại.",
}

ACTIONS = {
    "*": {
        # "đóng": {"type": "close"},
    },
    # Màn System Design (bắt buộc): minh họa hộp thoại, thông báo, xác nhận xóa, nút thao tác trong bảng.
    "system-design": {
        "mở hộp thoại": {
            "type": "modal", "title": "Cập nhật địa chỉ giao hàng", "confirm": "Lưu", "toast": "Đã cập nhật địa chỉ",
            "fields": [
                {"label": "Người nhận", "type": "text", "required": True, "value": "Nguyễn Thu Hà"},
                {"label": "Địa chỉ", "type": "textarea", "required": True},
            ],
        },
        "hiện thông báo": {"type": "toast", "message": "Đã lưu đơn DH-10293"},
        "thử lại": {"type": "toast", "message": "Đã tải lại dữ liệu", "delay": 800},
        "xem": {"type": "toast", "message": "Mở chi tiết đơn hàng"},
        "sửa": {"type": "toast", "message": "Mở form sửa đơn hàng"},
        "xóa": {"type": "confirm", "title": "Xóa đơn hàng?", "body": "Thao tác này không hoàn tác được.", "toast": "Đã xóa đơn hàng"},
    },
    # "danh-sach-don": {
    #     "thêm đơn": {
    #         "type": "modal", "title": "Thêm đơn hàng", "confirm": "Lưu", "toast": "Đã thêm đơn hàng",
    #         "fields": [
    #             {"label": "Khách hàng", "type": "text", "required": True},
    #             {"label": "Trạng thái", "type": "select", "options": ["Mới", "Đang giao", "Hoàn tất"]},
    #         ],
    #     },
    #     "bộ lọc": {"type": "toggle", "region": "filters"},
    #     "xuất excel": {"type": "toast", "message": "Đã xuất file", "delay": 800},
    #     "xóa": {"type": "confirm", "title": "Xóa đơn hàng?", "body": "Thao tác này không hoàn tác được."},
    #     "xem": {"type": "goto", "screen": "chi-tiet-don"},
    # },
}
