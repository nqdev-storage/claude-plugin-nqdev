---
description: Truy vấn Jira (Atlassian) qua REST API — search theo JQL, list theo project, xem epic + subtasks, transition trạng thái, tạo issue mới (epic/sprint/fix-version/labels/estimate). Mặc định ẩn issue Done khỏi mọi kết quả liệt kê.
argument-hint: "menu | search --jql \"...\" [--status \"...\"] | list --project KEY [--status \"...\"] | epic --key KEY [--status \"...\"] | transition --key KEY --status \"...\" | estimate --key KEY --original \"...\" | create --project KEY --summary \"...\" [--type \"...\"] [--description \"...\"] [--epic KEY] [--sprint \"...\" | --no-sprint] [--fix-version \"...\" | --no-fix-version] [--labels \"...\"] [--original \"...\"]"
allowed-tools: Bash(curl:*), Bash(date:*), Bash(printenv:*)
---

# Jira Tracker (nqdev) — $ARGUMENTS

## Bước 0 — Nếu $ARGUMENTS rỗng hoặc là `menu`

Hiển thị NGAY khối menu bên dưới rồi DỪNG — không gọi API, không cần kiểm tra credentials.

```
📋 /nqdev:tracker-jira-nqdev — Jira Cloud (<your-domain>.atlassian.net)

  menu                                            Hiện menu này
  search --jql "<JQL>" [--status "..."]           Tìm issue theo JQL (API v3: /search/jql)
  list --project <KEY> [--status "..."]           Liệt kê issue theo project
  epic --key <EPIC-KEY> [--status "..."]          Xem epic + toàn bộ children
  transition --key <KEY> --status "<STATUS>"      Chuyển trạng thái issue
  estimate --key <KEY> --original "<DURATION>"    Ghi Time Tracking (Original Estimate)
  create --project <KEY> --summary "<TEXT>" ...   Tạo issue mới (epic/sprint/fix-version/labels/estimate)

Mặc định MỌI lệnh liệt kê (search/list/epic) tự ẩn issue trạng thái Done khỏi kết quả.
Muốn xem cả Done (hoặc lọc đúng 1/nhiều trạng thái cụ thể): thêm --status "Done" hoặc
--status "Done,In Progress" (phân tách bởi dấu phẩy).

Ví dụ:
  /nqdev:tracker-jira-nqdev search --jql 'text ~ "dakia"'
  /nqdev:tracker-jira-nqdev epic --key QUYIT-465
  /nqdev:tracker-jira-nqdev epic --key QUYIT-465 --status "Done"
  /nqdev:tracker-jira-nqdev list --project QUYIT --status "In Progress"
  /nqdev:tracker-jira-nqdev list --project QUYIT --status "Done,Rejected"
  /nqdev:tracker-jira-nqdev estimate --key QUYIT-653 --original "3h"
  /nqdev:tracker-jira-nqdev create --project QUYIT --summary "Thêm export Excel" --epic QUYIT-695 --original "2d"
  (không truyền --sprint/--fix-version => tự gắn Sprint Active và version "Tháng MM/YYYY" của tháng hiện tại;
   ghi đè bằng --sprint "QUYIT Sprint 34" --fix-version "Tháng 09/2026"; bỏ bằng --no-sprint / --no-fix-version)

Cần cấu hình trước: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN (xem mục "Cấu hình bắt buộc" bên dưới)
```

## Cấu hình bắt buộc (biến môi trường, KHÔNG hardcode, KHÔNG ghi vào file)

- `JIRA_BASE_URL` — bắt buộc đặt, ví dụ `https://<your-domain>.atlassian.net` (không có giá trị mặc định)
- `JIRA_EMAIL` — email tài khoản Atlassian gắn với token
- `JIRA_API_TOKEN` — tạo tại https://id.atlassian.com/manage-profile/security/api-tokens

Kiểm tra trước lần gọi API đầu tiên bằng `printenv JIRA_BASE_URL JIRA_EMAIL` và `printenv JIRA_API_TOKEN > /dev/null` (chỉ xem mã thoát, không in token). Nếu thiếu biến nào: dừng lại, yêu cầu người dùng `export JIRA_EMAIL=... JIRA_API_TOKEN=... JIRA_BASE_URL=...` trước khi chạy tiếp.
**Không bao giờ hỏi xin token qua chat, không echo/log/ghi giá trị token ra bất kỳ file nào.**

