import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 12
GAP = 3
LEFT_PAD = 28
TOP_PAD = 20
BOTTOM_PAD = 34

def load_weeks(path="data/contributions.json"):
    data = json.load(open(path))
    days = data["days"]  # chronological
    # bucket into weeks starting Sunday, like GitHub's calendar
    weeks = []
    week = [None] * 7
    from datetime import date as ddate
    for d in days:
        y, m, dd = map(int, d["date"].split("-"))
        weekday = ddate(y, m, dd).isoweekday() % 7  # Sun=0
        week[weekday] = d
        if weekday == 6:
            weeks.append(week)
            week = [None] * 7
    if any(week):
        weeks.append(week)
    return weeks, data

def build_svg(weeks, meta, out_path="contrib-heatmap.svg"):
    n_weeks = len(weeks)
    width = LEFT_PAD + n_weeks * (CELL + GAP) + 200  # extra room for legend
    height = TOP_PAD + 7 * (CELL + GAP) + BOTTOM_PAD

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
                  f'font-family="Consolas, Menlo, monospace" font-size="11">')
    parts.append('<style>.dow{fill:#8b949e;}</style>')

    dow_labels = {1: "Mon", 3: "Wed", 5: "Fri"}
    for wd, label in dow_labels.items():
        y = TOP_PAD + wd * (CELL + GAP) + CELL - 2
        parts.append(f'<text x="0" y="{y}" class="dow">{label}</text>')

    idx = 0
    for wi, week in enumerate(weeks):
        for wd in range(7):
            d = week[wd]
            if d is None:
                continue
            level = d["level"]
            color = PALETTE[min(level, len(PALETTE)-1)]
            x = LEFT_PAD + wi * (CELL + GAP)
            y = TOP_PAD + wd * (CELL + GAP)
            delay = 0.15 + (wi + wd * 0.15) * 0.012
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{color}" opacity="0" transform="translate(-8,-8)">'
                f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" '
                f'dur="0.3s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" '
                f'from="-8 -8" to="0 0" begin="{delay:.3f}s" dur="0.3s" fill="freeze" '
                f'calcMode="spline" keySplines="0.2 0 0.2 1"/>'
                f'</rect>'
            )
            idx += 1

    # legend
    leg_x = LEFT_PAD + n_weeks * (CELL + GAP) + 10
    leg_y = TOP_PAD + 2
    parts.append(f'<text x="{leg_x}" y="{leg_y+9}" class="dow">Less</text>')
    for i, c in enumerate(PALETTE):
        parts.append(f'<rect x="{leg_x+38+i*15}" y="{leg_y}" width="{CELL}" height="{CELL}" '
                     f'rx="2.5" fill="{c}"/>')
    parts.append(f'<text x="{leg_x+38+len(PALETTE)*15+6}" y="{leg_y+9}" class="dow">More</text>')

    # footer stats
    footer_y = height - 10
    total_text = meta.get("total_contributions_text") or f"{meta['total_days_recorded']} days tracked"
    footer = f"{total_text}  *  current streak {meta['current_streak']}  *  longest streak {meta['longest_streak']}"
    parts.append(f'<text x="{LEFT_PAD}" y="{footer_y}" class="dow">{footer}</text>')

    parts.append('</svg>')
    with open(out_path, "w") as f:
        f.write("\n".join(parts))
    print("wrote", out_path)

if __name__ == "__main__":
    weeks, meta = load_weeks()
    build_svg(weeks, meta)
