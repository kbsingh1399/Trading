import json

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

for sym, windows in results.items():
    print(f"{sym}: {len(windows)} windows tested")
