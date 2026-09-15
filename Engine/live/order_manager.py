import MetaTrader5 as mt5
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrderManager:
    def __init__(self, connection):
        self.conn = connection
        self.open_trades = {}  # ticket -> trade_info
        
    def calculate_lot_size(self, symbol: str, risk_usd: float, sl_dist: float) -> float:
        """
        Calculates exact MT5 lot size for risk_usd and stop distance sl_dist in price.
        Clamps to broker volume_min, volume_max, and steps.
        """
        real_symbol = self.conn.resolve_symbol(symbol)
        info = mt5.symbol_info(real_symbol)
        if info is None or sl_dist <= 0:
            return 0.01  # Safe minimum fallback
            
        tick_value = info.trade_tick_value if info.trade_tick_value > 0 else 1.0
        tick_size = info.trade_tick_size if info.trade_tick_size > 0 else (info.point if info.point > 0 else 0.0001)
        
        # Loss per 1.0 lot for this stop distance
        loss_per_lot = (sl_dist / tick_size) * tick_value
        if loss_per_lot <= 0:
            return info.volume_min
            
        raw_lots = risk_usd / loss_per_lot
        step = info.volume_step if info.volume_step > 0 else 0.01
        lots = round(raw_lots / step) * step
        lots = max(info.volume_min, min(lots, info.volume_max))
        return round(float(lots), 2)

    def place_market_order(self, symbol, order_type, volume=None, sl_price=None, tp_price=None, risk_usd=50.0):
        if not self.conn.connected:
            logging.error("Not connected to MT5")
            return None
            
        real_symbol = self.conn.resolve_symbol(symbol)
        tick = self.conn.get_last_tick(real_symbol)
        if tick is None:
            return None
            
        price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
        
        # Dynamic lot sizing if volume not specified
        if volume is None or volume <= 0:
            sl_dist = abs(price - sl_price) if sl_price is not None else 0.0
            volume = self.calculate_lot_size(real_symbol, risk_usd=risk_usd, sl_dist=sl_dist)
            
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": real_symbol,
            "volume": float(volume),
            "type": order_type,
            "price": price,
            "sl": float(sl_price) if sl_price is not None else 0.0,
            "deviation": 20,
            "magic": 123456,
            "comment": "ML Forex Strategy",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        if tp_price:
            request["tp"] = float(tp_price)
            
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Order send failed, retcode={result.retcode}")
            return None
            
        logging.info(f"Order placed successfully: ticket={result.order}, fill_price={result.price}, volume={volume}")
        
        # Use actual execution fill price from MT5 result
        entry_fill_price = result.price if result.price > 0 else price
        
        # Calculate R value (distance from fill price to SL)
        r_dist = abs(entry_fill_price - sl_price) if sl_price is not None else 0.0001
        if r_dist == 0:
            r_dist = 0.0001
            
        self.open_trades[result.order] = {
            "symbol": real_symbol,
            "ticket": result.order,
            "type": order_type,
            "volume": volume,
            "entry_price": entry_fill_price,
            "sl": sl_price,
            "tp": tp_price,
            "r_dist": r_dist,
            "bars_elapsed": 0,
            "highest_r": 0.0,
            "last_bar_time": None
        }
        
        return result.order
        
    def close_position(self, ticket):
        if not self.conn.connected:
            return False
            
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            logging.error(f"Position {ticket} not found")
            return False
            
        position = position[0]
        tick = self.conn.get_last_tick(position.symbol)
        if tick is None:
            return False
            
        close_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = tick.bid if position.type == mt5.POSITION_TYPE_BUY else tick.ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Close Position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Close failed, retcode={result.retcode}")
            return False
            
        logging.info(f"Position {ticket} closed successfully")
        if ticket in self.open_trades:
            del self.open_trades[ticket]
        return True
        
    def modify_sl(self, ticket, new_sl):
        if not self.conn.connected:
            return False
            
        position = mt5.positions_get(ticket=ticket)
        if position is None or len(position) == 0:
            return False
            
        pos = position[0]
        
        # Check minimum broker stop distance (trade_stops_level)
        info = mt5.symbol_info(pos.symbol)
        if info is not None:
            min_dist = info.trade_stops_level * info.point
            tick = self.conn.get_last_tick(pos.symbol)
            if tick is not None:
                current_price = tick.bid if pos.type == mt5.POSITION_TYPE_BUY else tick.ask
                if abs(new_sl - current_price) < min_dist:
                    logging.warning(f"Proposed SL {new_sl:.5f} too close to current price {current_price:.5f} (min dist: {min_dist:.5f}). Skipping modify.")
                    return False
        
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": pos.symbol,
            "sl": float(new_sl),
            "tp": pos.tp
        }
        
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Modify SL failed for {ticket}, retcode={result.retcode}")
            return False
            
        logging.info(f"SL modified for {ticket} to {new_sl}")
        if ticket in self.open_trades:
            self.open_trades[ticket]["sl"] = new_sl
        return True

    def manage_open_trades(self, current_bar_time=None):
        """
        To be called every minute or tick to manage stops and time decay.
        current_bar_time should be the timestamp of the latest 15m bar to track 24-bar decay.
        """
        if not self.conn.connected:
            return
            
        tickets_to_check = list(self.open_trades.keys())
        
        for ticket in tickets_to_check:
            position = mt5.positions_get(ticket=ticket)
            if position is None or len(position) == 0:
                # Closed manually or hit SL/TP
                del self.open_trades[ticket]
                continue
                
            pos = position[0]
            trade_info = self.open_trades[ticket]
            
            # Update elapsed bars
            if current_bar_time and trade_info["last_bar_time"] != current_bar_time:
                trade_info["bars_elapsed"] += 1
                trade_info["last_bar_time"] = current_bar_time
                
            tick = self.conn.get_last_tick(pos.symbol)
            if tick is None:
                continue
                
            current_price = tick.bid if pos.type == mt5.POSITION_TYPE_BUY else tick.ask
            entry = trade_info["entry_price"]
            r_dist = trade_info["r_dist"]
            
            # Calculate current R
            if pos.type == mt5.POSITION_TYPE_BUY:
                current_r = (current_price - entry) / r_dist
            else:
                current_r = (entry - current_price) / r_dist
                
            trade_info["highest_r"] = max(trade_info["highest_r"], current_r)
            
            # Time Decay Exit: 24 bars elapsed and hasn't gained 0.20R
            if trade_info["bars_elapsed"] >= 24 and trade_info["highest_r"] < 0.20:
                logging.info(f"Time decay exit for {ticket}, bars={trade_info['bars_elapsed']}, high_R={trade_info['highest_r']}")
                self.close_position(ticket)
                continue
                
            # Microstructure Ratchets (Exact parity with s2_ict_ml_forex.py)
            # Lock 0.15R at 1.0R, Lock 1.0R at 1.5R, Lock 1.8R at 2.0R, Lock 2.3R at 2.5R, Lock 2.8R at 3.0R, Lock 3.3R at 3.5R
            new_sl_r = None
            if trade_info["highest_r"] >= 3.5:
                new_sl_r = 3.3
            elif trade_info["highest_r"] >= 3.0:
                new_sl_r = 2.8
            elif trade_info["highest_r"] >= 2.5:
                new_sl_r = 2.3
            elif trade_info["highest_r"] >= 2.0:
                new_sl_r = 1.8
            elif trade_info["highest_r"] >= 1.5:
                new_sl_r = 1.0
            elif trade_info["highest_r"] >= 1.0:
                new_sl_r = 0.15
                
            if new_sl_r is not None:
                # Calculate new SL price
                if pos.type == mt5.POSITION_TYPE_BUY:
                    new_sl_price = entry + (new_sl_r * r_dist)
                    # Ensure we only move SL up
                    if new_sl_price > pos.sl:
                        self.modify_sl(ticket, new_sl_price)
                else:
                    new_sl_price = entry - (new_sl_r * r_dist)
                    # Ensure we only move SL down (for short, SL is above entry)
                    if new_sl_price < pos.sl or pos.sl == 0:
                        self.modify_sl(ticket, new_sl_price)
