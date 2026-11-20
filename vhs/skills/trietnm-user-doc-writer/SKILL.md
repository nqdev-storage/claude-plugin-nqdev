---
name: trietnm-user-doc-writer
description: >-
  Quét source code của một phần mềm và sinh tài liệu hướng dẫn sử dụng (user guide)
  chi tiết, dễ hiểu cho người dùng cuối — có sẵn placeholder chèn ảnh và ví dụ minh họa
  cho từng tính năng. Hỗ trợ viết full toàn bộ phần mềm hoặc từng module, có lập kế hoạch
  (DOC-PLAN) và style guide chung để các đợt viết nối tiếp nhau mượt và nhất quán về
  format / cấu trúc nội dung. Skill global, dùng được cho mọi dự án.
  Use when: user nói "viết tài liệu hướng dẫn sử dụng", "tạo user guide", "viết hướng dẫn
  sử dụng phần mềm", "soạn tài liệu HDSD", "document phần mềm cho người dùng cuối",
  "viết manual/user manual", "lên kế hoạch viết tài liệu người dùng", "viết tài liệu cho
  module X", hoặc hỏi "hướng dẫn dùng skill trietnm-user-doc-writer".
  Lệnh: help | plan | full | module {{tên}}.
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai
version: 1.0.0
author: ViHAT
created_date: 2026-11-18
updated_date: 2026-11-18
argument-hint: "help | plan | full | module <tên>"
metadata:
  author: ViHAT
  version: "1.0.0"
  created_date: "2026-11-18"
  updated_date: "2026-11-18"
---

# trietnm-user-doc-writer — Viết tài liệu hướng dẫn sử dụng từ source code

Skill này đọc source code của dự án đang mở, hiểu phần mềm **dưới góc nhìn người dùng cuối**, rồi
viết tài liệu hướng dẫn sử dụng bằng tiếng Việt: mô tả tính năng, các bước thao tác, ví dụ minh
họa, và các vị trí gợi ý sẵn để chèn ảnh chụp màn hình.

Skill **project-agnostic**: tự phát hiện ngôn ngữ / framework / cấu trúc thư mục, không giả định
tech stack nào.

---

## 1. Lệnh & cú pháp

Người dùng gọi skill kèm một tham số. Nếu **không có tham số** → in nội dung `help` (mục 7) rồi
hỏi người dùng muốn chạy chế độ nào, **không tự chạy tiếp**.

| Lệnh | Ý nghĩa | Có quét source? | Có tạo/sửa file? |
|------|---------|-----------------|------------------|
| `help` | In hướng dẫn sử dụng chính skill này (mục 7, in gần như nguyên văn) | Không | Không |
| `plan` | Khảo sát source, liệt kê module / màn hình / tính năng chính, tạo hoặc cập nhật `DOC-PLAN.md` và `_style-guide.md` | Có | Có |
| `full` | Viết tài liệu cho **toàn bộ** phần mềm: chạy `plan` (nếu chưa có), rồi viết lần lượt từng module | Có | Có |
| `module <tên hoặc slug>` | Viết / cập nhật tài liệu cho **một** module do người dùng chọn | Có | Có |

Ví dụ:
- `plan`
- `full`
- `module Quản lý đơn hàng`
- `module orders`

---

## 2. Vị trí file đầu ra

Toàn bộ tài liệu ghi vào thư mục **`docs/user-guide/`** ở gốc dự án đang mở (tạo nếu chưa có):

```
docs/user-guide/
├── README.md            # Mục lục / trang chủ user guide, link tới từng module
├── _style-guide.md      # Quy ước format + bảng thuật ngữ thống nhất (nguồn sự thật)
├── DOC-PLAN.md          # Kế hoạch: danh sách module + trạng thái + nhật ký các đợt viết
├── images/              # Ảnh chụp màn hình (người dùng tự bổ sung sau theo placeholder)
├── <module-slug>.md     # 1 file / module, mỗi module chứa nhiều mục tính năng
└── ...
```

