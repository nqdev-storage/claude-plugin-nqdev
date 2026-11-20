"""Kiểm tra bộ prototype, CHỈ ĐỌC (không ghi file, không publish, không chạy app).

Chạy:  python _gen/check.py [--strict]

Gồm:
  1. interact.py --all --dry   nút thiếu hành vi, hành vi mồ côi, màn thiếu trong canvas.json, đầu ra cũ/chưa dựng
  2. lint_theme.py             lệch theme (gradient, bóng màu, bo góc, trọng số chữ, màu ngoài token)
  3. UI sạch                   câu dài hiển thị trên giao diện, "Lorem", "TODO" (ngoài comment/script/style)
  4. Publish                   màn đã đổi so với bản đã publish (.artifact.json); chưa publish thì ghi "chưa publish"
Thoát mã 1 nếu --strict và có vấn đề ở mục 1-3 (mục 4 chỉ để thông tin).
"""
import re
import subprocess
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent
ROOT = GEN.parent
LONG = 90  # số ký tự của một đoạn chữ hiển thị bị coi là "mô tả"


def run(*args):
    p = subprocess.run([sys.executable, str(GEN / args[0])] + list(args[1:]), capture_output=True, text=True, encoding="utf-8")
    return p.returncode, (p.stdout + p.stderr).strip()


def clean_ui():
    issues = []
    for f in sorted(list((GEN / "orig").glob("*")) + list((GEN / "frag").glob("*"))):
        if not f.is_file() or f.stem.split(".")[0] in ("system-design", "blank"):
            continue  # System Design là tài liệu thiết kế, cho phép chữ giải thích ("blank" là tên cũ)
        src = f.read_text(encoding="utf-8", errors="ignore")
        src = re.sub(r"<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>", " ", src, flags=re.S | re.I)
        for m in re.finditer(r">([^<>]+)<", src):
            txt = " ".join(m.group(1).split())
            if re.search(r"lorem|\bTODO\b|mô tả ở đây", txt, re.I):
                issues.append("%s  placeholder: %s" % (f.name, txt[:70]))
            elif len(txt) >= LONG:
                issues.append("%s  đoạn chữ dài (có thể là mô tả tính năng): %s…" % (f.name, txt[:70]))
    return issues


def main(argv):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    problems = 0

    rc, out = run("interact.py", "--all", "--dry")
    warn = [l for l in out.splitlines() if l.startswith(("CẢNH BÁO", "LỖI"))]
    print("== 1. Nút, hành vi, canvas, đầu ra ==")
    print("\n".join(warn) if warn else "Sạch.")
    problems += len(warn) + (1 if rc not in (0, 1) else 0)

    rc, out = run("lint_theme.py")
    print("\n== 2. Lệch theme ==")
    print(out)
    problems += len([l for l in out.splitlines() if re.search(r":\d+  ", l)])

    ui = clean_ui()
    print("\n== 3. UI sạch ==")
    print("\n".join(ui) if ui else "Sạch.")
    problems += len(ui)

    rc, out = run("interact.py", "--changed")
    print("\n== 4. Publish (thông tin) ==")
    meta = ROOT / ".artifact.json"
    if not meta.is_file() or '"url"' not in meta.read_text(encoding="utf-8"):
        print("Chưa publish.")
    else:
        print("Màn đã đổi so với bản đã publish:\n" + out if out else "Không có màn nào đổi.")

    print("\nTổng: %d vấn đề." % problems)
    return 1 if (problems and "--strict" in argv) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
