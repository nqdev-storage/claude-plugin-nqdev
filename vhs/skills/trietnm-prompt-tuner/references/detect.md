# Nhận diện lĩnh vực của prompt

## Nguyên tắc phân định

**Xét theo ĐẦU RA user muốn, không theo chủ đề của prompt.**

- "viết tài liệu về kiến trúc hệ thống" → `docs` (đầu ra là tài liệu), không phải `architecture`
- "phân tích tại sao API trả về 500" → `debug` (đầu ra là nguyên nhân lỗi), không phải `analyze`
- "review giúp tôi câu SQL này" → `review` (đầu ra là nhận xét), không phải `data`
- "viết câu SQL lấy doanh thu theo tháng" → `data` (đầu ra là SQL)

## Bảng tín hiệu

| Lĩnh vực | Đầu ra mong muốn | Từ khoá tín hiệu |
|---|---|---|
| `code` | Code chạy được / thay đổi trong repo | viết hàm, implement, thêm chức năng, tạo API/endpoint/component, CRUD, refactor, tách hàm, đổi tên, sửa code, làm giúp tôi tính năng |
| `analyze` | Hiểu biết về code/hệ thống hiện có | phân tích, đọc hiểu, luồng, flow, trace, khảo sát, reverse engineer, "code này làm gì", "chạy thế nào", mapping, dependency, tổng quan module |
| `debug` | Nguyên nhân + cách sửa một lỗi cụ thể | lỗi, bug, exception, stacktrace, crash, treo, timeout, "không chạy", "sao bị", sai kết quả, fix, log lỗi, nguyên nhân |
| `review` | Nhận xét / danh sách vấn đề | review, đánh giá code, chất lượng, code smell, best practice, audit, bảo mật, security, lỗ hổng, PR, merge request, chấm điểm |
| `architecture` | Quyết định thiết kế / so sánh phương án | kiến trúc, thiết kế hệ thống, nên dùng gì, so sánh phương án, trade-off, scale, microservice, monolith, pattern, ADR, chiến lược migration |
| `data` | Schema / SQL / thay đổi dữ liệu | database, DB, schema, bảng, table, SQL, query, index, migration, ERD, stored procedure, tối ưu truy vấn, Postgres, SQL Server, MySQL, Mongo, Redis |
| `devops` | Cấu hình hạ tầng / pipeline | deploy, CI/CD, pipeline, docker, k8s, container, hạ tầng, monitoring, alert, log tập trung, môi trường, env, release, rollback |
| `test` | Test case / test code / kế hoạch kiểm thử | test, unit test, integration, e2e, QA, kịch bản kiểm thử, test case, coverage, mock, regression |
| `docs` | Văn bản cho người đọc | tài liệu, viết mô tả, BRD, PRD, spec, user guide, HDSD, README, changelog, release note, mô tả task, Jira, tài liệu nghiệp vụ |
| `general` | Ngoài phạm vi IT | mọi thứ còn lại: dịch thuật, viết nội dung phi kỹ thuật, câu hỏi kiến thức chung, kế hoạch cá nhân |

## Tín hiệu bổ trợ (cộng điểm, không quyết định một mình)

- **File đang mở / đang chọn trong IDE**: `.sql` → `data`; file test → `test`; `Dockerfile`, `.yml` trong `.github/workflows` → `devops`; `.md` → `docs`
- **Nội dung user paste kèm**: stacktrace/log lỗi → `debug`; diff/PR → `review`; bảng dữ liệu → `data`
- **Động từ mở đầu**: "viết/tạo/thêm" → thiên về tạo mới (`code`, `data`, `docs`, `test`); "tại sao/vì sao" → `debug` hoặc `analyze`; "nên/có nên" → `architecture`

## Xử lý xung đột

1. Có tín hiệu lỗi cụ thể (thông báo lỗi, stacktrace, "không chạy") → `debug` thắng `analyze` và `code`.
2. Có từ "review/đánh giá/audit" + đối tượng là code có sẵn → `review` thắng mọi lĩnh vực kỹ thuật khác.
3. Đầu ra là văn bản cho người khác đọc → `docs` thắng lĩnh vực chủ đề.
4. Vừa thiết kế vừa code ("thiết kế rồi implement") → `architecture`, và ghi chú trong prompt refined rằng phần implement là bước sau.

## Khi mơ hồ — BẮT BUỘC hỏi

Điều kiện coi là mơ hồ:
- Hai lĩnh vực có số tín hiệu chênh nhau **< 2**, hoặc
- Không có tín hiệu nào rõ ràng, hoặc
- Prompt quá ngắn để suy ra đầu ra (VD: "cái này ổn chưa")

Cách hỏi — dùng tool **AskUserQuestion** nếu có, mỗi lựa chọn kèm 1 dòng giải thích *đầu ra sẽ khác nhau thế nào*:

> Prompt của bạn có thể thuộc 2 hướng, đầu ra sẽ khác nhau:
> - `analyze` — tôi sẽ đọc source và mô tả luồng hiện tại đang chạy ra sao
> - `review` — tôi sẽ chỉ ra các điểm chưa tốt kèm mức độ ưu tiên

**Không refine khi chưa chốt được lĩnh vực.**