Quy ước slug: viết thường, bỏ dấu, thay khoảng trắng bằng `-` (VD "Quản lý đơn hàng" → `quan-ly-don-hang`).

Nếu dự án đã có nơi đặt tài liệu khác (VD `docs/`, `wiki/`), hỏi người dùng 1 câu có muốn đổi vị trí không, mặc định vẫn là `docs/user-guide/`.

---

## 3. Quy trình theo từng lệnh

### 3.1. `help`
In nội dung ở **mục 7** (giữ gần như nguyên văn, có thể rút gọn phần thừa). Không làm gì thêm.

### 3.2. `plan`
1. Khảo sát source để hiểu phần mềm:
   - Phát hiện stack (file manifest: `package.json`, `*.csproj`, `pom.xml`, `go.mod`, `requirements.txt`…).
   - Tìm các điểm vào giao diện: route/page/screen/controller/menu/navigation, form, màn hình chính.
   - Nhóm thành **module** theo chức năng nghiệp vụ mà người dùng nhìn thấy (không theo layer kỹ thuật).
   - Với mỗi module, liệt kê các **tính năng** chính (thao tác người dùng làm được: tạo, sửa, xoá, tìm kiếm, xuất báo cáo, cấu hình…).
2. Tạo `docs/user-guide/` nếu chưa có.
3. Nếu chưa có `_style-guide.md` → copy từ `templates/_style-guide.md`, điền phần "Bảng thuật ngữ" bằng các thuật ngữ nghiệp vụ tìm được trong source (tên menu, nhãn nút, tên trạng thái…).
4. Nếu chưa có `DOC-PLAN.md` → copy từ `templates/DOC-PLAN.md`. Điền bảng module: STT, tên module, slug, mô tả ngắn, độ ưu tiên (đề xuất), trạng thái = `chưa viết`, file dự kiến.
   Nếu đã có → **merge**: thêm module mới, giữ nguyên trạng thái các module cũ.
5. Tạo/cập nhật `README.md` (mục lục) với link tới file từng module (kể cả file chưa viết — đánh dấu "đang biên soạn").
6. Báo cáo: số module, số tính năng ước tính, đề xuất thứ tự viết. **Dừng ở đây**, hỏi người dùng muốn viết module nào trước (hoặc chạy `full`).

### 3.3. `module <tên>`
1. **Bắt buộc đọc trước khi viết** (bước nhất quán — xem mục 4):
   - `docs/user-guide/_style-guide.md`
   - `docs/user-guide/DOC-PLAN.md`
   - 1–2 file module `.md` đã viết gần nhất (nếu có) để bám theo cấu trúc / giọng văn / cách đặt caption ảnh.
   Nếu `_style-guide.md` / `DOC-PLAN.md` chưa tồn tại → chạy `plan` trước.
2. Xác định module mục tiêu từ tham số (khớp tên hoặc slug trong `DOC-PLAN.md`). Không khớp → liệt kê module có sẵn, hỏi lại.
3. Đọc kỹ source của module đó: các màn hình, form, trường dữ liệu, nút, luồng thao tác, điều kiện hiển thị, thông báo lỗi, quyền truy cập.
4. Viết file `docs/user-guide/<module-slug>.md` theo `templates/module.md`; mỗi tính năng là một block theo `templates/feature.md`, gồm đủ: mục đích, đối tượng/khi nào dùng, tiền điều kiện, các bước thao tác đánh số, **ví dụ minh họa có dữ liệu mẫu + kết quả mong đợi**, **placeholder ảnh** (format ở mục 5) đặt đúng vị trí trong luồng, lỗi thường gặp / lưu ý.
5. Cập nhật `DOC-PLAN.md`: trạng thái module → `xong` (hoặc `đang viết` nếu còn dở), điền cột file + ngày cập nhật, thêm 1 dòng vào "Nhật ký các đợt viết".
6. Cập nhật `README.md`: bỏ nhãn "đang biên soạn" ở module vừa xong.
7. Nếu phát sinh thuật ngữ mới → thêm vào bảng thuật ngữ trong `_style-guide.md`.

