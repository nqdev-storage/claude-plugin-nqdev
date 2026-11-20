# Kiểm tra, bàn giao, đối chiếu với code thật

Nạp khi có `--check`, hoặc khi user nhắc bàn giao, đối chiếu UI thật, hay sửa repo thật.

## Chế độ `--check` (kiểm tra bộ prototype, chỉ đọc)

Dùng để biết bộ prototype đang có vấn đề gì mà **không sửa, không dựng lại, không publish, không chạy app**.

1. Không có `docs/prototype/_gen/` (và project không có `_gen/interact.py`) thì báo "chưa có bộ prototype để kiểm tra" và dừng. Không scaffold, không tạo file.
2. Chạy `python3 docs/prototype/_gen/check.py` (project có bộ dựng riêng không kèm `check.py` thì chạy lần lượt `interact.py --all --dry`, `lint_theme.py` nếu có, và tự quét như dưới). Bộ này gồm:
   - **Nút, hành vi, canvas, đầu ra**: nút chưa có hành vi, hành vi không khớp nút, `goto`/`toggle` trỏ sai, màn chưa khai báo trong `canvas.json`, `project/*.dc.html` thiếu hoặc **cũ so với nguồn** (`--dry` so với bản dựng mới mà không ghi);
   - **Lệch theme**: gradient, bóng đổ có màu, bo góc, trọng số chữ, màu ngoài token (`lint_theme.py`); token xấp xỉ thì nhắc cần chủ sản phẩm xác nhận;
   - **UI sạch**: đoạn chữ dài hiển thị trên giao diện, `Lorem`, `TODO` (bỏ qua comment, script, style và màn `system-design`);
   - **Publish** (thông tin): màn đã đổi so với bản đã publish, hoặc "chưa publish".
3. Đọc thêm bằng mắt những gì script không thấy: màn `system-design` và `docs/specs/ui-ux.md` còn khớp token trong `frame.html` không, bộ có đủ 8 khối của System Design không, `.theme.json` có khớp theme trong nguồn không.
   - **Truy vết** (chỉ khi repo có `docs/brd/`): màn nghiệp vụ thiếu dòng `<!--traces: ...-->`; mã trong `traces` không có trong BRD (đã đổi hay đã bỏ); bảng "Truy vết màn ↔ UC/AC" trong `docs/specs/ui-ux.md` lệch với nguồn. Màn `system-design` không cần `traces`. Màn làm trước 3.4.0 hoặc không theo BRD nào thì báo ở mức thông tin (liệt kê để user gắn mã nếu muốn), không tính là lỗi.
4. Báo cáo tóm tắt: số vấn đề theo từng nhóm, mỗi vấn đề kèm file và dòng, sau đó **gợi ý cách sửa** (vd "dựng lại: `interact.py <màn>`", "thêm hành vi cho nút X trong `actions.py`"). Không tự sửa; user muốn thì làm ở lượt sau.
5. `--check` đi cùng `--publish`, `--unpublish` hoặc `--revert-design` thì hỏi một câu muốn làm cái nào, không làm cả hai. Đi cùng brief thì bỏ qua brief và báo đã bỏ qua.
6. Không kiểm tra giao diện app thật; việc đó là "Đối chiếu UI thật với prototype" và chỉ làm khi user yêu cầu.

## Bàn giao sang code thật

Khi prototype xong (user nói chốt thiết kế, hoặc bạn vừa hoàn tất một đợt), **đề xuất** lập plan và Jira để cập nhật UI thật theo prototype. Chỉ đề xuất bằng một câu; **không tự tạo** khi user chưa đồng ý.

Nếu user đồng ý:
1. **Plan** theo skill `nqdev-write-plan` (đi kèm plugin `nqdev`, nạp bằng `Skill`); không nạp được thì theo khuôn plan của `nqdev-task-flow` (`references/feature.md` của skill `nqdev-task-flow`, nằm cạnh skill này trong cùng thư mục `skills/`). Chia task theo lớp: token và font, `components/ui`, layout, từng nhóm màn, tài liệu, QA. Mỗi task có ước lượng giờ (bước 0.5, mô hình AI làm và DEV review như `nqdev-requirement-estimator`) và rủi ro.
2. **Jira** (tuỳ chọn): có skill `jira-nqdev-insight-create-issue` thì dùng; không có thì dùng `/nqdev:tracker-jira-nqdev create` (cần `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`), thiếu cả hai thì bỏ qua bước này. Hỏi trước: một issue tổng hay tách nhiều issue, và sprint nào. Không tạo gì trước khi có câu trả lời.
3. Phần chưa có prototype (ví dụ dark mode) tách thành plan và issue **riêng**, không nhồi vào issue chính.
4. Không thấy skill nêu trên trong session thì nói rõ, soạn plan theo cấu trúc trên và hỏi user cách tạo issue.

## Đối chiếu UI thật với prototype

Chỉ làm khi user yêu cầu kiểm tra (khác với R7 của `--revert-design`, vốn đối chiếu bản khôi phục với sản phẩm).

1. **Chạy app thật bằng Playwright** (hoặc công cụ trình duyệt trong session), chỉ local/dev. Mock API theo envelope của project (ví dụ `{"success": true, "data": ...}`), đặt phiên đăng nhập qua `localStorage`. Nói rõ lệnh trước khi chạy; thiếu cấu hình thì hỏi, không tự sửa.
2. **So pixel bằng `getBoundingClientRect`** (và computed style khi cần) giữa phần tử tương ứng của app và prototype. Prototype phục vụ qua `python3 -m http.server`, thêm query chống cache (ví dụ `?v=<timestamp>`). Lệch từ 1px trở lên thì ghi: phần tử, giá trị app, giá trị prototype.
3. **Checklist** (mục nào không làm được thì ghi "chưa kiểm tra" kèm lý do):
   - [ ] responsive dưới 768px (ví dụ 375px), tìm tràn ngang;
   - [ ] hộp thoại;
   - [ ] các màn chưa có prototype;
   - [ ] dark mode (nếu app hỗ trợ);
   - [ ] cổng API trong `.env.local` khớp với mock/server đang chạy;
   - [ ] trạng thái đang tải, rỗng, lỗi.
4. **Mock gây lỗi giả thì sửa mock trước**, chạy lại, rồi mới kết luận là lỗi code. Không báo lỗi code dựa trên kết quả khi mock còn sai.
5. Kết quả: bảng lệch (màn, phần tử, app, prototype), danh sách "chưa kiểm tra". Sửa code app chỉ khi user yêu cầu, theo "Quy tắc làm việc với repo thật".
6. Ảnh chụp và dữ liệu chạy thử lưu ở thư mục tạm, không đưa vào `docs/prototype/`. Tắt tiến trình đã chạy khi xong.

## Quy tắc làm việc với repo thật

Áp dụng khi sửa code app, tài liệu hay Jira của project (bàn giao, đối chiếu, re-theme có đụng file ngoài `docs/prototype/`):

1. **Không tự commit.** Repo có submodule thì nêu rõ là có **hai commit riêng** (submodule và repo cha) và hỏi từng cái.
2. **Sửa hàng loạt bằng script phải có kiểm chứng**: chạy thử không ghi (liệt kê thay đổi), xét ngữ cảnh nền trước khi đổi màu (ví dụ chữ `text-blue-100` trên nền xanh không được đổi thành primary mờ), chạy lại kiểm tra sau khi sửa. Không chắc ngữ cảnh thì bỏ qua chỗ đó và liệt kê để xem tay.
3. **Cuối mỗi đợt**, cập nhật trạng thái plan và Jira (nếu có), và nói rõ **việc nào chưa xong**.
