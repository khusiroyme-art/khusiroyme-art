import json, sys, requests
from bs4 import BeautifulSoup
from datetime import datetime

USERNAME = "khusiroyme-art"

def fetch(username=USERNAME):
    url = f"https://github.com/users/{username}/contributions"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    days = []
    cells = soup.select("td.ContributionCalendar-day") or soup.select("rect.ContributionCalendar-day")
    for c in cells:
        date = c.get("data-date")
        count = c.get("data-level")  # fallback
        if date is None:
            continue
        # newer markup: data-date + data-level (0-4); count text sometimes in tooltip
        level = c.get("data-level")
        days.append({
            "date": date,
            "level": int(level) if level is not None else 0,
        })

    if not days:
        print("WARNING: no cells parsed, GitHub markup may differ", file=sys.stderr)

    days.sort(key=lambda d: d["date"])  # DOM order is row-major (by weekday); fix to chronological

    h2 = soup.select_one("h2.f4")
    total_text = " ".join(h2.get_text(strip=True).split()) if h2 else None

    total = len(days)
    streak = 0
    longest = 0
    cur = 0
    for d in days:
        if d["level"] and int(d["level"]) > 0:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0
    # current streak = trailing run
    for d in reversed(days):
        if d["level"] and int(d["level"]) > 0:
            streak += 1
        else:
            break

    data = {
        "username": username,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "days": days,
        "current_streak": streak,
        "longest_streak": longest,
        "total_days_recorded": total,
        "total_contributions_text": total_text,
    }
    with open("data/contributions.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"wrote data/contributions.json ({total} days, streak {streak})")

if __name__ == "__main__":
    fetch(sys.argv[1] if len(sys.argv) > 1 else USERNAME)