### 3.4. `full`
1. Chạy `plan` (nếu `DOC-PLAN.md` chưa có hoặc người dùng yêu cầu làm mới).
2. Lặp qua từng module theo thứ tự ưu tiên trong `DOC-PLAN.md`, với mỗi module thực hiện đúng quy trình `module <tên>` (mục 3.3), **tái sử dụng cùng `_style-guide.md`** để giữ nhất quán.
3. Sau mỗi module: cập nhật `DOC-PLAN.md` + `README.md` ngay (để nếu bị ngắt vẫn tiếp tục được).
4. Kết thúc: rà lại `README.md`, kiểm tra mọi module `xong`, báo cáo tổng số file + số placeholder ảnh cần chụp.

---

## 4. Quy tắc nhất quán (bắt buộc với mọi lệnh viết)

- **Luôn đọc `_style-guide.md` + `DOC-PLAN.md` trước khi viết bất kỳ nội dung nào.** Style guide là nguồn sự thật về: cấp heading, cách đánh số bước, giọng văn, thuật ngữ, format ảnh, cách đặt tên file/ảnh.
- **Không đổi cấu trúc giữa chừng.** Nếu thấy cần cải tiến template → cập nhật `_style-guide.md` trước, ghi chú lý do vào "Nhật ký", rồi mới áp dụng; các module đã viết sẽ được rà lại sau, không để lẫn 2 style.
- **Thuật ngữ dùng một cách duy nhất** xuyên suốt (theo bảng thuật ngữ). Ví dụ đã chọn "Đơn hàng" thì không lúc "phiếu đặt", lúc "order".
- **Viết cho người dùng cuối**: mô tả thao tác trên giao diện ("Nhấn nút **Lưu**"), không nhắc tên hàm / class / bảng DB / endpoint.
- **Mỗi đợt viết nối tiếp đợt trước**: mở đầu file module mới bám đúng bố cục file module gần nhất; cross-link tới module liên quan bằng đường dẫn tương đối (`[Quản lý khách hàng](./quan-ly-khach-hang.md)`).
- Sau khi viết xong luôn cập nhật `DOC-PLAN.md` và `README.md` trong cùng lượt.

---

## 5. Format placeholder ảnh (cố định, không đổi)

Chèn đúng tại vị trí trong luồng thao tác nơi người đọc cần nhìn màn hình:

```md
<!-- SCREENSHOT: [mô tả cảnh cần chụp] | Gợi ý: [trạng thái màn hình, phần tử cần làm nổi bật / khoanh đỏ] -->
![<caption ngắn gọn>](./images/<module-slug>-<NN>-<mo-ta-ngan>.png)
```

- `<NN>` = số thứ tự 2 chữ số trong phạm vi module (`01`, `02`…), tăng dần theo thứ tự xuất hiện.
- Ảnh chưa tồn tại là bình thường — placeholder chính là "vị trí gợi ý sẵn" để người dùng chụp và bỏ vào `images/` sau.
- Mỗi màn hình / bước quan trọng nên có tối thiểu 1 placeholder. Không nhồi ảnh cho thao tác hiển nhiên.

Ví dụ:
```md
<!-- SCREENSHOT: Màn hình danh sách Đơn hàng | Gợi ý: khoanh đỏ nút "Tạo đơn hàng" ở góc trên bên phải -->
![Danh sách đơn hàng và nút tạo mới](./images/quan-ly-don-hang-01-danh-sach.png)
```

---

## 6. Template

Các file mẫu nằm trong thư mục `templates/` của skill:

| File | Dùng làm gì |
|------|-------------|
| `templates/_style-guide.md` | Copy vào `docs/user-guide/_style-guide.md` ở lần `plan` đầu tiên; sau đó là nguồn sự thật về format |
| `templates/DOC-PLAN.md` | Copy vào `docs/user-guide/DOC-PLAN.md`; bảng theo dõi module + nhật ký |
| `templates/module.md` | Khung 1 file tài liệu module (header, mục lục tính năng, phần chung) |
| `templates/feature.md` | Khung 1 mục tính năng bên trong file module |

