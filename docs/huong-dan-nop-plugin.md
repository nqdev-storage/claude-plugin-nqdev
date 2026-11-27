# Hướng dẫn nộp plugin `nqdev` lên Claude Plugin Directory

> Cập nhật: 2026-11-27 · Áp dụng cho plugin `nqdev` v2.7.1
> Nguồn: tài liệu chính thức của Anthropic (liệt kê ở cuối bài). Quy định có thể thay đổi, hãy đối chiếu lại trước khi nộp.

## 1. Tổng quan

Có **hai con đường** phát hành plugin. Chúng khác nhau hoàn toàn.

| | Con đường A: Directory chính thức | Con đường B: Marketplace riêng |
|---|---|---|
| Là gì | Plugin được liệt kê trên https://claude.com/marketplace/plugins | Repo GitHub của bạn tự đóng vai marketplace |
| Cần form nộp | Có, qua developer portal | Không |
| Duyệt | Quét tự động và người duyệt bản đầu tiên | Không ai duyệt |
| Người dùng cài bằng | Duyệt trong `/plugin`, plugin hiện dạng `nqdev@synced` | `/plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist` |
| Yêu cầu | Tài khoản Claude trả phí | Chỉ cần repo public hoặc quyền truy cập repo |

> `claude-plugins-official` (marketplace do Anthropic quản lý) **không nhận submission qua portal**. Đừng nộp vào đó.

Repo này đã sẵn sàng cho **cả hai** đường: có `plugin.json` và `marketplace.json`.

## 2. Con đường B: dùng ngay, không cần duyệt

Sau khi push repo lên GitHub, người dùng cài như sau:

```bash
claude plugin marketplace add nqdev-storage/claude-plugin-nqdev#dist
claude plugin install nqdev@nqdev-marketplace
```

Trong phiên Claude Code có thể dùng dạng `/plugin marketplace add ...` và `/plugin install ...`.

Khi có bản mới, tăng `version` trong `plugin.json`, đẩy tag `vX.Y.Z` (workflow `publish-dist.yml` cập nhật branch `dist`), rồi người dùng cập nhật plugin.

## 3. Con đường A: nộp vào Directory chính thức

### 3.1. Điều kiện
- **Gói Claude trả phí**: Pro, Max, Ultra, Team hoặc Enterprise. Tài khoản Free không nộp được.
- Gói Team/Enterprise: cần quyền **Owner** (hoặc vai trò tuỳ chỉnh có quyền Directory).
- Repo GitHub chứa plugin. Có thể validate và nộp khi repo còn private, nhưng **phải chuyển public trước khi publish**. Repo private cần xác nhận upload source và cài Claude GitHub App.
- Tuân thủ **Anthropic Software Directory Terms** và **Software Directory Policy**.

### 3.2. Checklist chuẩn bị (làm trước khi nộp)

Đánh dấu từng mục:

- [ ] `name` là `nqdev`, dạng kebab-case, không bắt đầu bằng `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-`
- [ ] **Tên không đổi được sau khi publish.** Muốn đổi nhãn hiển thị thì sửa `displayName`
- [ ] `version`: nếu có thì **phải tăng ở mỗi lần phát hành**
- [ ] `description`, `author`, `homepage`, `repository`, `license` đã điền (hiện đã có)
- [ ] `README.md` ở root plugin (hiện đã có, tiếng Việt)
- [ ] **Icon**: PNG hoặc JPEG vuông, 512–2048 px mỗi cạnh, dưới 2 MB (không nhận SVG, WebP).
  - Hiện có [nqdev/.claude-plugin/icon.png](../nqdev/.claude-plugin/icon.png) 1024×1024.
  - **Icon chỉ được ghi nhận một lần** ở lần nộp đầu, sửa sau không đổi icon trên listing.
