---
name: nqdev-write-plan
description: "Viết execution plan (trước khi làm) hoặc nhật ký công việc (sau khi làm) thành file markdown trong thư mục plans/ ở gốc repo, theo quy ước plans/<stt>-<YYYY-MM-DD>-<slug>.md (stt là số thứ tự 3 chữ số) và template có frontmatter, bắt buộc có thời gian ước lượng, cộng dồn thời gian thực tế sau mỗi lần làm, và cập nhật trạng thái plan khi làm tiếp hoặc xong việc. Dùng khi người dùng nói \"viết execution plan\", \"lên kế hoạch rồi ghi vào plans\", \"ghi lại kế hoạch\", \"cập nhật trạng thái plan\", \"ghi nhận thời gian làm vào plan\", \"log công việc vừa làm\", \"viết nhật ký công việc\", \"lưu lại những gì vừa làm\", \"save work log\", \"record decision\", \"write execution plan\", hoặc khi một quy trình khác (VD Development Workflow Policy của nqdev-init-agents) yêu cầu viết plan trước khi code. Có thể chủ động đề xuất sau một chuỗi thay đổi đáng ghi, nhưng chỉ ghi file khi người dùng đồng ý. Không dùng khi người dùng chỉ muốn bàn kế hoạch trong chat, viết BRD/PRD (nqdev-brd-prd-writer) hay estimate (nqdev-requirement-estimator)."
license: MIT
compatibility: Claude Code, OpenCode, Gemini CLI, Codex CLI, Claude.ai
version: '1.5.0'
author: QuyIT Platform
created_date: '2026-11-17'
updated_date: '2026-11-19'
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(git rev-parse:*), Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(mkdir:*)
metadata:
  author: QuyIT Platform
  version: "1.5.0"
  created_date: "2026-11-17"
  updated_date: "2026-11-19"
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
planning → in_progress → completed
               ↘ blocked / paused ↗
```

- **Bắt đầu làm:** `status: in_progress`. Cập nhật cột Trạng thái trong bảng *Tiến độ* (`chưa làm` / `đang làm` / `xong` / `bỏ`) sau mỗi bước, để plan luôn khớp tiến độ thật.
- **Sau mỗi lần làm:** thêm một dòng vào *Nhật ký thời gian* và cộng dồn vào `time_spent_hours` (xem *Ghi nhận thời gian*).
- **Plan đổi đáng kể khi đang làm:** sửa mục Approach / Tiến độ và thêm một dòng vào *Nhật ký thay đổi plan* (ngày: đổi gì, vì sao). Nếu plan cần duyệt, xin duyệt lại.
- **Xong hoặc tạm dừng:** thêm mục `## Kết quả` ngay trước *Nhật ký thời gian* (cấu trúc như mục 2–6 của Template Post), đổi `status`, ghi dòng thời gian của lần làm cuối và điền `completed_date` (khi `completed`).

## Frontmatter (chung cho cả hai chế độ)

```yaml
---
mode: <pre | post>
type: <bug-fix | refactor | feature | architecture | investigation | other>
status: <planning | in_progress | blocked | paused | completed>
priority: <low | medium | high>
complexity: <low | medium | high>
impact: <low | medium | high>
related_issues: []
related_prs: []
estimated_hours:      # Pre: bắt buộc, điền khi lập plan (VD 4, bước 0.5). Post: tuỳ chọn
time_spent_hours: 0   # tổng thời gian thực tế, cộng dồn sau mỗi lần làm
completed_date:       # YYYY-MM-DD khi status = completed
---
```

Số giờ ghi dạng số (`4`, `1.5`), không dùng `~`. Trường không có giá trị thì để trống, không xoá, để mọi file cùng schema và lọc được bằng grep (VD `grep -l "status: in_progress" plans/*.md`).

## Ghi nhận thời gian

