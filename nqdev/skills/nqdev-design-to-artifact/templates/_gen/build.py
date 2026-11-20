"""Ghép fragment giao diện vào khung chung.

Fragment:  _gen/frag/<màn>.html   (chỉ phần nội dung riêng của màn)
Khung:     _gen/frame.html        (khung chung: header, sidebar... có chỗ {{title}} và {{content}})

Tiêu đề màn khai báo ngay trong fragment bằng một comment ở đầu:  <!--title: Danh sách đơn hàng-->
Không có thì dùng tên màn.

Chạy riêng để xem kết quả ghép:  python _gen/build.py <màn>
Thường không cần gọi trực tiếp: interact.py tự dùng render() cho màn chỉ có fragment.
"""
import html
import re
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent


def render(name):
    frag = (GEN / "frag" / (name + ".html")).read_text(encoding="utf-8")
    frame = (GEN / "frame.html").read_text(encoding="utf-8")
    m = re.search(r"<!--\s*title:\s*(.*?)\s*-->", frag)
    title = m.group(1) if m else name
    if m:
        frag = frag.replace(m.group(0), "", 1).lstrip("\r\n")
    # chỉ thay chỗ giữ chỗ nằm ngoài comment, để comment trong khung không bị chèn nội dung
    parts = re.split(r"(<!--.*?-->)", frame, flags=re.S)
    for i, part in enumerate(parts):
        if not part.startswith("<!--"):
            parts[i] = part.replace("{{title}}", html.escape(title)).replace("{{content}}", frag)
    return "".join(parts)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Cách dùng: python _gen/build.py <màn>")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(render(sys.argv[1]))