- [ ] **Bốn URL cho Directory** (chỉ đặt trong `plugin.json`, không đặt trong marketplace entry, và đều phải là `https://`):
  - `documentationUrl`: trang tài liệu
  - `supportUrl`: nơi người dùng xin hỗ trợ (ví dụ trang Issues của repo)
  - `privacyPolicyUrl`: chính sách quyền riêng tư
  - `termsOfServiceUrl`: điều khoản sử dụng
  - Đã khai báo trong `plugin.json` với domain `https://blogs.nhquydev.net/` (xem bảng bên dưới). **Bốn trang này cần có nội dung thật và truy cập công khai trước khi nộp.**

    | Field | URL | Nội dung cần viết |
    |---|---|---|
    | `documentationUrl` | https://blogs.nhquydev.net/claude-plugin-nqdev/ | Giới thiệu plugin, cách cài, danh sách skill và slash command, ví dụ dùng |
    | `supportUrl` | https://blogs.nhquydev.net/claude-plugin-nqdev/support/ | Cách liên hệ, báo lỗi (link Issues của repo), thời gian phản hồi dự kiến |
    | `privacyPolicyUrl` | https://blogs.nhquydev.net/claude-plugin-nqdev/privacy-policy/ | Dữ liệu nào plugin đọc hoặc gửi đi (Jira, Google Sheet theo cấu hình người dùng), không thu thập gì riêng |
    | `termsOfServiceUrl` | https://blogs.nhquydev.net/claude-plugin-nqdev/terms-of-service/ | Điều khoản sử dụng, giấy phép Apache-2.0, giới hạn trách nhiệm |
