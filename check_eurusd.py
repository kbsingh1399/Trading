import json

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

print("EURUSD Performance:")
for w in results['EURUSD']:
    print(f"Window: {w['window']} | Trades: {w['trades']} | PnL: {w['pnl']}")
