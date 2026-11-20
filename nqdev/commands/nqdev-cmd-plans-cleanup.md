---
description: "Gọi bằng: /nqdev:nqdev-cmd-plans-cleanup [file1 file2 ... | regex] — Quét toàn bộ plans/ hoặc chỉ các file được chỉ định (nhiều tên file hoặc 1 regex), phát hiện nội dung trùng lặp (nội bộ 1 file + chéo giữa nhiều file) và frontmatter mâu thuẫn với nội dung, hỏi xác nhận từng thay đổi trước khi sửa, rồi tạo báo cáo tổng hợp sau khi chạy"
argument-hint: "[file1.md file2.md ... | \"regex\"] (bỏ trống = quét toàn bộ plans/)"
---

# Dọn dẹp & sửa lỗi Plans — $ARGUMENTS

Tham số là **tùy chọn**, dùng để giới hạn phạm vi file cần dọn trong `plans/`:

- **Bỏ trống** ($ARGUMENTS rỗng): quét & xử lý toàn bộ `plans/*.md` như mặc định.
- **Danh sách tên/đường dẫn file** (2 token trở lên, phân tách bằng khoảng trắng hoặc dấu phẩy — VD: `001-2026-09-01-foo.md, 002-2026-09-05-bar.md`): chỉ xử lý đúng các file này.
- **1 token duy nhất**: nếu khớp chính xác 1 file có thật trong `plans/` thì coi là tên file; ngược lại coi là **regex**, áp dụng match lên tên file (basename, không gồm đường dẫn) của toàn bộ file trong `plans/`.

## Bước 0 — Xác định phạm vi & kiểm tra `plans/`

1. Nếu thư mục `plans/` không tồn tại, hoặc tồn tại nhưng không chứa file `.md` nào (không tính `cleanup-report-*.md`): hiển thị thông báo sau rồi **dừng ngay**, không thực hiện gì thêm.

```
📁 Không tìm thấy file plan nào trong plans/.

Chưa có gì để dọn dẹp. Tạo plan bằng `/nqdev:nqdev-task-flow feature` (bước plan), hoặc skill `nqdev-write-plan`.
```

2. Resolve **tập file target** theo $ARGUMENTS đúng quy tắc ở trên (danh sách file / regex / toàn bộ nếu bỏ trống). Loại `cleanup-report-*.md` khỏi mọi trường hợp resolve.
3. Nếu có tham số nhưng tập target resolve ra **rỗng** (không file nào khớp tên đã liệt kê, hoặc regex không match file nào): hiển thị thông báo rồi **dừng ngay**, không tự ý fallback về quét toàn bộ.

```
⚠️ Không tìm thấy file nào khớp với "<tham số đã truyền>" trong plans/.

Các file hiện có trong plans/: <liệt kê tên file, hoặc "(không có)">
```

4. In ra danh sách file target sẽ xử lý trong lần chạy này trước khi sang Bước 1, để user biết rõ phạm vi.

## Bước 1 — Thu thập dữ liệu

- Với **tập file target** (đã resolve ở Bước 0): đọc đầy đủ frontmatter (`type`, `complexity`, `status`/`impact`, `related_issues`, `related_prs`, ...) và toàn bộ nội dung theo mục. Nhận dạng file thuộc khuôn nào theo các mục nó có:
  - **Plan của `nqdev-task-flow`** (khuôn trong `${CLAUDE_PLUGIN_ROOT}/skills/nqdev-task-flow/references/feature.md`): Mục tiêu, Phạm vi, File dự kiến thay đổi, Các bước, Kiểm thử, Rủi ro và câu hỏi mở; frontmatter `status` là `todo` / `approved` / done
  - **Pre-Execution Planning** (khuôn của skill `nqdev-write-plan`): mục 1–6 (Bối cảnh, Approach và quyết định đã chốt, Tiến độ, Risks và Unknowns, Tiêu chí hoàn thành, Câu hỏi / Phụ thuộc); plan cũ có thể dùng tên cũ (Phân tích/Bối cảnh, Approach/Strategy, Todo, Risks & Unknowns, Success Criteria, Questions/Dependencies)
  - **Post-Execution Logging** (khuôn của skill `nqdev-write-plan`): mục 1–7 (Bối cảnh, Công việc đã thực hiện, Files đã thay đổi, Trạng thái hiện tại, Việc còn mở, Bài học rút ra, Tham khảo bên ngoài)
- Nếu target chỉ là 1 phần của `plans/` (do có tham số lọc): vẫn đọc thêm phần "Bối cảnh"/"Công việc đã thực hiện" của các file **còn lại** trong `plans/` (ngoài target) — chỉ để làm dữ liệu đối chiếu ở Bước 3, không đưa các file này vào diện được sửa.
- Nếu 1 file không khớp cả 2 template (thiếu frontmatter hoặc cấu trúc mục khác hẳn): vẫn đọc nội dung thô, nhưng ghi chú "không theo template chuẩn" khi báo cáo phát hiện ở file đó — không ép sửa cấu trúc file này trừ khi user xác nhận riêng.

## Bước 2 — Phát hiện trùng lặp nội bộ (trong 1 file)

- Chỉ áp dụng cho **file target**. Trong từng file, so sánh nội dung giữa các mục (không so heading, so nội dung thực chất) để tìm đoạn bị lặp lại — ví dụ cùng một mô tả rủi ro xuất hiện cả ở "Bối cảnh" lẫn "Risks & Unknowns", hoặc cùng một bước công việc bị liệt kê 2 lần trong "Công việc đã thực hiện".
- Chỉ tính là trùng lặp khi nội dung **giống nhau về ý nghĩa** (paraphrase cũng tính), không phải cụm từ ngắn trùng ngẫu nhiên.