## Parse hành động từ $ARGUMENTS

(Trường hợp `menu`/rỗng đã xử lý ở Bước 0 — các action dưới đây đều cần credentials.)

### Quy tắc lọc mặc định: ẩn issue Done (áp dụng cho `search`, `list`, `epic`)

Đây là hành vi mặc định của toàn bộ lệnh liệt kê, **không áp dụng** cho `transition`/`estimate`
(không phải hành động liệt kê):

- Nếu người dùng **không** truyền `--status`: tự thêm mệnh đề `AND status != "Done"` vào JQL trước
  khi gọi `search/jql`, để ẩn hẳn issue đã Done khỏi kết quả — tránh rác kết quả cũ đã xong việc.
- Nếu người dùng **có** truyền `--status "<S1>[,<S2>,...]"` (1 hoặc nhiều trạng thái, phân tách bởi
  dấu phẩy, có thể gồm cả `Done`): **bỏ** mệnh đề ẩn Done, thay bằng `AND status IN ("<S1>", "<S2>", ...)`.
  Đây là cách duy nhất để issue Done xuất hiện lại trong kết quả — người dùng phải chủ động xin.
- Nếu kết quả có issue bị ẩn bởi rule này (tức có filter Done đang áp dụng), ghi 1 dòng ghi chú ngắn ở
  cuối bảng kết quả, ví dụ: `(Đã ẩn N issue Done — dùng --status "Done" để xem)`. Không cần đếm chính
  xác N nếu tốn thêm 1 lượt gọi API chỉ để đếm — có thể bỏ qua con số, chỉ cần câu ghi chú chung.

### `search --jql "<JQL>" [--status "<STATUS>[,...]"]`
Ghép JQL người dùng đưa vào với mệnh đề status theo quy tắc ở trên rồi gọi:
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "Accept: application/json" \
  --data-urlencode "jql=<JQL> AND status != \"Done\" ORDER BY updated DESC" \
  --data-urlencode "fields=summary,status,issuetype,project,updated" \
  --data-urlencode "maxResults=50" \
  -G "$JIRA_BASE_URL/rest/api/3/search/jql"
```
(thay `AND status != "Done"` bằng `AND status IN (...)` nếu có `--status`). Lưu ý: endpoint cũ
`/rest/api/3/search` đã bị Atlassian deprecate (trả `410 Gone`) — luôn dùng `/rest/api/3/search/jql`.

### `list --project <KEY> [--status "<STATUS>[,...]"]`
Build JQL: `project = <KEY>` + mệnh đề status theo quy tắc ở trên (mặc định `AND status != "Done"`;
nếu có `--status` thì `AND status IN ("<S1>", "<S2>", ...)`), rồi gọi endpoint như trên.

### `epic --key <EPIC-KEY> [--status "<STATUS>[,...]"]`
1. Lấy chi tiết epic (luôn hiển thị epic dù trạng thái epic là gì — rule ẩn Done chỉ áp dụng cho
   danh sách children, không áp dụng cho chính issue epic):
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "Accept: application/json" \
     "$JIRA_BASE_URL/rest/api/3/issue/<EPIC-KEY>?fields=summary,status,issuetype"
   ```
2. Lấy children bằng JQL `parent = <EPIC-KEY>` + mệnh đề status theo quy tắc ở trên (mặc định
   `AND status != "Done"`), `ORDER BY status`, qua endpoint `search/jql` ở trên.

### `transition --key <ISSUE-KEY> --status "<STATUS-NAME>"`
1. `GET $JIRA_BASE_URL/rest/api/3/issue/<ISSUE-KEY>/transitions` — tìm phần tử có `name` khớp `<STATUS-NAME>`, lấy `id`.
2. `POST $JIRA_BASE_URL/rest/api/3/issue/<ISSUE-KEY>/transitions` với body `{"transition": {"id": "<id>"}}`.