- [ ] Đã quét secret, token, đường dẫn máy cá nhân trong `nqdev/skills/` và `nqdev/commands/` (đã làm ở lần đóng gói)
- [ ] Các biến môi trường cần thiết được nêu trong README (Jira: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`)

### 3.3. Validate cục bộ

```bash
claude plugin validate . --strict
```

- `--strict` làm cảnh báo cũng thành lỗi, nên dùng trước khi nộp.
- Kết quả sạch ở máy **không đảm bảo** qua portal. Portal áp thêm quy tắc riêng của Directory.
- Cài thử local để chắc các skill và slash command gọi được:

```bash
claude plugin marketplace add .
claude plugin install nqdev@nqdev-marketplace
```

### 3.4. Các bước trên portal

Vào https://claude.ai/directory/manage (cần đăng nhập). Trang hướng dẫn: https://claude.com/docs/plugins/submit

1. Chọn **Submit new**, rồi chọn loại **Plugin bundle**.
2. **Source:**
   - *Repository*: `nqdev-storage/claude-plugin-nqdev` (bắt buộc)
   - *Plugin path*: `nqdev` (thư mục chứa `.claude-plugin/plugin.json` của plugin)
   - *Branch or tag*: nhập `dist`. Repo public chỉ có branch `dist` và `gh-pages`, không có `main`, nên để trống (nhánh mặc định) hay nhập `main` đều không đúng
   - Bấm **Validate** và sửa hết lỗi nếu có.
3. **Listing details:** chỉ đọc. Nội dung lấy từ `nqdev/.claude-plugin/plugin.json` và `nqdev/README.md`. Muốn đổi thì sửa hai file này rồi validate lại.
4. **Data handling**, bạn trả lời các câu hỏi về dữ liệu:
   - Plugin có đọc hoặc lưu dữ liệu cá nhân không?
   - Có gửi dữ liệu tới dịch vụ khác ngoài các connector đã khai báo không?
   - Giữ dữ liệu bao lâu?
   - Có dành cho người dưới 18 tuổi không?

   Gợi ý cho `nqdev`: plugin chỉ gồm skill và slash command dạng văn bản, không có server hay hook.

   Tuy vậy các slash command Jira và Google Sheet gọi dịch vụ ngoài theo cấu hình của người dùng. Hãy trả lời trung thực theo đúng điều này.
5. **Compliance:** nhập email liên hệ và tick đủ **bốn** mục xác nhận.
6. **Review and submit:**
   - *Auto-publish passing versions*: bật nếu muốn bản đạt kiểm tra tự động lên luôn.
   - *How new versions reach the directory*: **GitHub push webhook** (mặc định) hoặc **Scheduled check only**.
   - Bấm **Submit for review**.

### 3.5. Giới hạn cần nhớ
- Tối đa **10 submission trong 24 giờ** cho mỗi tổ chức.
- Mỗi cặp repo + thư mục chỉ có **một** submission. Nếu tổ chức khác đã nộp, bạn sẽ bị chặn trùng.

## 4. Sau khi nộp

### 4.1. Quy trình duyệt
- Mỗi version đều qua **validate tự động và quét bảo mật**. Listing mới được **người duyệt** xem trước khi lên.
- Thời gian duyệt **không cố định**. Theo dõi trạng thái ngay trên portal.
- Kết quả quét có 3 dạng: *Passes every check*, *Held for a reviewer*, *Doesn't pass*.
- Nhãn **Anthropic verified** do Anthropic quyết định trong lúc duyệt, không có đơn riêng.

### 4.2. Cập nhật phiên bản
- Listing luôn phục vụ **bản đã publish gần nhất** cho tới khi có bản mới được publish.
- Quy trình: sửa code, **tăng `version`**, merge vào `main` ở repo phát triển rồi đẩy tag `vX.Y.Z`. Workflow cập nhật nhánh `dist` ở repo public, và hệ thống tự nhận bản mới (theo webhook hoặc kiểm tra định kỳ).
- Đổi nhánh hoặc tag được theo dõi thì bản đang chạy vẫn giữ nguyên.

### 4.3. Nếu bị từ chối
1. Mở tab **Review**, đọc mục **Requested changes**.
2. Sửa, push lên repo.
3. Bấm **Resubmit for review** (chạy lại toàn bộ kiểm tra). Nếu chưa bị từ chối chính thức thì chỉ cần **Check for new commits**.
4. Muốn rút lại: **Withdraw submission** (khi chưa publish). Muốn gỡ: **Delist plugin**. **Relist plugin** chỉ là yêu cầu và có thể bị từ chối.

## 5. Lưu ý riêng cho `nqdev`

| Vấn đề | Việc cần làm |
|---|---|
| 4 URL của Directory chưa có nội dung | URL đã khai báo trong `plugin.json`. Cần viết và publish đủ 4 trang trên `blogs.nhquydev.net` trước khi nộp. Lần kiểm gần nhất (2026-11-20) cả 4 trả HTTP 404, xem [submit-plugin-directory.md](submit-plugin-directory.md) mục 6. |
| Slash command Jira, Google Sheet gọi dịch vụ ngoài | Khai báo rõ ở bước Data handling và trong README. Không nhúng sẵn domain hay token. |
| `sync-git-ship`, `sync-status` có commit và push | Hành vi do người dùng tự kích hoạt. Nên nêu rõ trong README để người duyệt không hiểu nhầm. |
| Tên plugin không đổi được | Chốt `nqdev` ngay từ đầu. Nếu buộc phải đổi, cần khai báo `renames` trong `marketplace.json`. |
| Icon chỉ ghi nhận một lần | Chốt hình dạng cuối cùng trước lần nộp đầu tiên. |

## 6. Những điều chưa được kiểm chứng

Các nội dung sau chưa được đối chiếu với nguồn gốc tại thời điểm viết bài. Hãy xem trực tiếp trước khi nộp:

- **Form thật trên portal** (cần đăng nhập). Các bước ở mục 3.4 lấy từ tài liệu mô tả form, có thể khác giao diện thực tế.
- **Pre-submission checklist**: https://claude.com/docs/plugins/pre-submission-checklist (có thể chứa quy tắc chi tiết về icon, privacy policy, support URL và danh sách kiểm tra quét bảo mật).

## 7. Tài liệu tham khảo

- Trang marketplace: https://claude.com/marketplace/plugins
- Hướng dẫn nộp: https://claude.com/docs/plugins/submit
- Quy trình publish của Directory: https://claude.com/docs/directory/publish
- Publish plugin (Claude Code docs): https://code.claude.com/docs/en/plugins/publish
- Plugins reference (schema manifest): https://code.claude.com/docs/en/plugins-reference
- Plugin marketplaces (marketplace riêng): https://code.claude.com/docs/en/plugin-marketplaces
