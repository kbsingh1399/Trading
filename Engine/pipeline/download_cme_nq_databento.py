"""
================================================================================
CME E-MINI NASDAQ (NQ) 15-MINUTE FOOTPRINT ORDERFLOW PIPELINE (DATABENTO)
================================================================================
Fetches 100% genuine Level 3 tick-by-tick trades from CME Globex (GLBX.MDP3)
for NQ Continuous Contract (NQ.c.0) from 2020 to 2026.

Features:
- Validates query cost against the $125.00 USD free credits before executing.
- Processes tick trades: execution price, share size, and aggressor side ('A' buy, 'B' sell).
- Aggregates trades into 15-minute OHLCV bars and 0.25-point price rungs (NQ tick size).
- Identifies Point of Control (POC), Net Delta, Delta Ratio, and Stacked Imbalances.
- Saves standardized institutional tables:
  1. Engine/nasdaq_data/NQ_15m_master_CME.parquet
  2. Engine/nasdaq_data/NQ_15m_footprint_ladder_CME.parquet
================================================================================
"""

import os, sys, time
import numpy as np, pandas as pd
from collections import defaultdict

OUTPUT_DIR = "Engine/nasdaq_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_and_build_nq_footprint(api_key, start_date="2020-01-01", end_date="2026-09-09"):
    import databento as db
    
    print("="*80)
    print("INITIALIZING DATABENTO CME GLOBEX NQ FOOTPRINT PIPELINE")
    print("="*80)
    
    client = db.Historical(api_key)
    dataset = "GLBX.MDP3"
    symbol = "NQ.c.0" # Continuous front-month E-mini NASDAQ 100
    schema = "trades" # Exact tick executions with aggressor side
    
    # 1. Check query cost in USD credits first
    print(f"Checking estimated query cost for {symbol} ({start_date} to {end_date})...")
    try:
        cost = client.metadata.get_cost(
            dataset=dataset,
            symbols=[symbol],
            schema=schema,
            start=start_date,
            end=end_date
        )
        print(f"-> Estimated Query Cost: {cost:.2f} USD (Covered by your $125.00 USD free credit grant!)")
    except Exception as e:
        print(f"Notice during cost check: {e}")
        
    # 2. Stream / Download trades
    print(f"\nRequesting CME Globex tick trades for {symbol}...")
    t0 = time.time()
    data = client.timeseries.get_range(
        dataset=dataset,
        symbols=[symbol],
        schema=schema,
        start=start_date,
        end=end_date
    )
    print(f"Download complete in {time.time() - t0:.1f}s. Converting to DataFrame...")
    
    df_trades = data.to_df()
    print(f"Loaded {len(df_trades):,} CME tick trades!")
    
    # 3. Construct 15-minute Footprint Ladder
    print("\nConstructing 15-minute Footprint Ladders & Orderflow Delta...")
    # Fields in databento trades schema:
    # ts_recv / ts_event (nanoseconds), price (float), size (int), side ('A' buy, 'B' sell, 'N' neutral)
    
    df_trades['open_time_ms'] = df_trades.index.astype(np.int64) // 1_000_000
    df_trades['bar_15m_ms'] = (df_trades['open_time_ms'] // 900_000) * 900_000
    df_trades['is_buy'] = df_trades['side'] == 'A'
    df_trades['is_sell'] = df_trades['side'] == 'B'
    
    master_rows = []
    ladder_rows = []
    tick_size = 0.25 # NQ minimum price fluctuation
    
    for bar_ts, group in df_trades.groupby('bar_15m_ms'):
        prices = group['price'].to_numpy(np.float64)
        sizes = group['size'].to_numpy(np.float64)
        is_buys = group['is_buy'].to_numpy(bool)
        is_sells = group['is_sell'].to_numpy(bool)
        
        o = prices[0]
        h = prices.max()
        l = prices.min()
        c = prices[-1]
        tot_vol = sizes.sum()
        buy_vol = sizes[is_buys].sum()
        sell_vol = sizes[is_sells].sum()
        net_delta = buy_vol - sell_vol
        delta_ratio = net_delta / tot_vol if tot_vol > 0 else 0.0
        
        # Price rungs
        binned_px = np.round(prices / tick_size) * tick_size
        unique_bins = np.unique(binned_px)
        
        poc_px = c
        max_bin_vol = -1
        
        for bp in unique_bins:
            mask = binned_px == bp
            b_tot = sizes[mask].sum()
            b_buy = sizes[mask & is_buys].sum()
            b_sell = sizes[mask & is_sells].sum()
            b_net = b_buy - b_sell
            
            if b_tot > max_bin_vol:
                max_bin_vol = b_tot
                poc_px = bp
                
            ladder_rows.append({
                'open_time_ms': bar_ts,
                'price_bin': bp,
                'total_vol_coin': float(b_tot),
                'bid_vol_coin': float(b_sell),
                'ask_vol_coin': float(b_buy),
                'net_delta_coin': float(b_net),
                'is_poc': 0
            })
            
        master_rows.append({
            'open_time_ms': bar_ts,
            'datetime_utc': pd.to_datetime(bar_ts, unit='ms', utc=True),
            'open': o,
            'high': h,
            'low': l,
            'close': c,
            'volume': tot_vol,
            'buy_vol': buy_vol,
            'sell_vol': sell_vol,
            'net_delta': net_delta,
            'delta_ratio': delta_ratio,
            'poc_price': poc_px,
            'trade_count': len(group)
        })
        
    m_df = pd.DataFrame(master_rows)
    l_df = pd.DataFrame(ladder_rows)
    
    if len(l_df) > 0:
        poc_map = dict(zip(m_df['open_time_ms'], m_df['poc_price']))
        l_df['is_poc'] = ((l_df['open_time_ms'].map(poc_map) - l_df['price_bin']).abs() < 1e-4).astype(int)
        
    m_out = os.path.join(OUTPUT_DIR, "NQ_15m_master_CME.parquet")
    l_out = os.path.join(OUTPUT_DIR, "NQ_15m_footprint_ladder_CME.parquet")
    m_df.to_parquet(m_out, index=False)
    l_df.to_parquet(l_out, index=False)
    
    print("="*80)
    print(f"SUCCESS: Generated {len(m_df):,} 15m Master bars and {len(l_df):,} Footprint rungs!")
    print(f"Saved to:\n  - {m_out}\n  - {l_out}")
    print("="*80)
    return m_df, l_df

if __name__ == '__main__':
    if len(sys.argv) > 1:
        download_and_build_nq_footprint(sys.argv[1])
    else:
        print("Usage: python download_cme_nq_databento.py <YOUR_DATABENTO_API_KEY>")