### `estimate --key <ISSUE-KEY> --original "<DURATION>"`
Ghi field Time Tracking → Original Estimate (đồng thời set luôn Remaining Estimate bằng giá trị này —
hành vi mặc định của Jira khi PUT `originalEstimate` trên 1 issue chưa log time nào). `<DURATION>` là
chuỗi duration chuẩn Jira: `"3h"`, `"1d"`, `"2h 30m"`, `"1d 4h"`... (đơn vị ngày quy đổi theo cấu hình
time-tracking của site, thường 1d = 8h; không chắc thì hỏi người dùng).
```bash
curl -s -o /dev/null -w "%{http_code}" -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -X PUT -H "Content-Type: application/json" \
  -d "{\"fields\":{\"timetracking\":{\"originalEstimate\":\"<DURATION>\"}}}" \
  "$JIRA_BASE_URL/rest/api/3/issue/<ISSUE-KEY>"
```
Kỳ vọng HTTP `204` (không có response body). Nếu project/issue type không bật Time Tracking, Jira trả
`400` kèm lỗi field không hợp lệ trong body — báo rõ lỗi đó cho người dùng thay vì coi là đã ghi thành
công. Không tự suy ra `<DURATION>` nếu người dùng chỉ đưa "estimated_hours" dạng free-text nhiều phần
(vd. `"~1 (điều tra) + ~2-3 (fix)"` từ frontmatter file `plans/*.md`) — cộng dồn thành 1 con số rõ ràng
trước khi gọi (lấy trung điểm mỗi khoảng `~X-Y`), và nói rõ cách quy đổi đã dùng trong phần trình bày
kết quả, không âm thầm làm tròn.

### `create --project <KEY> --summary "<TEXT>" [--type "<ISSUE-TYPE>"] [--description "<TEXT>"] [--epic <EPIC-KEY>] [--sprint "<SPRINT-NAME>" | --no-sprint] [--fix-version "<VERSION-NAME>" | --no-fix-version] [--labels "<L1>,<L2>,..."] [--original "<DURATION>"]`

Tạo issue mới. Không truyền `--sprint` → tự gắn **Sprint Active**; không truyền `--fix-version` → tự gắn version **`Tháng MM/YYYY`** của tháng hiện tại (xem mục 3, 4). `--type` mặc định `Task` nếu không truyền. Build JSON body cho `POST $JIRA_BASE_URL/rest/api/3/issue`
theo từng field tuỳ chọn dưới đây — field nào không được truyền thì bỏ hẳn key đó khỏi body, không set giá trị rỗng:

1. **`description`** (nếu có): API v3 yêu cầu ADF, không phải plain text — bọc tối thiểu:
   ```json
   {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "<TEXT>"}]}]}
   ```

