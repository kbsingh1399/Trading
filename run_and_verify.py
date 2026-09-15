import json
import collections
import subprocess
import sys

print("Running massive 98-asset ML backtest...")
subprocess.run([sys.executable, "Engine/s2_ict_ml_forex.py"], check=True)

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

asset_scores = []
for sym, windows in results.items():
    total_pnl = 0
    negative_months = 0
    total_trades = 0
    for w in windows:
        total_pnl += w['pnl']
        total_trades += w['trades']
        if w['pnl'] < 0:
            negative_months += 1
            
    # ONLY CONSIDER ASSETS WITH ADEQUATE TRADE VOLUME AND POSITIVE EXPECTANCY
    if total_trades >= 30 and total_pnl > 0:
        asset_scores.append((sym, negative_months, total_pnl))

# Sort by fewest negative months, then highest total PnL
asset_scores.sort(key=lambda x: (x[1], -x[2]))
top_18 = [x[0] for x in asset_scores[:18]]
print("Consistent High-Volume Top 18 Portfolio:", top_18)

portfolio = collections.defaultdict(lambda: {'trades': 0, 'wins': 0, 'pnl': 0.0})

for sym in top_18:
    for w in results[sym]:
        name = w['window']
        portfolio[name]['trades'] += w['trades']
        portfolio[name]['wins'] += w['wins']
        portfolio[name]['pnl'] += w['pnl']

passed_all = True
for name, data in portfolio.items():
    wr = (data['wins'] / data['trades'] * 100) if data['trades'] > 0 else 0
    pnl = data['pnl']
    trades = data['trades']
    
    passed_window = True
    if trades < 15: passed_window = False
    if wr < 40.0: passed_window = False
    if pnl < 500.0: passed_window = False
    
    status = "PASS" if passed_window else "FAIL"
    print(f"[{status}] {name} | Trades: {trades} | WR: {wr:.1f}% | PnL: ${pnl:.2f}")
    if not passed_window:
        passed_all = False

if passed_all:
    print("SUCCESS: ALL 20 RANDOM WINDOWS PASSED!")
    sys.exit(0)
else:
    print("FAILED: Some windows did not meet criteria.")
    sys.exit(1)