---

## 7. Nội dung lệnh `help` (in ra khi gọi `help` hoặc gọi không tham số)

```text
════════════════════════════════════════════════════════════════════
  trietnm-user-doc-writer — Viết tài liệu hướng dẫn sử dụng từ source code
════════════════════════════════════════════════════════════════════

CÔNG DỤNG
  Quét source code dự án đang mở, viết tài liệu hướng dẫn sử dụng
  (user guide) bằng tiếng Việt cho người dùng cuối: mô tả tính năng,
  các bước thao tác, ví dụ minh họa, và các vị trí gợi ý sẵn để chèn
  ảnh chụp màn hình. Viết được toàn bộ phần mềm hoặc từng module,
  các đợt viết nhất quán với nhau về format và thuật ngữ.

CÁCH GỌI
  Gọi skill kèm 1 trong các lệnh sau:

  help
      In bảng hướng dẫn này. Gọi skill mà không kèm lệnh cũng ra đây.

  plan
      Khảo sát source, liệt kê module / màn hình / tính năng chính.
      Tạo:  docs/user-guide/DOC-PLAN.md      (kế hoạch + trạng thái)
            docs/user-guide/_style-guide.md  (quy ước format + thuật ngữ)
            docs/user-guide/README.md        (mục lục)
      Chạy bước này TRƯỚC KHI viết, để chọn thứ tự làm từng phần.

  full
      Viết tài liệu cho TOÀN BỘ phần mềm. Tự chạy plan nếu chưa có,
      rồi viết lần lượt từng module, cập nhật tiến độ sau mỗi module
      (bị ngắt vẫn chạy lại tiếp được).

  module <tên hoặc slug>
      Viết / cập nhật tài liệu cho MỘT module.
      Ví dụ:  module Quản lý đơn hàng
              module orders
      Skill sẽ đọc lại _style-guide.md + DOC-PLAN.md + tài liệu đã
      viết trước đó để giữ đúng cấu trúc và giọng văn.

KẾT QUẢ ĐẶT Ở ĐÂU
  docs/user-guide/
    README.md          Mục lục, link tới từng module
    _style-guide.md    Quy ước format + bảng thuật ngữ thống nhất
    DOC-PLAN.md        Danh sách module + trạng thái + nhật ký các đợt viết
    images/            Nơi bỏ ảnh chụp màn hình (theo placeholder trong tài liệu)
    <module-slug>.md   1 file / module

MỖI MỤC TÍNH NĂNG GỒM
  - Mục đích + đối tượng / khi nào dùng
  - Tiền điều kiện (quyền, dữ liệu cần có trước)
  - Các bước thao tác (đánh số, mỗi bước 1 hành động trên giao diện)
  - Ví dụ minh họa (dữ liệu mẫu + kết quả mong đợi)
  - Vị trí gợi ý chèn ảnh:  <!-- SCREENSHOT: ... --> + ![caption](./images/...)
  - Lỗi thường gặp / lưu ý

QUY TRÌNH KHUYẾN NGHỊ
  1) plan                → xem danh sách module, chốt thứ tự
  2) module <A>          → viết module quan trọng nhất trước, xem thử
  3) module <B>, <C>...  → viết tiếp từng phần, tài liệu tự nối mạch
  hoặc dùng full nếu muốn làm một mạch toàn bộ.
════════════════════════════════════════════════════════════════════
```

---

## 8. Ghi chú

- Không tự ý commit/push. Chỉ tạo file trong `docs/user-guide/`.
- Nếu source quá lớn, ưu tiên các màn hình có route/menu rõ ràng; ghi các phần chưa chắc vào cột "Ghi chú" của `DOC-PLAN.md` thay vì đoán.
- Trả lời và toàn bộ nội dung tài liệu bằng tiếng Việt; giữ nguyên thuật ngữ kỹ thuật khi cần.
