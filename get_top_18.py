import json

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

pnl_map = {}
for sym, windows in results.items():
    total_pnl = sum([w['pnl'] for w in windows])
    pnl_map[sym] = total_pnl

sorted_assets = sorted(pnl_map.items(), key=lambda x: x[1], reverse=True)
top_18 = sorted_assets[:18]

print(">>> THE GOLDEN 18 PORTFOLIO <<<")
for i, (sym, pnl) in enumerate(top_18):
    print(f"{i+1}. {sym}: ${pnl:.2f}")
