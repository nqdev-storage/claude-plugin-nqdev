---
description: Kiểm tra thay đổi, git add, commit (tiếng Anh, kiểu conventional) và push lên origin. Chặn commit dữ liệu thật/secret
argument-hint: "[thông điệp commit gợi ý | --no-push | trống = tự soạn từ diff]"
allowed-tools: Bash(git:*), Bash(ls:*), Bash(grep:*), Bash(sleep:*), Read, Grep
model: haiku
---

# Git commit và push

Đầu vào (có thể trống): `$ARGUMENTS`  (`--no-push` thì chỉ commit)

## Bước 1. Xem trạng thái
```bash
git status -sb
git diff --stat
git log --oneline -5
```
- Không có thay đổi: báo "không có gì để commit" và kiểm tra `git status -sb` xem nhánh có đi trước remote không (nếu có, hỏi có push không).
- Đang ở nhánh mặc định (`main`/`master`) thì **không commit thẳng**: dừng và hỏi tạo nhánh mới.

## Bước 2. Kiểm tra an toàn trước khi add
Dừng và báo nếu danh sách thay đổi (`git status --short`) hoặc diff có:
- File dữ liệu/bí mật: `.env*` (trừ `.env.example`), `*.db`, `*.sqlite*`, `*.xlsx`, `*.pem`, `*.key`, file mật khẩu, thư mục `data/`, `backups/`.
- Chuỗi giống token/secret (`ghp_`, `github_pat_`, `AKIA`, `-----BEGIN`, `password=`, `api_key`): `git diff | grep -nE '...'` rồi xem ngữ cảnh.
- File rác sinh ra khi chạy: `*.log`, `.next/`, `node_modules/`, file tạm trong thư mục làm việc, file Next tự sửa (`next-env.d.ts`, `tsconfig.json`) mà bạn không chủ ý đổi.
Thấy gì thì **không add** file đó; nói rõ cho người dùng và chỉ commit phần an toàn (hoặc dừng nếu không tách được).

## Bước 3. Add
Đã kiểm tra ở Bước 2 thì `git add -A`; nếu có file cần bỏ ra thì add từng đường dẫn cụ thể. Kiểm tra lại bằng `git diff --cached --stat`.

## Bước 4. Commit
- Thông điệp tiếng Anh, dòng đầu dạng `type(scope): mô tả ngắn` (feat, fix, docs, refactor, test, chore), dưới 72 ký tự; thân bài (nếu cần) liệt kê thay đổi chính bằng gạch đầu dòng, nêu **vì sao** chứ không chỉ liệt kê file. `$ARGUMENTS` có gợi ý thì dùng làm gốc.
- Nhiều nhóm thay đổi không liên quan thì đề xuất tách commit; nếu các file đan xen nhau không tách sạch được thì gộp một commit và nói rõ.
- Tên/email tác giả lấy từ `git config user.name/user.email` của repo; thiếu thì hỏi, không tự bịa. Kết thúc thông điệp bằng dòng ghi công (Co-Authored-By) theo hướng dẫn của hệ thống nếu có. Không ghi tên mô hình vào thông điệp commit.
- Dùng HEREDOC: `git commit -F - <<'EOF' ... EOF`. **Không** dùng `--no-verify`, không `--amend` commit đã push.
- Hook lỗi: đọc lỗi, sửa nguyên nhân, add lại và tạo commit mới.

## Bước 5. Push
```bash
git push -u origin <nhánh hiện tại>
```
- Chỉ retry khi lỗi mạng, tối đa 4 lần cách 2s, 4s, 8s, 16s. Bị từ chối vì remote đi trước thì `git fetch origin <nhánh>` rồi báo, **không** force push; hỏi người dùng muốn rebase hay merge.
- Không tự tạo hay merge Pull Request, trừ khi người dùng yêu cầu rõ.

## Bước 6. Báo cáo
Một đến hai câu: hash và tiêu đề commit, nhánh, `git status -sb` sau push (đã khớp remote chưa). Có file bị bỏ qua vì lý do an toàn thì liệt kê. Nhắc PR đang mở (nếu biết) sẽ tự nhận commit mới.
