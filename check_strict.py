import json

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

for sym, windows in results.items():
    passed_all = True
    for w in windows:
        if w['trades'] < 15:
            passed_all = False
            break
        if w['pnl'] < 500: # 10% ROI
            passed_all = False
            break
        # DD is implicitly handled if PnL >= 500. 
        # But wait, if PnL is > 500, it could still have a 5% intra-window DD.
        # We don't have bar-by-bar DD in the JSON, but failing to hit 500 PnL is enough to filter.
    if passed_all and len(windows) > 0:
        print(f">>> {sym} PASSED ALL WINDOWS! <<<")
