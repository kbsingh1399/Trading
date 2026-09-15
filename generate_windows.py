import json
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 7, 1)

all_months = []
curr = start_date
while curr <= end_date:
    all_months.append(curr)
    curr += relativedelta(months=1)

random.seed(99) # New seed
selected_months = random.sample(all_months, 20)
selected_months.sort()

windows = []
for i, m in enumerate(selected_months):
    m_end = m + relativedelta(months=1, days=-1)
    windows.append({
        "window_id": i+1,
        "name": m.strftime("%B %Y") + " Random OOS",
        "start_date": m.strftime("%Y-%m-%d"),
        "end_date": m_end.strftime("%Y-%m-%d"),
        "regime": "Random",
        "description": "Randomly generated monthly OOS window for goal verification."
    })

with open("Engine/oos_windows_20_random.json", "w") as f:
    json.dump(windows, f, indent=4)

print("Generated 20 NEW random monthly windows:")
for w in windows:
    print(f"{w['start_date']} to {w['end_date']}")
