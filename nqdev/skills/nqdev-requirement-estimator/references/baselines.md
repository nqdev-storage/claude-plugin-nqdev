# Baselines & Hệ số điều chỉnh

Nguồn số duy nhất cho estimate. Đơn vị: **giờ, làm tròn đến 0.5 (30 phút)**. Con số là điểm xuất phát dựa trên kinh nghiệm, không phải số đo; hiệu chỉnh bằng dữ liệu thực tế của team (xem "Hiệu chỉnh").

## Mô hình estimate

**AI là người làm, DEV là người review và góp ý.** Mỗi dòng có 3 cột, tất cả là thời gian end-to-end để một hạng mục sẵn sàng merge:

| Cột | Gồm |
|---|---|
| **AI** | AI đọc ngữ cảnh, viết code, test, tài liệu, chạy build/test, tự sửa lỗi, và sửa lại theo từng vòng góp ý |
| **DEV review** | DEV đọc diff, chạy thử, góp ý, duyệt lại sau mỗi vòng sửa |
| **Tổng** | AI + DEV review |

Giả định chuẩn (nêu lại trong mục Assumptions của mỗi bản estimate, đổi khi khác):
- AI là coding agent chạy trong repo có build và test chạy được; giờ AI là thời gian chờ thực tế (wall-clock), không phải thời gian tính toán.
- DEV senior, quen codebase, review từng thay đổi nhỏ; thời gian DEV chờ AI chạy không tính vào cột DEV.
- BRD/PRD và tiêu chí chấp nhận đã duyệt.
- Trung bình 1 vòng góp ý cho hạng mục thường, 2 vòng cho logic nghiệp vụ hoặc tích hợp; mỗi vòng đã nằm trong con số.
- AI chạy tuần tự; các module độc lập có thể chạy song song bằng nhiều agent, nhưng DEV vẫn là người review từng phần.

Bảng dưới là baseline trước khi áp hệ số context.

## Setup & Auth

| Task | AI | DEV review | Tổng |
|---|---|---|---|
| Setup greenfield: repo, CI/CD cơ bản, DB schema + migrations, Docker + deploy script, JWT login đơn giản | 3–6 | 3–5 | 6–11 |
| JWT login đơn giản (đứng riêng, không nằm trong setup) | 1.5–3 | 2–3 | 3.5–6 |
| SSO + phân quyền theo role | 4–8 | 5–8 | 9–16 |

Tránh tính đôi: nếu đã dùng dòng "Setup greenfield" thì không cộng thêm JWT login.

## Tính năng dữ liệu (CRUD và add-on)

| Task | AI | DEV review | Tổng |
|---|---|---|---|
| CRUD đơn giản (1 entity, list/detail/form) | 1.5–2.5 | 1.5–2.5 | 3–5 |
| CRUD + validation + business logic | 3–5 | 3–4 | 6–9 |
| CRUD + search/filter/sort + pagination | 3–5 | 2.5–4 | 5.5–9 |
| Add-on: search/filter/sort ở mức DB (trên CRUD có sẵn) | 1.5–3 | 1.5–2.5 | 3–5.5 |
| Add-on: search engine riêng (Elasticsearch...) | 4–7 | 3–5 | 7–12 |
| Add-on: file upload (ảnh, PDF) | 2–3.5 | 2–3 | 4–6.5 |
| Add-on: import/export CSV hoặc Excel | 2–4 | 2–3.5 | 4–7.5 |
| Add-on: import/export XML | 2.5–4.5 | 2.5–4 | 5–8.5 |
| Add-on: audit log + history | 2.5–4 | 2.5–4 | 5–8 |
| Add-on: rollback/restore (trên audit log) | 1.5–2.5 | 1.5–2.5 | 3–5 |

## UI

| Task | AI | DEV review | Tổng |
|---|---|---|---|
| Dashboard + stats cards | 1.5–3 | 1.5–2.5 | 3–5.5 |
| Dashboard + charts | 3–5 | 2.5–4 | 5.5–9 |
| Tree view / hierarchy navigation | 2–3.5 | 2–3 | 4–6.5 |
| Diff viewer (side-by-side) | 3–5 | 3–4.5 | 6–9.5 |
| Rich text editor | 2–3.5 | 2–3.5 | 4–7 |
| Drag-and-drop | 2.5–4 | 2.5–4 | 5–8 |
| Responsive mobile (không được plan từ đầu) | +20% phần FE | +20% phần FE | |
| Đa ngôn ngữ (i18n) | +10–15% phần FE | +10–15% phần FE | |

## Tích hợp & nâng cao