- **Đơn vị:** giờ. **Thời gian thực tế** (`time_spent_hours`, bảng nhật ký) làm tròn đến 0.25 (15 phút); lần làm ngắn hơn vẫn ghi 0.25. **Ước lượng** (`estimated_hours`) làm tròn đến **0.5** (30 phút).
- **Ước lượng:** `estimated_hours` bắt buộc với plan Pre, điền khi lập plan. Nhật ký Post không có ước lượng trước thì để trống. Mô hình: **AI là người làm, DEV là người review và góp ý**; `estimated_hours` là tổng end-to-end (thời gian AI làm, DEV review và các vòng sửa theo góp ý) tới khi sẵn sàng merge. Baseline tham khảo: `nqdev-requirement-estimator` (`references/baselines.md`).
- **Một lần làm** là một phiên có thực hiện ít nhất một task của plan (code, điều tra, test, sửa plan theo yêu cầu). Chỉ mở plan ra tra cứu thì không tính.
- **Cuối mỗi lần làm** (trước khi báo xong bước hoặc kết thúc phiên):
  1. Đề xuất số giờ của lần này từ các mốc có được: lúc bắt đầu và kết thúc phiên, thời điểm tin nhắn, thời điểm commit. Không có căn cứ thì hỏi thẳng.
  2. Hỏi người dùng xác nhận hoặc sửa, VD: "Lần này khoảng 1.5h, ghi nhận vậy nhé?"
  3. Thêm một dòng vào *Nhật ký thời gian* và đặt `time_spent_hours` bằng tổng cột Số giờ.
  - Không có người để hỏi (VD phiên chạy theo lịch) → ghi số đề xuất, cột Ghi chú ghi "ước lượng, chưa xác nhận".
- **Vượt ước lượng:** chỉ ghi nhận, không tự sửa `estimated_hours`. Người dùng muốn ước lượng lại → sửa `estimated_hours` và ghi một dòng vào *Nhật ký thay đổi plan* (cũ → mới, lý do).
- **Plan cũ chưa có bảng:** thêm bảng khi cập nhật lần đầu. Nếu `time_spent_hours` đã có số, ghi một dòng "Trước khi có nhật ký thời gian" với số đó để tổng vẫn khớp; giá trị dạng `~X` đổi thành `X`.

```markdown
## Nhật ký thời gian
| Ngày | Số giờ | Việc đã làm | Ghi chú |
|---|---|---|---|
| YYYY-MM-DD | 1.5 | <task/bước đã làm trong lần này> | |
| **Tổng** | **1.5** | | Ước lượng: 4 |
```

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
| # | Bước | Trạng thái | Ghi chú |
|---|---|---|---|
| 1 | <bước 1> | chưa làm | |
| 2 | <bước 2> | chưa làm | |

Trạng thái: `chưa làm` / `đang làm` / `xong` / `bỏ` (bỏ thì ghi lý do ở cột Ghi chú).

## 4. Risks và Unknowns
- **Risk:** <mô tả> → **Mitigation:** <cách xử lý>
- **Unknown:** <chưa rõ gì> → **Plan:** <cách tìm hiểu>

## 5. Tiêu chí hoàn thành
<Điều kiện cụ thể để coi là xong: test pass, hành vi mong đợi, checklist.>

## 6. Câu hỏi / Phụ thuộc (Tùy chọn)
<Cần input từ ai, phụ thuộc task nào, cần review trước khi làm không.>

## Nhật ký thời gian
| Ngày | Số giờ | Việc đã làm | Ghi chú |
|---|---|---|---|
| **Tổng** | **0** | | Ước lượng: <estimated_hours> |

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

## Nhật ký thời gian
| Ngày | Số giờ | Việc đã làm | Ghi chú |
|---|---|---|---|
| YYYY-MM-DD | <số giờ> | <việc đã làm> | |
| **Tổng** | **<time_spent_hours>** | | |
```

**Quy tắc điền:**
- Mục **bắt buộc** không có nội dung → giữ heading, ghi "Không có". Mục **(Tùy chọn)** không có nội dung → bỏ hẳn.
- *Nhật ký thời gian* là mục bắt buộc ở cả hai template; hàng **Tổng** luôn bằng `time_spent_hours`.
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