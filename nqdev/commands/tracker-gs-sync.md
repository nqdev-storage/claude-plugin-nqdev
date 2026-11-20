---
description: Đồng bộ & lọc issue từ Google Sheet tracker theo sprint — mỗi sprint có 1 link sheet riêng, lưu mapping sprint→link để dùng lại không phải dán link mỗi lần. Cần bật connector Google Drive của claude.ai
argument-hint: "menu | add --sprint \"<name>\" --url \"<sheet_url>\" | sprints | sync [--sprint \"<name>\" | --url \"<sheet_url>\"] --dev \"<name>[,<name>...]\" [--save <path>]"
allowed-tools: mcp__claude_ai_Google_Drive__read_file_content, mcp__claude_ai_Google_Drive__get_file_metadata, Read, Write, Edit, Bash(mkdir:*), Bash(echo:*), Bash(cygpath:*)
---

# Tracker Google Sheet Sync (theo sprint) — $ARGUMENTS

## Bước 0 — Nếu $ARGUMENTS rỗng hoặc là `menu`

Hiển thị NGAY khối menu bên dưới rồi DỪNG — không gọi tool nào.

```
📊 /nqdev:tracker-gs-sync — Đồng bộ issue từ Google Sheet, mỗi sprint 1 link riêng

  menu                                                  Hiện menu này
  add --sprint "<name>" --url "<sheet_url>"             Lưu link sheet cho 1 sprint
  sprints                                                Liệt kê các sprint đã lưu
  sync --sprint "<name>" --dev "<name>[,<name>...]"     Sync theo sprint đã lưu
       [--save <path>]
  sync --url "<sheet_url>" --dev "<name>[,<name>...]"   Sync trực tiếp bằng link (không lưu)
       [--save <path>]

Ví dụ:
  /nqdev:tracker-gs-sync add --sprint "Sprint 17/7-31/7" --url "https://docs.google.com/spreadsheets/d/<fileId>/edit?gid=123#gid=123"
  /nqdev:tracker-gs-sync sprints
  /nqdev:tracker-gs-sync sync --sprint "Sprint 17/7-31/7" --dev "Quý"
  /nqdev:tracker-gs-sync sync --url "https://docs.google.com/spreadsheets/d/<fileId>" --dev "Quý,Phúc" --save "sprint-issues.md"

Ghi chú quan trọng:
  - Cần bật connector Google Drive trong claude.ai (Settings → Connectors). Chưa bật thì lệnh không đọc được sheet.
  - Sheet phải được share (tối thiểu Viewer) cho tài khoản Google đang kết nối với Drive integration —
    nếu không sẽ gặp lỗi 401/"Requested entity was not found".
  - Mapping sprint→link được lưu tại: $HOME/.claude/tracker-gs-sprints.json (dùng chung mọi project,
    không theo repo cụ thể).
```

## Registry file

Đường dẫn cố định: `$HOME/.claude/tracker-gs-sprints.json` (Windows: thường là `C:\Users\<user>\.claude\tracker-gs-sprints.json`). Read/Write cần đường dẫn tuyệt đối: lấy thư mục home bằng `echo $HOME`, không đoán. Trên Windows (Git Bash) kết quả có dạng `/c/Users/...`: đổi sang dạng `C:\Users\...` bằng `cygpath -w "$HOME"` trước khi đưa vào Read/Write.

Cấu trúc:
```json
{
  "<sprint name>": {
    "url": "<full sheet url as given by user>",
    "fileId": "<extracted file id>",
    "addedAt": "<ISO date, dùng ngày hiện tại theo context>"
  }
}
```

Nếu file chưa tồn tại: coi như registry rỗng `{}` khi đọc; khi ghi lần đầu, tạo mới file này (không cần `mkdir` vì `.claude` đã tồn tại trong home directory).

Vì registry là global (dùng chung mọi project), tên sprint nên đủ để phân biệt project nếu người dùng làm nhiều dự án song song (vd `"<dự-án> Sprint 17/7-31/7"` thay vì chỉ `"Sprint 17/7-31/7"`) — nếu người dùng không tự phân biệt và có trùng tên sprint giữa các project, hỏi lại trước khi ghi đè.

## Trích `fileId` từ URL

Từ mọi dạng link Google Sheets, lấy đoạn giữa `/d/` và `/` tiếp theo:
`https://docs.google.com/spreadsheets/d/<fileId>/edit?gid=...` → `<fileId>`.

`gid` (nếu có) chỉ để tham khảo tên tab — **không** dùng để lọc nội dung, vì `read_file_content` trả về **toàn bộ** nội dung spreadsheet (mọi tab/section) dưới dạng markdown, không tách theo gid.

