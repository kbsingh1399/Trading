import json
import collections

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

portfolio = collections.defaultdict(lambda: {'trades': 0, 'wins': 0, 'pnl': 0.0})

for sym, windows in results.items():
    for w in windows:
        name = w['window']
        portfolio[name]['trades'] += w['trades']
        portfolio[name]['wins'] += w['wins']
        portfolio[name]['pnl'] += w['pnl']

print("Portfolio OOS Performance (All Assets Aggregated):")
for name, data in portfolio.items():
    wr = (data['wins'] / data['trades'] * 100) if data['trades'] > 0 else 0
    pnl = data['pnl']
    print(f"[{name}] Trades: {data['trades']} | WR: {wr:.1f}% | PnL: ${pnl:.2f}")
