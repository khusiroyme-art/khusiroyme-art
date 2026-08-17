import os

WIDTH = 490
LINE_H = 24
PAD_X = 18
TITLE_H = 34

BG = "#0d1117"
BORDER = "#30363d"
TITLE_BG = "#161b22"
DOT_RED, DOT_YEL, DOT_GRN = "#ff5f56", "#ffbd2e", "#27c93f"
KEY_COLOR = "#39d353"     # green like prompt
VAL_COLOR = "#c9d1d9"
DIM = "#8b949e"

# (key, value) rows -- fits her real stack from memory
ROWS = [
    ("OS",       "Full-Stack Developer & AI Engineer"),
    ("Host",     "Guru Nanak Institute of Technology"),
    ("Now",      "AI Intern Candidate @ IntraEats"),
    ("Stack",    "React * Flask * Node.js * Three.js"),
    ("Learning", "ML / NLP * Sentiment Analysis * scikit-learn"),
    ("Project",  "Innovation_Nova - AI Interior Designer"),
    ("Hobbies",  "Guitar * Reading * Personal Style"),
    ("Fun fact", "Debugs better with music on"),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_svg(rows, out_path="info-card.svg"):
    static = os.environ.get("STATIC") == "1"
    height = TITLE_H + len(rows) * LINE_H + 26

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
                  f'font-family="Consolas, Menlo, monospace" font-size="13.5">')
    parts.append(f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{height-1}" rx="8" '
                 f'fill="{BG}" stroke="{BORDER}"/>')
    # title bar
    parts.append(f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{TITLE_H}" rx="8" fill="{TITLE_BG}"/>')
    parts.append(f'<rect x="0.5" y="{TITLE_H-8}" width="{WIDTH-1}" height="8" fill="{TITLE_BG}"/>')
    parts.append(f'<circle cx="26" cy="{TITLE_H/2}" r="6" fill="{DOT_RED}"/>')
    parts.append(f'<circle cx="46" cy="{TITLE_H/2}" r="6" fill="{DOT_YEL}"/>')
    parts.append(f'<circle cx="66" cy="{TITLE_H/2}" r="6" fill="{DOT_GRN}"/>')
    parts.append(f'<text x="{WIDTH/2}" y="{TITLE_H/2+5}" fill="{DIM}" text-anchor="middle" '
                 f'font-size="12">khusi@github: ~</text>')

    key_w = max(len(k) for k, _ in rows) + 1

    for i, (k, v) in enumerate(rows):
        y = TITLE_H + 26 + i * LINE_H
        delay = 0.5 + i * 0.12
        opacity = "1" if static else "0"
        anim = "" if static else (
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" '
            f'dur="0.35s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-6 0" to="0 0" begin="{delay:.2f}s" dur="0.35s" fill="freeze" '
            f'calcMode="spline" keySplines="0.2 0 0.2 1"/>'
        )
        parts.append(
            f'<g opacity="{opacity}">'
            f'<text x="{PAD_X}" y="{y}" fill="{KEY_COLOR}">{esc(k)}</text>'
            f'<text x="{PAD_X + key_w*8.1}" y="{y}" fill="{VAL_COLOR}">{esc(v)}</text>'
            f'{anim}'
            f'</g>'
        )

    # color swatch row at bottom like real neofetch
    swatches = ["#0d1117","#ff5f56","#27c93f","#ffbd2e","#39d353","#58a6ff","#bc8cff","#c9d1d9"]
    sw_y = TITLE_H + 26 + len(rows) * LINE_H
    for i, c in enumerate(swatches):
        delay = 0.5 + len(rows) * 0.12 + 0.1
        parts.append(f'<rect x="{PAD_X + i*20}" y="{sw_y - 10}" width="16" height="12" rx="2" '
                     f'fill="{c}" stroke="{BORDER}" opacity="{"1" if static else "0"}">')
        if not static:
            parts.append(f'<animate attributeName="opacity" from="0" to="1" '
                         f'begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>')
        parts.append('</rect>')

    parts.append('</svg>')
    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print("wrote", out_path)

if __name__ == "__main__":
    build_svg(ROWS)
