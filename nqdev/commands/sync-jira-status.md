---
description: Cập nhật trạng thái Jira theo công việc đã làm (chuyển trạng thái task, comment kết quả, tạo task cho việc chưa có task). Cần JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN
argument-hint: "[EPIC-KEY hoặc KEY,KEY | trống = suy ra từ plans/ và git log]"
allowed-tools: Bash(curl:*), Bash(git:*), Bash(date:*), Bash(python3:*), Bash(printenv:*), Read, Grep
model: haiku
---

# Cập nhật trạng thái Jira

Đầu vào (có thể trống): `$ARGUMENTS`

## Quy tắc an toàn
- Dùng biến môi trường `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`. Kiểm tra trước lần gọi API đầu tiên bằng `printenv JIRA_BASE_URL JIRA_EMAIL` và `printenv JIRA_API_TOKEN > /dev/null` (chỉ xem mã thoát, không in token). Thiếu biến nào thì dừng và nói rõ biến thiếu. **Không in, không ghi token ra chat hay file, không hỏi token qua chat.**
- Chỉ chuyển trạng thái khi có **bằng chứng** (commit, test đạt, người dùng xác nhận). Không có bằng chứng thì chỉ comment hoặc để nguyên.
- Việc cần người dùng làm (publish, chạy thử ở máy khác) không tự chuyển Done.
- Tạo issue, chuyển trạng thái, comment, tạo version là thao tác ghi lên hệ thống ngoài: **luôn** trình bảng thay đổi dự kiến (Bước 2b) và chờ người dùng xác nhận rõ trước khi ghi, dù chỉ 1 issue. Chỉ làm các dòng được duyệt.

## Bước 1. Xác định phạm vi
1. `$ARGUMENTS` có `KEY` thì dùng; có `EPIC-KEY` thì lấy các issue con. Trống thì tìm mã dạng `[A-Z]+-\d+` trong `plans/*.md` và `git log -30 --format=%s%n%b`, đề xuất epic xuất hiện nhiều nhất kèm bằng chứng, và **hỏi người dùng xác nhận epic** trước khi đi tiếp.
2. Lấy danh sách (API v3, endpoint `search/jql`, không dùng `/search` cũ đã bị gỡ):
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -G "$JIRA_BASE_URL/rest/api/3/search/jql" \
  --data-urlencode 'jql=parent = EPIC OR key = EPIC ORDER BY key' --data-urlencode 'fields=summary,status,issuetype' --data-urlencode 'maxResults=50'
```

## Bước 2. Đối chiếu công việc với issue
- Gom việc đã làm từ `git log` (từ lần cập nhật Jira trước, hoặc 20 commit gần nhất), từ mục "Cập nhật" mới nhất trong `plans/`, và từ nội dung phiên làm việc.
- Ghép từng việc với issue; việc **chưa có issue** thì đề xuất tạo mới (Bước 4).
- Với mỗi issue ghi: trạng thái hiện tại, trạng thái nên có, bằng chứng, việc còn lại.

## Bước 2b. Xin duyệt trước khi ghi
Trình bảng `Key (hoặc "mới") | Việc | Thay đổi dự kiến (tạo / chuyển A -> B / comment / tạo version) | Bằng chứng`, rồi dừng chờ người dùng duyệt. Người dùng bỏ dòng nào thì không làm dòng đó. Không có câu trả lời rõ thì không ghi gì.

## Bước 3. Chuyển trạng thái và comment
- Lấy id transition thật của issue (id khác nhau giữa project, không đoán):
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/issue/KEY/transitions"
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H 'Content-Type: application/json' -X POST -d '{"transition":{"id":"<ID>"}}' "$JIRA_BASE_URL/rest/api/3/issue/KEY/transitions"
```
- Comment dùng ADF (API v3 không nhận chuỗi thô): `{"body":{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"..."}]}]}}`, POST tới `/rest/api/3/issue/KEY/comment`.
- Nội dung comment: đã làm gì, mã commit ngắn, kết quả kiểm thử, **việc còn lại và hạn chế**, không dán dữ liệu thật hay secret. Kiểm tra mã HTTP (201/204); lỗi thì báo, không coi là thành công.
- Viết body bằng `python3` + `urllib` hoặc `curl --data @-` để tránh lỗi nháy/dấu ngoặc khi nội dung có tiếng Việt.

## Bước 4. Tạo issue cho việc chưa có
Chỉ tạo các issue đã được duyệt ở Bước 2b. Theo quy ước của command `/nqdev:tracker-jira-nqdev` (mục `create`): loại `Task`, gắn Epic (project company-managed dùng field "Epic Link", tra id bằng `GET /rest/api/3/field`; team-managed dùng `parent`), **Sprint đang Active** (agile API `board/<id>/sprint?state=active`, field "Sprint" nhận id số) và fixVersion `Tháng MM/YYYY` của tháng hiện tại (`date +"Tháng %m/%Y"`; có bản không đệm số 0 thì dùng bản đó, đừng tạo trùng; chưa có version nào khớp thì hỏi người dùng trước khi tạo). Mô tả bằng ADF, ghi commit/plan liên quan. Chỉ chuyển Done khi có bằng chứng và dòng đó đã được duyệt.

## Bước 5. Báo cáo
Bảng `Key | Tóm tắt | Trạng thái cũ -> mới | Ghi chú`. Cuối cùng nêu: issue còn mở và vì sao (cần người dùng làm gì), epic nên đóng khi nào. Nếu có issue không đổi vì thiếu bằng chứng thì nói rõ.