## Parse hành động từ $ARGUMENTS

### `add --sprint "<name>" --url "<url>"`
1. Trích `fileId` từ `<url>` theo quy tắc trên.
2. Đọc registry (nếu có), set/ghi đè key `<name>` = `{url, fileId, addedAt}`, ghi lại file bằng Write/Edit.
3. Xác nhận ngắn gọn: đã lưu sprint nào, fileId gì.

### `sprints`
Đọc registry, in bảng: `Sprint | fileId | Added at`. Nếu rỗng, báo "Chưa có sprint nào được lưu — dùng `add` trước."

### `sync --sprint "<name>" --dev "<...>" [--save <path>]`
1. Đọc registry, tìm `<name>`. Không thấy → báo lỗi kèm gợi ý `sprints` để xem danh sách, hoặc `add` để tạo mới.
2. Lấy `fileId`, chuyển sang nhánh xử lý chung bên dưới ("Xử lý chung sau khi có fileId").

### `sync --url "<url>" --dev "<...>" [--save <path>]`
1. Trích `fileId` từ `<url>`.
2. Chuyển sang nhánh xử lý chung. Sau khi trả kết quả, gợi ý nhẹ (không bắt buộc): "Muốn lưu link này cho lần sau? Dùng `/nqdev:tracker-gs-sync add --sprint \"<name>\" --url \"<url>\"`".

Nếu thiếu `--dev`: dừng lại, báo `Thiếu --dev. Ví dụ: /nqdev:tracker-gs-sync sync --sprint "Sprint X" --dev "Quý"`.

## Xử lý chung sau khi có `fileId`

1. Gọi `mcp__claude_ai_Google_Drive__read_file_content` với `fileId`.
   Tool này không có trong phiên (chưa bật connector Google Drive): dừng, báo người dùng bật connector Google Drive trong claude.ai (Settings → Connectors) rồi chạy lại. Không thay bằng cách đọc khác.
2. Nếu lỗi (401 / "Requested entity was not found" / not found):
   dừng lại, báo rõ: sheet chưa được share cho tài khoản Google đang kết nối với Drive integration.
   Gợi ý: share sheet ở chế độ Viewer cho tài khoản đó, hoặc đổi sang "Anyone with the link", rồi chạy lại lệnh.
   **Không** tự ý thử `search_files` để đoán fileId khác — nếu không tìm thấy đúng file nghĩa là chưa có quyền truy cập.
3. Nội dung trả về là markdown gồm nhiều bảng (mỗi sprint/section 1 hoặc nhiều bảng). Tìm (các) bảng có header chứa đồng thời các cột kiểu `STT`, `Mô tả`, `DEV` (hoặc `Dev`), `Trạng thái` — đây là bảng issue/bug cần lọc. Bỏ qua các bảng task-tracking khác (cột `Developer`, `Testcase`, `Est (day)`...) trừ khi người dùng yêu cầu khác.
4. Với mỗi tên trong `--dev "<name>[,<name>...]"` (tách theo dấu phẩy, trim khoảng trắng): giữ lại dòng nếu cột DEV **chứa** tên đó (so khớp substring, không phân biệt hoa/thường) — để bắt được cả các ô ghép kiểu `"Quý & Phúc"` khi lọc theo `Quý` hoặc `Phúc`.
5. Bỏ qua các dòng trống (không có Mô tả và DEV).

## Output

- In bảng: `STT | Mô tả | DEV | Trạng thái` (thêm cột `Ghi chú`/`Dev note` nếu người dùng cần chi tiết thêm).
- Cuối bảng: tổng số issue tìm được, và breakdown theo Trạng thái (vd: To do: 3, Test Environment: 17, Done: 3...).
- Nếu không có issue nào khớp `--dev`: báo rõ "Không tìm thấy issue nào gán cho <dev>" — không im lặng trả bảng rỗng.
- Nếu có `--save <path>`: ghi toàn bộ bảng + tổng kết ra file tại `<path>` (dùng Write), rồi xác nhận đã lưu.

## Ví dụ thực tế

```
/nqdev:tracker-gs-sync add --sprint "<dự-án> Sprint 17/7-31/7" --url "https://docs.google.com/spreadsheets/d/<fileId>/edit?gid=<gid>#gid=<gid>"
/nqdev:tracker-gs-sync sprints
/nqdev:tracker-gs-sync sync --sprint "<dự-án> Sprint 17/7-31/7" --dev "Quý"
/nqdev:tracker-gs-sync sync --url "https://docs.google.com/spreadsheets/d/<fileId>" --dev "Quý,Phúc" --save "sprint-issues.md"
```
