# Chế độ --revert-design

Nạp khi có `--revert-design[=<path|feature>]`. Mục tiêu: project đã có UI nhưng chưa có thiết kế. Khôi phục UI hiện có thành các màn hoàn chỉnh có tương tác, GIỐNG UI gốc, đi qua kiến trúc `_gen` (xem source-layout.md). Không sáng tạo thêm, không làm đẹp trừ khi user yêu cầu. Màn khôi phục cùng bộ prototype, cùng `canvas.json`, cùng canvas với mọi thiết kế khác.

## Kết quả cần đạt
- Mỗi màn mở lên là dùng được (HTML, CSS, JS qua `actions.py`): đủ trạng thái hover/focus/disabled/lỗi/rỗng như UI gốc, nút đúng chữ gốc, điều hướng đúng đích bằng `goto`, layout dùng chung nhất quán (ưu tiên `frame.html` + `frag/`), dữ liệu mẫu thực tế, backend giả lập bằng phản hồi mô phỏng, đăng nhập giả lập bằng tài khoản hư cấu.
- Phạm vi: đối số nếu có; không thì dò nhẹ (vài lệnh Glob/Grep) theo file giao diện và file định tuyến/menu, lập bản đồ điều hướng và để user chọn. Màn được chọn kéo theo màn có quan hệ trực tiếp (chi tiết, sửa, tạo mới) để luồng không cụt; nói rõ màn nào được kéo theo. Nhiều hơn 5 màn thì làm theo đợt.
- Comment đầu mỗi nguồn ghi nguồn gốc (đường dẫn trong repo) và phần đã đơn giản hóa.
- Chữ đang hiển thị trên UI gốc giữ trung thực, kể cả đoạn mô tả có sẵn: liệt kê trong tóm tắt và hỏi user có gỡ không.
- Không chép dữ liệu thật, secret, token, chuỗi kết nối, email hay số điện thoại thật vào nguồn.
- UI gốc dùng thư viện UI thì mô phỏng bằng HTML/CSS; thư viện CSS thuần có thể nạp từ CDN cho phép.

## Đối chiếu với sản phẩm đang chạy (khi chạy được)
Mục tiêu: UI, quan hệ giữa màn và sự kiện click của bản khôi phục khớp sản phẩm thật. Việc này tạo nhiều đầu ra lớn (ảnh chụp, DOM); nếu môi trường có subagent thì giao cho một subagent và chỉ nhận lại bảng khớp/lệch.
- Cách chạy lấy từ README, CLAUDE.md, package.json, launchSettings, docker-compose; chỉ lệnh dev/local có sẵn. Nói rõ lệnh trước khi chạy; cần cài dependency hoặc thiếu cấu hình thì hỏi trước.
- Chỉ local/dev, không production hay secret thật. Không bấm hành động ghi/xóa/gửi/thanh toán lên dữ liệu thật: đọc handler trong code thay thế.
- Với mỗi màn so bố cục, style (computed style khi cần), trạng thái và kết quả mỗi cú click giữa sản phẩm và `project/<màn>.dc.html`. Lệch thì sửa nguồn `_gen/` rồi dựng lại, tối đa 2 vòng; còn lệch thì ghi vào tóm tắt.
- Ảnh chụp và dữ liệu thấy khi chạy chỉ để đối chiếu, để ở thư mục tạm, không đưa vào `docs/prototype/`. Tắt tiến trình khi xong.
- Không chạy được: đối chiếu từ code và nói rõ "chưa đối chiếu với sản phẩm đang chạy" kèm lý do.

## Kết thúc
Mặc định dừng ở local; `--publish` thì theo publish.md. Màn đăng nhập/thanh toán hoặc mang thương hiệu thật: khi publish dùng thương hiệu hư cấu hoặc giữ ở local. Tóm tắt: màn đã khôi phục (và màn kéo theo), luồng đã nối, kết quả đối chiếu (đã chạy hay chưa, số mục khớp/lệch), phần đơn giản hóa.
