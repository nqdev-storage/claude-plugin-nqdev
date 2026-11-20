# Visual Output (tùy chọn)

Chỉ dùng khi môi trường có `show_widget` (claude.ai) và người dùng muốn bản trình bày trực quan. Nếu không, trình bày bằng Markdown theo "Đầu ra bắt buộc" trong SKILL.md. Nếu tool yêu cầu nạp module hướng dẫn thiết kế trước khi render thì làm theo.

## Bố cục (từ trên xuống)

1. 4 metric: Tổng giờ (range) | Giờ DEV review (range) | Số module | Phạm vi MVP (giờ)
2. Một card mỗi module: tên, badge loại việc, danh sách task, mức ưu tiên, estimate (range) với 3 giá trị AI | DEV review | Tổng
3. Assumptions và Exclusions (danh sách ngắn)
4. Rủi ro (icon theo mức độ) và câu hỏi clarify
5. Phase breakdown
6. Thanh tổng: Dev, QA/UAT (một dòng), Tổng (giờ; không có PM và số tuần)

Nguồn là BRD/PRD: mỗi card module hiển thị mã BR/FR phủ; giai đoạn theo nguồn, đề xuất khác gắn nhãn "đề xuất đổi".

## CSS tối thiểu

Dùng biến màu của môi trường (có fallback) để hỗ trợ dark mode; không hard-code nền sáng.

```css
.est-root{font-family:var(--font-sans,system-ui);padding:1rem 0}
.sec{font-size:13px;font-weight:500;color:var(--color-text-secondary,#666);text-transform:uppercase;letter-spacing:.06em;margin:1.5rem 0 .75rem}
.card{background:var(--color-background-primary,transparent);border:.5px solid var(--color-border-tertiary,#8884);border-radius:12px;padding:1rem 1.25rem;margin-bottom:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
.metric{background:var(--color-background-secondary,#8881);border-radius:8px;padding:1rem;text-align:center}
.metric b{display:block;font-size:24px;font-weight:500}
.badge{font-size:11px;font-weight:500;padding:3px 10px;border-radius:20px;background:#8882}
.row{display:flex;justify-content:space-between;align-items:center;gap:12px}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
```

## Quy ước nhãn

- Loại việc: Frontend, Backend / API, Full-stack, DevOps / Setup, QA.
- Ưu tiên: Bắt buộc (MVP), Quan trọng (post-MVP), Nice-to-have (Phase 2).
- Rủi ro: `!` Cao, `~` Trung bình, `?` Cần clarify.
- Mọi con số estimate hiển thị dạng range (low–high), đơn vị giờ, bước 0.5.
