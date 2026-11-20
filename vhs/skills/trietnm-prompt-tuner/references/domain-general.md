# Lĩnh vực `general` — ngoài phạm vi IT

**Đầu ra:** bất cứ thứ gì không thuộc 9 lĩnh vực kỹ thuật (dịch thuật, nội dung phi kỹ thuật, câu hỏi kiến thức, kế hoạch cá nhân, soạn email...).

## Nguyên tắc riêng của lĩnh vực này

**Không chạy context probe. Không gắn repo, tech stack, đường dẫn file vào prompt refined.** Đây là lỗi thường gặp khi skill đã quen với ngữ cảnh lập trình.

**Ưu tiên mẫu light.** Phần lớn prompt `general` chỉ cần 3 mục: Mục tiêu / Yêu cầu / Output format. Chỉ dùng mẫu full khi prompt thật sự nhiều nhiệm vụ.

## Mục bắt buộc thêm (chỉ khi dùng mẫu full)

- **Đối tượng nhận kết quả** (nếu là nội dung gửi cho ai đó).
- **Giọng điệu**: trang trọng / thân mật / trung tính.
- **Độ dài mong muốn**.

## Checklist đặc thù

- [ ] **Có cần thông tin thời sự / cập nhật không?** Nếu có thì ghi rõ để AI biết phải tra cứu.
- [ ] **Ngôn ngữ đầu ra** — đặc biệt khi liên quan dịch thuật.
- [ ] **Định dạng**: đoạn văn, bullet, bảng, kịch bản hội thoại.
- [ ] **Có ràng buộc gì không được nhắc tới** (thông tin nội bộ, tên khách hàng thật...).

## Bẫy hay gặp

- Refine quá tay: prompt "dịch đoạn này sang tiếng Anh" mà bị phồng thành 6 mục là hỏng. Prompt như vậy thường đã đạt bypass hoặc chỉ cần mẫu light.
- Prompt `general` nhưng nội dung có yếu tố kỹ thuật nhẹ (VD "giải thích API là gì cho người không biết code") → vẫn là `general`, vì đầu ra là giải thích cho người thường, không phải làm việc trên repo.

## Ví dụ rút gọn

**Thô:** *"soạn giúp tôi email báo khách hàng về lịch bảo trì hệ thống"*

**Refined (mẫu light):**

```
## Mục tiêu
Soạn email thông báo lịch bảo trì hệ thống gửi khách hàng.

## Yêu cầu
1. Nêu thời gian bảo trì, dịch vụ bị ảnh hưởng, và ảnh hưởng cụ thể tới khách
2. Có lời xin lỗi ngắn gọn và kênh liên hệ khi cần hỗ trợ
3. [cần xác nhận: khung giờ bảo trì và dịch vụ nào bị gián đoạn?]

## Output format
Email tiếng Việt, giọng trang trọng, tối đa 200 từ, có sẵn dòng tiêu đề
```
