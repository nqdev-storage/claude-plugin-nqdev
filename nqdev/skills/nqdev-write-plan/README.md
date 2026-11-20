# nqdev-write-plan

Viết **execution plan** (trước khi làm) hoặc **nhật ký công việc** (sau khi làm) thành file markdown trong `plans/` ở gốc repo, và giữ plan khớp tiến độ thật cho tới khi xong.

- **Phiên bản:** 1.8.0 · **Tác giả:** QuyIT Platform · **License:** MIT
- **Hỗ trợ:** Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai

## Dùng khi nào

- Trước khi code một task phức tạp: "viết execution plan cho việc X", "lên kế hoạch rồi ghi vào plans".
- Khi quy trình yêu cầu plan được duyệt trước khi code (VD Development Workflow Policy do `nqdev-init-agents` sinh ra).
- Sau khi xong một chuỗi thay đổi: "log công việc vừa làm", "lưu lại những gì vừa làm".
- Khi đang làm: "cập nhật trạng thái plan", "ghi nhận thời gian làm vào plan".

Không dùng để bàn kế hoạch trong chat, viết BRD/PRD (`nqdev-brd-prd-writer`) hay estimate (`nqdev-requirement-estimator`).

## Đầu vào / Đầu ra

| | |
|---|---|
| **Đầu vào** | Mô tả công việc (sắp làm hoặc vừa làm), context phiên làm việc, `git status` / `git log` nếu có |
| **Đầu ra** | File `plans/<stt>-<YYYY-MM-DD>-<slug>.md` mới hoặc được cập nhật, kèm link và tóm tắt 1–2 dòng |

## Cài đặt

| Tool | Thư mục project | Thư mục global |
|---|---|---|
| Claude Code | `.claude/skills/nqdev-write-plan/` | `~/.claude/skills/nqdev-write-plan/` |
| OpenCode | `.opencode/skills/nqdev-write-plan/` (hoặc `.agents/skills/`) | `~/.config/opencode/skills/nqdev-write-plan/` |
| Gemini CLI | `.gemini/skills/nqdev-write-plan/` (hoặc `.agents/skills/`) | `~/.gemini/skills/nqdev-write-plan/` |
| Codex CLI | `.agents/skills/nqdev-write-plan/` | `~/.agents/skills/nqdev-write-plan/` |
| Claude.ai | Import file `.skill` trong Settings → Skills | |

## Hành vi theo tool

- **Claude Code:** `allowed-tools` cho phép đọc/ghi file, `mkdir` và một số lệnh git chỉ đọc mà không phải hỏi.
- **OpenCode / Gemini CLI / Codex CLI:** bỏ qua `allowed-tools`; quyền theo cấu hình của tool. Gemini CLI hỏi trước khi kích hoạt skill.
- **Claude.ai:** thường không có repo, nên skill trả nội dung plan trong chat kèm tên file đề xuất thay vì ghi file.

## Theo dõi thời gian

- Plan Pre bắt buộc có `estimated_hours` khi lập: giờ, làm tròn 0.5, là tổng end-to-end của mô hình AI làm và DEV review (xem `nqdev-requirement-estimator`).
- Mỗi lần làm một task, agent ghi mốc **Bắt đầu / Kết thúc** (`YYYY-MM-DD HH:mm`) và **Delta** (số phút thô) vào bảng **Tiến độ**, người dùng xác nhận. Task làm qua nhiều lần thì mỗi lần một dòng, nên thời gian chờ review không được tính.
- `time_spent_hours` = tổng Delta của mọi task (kể cả task `bỏ`), đổi ra giờ và làm tròn 0.25h. Chỉ làm tròn ở Tổng, không làm tròn từng dòng.
- Vượt ước lượng thì chỉ ghi nhận; ước lượng lại phải do người dùng quyết định và được ghi vào Nhật ký thay đổi plan.

## File giao việc

- Chỉ dùng cho **plan lớn** (≥ 10 bước, hoặc ước lượng ≥ 40h, hoặc có bước chạy song song / giao agent khác): lúc duyệt, skill đề xuất, người dùng chốt và ghi `assign_tasks: true`. Việc nhỏ làm thẳng theo plan.
- Plan lớn được duyệt (`status: approved`) thì điền bảng **Giao việc** (agent, lô, phụ thuộc) và sinh `.claude/assign-tasks/<tên plan>.jsonl`, mỗi bước một dòng. `nqdev-task-flow` đọc file này để chạy theo lô.
- File `.jsonl` chỉ là danh sách điều phối (không commit); mọi thông tin vẫn nằm trong plan. Mất hoặc lệch thì sinh lại từ plan.

## Giới hạn

- Chỉ ghi điều có thật trong phiên; không tự suy ra commit hash hay kết quả test.
- Agent không có đồng hồ đo giờ làm: mốc thời gian lấy từ giờ hệ thống, thời điểm tin nhắn hoặc commit, cần người dùng xác nhận. Không ai xác nhận thì dòng đó được đánh dấu "ước lượng, chưa xác nhận".
- Không tự commit file plan.
- Skill vẫn để model tự kích hoạt (`disable-model-invocation` không bật) để có thể đề xuất ghi plan; việc ghi file luôn cần người dùng đồng ý hoặc quy trình yêu cầu.

## Cấu trúc

```text
nqdev-write-plan/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── example-plan.md
```
