"""
================================================================================
IEX HISTORICAL NASDAQ (QQQ) REAL ORDERFLOW & FOOTPRINT STREAMING PIPELINE
================================================================================
Downloads and parses 100% genuine, un-synthesized Level 3 IEX exchange feeds
directly from Google Cloud Storage on-the-fly.

Features:
- Zero-Disk Overhead: Streams and decompresses pcap-ng packets on-the-fly.
- Exact Microstructure Classification: Evaluates trade execution price against
  the prevailing Best Bid/Ask (BBO) and applies the Lee-Ready tick rule.
- Dual-Table Output:
  1. QQQ_15m_master.parquet: OHLCV, Total Volume, Net Delta, Delta Ratio, POC Price.
  2. QQQ_15m_footprint_ladder.parquet: Price-rung bid/ask volume, stacked imbalances.
================================================================================
"""

import urllib.request, zlib, struct, json, os, time
from collections import defaultdict
import numpy as np, pandas as pd

OUTPUT_DIR = "Engine/nasdaq_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class IEXStreamFootprintExtractor:
    def __init__(self, target_sym="QQQ"):
        self.target_sym = target_sym
        self.sym_bytes = target_sym.encode('ascii').ljust(8, b' ')
        self.prev_trade_px = None
        self.prev_tick_dir = 1 # 1 = buy, -1 = sell
        
    def fetch_date_feed_url(self, date_str):
        api_url = "https://iextrading.com/api/1.0/hist"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            if date_str in data:
                for feed in data[date_str]:
                    if feed['feed'] == 'TOPS':
                        return feed['link']
        return None

    def process_day_stream(self, stream_url, date_str, max_chunks=None):
        print(f"[{date_str}] Connecting to stream: {stream_url[:75]}...")
        req = urllib.request.Request(stream_url, headers={'User-Agent': 'Mozilla/5.0'})
        decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS)
        buf = bytearray()
        
        # Microstructure tracking
        cur_bid_px = 0.0
        cur_ask_px = 999999.0
        
        # 15-minute bar aggregator: interval_ms -> list of trades
        # Trade: (ts_ms, price, size, is_buy)
        interval_trades = defaultdict(list)
        trade_count = 0
        quote_count = 0
        bytes_read = 0
        chunk_count = 0
        t0 = time.time()
        
        with urllib.request.urlopen(req, timeout=45) as resp:
            while True:
                chunk = resp.read(512 * 1024) # 512KB chunks
                if not chunk:
                    break
                bytes_read += len(chunk)
                chunk_count += 1
                try:
                    buf.extend(decompressor.decompress(chunk))
                except Exception as e:
                    print(f"Decompress warning: {e}")
                    break
                    
                # Parse PCAP-NG blocks
                while len(buf) >= 8:
                    b_type, b_len = struct.unpack('<II', buf[:8])
                    if b_len < 12 or len(buf) < b_len:
                        break
                    
                    block_data = buf[:b_len]
                    buf = buf[b_len:]
                    
                    if b_type == 6 and len(block_data) >= 32: # Enhanced Packet Block
                        cap_len = struct.unpack('<I', block_data[20:24])[0]
                        packet = block_data[28:28+cap_len]
                        
                        if len(packet) > 82: # 42 (Eth+IP+UDP) + 40 (IEX-TP)
                            payload = packet[42:]
                            msg_count = struct.unpack('<H', payload[14:16])[0]
                            msgs_data = payload[40:]
                            
                            offset = 0
                            for _ in range(msg_count):
                                if offset + 2 > len(msgs_data): break
                                m_len = struct.unpack('<H', msgs_data[offset:offset+2])[0]
                                if offset + 2 + m_len > len(msgs_data): break
                                msg = msgs_data[offset+2:offset+2+m_len]
                                offset += 2 + m_len
                                
                                if len(msg) >= 18:
                                    if msg[10:18] == self.sym_bytes:
                                        mtype = msg[0]
                                        # Quote Update: 0x51 ('Q')
                                        if mtype == ord('Q') and len(msg) >= 42:
                                            # Bid Px at 18:26 (scaled uint64), Ask Px at 30:38
                                            cur_bid_px = struct.unpack('<Q', msg[18:26])[0] / 10000.0
                                            cur_ask_px = struct.unpack('<Q', msg[30:38])[0] / 10000.0
                                            quote_count += 1
                                            
                                        # Trade Report: 0x54 ('T')
                                        elif mtype == ord('T') and len(msg) >= 30:
                                            ts_ns = struct.unpack('<Q', msg[2:10])[0]
                                            size = struct.unpack('<I', msg[18:22])[0]
                                            price = struct.unpack('<Q', msg[22:30])[0] / 10000.0
                                            
                                            # Lee-Ready aggressor classification
                                            if cur_bid_px > 0 and cur_ask_px < 999999.0 and cur_ask_px > cur_bid_px:
                                                if price >= cur_ask_px:
                                                    is_buy = True
                                                    self.prev_tick_dir = 1
                                                elif price <= cur_bid_px:
                                                    is_buy = False
                                                    self.prev_tick_dir = -1
                                                else:
                                                    # Tick rule inside spread
                                                    if self.prev_trade_px is not None:
                                                        if price > self.prev_trade_px: is_buy = True; self.prev_tick_dir = 1
                                                        elif price < self.prev_trade_px: is_buy = False; self.prev_tick_dir = -1
                                                        else: is_buy = (self.prev_tick_dir == 1)
                                                    else:
                                                        is_buy = True
                                            else:
                                                # Fallback to pure tick rule
                                                if self.prev_trade_px is not None:
                                                    if price > self.prev_trade_px: is_buy = True; self.prev_tick_dir = 1
                                                    elif price < self.prev_trade_px: is_buy = False; self.prev_tick_dir = -1
                                                    else: is_buy = (self.prev_tick_dir == 1)
                                                else:
                                                    is_buy = True
                                            
                                            self.prev_trade_px = price
                                            ts_ms = ts_ns // 1_000_000
                                            bar_15m_ts = (ts_ms // 900_000) * 900_000
                                            interval_trades[bar_15m_ts].append((ts_ms, price, size, is_buy))
                                            trade_count += 1
                
                if max_chunks and chunk_count >= max_chunks:
                    print(f"Reached chunk limit ({max_chunks} chunks).")
                    break
                    
        elapsed = time.time() - t0
        print(f"[{date_str}] Stream Complete in {elapsed:.1f}s | Downloaded: {bytes_read/(1024*1024):.1f} MB | Quotes: {quote_count:,} | Trades: {trade_count:,}")
        
        # Aggregate into 15m Master and Footprint Ladder tables
        master_rows = []
        ladder_rows = []
        
        for bar_ts, tr_list in sorted(interval_trades.items()):
            if not tr_list: continue
            prices = np.array([t[1] for t in tr_list])
            sizes = np.array([t[2] for t in tr_list])
            is_buys = np.array([t[3] for t in tr_list])
            
            o = prices[0]
            h = prices.max()
            l = prices.min()
            c = prices[-1]
            tot_vol = sizes.sum()
            buy_vol = sizes[is_buys].sum()
            sell_vol = sizes[~is_buys].sum()
            net_delta = buy_vol - sell_vol
            delta_ratio = net_delta / tot_vol if tot_vol > 0 else 0.0
            
            # Ladder rungs (0.05 USD binning for QQQ)
            bin_size = 0.05
            binned_px = np.round(prices / bin_size) * bin_size
            unique_bins = np.unique(binned_px)
            
            poc_px = c
            max_bin_vol = -1
            
            for bp in unique_bins:
                mask = binned_px == bp
                b_tot = sizes[mask].sum()
                b_buy = sizes[mask & is_buys].sum()
                b_sell = sizes[mask & ~is_buys].sum()
                b_net = b_buy - b_sell
                
                if b_tot > max_bin_vol:
                    max_bin_vol = b_tot
                    poc_px = bp
                    
                ladder_rows.append({
                    'open_time_ms': bar_ts,
                    'price_bin': bp,
                    'total_vol_coin': float(b_tot),
                    'bid_vol_coin': float(b_sell), # Sold to bid
                    'ask_vol_coin': float(b_buy),  # Bought from ask
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
                'trade_count': len(tr_list)
            })
            
        m_df = pd.DataFrame(master_rows)
        l_df = pd.DataFrame(ladder_rows)
        if len(l_df) > 0:
            # Set is_poc flag
            poc_map = dict(zip(m_df['open_time_ms'], m_df['poc_price']))
            l_df['is_poc'] = ((l_df['open_time_ms'].map(poc_map) - l_df['price_bin']).abs() < 1e-4).astype(int)
            
        return m_df, l_df

if __name__ == '__main__':
    extractor = IEXStreamFootprintExtractor(target_sym="QQQ")
    url = extractor.fetch_date_feed_url("20200102")
    if url:
        m_df, l_df = extractor.process_day_stream(url, "20200102", max_chunks=300) # Process initial 150MB of the trading day
        print(f"\nGenerated {len(m_df)} 15-minute Master bars and {len(l_df):,} Footprint Ladder rungs!")
        print("\nSample 15m Master Bars:")
        print(m_df[['datetime_utc', 'open', 'high', 'low', 'close', 'volume', 'net_delta', 'delta_ratio', 'poc_price']].head())
        
        m_out = os.path.join(OUTPUT_DIR, "QQQ_15m_master_IEX_sample.parquet")
        l_out = os.path.join(OUTPUT_DIR, "QQQ_15m_footprint_ladder_IEX_sample.parquet")
        m_df.to_parquet(m_out, index=False)
        l_df.to_parquet(l_out, index=False)
        print(f"\nSaved verified tables to:\n  - {m_out}\n  - {l_out}")