| Task | AI | DEV review | Tổng |
|---|---|---|---|
| REST integration với dịch vụ ngoài | 3–6 | 3–5 | 6–11 |
| WebSocket / real-time (kèm reconnect, conflict, fallback polling) | 6–10 | 5–8 | 11–18 |
| Email notification | 2–3.5 | 2–3 | 4–6.5 |
| Push notification | 2.5–4.5 | 2.5–4 | 5–8.5 |
| Slack / Teams webhook | 1.5–2.5 | 1.5–2 | 3–4.5 |
| Notification đa kênh (email + push + chat) | 3–5 | 3–4.5 | 6–9.5 |
| Report PDF | 3–5 | 3–4 | 6–9 |
| Background jobs / queue | 3–5.5 | 3–5 | 6–10.5 |
| Git integration | 4–7 | 4–6 | 8–13 |
| Payment gateway (gợi ý, cần xác nhận theo nhà cung cấp; DEV review kỹ, dùng sandbox) | 6–10 | 6–10 | 12–20 |

AI/ML: không có baseline. Xem như R&D, estimate riêng bằng range rộng và nêu rõ.

## QA

| Hạng mục | Cách tính |
|---|---|
| QA + UAT mặc định (người kiểm thử chấp nhận; test tự động do AI viết đã nằm trong cột AI) | 15–20% Dev, **một dòng** |
| Yêu cầu coverage > 80% | +15% Dev |
| E2E test (Cypress/Playwright) | +10–15% Dev |
| Performance testing | AI 2–4, DEV review 3–5, Tổng 5–9 giờ |

## Hệ số context (áp lên đúng cột nêu)

| Tình huống | Điều chỉnh |
|---|---|
| DEV review là junior hoặc chưa quen codebase | × 1.3–1.5 cột DEV |
| BRD/AC mơ hồ hoặc hay đổi (thêm vòng sửa) | + 30% cả hai cột |
| Tích hợp legacy không có docs | + 40–60% cột AI, + 30% cột DEV |
| Security cao | + 30–50% cột DEV |
| Backward compatibility | + 10–15% cả hai cột |
| Không có môi trường chạy thử cho AI tự kiểm | + 50% cột DEV |
| Nhiều môi trường (Dev/Test/Staging/Prod) | + 1–3 giờ cột DEV |

## Công thức

- Dev = Σ module (đã áp hệ số). Cộng riêng cột AI và cột DEV review, Tổng = AI + DEV review.
- QA/UAT = 15–20% × Dev (một dòng).
- Tổng = Dev + QA/UAT. Làm tròn mỗi con số đến 0.5 gần nhất.
- Không có dòng PM và không quy ra số tuần.
- Kiểm tra khả thi (khi có deadline hoặc team cố định): giờ DEV cần = Σ cột DEV review + QA/UAT; quỹ giờ DEV = số DEV × 24 giờ/tuần × số tuần đến deadline (24 là mặc định cho thời gian review, còn lại là họp và việc khác; đổi theo team và nêu trong Assumptions). Giờ DEV cần lớn hơn quỹ giờ thì không khả thi. Cột AI không vào phép so này, vì AI chạy song song được; chỉ cảnh báo khi giờ AI vượt xa thời gian lịch có sẵn.

## Ví dụ tính

Web app kho nội bộ, 2 DEV senior review, greenfield:

| Module | AI | DEV review | Tổng |
|---|---|---|---|
| Setup (đã gồm JWT) | 3–6 | 3–5 | 6–11 |
| CRUD sản phẩm có validation | 3–5 | 3–4 | 6–9 |
| Import CSV | 2–4 | 2–3.5 | 4–7.5 |
| Dashboard stats cards | 1.5–3 | 1.5–2.5 | 3–5.5 |
| **Dev** | **9.5–18** | **9.5–15** | **19–33** |

QA/UAT 15–20%: thấp = 19 × 0.15 ≈ 3; cao = 33 × 0.20 ≈ 6.5. **Tổng 22–39.5 giờ.**

Khả thi (nếu deadline 1 tuần): giờ DEV cần = 9.5–15 + 3–6.5 = 12.5–21.5; quỹ giờ DEV = 2 × 24 × 1 = 48. Khả thi.

## Hiệu chỉnh

Con số trên là điểm xuất phát. Sau mỗi plan hoàn thành, so `estimated_hours` với `time_spent_hours` (skill `nqdev-write-plan`) và điều chỉnh baseline cho khớp tốc độ thật của team và công cụ AI đang dùng.

## Bẫy hay bị underestimate

- "Login đơn giản": thêm forgot password, session, remember me, security headers; DEV phải soi kỹ phần bảo mật.
- "Hiển thị data từ API": thêm error/loading/empty state, pagination, caching.
- "Real-time": thêm reconnect, conflict resolution, fallback.
- "Permission": mỗi role mới kéo theo thêm test, edge case và thời gian DEV review.
- "Export Excel/PDF": thêm định dạng, phân trang, hiệu năng tập dữ liệu lớn.
- AI viết nhanh nhưng DEV review không nhanh theo: logic nghiệp vụ, migration dữ liệu, tích hợp bên thứ ba và phần bảo mật cần soi kỹ nên cột DEV khó giảm nhiều.
- AI không tự kiểm được khi thiếu môi trường chạy thử hoặc tài liệu API: DEV phải thử tay, nên cộng hệ số tương ứng.
