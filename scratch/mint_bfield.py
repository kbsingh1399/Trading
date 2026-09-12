"""Mint fresh certification windows (B-field) from untouched gap months.

Rules:
- B months must be >34 days clear of ANY design/holdout window start or end date
  (covers 30d holds + warmup; entry-side fully disjoint from every W window).
- B windows never enter any optimizer objective; they exist solely for certification.
"""
import json
from datetime import datetime, timedelta

REPO = __import__("pathlib").Path(__file__).resolve().parent.parent
WINS = json.load(open(REPO / "Engine" / "oos_windows_20.json"))

# all window date boundaries
bounds = []
for w in WINS:
    s = datetime.strptime(w["start_date"], "%Y-%m-%d")
    e = datetime.strptime(w["end_date"], "%Y-%m-%d")
    bounds.append((s, e))

# candidate full months: 2020-09 .. 2026-08
months = []
y, m = 2020, 9
while (y, m) <= (2026, 8):
    s = datetime(y, m, 1)
    e = (datetime(y + (m == 12), (m % 12) + 1, 1) - timedelta(days=1))
    months.append((s, e))
    m += 1
    if m == 13:
        y += 1
        m = 1

CLEAR_D = 15
bfield = []
for s, e in months:
    ok = True
    for ws, we in bounds:
        # B month must not overlap [ws-CLEAR, we+CLEAR]
        if s <= we + timedelta(days=CLEAR_D) and e >= ws - timedelta(days=CLEAR_D):
            ok = False
            break
    if ok:
        bfield.append({"window_id": None, "start_date": s.strftime("%Y-%m-%d"),
                       "end_date": e.strftime("%Y-%m-%d")})

for i, b in enumerate(bfield, 1):
    b["window_id"] = i
    b["name"] = f"B-field month {i}"
    b["regime"] = "untouched-gap"
    b["description"] = "gap month >34d clear of all W01-W20 windows; never scored by optimizer"

out = REPO / "Engine" / "oos_windows_bfield.json"
json.dump(bfield, open(out, "w"), indent=2)
print(f"minted {len(bfield)} B-field windows -> {out}")
for b in bfield:
    print(f"B{b['window_id']:>2} {b['start_date']} -> {b['end_date']}")
