from PIL import Image

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense)

COLS = 100
ROWS = 53
CHAR_W = 6.1
CHAR_H = 11
FONT_SIZE = 11
FILL = "#8b949e"        # monochrome light-gray, GitHub dark-mode friendly

def img_to_ascii_rows(path, cols=COLS, rows=ROWS):
    img = Image.open(path).convert("L")
    # char cells are taller than wide -> sample with an aspect correction
    img = img.resize((cols, rows))
    px = img.load()
    lines = []
    ramp_len = len(RAMP) - 1
    for y in range(rows):
        line = []
        for x in range(cols):
            v = px[x, y]              # 0 dark .. 255 bright
            idx = int((255 - v) / 255 * ramp_len)
            line.append(RAMP[idx])
        lines.append("".join(line).rstrip())
    return lines

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace(" ", "&#160;"))

def build_svg(lines, out_path="avi-ascii.svg"):
    width = COLS * CHAR_W
    height = ROWS * CHAR_H
    row_dur = 0.045          # stagger per row
    wipe_dur = 0.35          # wipe speed per row

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
                  f'font-family="Consolas, Menlo, monospace" font-size="{FONT_SIZE}">')
    parts.append(f'<rect width="100%" height="100%" fill="transparent"/>')
    parts.append('<style>text{white-space:pre;}</style>')

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        y = (i + 1) * CHAR_H - 2
        delay = i * row_dur
        clip_id = f"clip{i}"
        text = esc(line)
        text_w = len(line) * CHAR_W
        parts.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="{y - CHAR_H}" width="0" height="{CHAR_H+4}">'
            f'<animate attributeName="width" from="0" to="{text_w:.0f}" '
            f'begin="{delay:.3f}s" dur="{wipe_dur}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.2 0 0.2 1"/>'
            f'</rect></clipPath>'
        )
        parts.append(
            f'<g clip-path="url(#{clip_id})">'
            f'<text x="0" y="{y}" fill="{FILL}">{text}</text>'
            f'</g>'
        )
        # small cursor block riding the wipe edge
        parts.append(
            f'<rect x="0" y="{y - CHAR_H + 2}" width="{CHAR_W:.1f}" height="{CHAR_H-2}" fill="{FILL}" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.9;1" '
            f'begin="{delay:.3f}s" dur="{wipe_dur}s" fill="freeze"/>'
            f'<animate attributeName="x" from="0" to="{text_w:.0f}" '
            f'begin="{delay:.3f}s" dur="{wipe_dur}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.2 0 0.2 1"/>'
            f'</rect>'
        )

    parts.append('</svg>')
    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print("wrote", out_path)

if __name__ == "__main__":
    lines = img_to_ascii_rows("source-prepped.png")
    build_svg(lines)
