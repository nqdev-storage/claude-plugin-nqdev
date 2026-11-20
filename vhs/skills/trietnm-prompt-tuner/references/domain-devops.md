# Lĩnh vực `devops` — CI/CD, deploy, hạ tầng, monitoring

**Đầu ra:** file cấu hình, pipeline, script, hoặc quy trình vận hành.

## Mục bắt buộc thêm vào mẫu full

- **Môi trường đích**: dev / staging / production — và đang chạy ở đâu (máy chủ vật lý, VM, cloud nào, k8s hay không).
- **Công cụ đang dùng**: GitHub Actions / GitLab CI / Jenkins / Octopus..., lấy từ file có thật trong repo.
- **Cách deploy hiện tại**: thủ công hay tự động, ai bấm, mất bao lâu.
- **Mức rủi ro cho phép**: có được downtime không, có cần rollback nhanh không.

## Checklist đặc thù

- [ ] **Secret / credential xử lý ra sao?** Cấm tuyệt đối đưa giá trị thật vào file cấu hình.
- [ ] **Áp cho một service hay toàn bộ hệ thống?**
- [ ] **Có được đụng vào hạ tầng production không**, hay chỉ soạn cấu hình để người khác duyệt.
- [ ] **Cách kiểm chứng**: sau khi áp dụng thì kiểm tra bằng lệnh/endpoint nào.
- [ ] **Rollback**: nếu hỏng thì quay lui thế nào.
- [ ] **Monitoring/alert**: ai nhận cảnh báo, kênh nào, ngưỡng bao nhiêu.

## Bẫy hay gặp

- AI hay sinh pipeline "mẫu" không khớp thực tế repo. Prompt refined phải bắt đọc file CI hiện có trước khi viết mới.
- Prompt đụng production phải nêu rõ **được phép thao tác** hay **chỉ soạn thảo** — mặc định nên là chỉ soạn thảo.

## Ví dụ rút gọn

**Thô:** *"viết pipeline build deploy tự động"*

**Refined (trích):**

```
## Mục tiêu
Soạn pipeline CI/CD tự động build và deploy service <X> lên môi trường <Y>.

## Context
- Công cụ CI đang dùng: <lấy từ .github/workflows | .gitlab-ci.yml | Jenkinsfile trong repo>
- Stack build: <từ csproj/package.json...>
- Cách deploy hiện tại: [cần xác nhận]
- Môi trường đích: [cần xác nhận: máy chủ riêng / container / k8s]

## Yêu cầu cụ thể
1. Đọc cấu hình CI hiện có, giữ nguyên quy ước đang dùng
2. Viết pipeline gồm các bước: restore, build, test, đóng gói, deploy
3. Nêu rõ biến môi trường/secret cần khai báo, kèm nơi khai báo

## Ràng buộc
- Không đưa giá trị secret thật vào file, chỉ tham chiếu tên biến
- Chỉ soạn file cấu hình, KHÔNG tự chạy deploy
- Không đổi công cụ CI hiện tại

## Tiêu chí hoàn thành
- Pipeline có bước kiểm chứng sau deploy và hướng dẫn rollback
- Liệt kê đầy đủ secret cần tạo trước khi chạy lần đầu
```
