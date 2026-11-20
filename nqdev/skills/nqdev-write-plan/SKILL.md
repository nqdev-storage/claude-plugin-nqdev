---
name: nqdev-write-plan
description: "Viết execution plan (trước khi làm) hoặc nhật ký công việc (sau khi làm) thành file markdown trong thư mục plans/ ở gốc repo, theo quy ước plans/<stt>-<YYYY-MM-DD>-<slug>.md và template có frontmatter, bắt buộc có thời gian ước lượng, ghi mốc bắt đầu/kết thúc từng task, và cập nhật trạng thái plan khi làm tiếp hoặc xong việc. Dùng khi người dùng nói \"viết execution plan\", \"lên kế hoạch rồi ghi vào plans\", \"ghi lại kế hoạch\", \"cập nhật trạng thái plan\", \"ghi nhận thời gian làm vào plan\", \"log công việc vừa làm\", \"viết nhật ký công việc\", \"lưu lại những gì vừa làm\", \"save work log\", \"record decision\", \"write execution plan\", hoặc khi một quy trình khác (VD Development Workflow Policy của nqdev-init-agents) yêu cầu viết plan trước khi code. Có thể chủ động đề xuất sau một chuỗi thay đổi đáng ghi, nhưng chỉ ghi file khi người dùng đồng ý. Không dùng khi người dùng chỉ muốn bàn kế hoạch trong chat, viết BRD/PRD (nqdev-brd-prd-writer) hay estimate (nqdev-requirement-estimator)."
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai
version: '1.8.0'
author: QuyIT Platform
created_date: '2026-11-17'
updated_date: '2026-11-20'
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(git rev-parse:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(mkdir:*)
metadata:
  author: QuyIT Platform
  version: "1.8.0"
  created_date: "2026-11-17"
  updated_date: "2026-11-20"
  audience: developers
---

# Ghi kế hoạch / nhật ký công việc (plans/)

Mỗi đơn vị công việc có ý nghĩa có **một file** trong `plans/`, đi theo nó từ lúc lên kế hoạch tới lúc xong. Người đọc là chính agent ở phiên sau hoặc team: họ cần biết **đã/sẽ làm gì**, **tại sao chọn cách đó**, **còn gì dang dở**.

## Hai chế độ

| Chế độ | Khi nào | Dùng |
|---|---|---|
| **Pre** — kế hoạch | Trước khi làm một task phức tạp, nhiều unknown, hoặc khi quy trình yêu cầu plan được duyệt trước khi code | Template Pre |
| **Post** — nhật ký | Vừa xong / tạm dừng một việc đáng ghi mà **chưa có** plan Pre | Template Post |

Đang làm theo một plan Pre đã có → **không tạo file mới**, cập nhật chính file đó (xem *Vòng đời*).

## Quy trình

1. **Xác định nơi ghi.** Chạy `git rev-parse --show-toplevel` → ghi vào `<root>/plans/` (tạo thư mục nếu chưa có).
   - Không phải git repo → dùng thư mục làm việc hiện tại và nói rõ với người dùng.
   - Không có filesystem của repo (VD chat Claude.ai không gắn repo) → trả nội dung plan trong chat kèm tên file đề xuất. Không nói là đã ghi.
2. **Tìm plan liên quan.** Liệt kê `plans/` và grep theo từ khoá chủ đề. Có file cùng chủ đề với `status` khác `completed` → cập nhật file đó. Không có → tạo file mới, lấy `stt` từ chính danh sách vừa liệt kê (xem *Quy ước tên file*).
3. **Chọn ngôn ngữ.** Theo quy ước tài liệu trong `AGENTS.md`, `CLAUDE.md`, `README`, `CONTRIBUTING`; không có → dùng ngôn ngữ người dùng đang giao tiếp.
4. **Soạn nội dung** theo template. Chỉ ghi điều có thật (file đã đổi, commit hash, kết quả test). Chưa biết thì ghi "chưa xác định", không đoán.
5. **Ghi nhận thời gian** nếu lần này có làm task của plan, theo mục *Ghi nhận thời gian*. Plan Pre vừa lập, chưa làm gì → `time_spent_hours: 0`.
6. **Xin phép trước khi ghi** nếu chính agent đề xuất viết plan. Người dùng yêu cầu rõ hoặc quy trình bắt buộc (VD Development Workflow Policy) → ghi luôn.
7. **Báo lại** đường dẫn file (markdown link tương đối) và tóm tắt 1–2 dòng.

## Quy ước tên file

```
plans/<stt>-<YYYY-MM-DD>-<slug>.md
```

Ví dụ: `plans/001-2026-11-17-auth-token-bugfix.md`, `plans/002-2026-11-18-search-api-refactor.md`.

- **stt** = số thứ tự 3 chữ số (`001`, `002`, …), **bộ đếm chung cho cả `plans/`** (không đếm lại theo ngày). Khi tạo file mới: liệt kê `plans/`, lấy số lớn nhất trong các tên file bắt đầu bằng đúng 3 chữ số rồi `-`, cộng 1, đệm số 0 cho đủ 3 chữ số. Chưa có file nào mang `stt` → `001`. Vượt `999` thì dùng 4 chữ số (`1000`). Bỏ qua file không có `stt` (file cũ, `cleanup-report-*.md`); không đánh lại `stt` cho file cũ trừ khi người dùng yêu cầu.
- **Ngày** = ngày tạo file: Pre là ngày lập kế hoạch, Post là ngày thực hiện công việc. Tên file **không đổi** (cả `stt` lẫn ngày) khi plan được cập nhật về sau; ngày xong ghi vào `completed_date`.
- **Slug**: 3–6 từ tiếng Anh viết thường, nối bằng `-`, dễ grep (`auth-token-bugfix`, `search-api-refactor`). Không cần hậu tố `-planning` / `-roadmap` vì chế độ đã nằm trong `mode`; file cũ có hậu tố vẫn hợp lệ.
- Nhiều việc **không liên quan** → nhiều file riêng. Không gộp thành "nhật ký ngày".

## Vòng đời một plan

```
planning → approved → in_progress → completed
                          ↘ blocked / paused ↗
```

- **Được duyệt** (plan Pre mà quy trình yêu cầu duyệt trước khi làm): `status: approved`. Xét plan có phải **plan lớn** không (xem *File giao việc*), đề xuất cho người dùng chốt và ghi `assign_tasks`. Chỉ khi `assign_tasks: true` mới điền bảng *Giao việc* và sinh `.jsonl`; plan nhỏ làm thẳng theo bảng Tiến độ. Quy trình không cần duyệt thì đi thẳng sang `in_progress`, không cần file giao việc.
- **Bắt đầu làm:** `status: in_progress`. Cập nhật cột Trạng thái trong bảng *Tiến độ* (`chưa làm` / `đang làm` / `xong` / `bỏ`) sau mỗi bước, để plan luôn khớp tiến độ thật.
- **Mỗi lần làm một task:** ghi mốc Bắt đầu/Kết thúc và Delta vào bảng *Tiến độ*, rồi cập nhật hàng Tổng và `time_spent_hours` (xem *Ghi nhận thời gian*).
- **Plan đổi đáng kể khi đang làm:** sửa mục Approach / Tiến độ và thêm một dòng vào *Nhật ký thay đổi plan* (ngày: đổi gì, vì sao). Nếu plan cần duyệt, xin duyệt lại.
- **Xong hoặc tạm dừng:** thêm mục `## Kết quả` ngay trước *Nhật ký thay đổi plan* (hoặc cuối file nếu không có mục đó), cấu trúc như mục 2–6 của Template Post. Đổi `status`, ghi mốc Kết thúc của lần làm cuối và điền `completed_date` (khi `completed`).

## Frontmatter (chung cho cả hai chế độ)

```yaml
---
mode: <pre | post>
type: <bug-fix | refactor | feature | architecture | investigation | other>
status: <planning | approved | in_progress | blocked | paused | completed>
priority: <low | medium | high>
complexity: <low | medium | high>
impact: <low | medium | high>
related_issues: []
related_prs: []
estimated_hours:      # Pre: bắt buộc, điền khi lập plan (VD 4, bước 0.5). Post: tuỳ chọn
time_spent_hours: 0   # tổng thời gian thực tế = tổng cột Delta của bảng Tiến độ, đổi ra giờ và làm tròn 0.25
completed_date:       # YYYY-MM-DD khi status = completed
assign_tasks:         # Pre: true = plan lớn, dùng file giao việc; false hoặc trống = làm thẳng theo plan
---
```

Số giờ ghi dạng số (`4`, `1.5`), không dùng `~`. Trường không có giá trị thì để trống, không xoá, để mọi file cùng schema và lọc được bằng grep (VD `grep -l "status: in_progress" plans/*.md`).

## Ghi nhận thời gian

- **Nguồn duy nhất:** bảng *Tiến độ*. Mỗi lần làm một task là một dòng có mốc `Bắt đầu` / `Kết thúc` (`YYYY-MM-DD HH:mm`, giờ địa phương) và `Delta (phút)` = Kết thúc − Bắt đầu, ghi số phút thô, **không làm tròn từng dòng**. Hàng **Tổng** cộng phút thô của mọi dòng, rồi đổi ra giờ ở cột Ghi chú; số giờ đó là `time_spent_hours`.
- **Làm tròn chỉ ở Tổng:** tổng phút ÷ 60, làm tròn đến 0.25h gần nhất; tổng > 0 mà dưới 0.25 thì vẫn ghi 0.25. Làm tròn từng dòng sẽ cộng dồn sai số khi có nhiều lần làm ngắn. **Ước lượng** (`estimated_hours`) làm tròn đến **0.5** (30 phút).
- **Task làm qua nhiều lần** (nhiều phiên, dừng chờ DEV review): mỗi lần thêm một dòng mới, giữ cùng `#`, cột Bước ghi "(tiếp)". Thời gian chờ nằm ngoài các cặp mốc nên không được tính. Delta của task = tổng Delta các dòng cùng `#`.
- **Task `bỏ`:** giữ nguyên các dòng đã có Delta và vẫn tính vào Tổng, vì đó là thời gian thật đã bỏ ra.
- **Ước lượng:** `estimated_hours` bắt buộc với plan Pre, điền khi lập plan. Nhật ký Post không có ước lượng trước thì để trống. Mô hình: **AI là người làm, DEV là người review và góp ý**; `estimated_hours` là tổng end-to-end (thời gian AI làm, DEV review và các vòng sửa theo góp ý) tới khi sẵn sàng merge. Baseline tham khảo: `nqdev-requirement-estimator` (`references/baselines.md`).
- **Một lần làm** là một đoạn liên tục thực hiện một task của plan (code, điều tra, test, sửa plan theo yêu cầu). Chỉ mở plan ra tra cứu thì không tính.
- **Bắt đầu một task:** ghi `Bắt đầu` theo giờ hiện tại (lấy từ lệnh `date`, thời điểm tin nhắn hoặc commit). Không có căn cứ thì hỏi thẳng.
- **Kết thúc một lần làm** (xong task, dừng chờ review, hết phiên):
  1. Ghi `Kết thúc` và tính Delta.
  2. Hỏi người dùng xác nhận hoặc sửa, VD: "Bước 2: 14:00–15:30, 90 phút, ghi nhận vậy nhé?"
  3. Cập nhật hàng Tổng (phút và giờ đã làm tròn) và đặt `time_spent_hours` bằng số giờ đó.
  - Không có người để hỏi (VD phiên chạy theo lịch) → ghi mốc đề xuất, cột Ghi chú ghi "ước lượng, chưa xác nhận".
- **Vượt ước lượng:** chỉ ghi nhận, không tự sửa `estimated_hours`. Người dùng muốn ước lượng lại → sửa `estimated_hours` và ghi một dòng vào *Nhật ký thay đổi plan* (cũ → mới, lý do).
- **Plan cũ** (bảng Tiến độ chưa có cột thời gian, còn mục *Nhật ký thời gian* hoặc checklist Todo): khi cập nhật lần đầu, đổi sang bảng Tiến độ mới. Nếu `time_spent_hours` đã có số, thêm dòng `0 | Trước khi có mốc thời gian | xong | | | <số giờ cũ × 60>` để tổng vẫn khớp, rồi xoá mục *Nhật ký thời gian*. Giá trị dạng `~X` đổi thành `X`.

```markdown
## 3. Tiến độ
| # | Bước | Trạng thái | Bắt đầu | Kết thúc | Delta (phút) | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | <bước 1> | xong | 2026-01-20 09:00 | 2026-01-20 10:30 | 90 | |
| 2 | <bước 2> | xong | 2026-01-20 10:30 | 2026-01-20 10:40 | 10 | dừng chờ review |
| 2 | (tiếp) | xong | 2026-01-21 14:00 | 2026-01-21 14:20 | 20 | sửa theo góp ý |
| 3 | <bước 3> | chưa làm | | | | |
| **Tổng** | | | | | **120** | = 2h · Ước lượng: 4 |
```

## File giao việc (.jsonl)

Danh sách điều phối để giao từng bước của plan cho agent và chạy theo lô (người chạy lô: `nqdev-task-flow`, hoặc agent chính). Chỉ sinh cho plan **Pre** đã `approved` **và** `assign_tasks: true`. Việc nhỏ không cần: làm thẳng theo bảng Tiến độ, mốc thời gian vẫn ghi như thường.

- **Plan lớn** khi thoả **ít nhất một** điều kiện:
  1. bảng Tiến độ có ≥ 10 bước;
  2. `estimated_hours` ≥ 40;
  3. có ≥ 2 bước chạy song song được, hoặc có bước nên giao cho agent khác `main`.
- **Ai quyết:** lúc plan được duyệt, xét ba điều kiện rồi đề xuất một câu, VD: "Plan có 12 bước (điều kiện 1) → đề xuất dùng file giao việc. Đồng ý?" hoặc "Không thoả điều kiện nào → chạy thẳng theo plan." Người dùng chốt; ghi kết quả vào `assign_tasks`. Ngưỡng chỉ để đề xuất, người dùng được chọn khác.
- **Plan đổi sau khi duyệt** (phải duyệt lại): xét lại ngưỡng. Chuyển sang `true` → điền Giao việc và sinh `.jsonl`; chuyển sang `false` → xoá bảng Giao việc, `.jsonl` không dùng nữa.
- **Plan cũ** không có trường `assign_tasks`: có bảng Giao việc thì coi như `true`, không có thì `false`.

- **Nguồn đúng là plan.** Bước, agent, lô và phụ thuộc được ghi trong bảng *Giao việc* của plan; mốc thời gian ghi trong bảng *Tiến độ*. File `.jsonl` chỉ chép lại các trường điều phối, không chép mô tả, ghi chú hay Approach. Hai file lệch nhau hoặc `.jsonl` bị mất → sinh lại từ plan.
- **Vị trí:** `<root>/.claude/assign-tasks/<tên file plan, đổi .md thành .jsonl>`, VD `.claude/assign-tasks/012-2026-01-20-login-rate-limit.jsonl`. Thư mục này **không commit**: lần đầu tạo thì kiểm `.gitignore` của repo, thiếu thì đề xuất thêm dòng `.claude/assign-tasks/`.
- **Mỗi dòng một bước** (mỗi `#` trong bảng Tiến độ), JSON trên một dòng, thứ tự theo `step`:

```json
{"plan":"plans/012-2026-01-20-login-rate-limit.md","step":1,"agent":"main","batch":1,"depends_on":[],"status":"done","started_at":"2026-01-20 09:00","ended_at":"2026-01-20 10:00"}
```

| Trường | Ý nghĩa |
|---|---|
| `plan` | Đường dẫn plan, tương đối từ root repo |
| `step` | Số `#` trong bảng Tiến độ |
| `agent` | Agent thực hiện. Chọn trong các agent mà tool đang có; không có agent phù hợp thì `main` (agent chính tự làm) |
| `batch` | Số lô, bắt đầu từ 1. Các bước cùng lô chạy song song, tối đa 3 bước một lô. Hai bước sửa trùng file thì không xếp chung lô |
| `depends_on` | Danh sách `step` phải `done` trước khi bước này được chạy |
| `status` | `todo` / `doing` / `done` / `skipped`, tương ứng `chưa làm` / `đang làm` / `xong` / `bỏ` |
| `started_at`, `ended_at` | `YYYY-MM-DD HH:mm` hoặc `null`. Bước làm qua nhiều lần: `started_at` của lần đầu, `ended_at` của lần cuối; từng lần làm chỉ ghi trong plan |

- **Ai ghi:** chỉ agent điều phối (luồng chính) ghi vào `.jsonl` và plan. Subagent làm xong chỉ trả kết quả, không tự sửa hai file này, để tránh ghi đè nhau khi chạy song song.
- **Đồng bộ:** mỗi lần đổi trạng thái hoặc mốc của một bước thì cập nhật cả bảng Tiến độ (theo *Ghi nhận thời gian*) và dòng tương ứng trong `.jsonl`, trong cùng một lượt.
- **Không có filesystem** (VD Claude.ai): trả nội dung `.jsonl` trong chat cùng plan, không nói là đã ghi.

## Template Pre — kế hoạch trước khi làm

```markdown
<frontmatter, mode: pre, status: planning>

# Kế hoạch: <tiêu đề ngắn mô tả công việc>

> **Ngày lập:** YYYY-MM-DD
> **Scope dự kiến:** <files/modules sẽ thay đổi>

## 1. Bối cảnh
<Vì sao cần làm: vấn đề, yêu cầu. Constraint, assumption đã biết.>

## 2. Approach và quyết định đã chốt
<Phương án chọn; phương án đã loại và lý do; tradeoff đã cân nhắc.
Quyết định đã chốt với người dùng (VD "giữ nguyên X", "chọn Y"), để phiên sau không làm lại.>

## 3. Tiến độ
| # | Bước | Trạng thái | Bắt đầu | Kết thúc | Delta (phút) | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | <bước 1> | chưa làm | | | | |
| 2 | <bước 2> | chưa làm | | | | |
| **Tổng** | | | | | **0** | = 0h · Ước lượng: <estimated_hours> |

Trạng thái: `chưa làm` / `đang làm` / `xong` / `bỏ` (bỏ thì ghi lý do ở cột Ghi chú). Mốc và Delta: xem *Ghi nhận thời gian*.

### Giao việc (chỉ plan lớn, `assign_tasks: true`; điền khi plan được duyệt, nguồn để sinh file giao việc)
| # | Agent | Lô | Phụ thuộc |
|---|---|---|---|
| 1 | <agent hoặc main> | 1 | |
| 2 | <agent hoặc main> | 2 | 1 |

## 4. Risks và Unknowns
- **Risk:** <mô tả> → **Mitigation:** <cách xử lý>
- **Unknown:** <chưa rõ gì> → **Plan:** <cách tìm hiểu>

## 5. Tiêu chí hoàn thành
<Điều kiện cụ thể để coi là xong: test pass, hành vi mong đợi, checklist.>

## 6. Câu hỏi / Phụ thuộc (Tùy chọn)
<Cần input từ ai, phụ thuộc task nào, cần review trước khi làm không.>

## Nhật ký thay đổi plan (Tùy chọn)
- YYYY-MM-DD: <đổi gì> — <vì sao>
```

## Template Post — nhật ký sau khi làm

```markdown
<frontmatter, mode: post>

# Nhật ký: <tiêu đề ngắn mô tả công việc>

> **Ngày:** YYYY-MM-DD
> **Phạm vi:** <files/thư mục chính bị ảnh hưởng>

## 1. Bối cảnh
<Vì sao làm việc này: vấn đề, yêu cầu, phát hiện ban đầu.>

## 2. Công việc đã thực hiện
<Theo thứ tự các bước. Mỗi bước nêu cả "làm gì" và "tại sao chọn cách này". Luôn ghi:
- Quyết định "giữ nguyên X theo yêu cầu người dùng", để phiên sau không vô tình sửa lại.
- Tradeoff giữa các phương án và lý do chọn.
- Bug/vấn đề phát hiện trong lúc làm, kể cả chưa sửa.>

## 3. Files đã thay đổi
| File | Thay đổi |
|---|---|
| [src/a.ts](../src/a.ts) | <mô tả ngắn> |
| [src/b.ts](../src/b.ts) (**Mới**) | <mô tả ngắn> |

## 4. Trạng thái hiện tại
<Đã commit chưa (kèm hash), đã test/verify chưa, đang chờ gì. Chưa commit thì ghi rõ.>

## 5. Việc còn mở
- [ ] <việc cố ý chưa làm, cần quyết định hoặc để sau>

## 6. Bài học rút ra (Tùy chọn)

## 7. Tham khảo (Tùy chọn)
<Issue, PR, tài liệu, thảo luận liên quan.>

## Tiến độ
| # | Bước | Trạng thái | Bắt đầu | Kết thúc | Delta (phút) | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | <bước đã làm, khớp mục 2> | xong | YYYY-MM-DD HH:mm | YYYY-MM-DD HH:mm | <phút> | |
| **Tổng** | | | | | **<tổng phút>** | = <time_spent_hours>h |
```

**Quy tắc điền:**
- Mục **bắt buộc** không có nội dung → giữ heading, ghi "Không có". Mục **(Tùy chọn)** không có nội dung → bỏ hẳn.
- Bảng *Tiến độ* có cột thời gian là mục bắt buộc ở cả hai template; hàng **Tổng** luôn bằng `time_spent_hours`.
- Bảng *Giao việc* chỉ có ở template Pre của plan lớn: để trống tới khi plan `approved`; plan chốt `assign_tasks: false` hoặc không cần duyệt thì bỏ hẳn.
- Đường dẫn file luôn là markdown link tương đối tính từ file plan (`../src/...`).

## Khi nào ghi / đề xuất

**Ghi khi** người dùng yêu cầu, quy trình yêu cầu, hoặc người dùng đồng ý với đề xuất.

**Đề xuất (hỏi một câu, không tự ghi)** khi vừa xong một chuỗi thay đổi chưa có plan nào ghi lại, và có ít nhất một dấu hiệu:
- sửa từ 3 file trở lên hoặc cả một module;
- sửa bug phải điều tra qua nhiều bước;
- có quyết định kiến trúc/thiết kế hoặc tradeoff đáng nhớ;
- vừa khảo sát/phân tích codebase phức tạp.

**Không cần** cho: sửa typo, lỗi cú pháp, rename đơn lẻ, đổi một chuỗi, chỉ chạy test / format / merge upstream.

## Ví dụ tham khảo

Đọc [`references/example-plan.md`](references/example-plan.md) trước khi viết plan đầu tiên trong một repo mới. Ví dụ minh hoạ mức chi tiết của phần thân; frontmatter và heading luôn theo template ở trên.