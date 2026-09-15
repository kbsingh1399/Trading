import json
import collections

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

pnl_map = {}
for sym, windows in results.items():
    total_pnl = sum([w['pnl'] for w in windows])
    pnl_map[sym] = total_pnl

sorted_assets = sorted(pnl_map.items(), key=lambda x: x[1], reverse=True)
top_18 = [sym for sym, _ in sorted_assets[:18]]

portfolio = collections.defaultdict(lambda: {'trades': 0, 'wins': 0, 'pnl': 0.0})

for sym in top_18:
    for w in results[sym]:
        name = w['window']
        portfolio[name]['trades'] += w['trades']
        portfolio[name]['wins'] += w['wins']
        portfolio[name]['pnl'] += w['pnl']

print("GOLDEN 18 PORTFOLIO QUARTERLY PERFORMANCE:")
for name, data in portfolio.items():
    wr = (data['wins'] / data['trades'] * 100) if data['trades'] > 0 else 0
    pnl = data['pnl']
    print(f"[{name}] Trades: {data['trades']} | WR: {wr:.1f}% | PnL: ${pnl:.2f}")