## Bước 3 — Phát hiện trùng lặp chéo (giữa nhiều file)

- So sánh nội dung "Bối cảnh"/"Phân tích"/"Công việc đã thực hiện" của **mỗi file target** với các file khác trong toàn bộ `plans/` (kể cả file ngoài target, dùng dữ liệu đối chiếu đã đọc ở Bước 1) để tìm 2+ file cùng ghi lại một quyết định/công việc giống nhau.
- Ưu tiên so sánh các file có slug tên gần giống nhau hoặc cùng chủ đề rõ rệt trước, sau đó mới xét toàn bộ tập file nếu số lượng file còn ít (tránh so sánh chéo O(n²) tốn thời gian khi `plans/` có nhiều file).
- Nếu phát hiện trùng lặp giữa 1 file target và 1 file **ngoài** target: chỉ đề xuất sửa ở phía file target (xóa/gộp phần trùng), không đụng vào file ngoài target dù nó cũng chứa nội dung trùng.
- Nếu cả 2 file trùng lặp đều nằm trong target: đề xuất sửa như phát hiện trùng lặp chéo bình thường (có thể hỏi xác nhận sửa ở 1 hoặc cả 2 file, tùy đề xuất cụ thể).

## Bước 4 — Phát hiện sai sót: frontmatter mâu thuẫn nội dung

Chỉ áp dụng cho **file target**. Với mỗi file, kiểm tra các mâu thuẫn sau giữa frontmatter và nội dung thật:

- `status: completed` (hoặc dòng `**Trạng thái:** ✅ Đã hoàn thành`) nhưng mục "Việc còn mở"/Todo vẫn còn ít nhất 1 dòng `- [ ]` chưa tick.
- `status: in_progress`/`blocked` nhưng nội dung mục "Trạng thái hiện tại" mô tả rõ ràng là đã xong toàn bộ.
- Dòng `> **Trạng thái:**` trong body ghi khác với `status` trong frontmatter (VD frontmatter `blocked` nhưng body ghi "🚧 Đang thực hiện").
- `type`/`complexity`/`impact` rõ ràng không khớp với mô tả trong file (VD `type: bug-fix` nhưng nội dung mô tả toàn bộ là thêm tính năng mới).

Không tự suy diễn mâu thuẫn ngoài 4 loại trên — nếu nghi ngờ nhưng không chắc, không liệt kê thành phát hiện.

## Bước 5 — Trình bày từng phát hiện & xin xác nhận

Với **mỗi** phát hiện (dedup nội bộ, dedup chéo, hoặc frontmatter mâu thuẫn), in theo format:

```
🔎 Phát hiện #<n> — <loại: Trùng lặp nội bộ | Trùng lặp chéo | Frontmatter mâu thuẫn>
File: <đường dẫn plan, hoặc 2 đường dẫn nếu là trùng lặp chéo>
Vị trí: <mục/dòng cụ thể>
Vấn đề: <mô tả ngắn gọn>
Đề xuất sửa: <nội dung sẽ thay đổi, diễn đạt rõ trước/sau>

Áp dụng thay đổi này? (Y/N)
```

- Hỏi xác nhận **từng phát hiện một**, không gộp nhiều phát hiện vào 1 lần hỏi.
- Chỉ ghi đè file khi nhận được **Y** rõ ràng cho đúng phát hiện đó. Mọi câu trả lời khác (N, bỏ qua, không rõ) → giữ nguyên file, ghi nhận là "bỏ qua".
- Khi sửa: chỉ xóa/gộp phần nội dung trùng lặp đã xác định, hoặc sửa đúng giá trị frontmatter/mục mâu thuẫn đã chỉ ra — không viết lại toàn bộ file, không thêm nội dung mới ngoài phạm vi đã đề xuất, giữ nguyên cấu trúc mục hiện có của file.
- Không sửa bất kỳ file nào ngoài `plans/`, và trong phạm vi `plans/` cũng **không sửa file nào ngoài tập file target** đã resolve ở Bước 0 — kể cả khi file đó xuất hiện trong 1 phát hiện trùng lặp chéo (xem quy tắc ở Bước 3).

## Bước 6 — Tạo báo cáo tổng hợp

Sau khi đã hỏi xác nhận hết toàn bộ phát hiện, tạo file `plans/cleanup-report-YYYY-MM-DD.md` (YYYY-MM-DD = ngày chạy lệnh) với nội dung:

```markdown
# Plans Cleanup Report — YYYY-MM-DD

## Phạm vi quét
- Tham số truyền vào: `<$ARGUMENTS hoặc "(không có — quét toàn bộ)">`
- File đã xử lý: <liệt kê tên file trong tập target>

## Đã áp dụng
| # | Loại | File | Thay đổi |
|---|---|---|---|
| 1 | Trùng lặp nội bộ / Trùng lặp chéo / Frontmatter mâu thuẫn | `<file>` | <mô tả ngắn> |

## Đã bỏ qua (không xác nhận)
| # | Loại | File | Lý do đề xuất |
|---|---|---|---|
| 1 | ... | `<file>` | <mô tả ngắn> |

## Tổng kết
- Tổng số phát hiện: <n>
- Đã áp dụng: <n>
- Bỏ qua: <n>
```

Nếu không có phát hiện nào ở Bước 2–4 (plans/ đã sạch), vẫn tạo báo cáo với nội dung "Không phát hiện trùng lặp hoặc sai sót nào trong lần quét này." — không bỏ qua bước tạo báo cáo.
