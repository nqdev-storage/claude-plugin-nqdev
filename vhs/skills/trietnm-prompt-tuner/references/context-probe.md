# Dò context từ workspace

Chạy khi lĩnh vực **≠ `general`**. Mục tiêu: sinh mục **Context** bằng dữ liệu có thật của repo đang mở, thay cho đường dẫn gắn cứng.

## Giới hạn (quan trọng)

- **Tối đa 5 lệnh shell**, ưu tiên lệnh rẻ. Không quét toàn repo, không `find` đệ quy không giới hạn.
- **Không đọc file > 200 dòng** — chỉ đọc phần đầu.
- **Probe 1 lần cho mỗi phiên làm việc**, lần refine sau dùng lại kết quả đã có.
- **Không suy diễn**: không có bằng chứng thì không ghi vào Context.

## Thứ tự dò

**1. Repo root + branch**
```
git rev-parse --show-toplevel
git branch --show-current
```
Không phải git repo → dùng thư mục làm việc hiện tại, và bỏ phần branch.

**2. Tài liệu chỉ dẫn sẵn có** (ưu tiên cao nhất — thường mô tả sẵn kiến trúc & quy ước)

Tìm ở repo root: `CLAUDE.md`, `AGENTS.md`, `README.md`. Có thì đọc ~100 dòng đầu và rút gọn thành 2–4 gạch đầu dòng.

**3. Tech stack — nhận qua file dấu hiệu ở root hoặc thư mục con cấp 1**

| File dấu hiệu | Kết luận ghi vào Context |
|---|---|
| `*.sln`, `*.csproj` | .NET (đọc `TargetFramework` trong csproj để biết phiên bản) |
| `package.json` | Node/JS — đọc `dependencies` để biết framework (React, Next, Vue, Express...) |
| `pnpm-workspace.yaml`, `turbo.json`, `lerna.json` | monorepo — ghi rõ công cụ quản lý |
| `go.mod` / `pom.xml`, `build.gradle` / `pyproject.toml`, `requirements.txt` / `composer.json` / `Cargo.toml` | Go / Java / Python / PHP / Rust |
| `docker-compose.yml`, `Dockerfile` | có container hoá — liệt kê service nếu là compose |
| `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` | CI hiện có |
| `docs/`, `plans/`, `draft/` | có kho tài liệu — nêu đường dẫn để prompt refined yêu cầu đọc trước |

**4. Vị trí đang làm việc**
- File đang mở / đoạn đang bôi đen trong IDE (ide_selection) — nếu liên quan tới prompt thì đưa vào Context làm điểm xuất phát.
- Nếu prompt nhắc tên module/tính năng: tìm nhanh bằng `git ls-files | grep -i <từ khoá>` (1 lệnh) để lấy đường dẫn thật thay vì đoán.

**5. Dữ liệu bổ sung theo lĩnh vực** — xem `domain-<lĩnh vực>.md` (VD `data` cần biết DBMS, `devops` cần biết môi trường deploy).

## Cách viết mục Context

- Đường dẫn **tương đối repo root**, dạng markdown link: `[Helpers/PriceHelpers.cs](vhg-api/AdvertisingAPI/Helpers/PriceHelpers.cs)`
- Không dùng đường dẫn tuyệt đối (`D:\...`, `/c/Users/...`).
- Mỗi gạch đầu dòng là **một sự thật kiểm chứng được**, không phải mô tả chung chung.
- Dò được ít → mục Context ngắn. **Thà ngắn còn hơn bịa.**
- Thứ prompt cần mà repo không trả lời được → `[cần xác nhận: ...]`.

**Ví dụ mục Context sinh ra từ probe:**
```
## Context
- Repo `esms-global-tach-dlr`, branch `develop`
- Web quản trị: ASP.NET MVC (`AdvertisingOnline.sln`), grid dùng Kendo MVC
- Service liên quan: [vhg.smpp-server/](vhg.smpp.server/vhg.smpp-server/) — .NET, chạy WinForms + MassTransit/RabbitMQ
- Tài liệu sẵn có: [docs/TAI-LIEU-NGHIEP-VU.md](vhg.smpp.server/docs/TAI-LIEU-NGHIEP-VU.md)
- [cần xác nhận: môi trường đang gặp vấn đề là dev hay production?]
```
