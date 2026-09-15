import json

with open('Engine/forex_oos_results.json', 'r') as f:
    results = json.load(f)

passed_symbols = []
for sym, windows in results.items():
    passed = True
    for w in windows:
        if w['trades'] < 15: # from the active context rule
            passed = False
            break
        if w['pnl'] < 0: # just rough check if it survived all quarters
            pass
            
    # For now let's just print the best performing ones
    total_pnl = sum([w['pnl'] for w in windows])
    if total_pnl > 1000:
        print(f"Good Candidate: {sym} | Total PnL: {total_pnl}")