2. **`--epic <EPIC-KEY>`** (Epic Link): dự án Jira Cloud có 2 kiểu quản lý issue khác nhau, phải xác định trước:
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/project/<KEY>?fields=style"
   ```
   - `style` = `"next-gen"` (team-managed) → set `fields.parent = {"key": "<EPIC-KEY>"}`.
   - `style` = `"classic"` (company-managed) → tìm id field "Epic Link":
     ```bash
     curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/field"
     ```
     lọc phần tử có `name == "Epic Link"`, lấy `id` (dạng `customfield_XXXXX`), set `fields[<id>] = "<EPIC-KEY>"`.

3. **`--sprint "<SPRINT-NAME>"`** — **mặc định là Sprint đang Active** khi KHÔNG truyền `--sprint` (muốn issue không thuộc sprint nào: truyền `--no-sprint`). Field Sprint luôn là custom field bất kể classic/next-gen, giá trị cần là **id số** của sprint, không phải tên:
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/agile/1.0/board?projectKeyOrId=<KEY>"
   # lấy id board đầu tiên trong values[]
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/agile/1.0/board/<BOARD-ID>/sprint?state=active,future,closed"
   # tìm phần tử values[].name == "<SPRINT-NAME>", lấy id
   ```
   Tìm id field "Sprint" qua `GET /rest/api/3/field` (lọc `name == "Sprint"`) như bước Epic Link, rồi
   `fields[<sprint-field-id>] = <sprint-id>` (số nguyên, không phải chuỗi). Nếu Jira trả `400` nói field
   cần dạng mảng, thử lại với `[<sprint-id>]`. Nếu không tìm thấy sprint tên khớp: dừng lại, báo lỗi rõ
   ràng cho người dùng (tên sprint sai hoặc project không gắn board này) — không âm thầm tạo issue thiếu sprint.

   **Khi không truyền `--sprint`:** lấy sprint Active thay vì tìm theo tên:
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/agile/1.0/board/<BOARD-ID>/sprint?state=active"
   ```
   Dùng `values[0].id` (nếu nhiều board hoặc nhiều sprint active, ưu tiên board có sprint active; còn nhiều
   sprint active thì chọn sprint có `startDate` mới nhất và nói rõ đã chọn sprint nào). Nếu **không có sprint
   Active nào**: vẫn tạo issue nhưng KHÔNG gắn sprint, và ghi rõ điều đó trong phần báo kết quả (không im lặng).
   Luôn in ra tên sprint đã gắn (hoặc "không gắn sprint") ở kết quả.

4. **`--fix-version "<VERSION-NAME>"`** — **mặc định là version của tháng hiện tại**, định dạng `Tháng MM/YYYY`
   (MM luôn 2 chữ số, vd. `Tháng 09/2026`, `Tháng 10/2026`) khi KHÔNG truyền `--fix-version` (muốn bỏ: truyền
   `--no-fix-version`). Lấy tháng/năm hiện tại bằng `date +"Tháng %m/%Y"` (giờ máy local). Tìm trong danh sách
   version của project có `name` khớp chuỗi đó; với tháng 1–9, nếu không có `Tháng 09/2026` mà đã có bản không
   đệm số 0 (`Tháng 9/2026`) thì dùng bản đã có, đừng tạo
   trùng. Cả hai đều chưa có thì **hỏi người dùng** có tạo version mới (đúng định dạng `Tháng MM/YYYY`) không; đồng ý mới tạo theo bước bên dưới, không thì tạo issue không có fixVersion. Kiểm tra version đã tồn tại chưa:
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" "$JIRA_BASE_URL/rest/api/3/project/<KEY>/versions"
   ```
   Người dùng đồng ý tạo: tạo version trước khi tạo issue:
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "Content-Type: application/json" -X POST \
     -d "{\"name\":\"<VERSION-NAME>\",\"project\":\"<KEY>\"}" "$JIRA_BASE_URL/rest/api/3/version"
   ```
   Set `fields.fixVersions = [{"name": "<VERSION-NAME>"}]`.

5. **`--labels "<L1>,<L2>,..."`**: tách theo dấu phẩy, trim khoảng trắng, `fields.labels = ["<L1>", "<L2>", ...]`.

6. **`--original "<DURATION>"`**: giống action `estimate` — `fields.timetracking.originalEstimate = "<DURATION>"`.

7. Gọi tạo issue:
   ```bash
   curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "Content-Type: application/json" -X POST \
     -d @- "$JIRA_BASE_URL/rest/api/3/issue" <<'EOF'
   {"fields": {"project": {"key": "<KEY>"}, "issuetype": {"name": "<TYPE>"}, "summary": "<TEXT>", ...}}
   EOF
   ```
   Thành công trả `201` kèm `key` issue mới — in ra `<NEW-KEY>` và link `$JIRA_BASE_URL/browse/<NEW-KEY>`.
   Nếu `400`: đọc `errors`/`errorMessages` trong response, báo rõ field nào bị từ chối (issue type không tồn
   tại, sprint field sai id, không có quyền tạo version...) — không báo thành công khi chưa có `key` trả về.

## Output

Trình bày kết quả dạng bảng: `Key | Summary | Status | Type`. Nếu không có issue nào khớp, báo rõ
"Không tìm thấy issue nào khớp" thay vì im lặng bỏ qua. Nếu rule ẩn Done đang áp dụng (không có
`--status`), thêm 1 dòng ghi chú cuối bảng theo mô tả ở mục "Quy tắc lọc mặc định" bên trên.

## Ví dụ thực tế (Dakia One / QuyIT Platform)

```
/nqdev:tracker-jira-nqdev search --jql 'text ~ "dakia"'
/nqdev:tracker-jira-nqdev epic --key QUYIT-465
/nqdev:tracker-jira-nqdev epic --key QUYIT-465 --status "Done"
/nqdev:tracker-jira-nqdev list --project QUYIT --status "In Progress"
```
