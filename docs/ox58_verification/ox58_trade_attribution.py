"""OX58-E3: Executed-trade attribution for elite_23_oos_all_trades.parquet.

Works with both the pristine artifact (window_id/time/pnl/sleeve) and the
OX58 symbol-traced artifact (+symbol/strategy/r_gain/risk/prob).

Usage:  python3 ox58_trade_attribution.py <trades.parquet>
"""
import sys
import pandas as pd

t = pd.read_parquet(sys.argv[1])
print(f"rows={len(t)} total_pnl={t['pnl'].sum():+,.2f}")
if "strategy" in t.columns:
    print(t.groupby("strategy").agg(n=("pnl", "size"), pnl=("pnl", "sum"),
                                    meanR=("r_gain", "mean")).round(2).to_string())
    fx = ["GER30", "FR40", "US2000", "GAS", "XAUCNH", "NICKEL"]
    orb = t[t.strategy == "ORB"]
    print(f"\nORB executed={len(orb)} pnl={orb['pnl'].sum():+,.2f}")
    if len(orb):
        print(orb["symbol"].value_counts().to_string())
        print(f"FOREX ORB executed={int(orb['symbol'].isin(fx).sum())}")
    non_crypto = sorted(set(t["symbol"]) - {"BTCUSDT", "ETHUSDT", "XRPUSDT", "BNBUSDT",
                                            "DOGEUSDT", "ADAUSDT", "TRXUSDT", "LINKUSDT",
                                            "DOTUSDT", "LTCUSDT", "BCHUSDT"})
    print("non-crypto symbols anywhere:", non_crypto)
else:
    print(t.groupby("sleeve").agg(n=("pnl", "size"), pnl=("pnl", "sum")).round(2).to_string())
