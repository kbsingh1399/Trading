import MetaTrader5 as mt5
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MT5Connection:
    def __init__(self, login=None, password=None, server=None):
        self.login = login
        self.password = password
        self.server = server
        self.connected = False
        
    def connect(self):
        if not mt5.initialize():
            logging.error(f"initialize() failed, error code = {mt5.last_error()}")
            return False
            
        if self.login and self.password and self.server:
            authorized = mt5.login(self.login, password=self.password, server=self.server)
            if not authorized:
                logging.error(f"Failed to connect at account #{self.login}, error code: {mt5.last_error()}")
                return False
            logging.info(f"Connected to MT5 account #{self.login} on {self.server}")
        else:
            logging.info("Connected to currently active MT5 terminal (no specific login provided)")
            
        self.connected = True
        return True
        
    def disconnect(self):
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logging.info("Disconnected from MT5")
            
    def resolve_symbol(self, symbol: str) -> str:
        """
        Resolves generic symbol name (e.g. 'EURUSD', 'GER30') to the exact MT5 broker symbol.
        Handles:
        1. Suffix resolution (.pi for forex, .p for CFDs)
        2. Renamed/transitioned instruments (GER30 -> GER40.p)
        """
        # Alias map for sunsetted/renamed instruments
        ALIASES = {
            "GER30": "GER40.p",
            "GER30.p": "GER40.p",
        }
        if symbol in ALIASES:
            target = ALIASES[symbol]
            mt5.symbol_select(target, True)
            return target

        # If symbol exists directly as-is
        info = mt5.symbol_info(symbol)
        if info is not None:
            if not info.visible:
                mt5.symbol_select(symbol, True)
            return symbol

        # Try common broker suffixes
        for suffix in [".pi", ".p", ".r", ".m", ""]:
            candidate = symbol + suffix
            info = mt5.symbol_info(candidate)
            if info is not None:
                if not info.visible:
                    mt5.symbol_select(candidate, True)
                return candidate

        logging.warning(f"Could not resolve MT5 symbol for '{symbol}'")
        return symbol

    def get_last_tick(self, symbol):
        if not self.connected:
            logging.error("Not connected to MT5")
            return None
            
        real_symbol = self.resolve_symbol(symbol)
        tick = mt5.symbol_info_tick(real_symbol)
        if tick is None:
            logging.error(f"Failed to fetch tick for {real_symbol} (original: {symbol}), error code = {mt5.last_error()}")
            return None
        return tick

    def get_current_bid(self, symbol: str) -> float:
        """Returns current market bid price as float, or 0.0 if tick unavailable."""
        tick = self.get_last_tick(symbol)
        return float(tick.bid) if tick else 0.0

    def get_current_ask(self, symbol: str) -> float:
        """Returns current market ask price as float, or 0.0 if tick unavailable."""
        tick = self.get_last_tick(symbol)
        return float(tick.ask) if tick else 0.0
        
    def get_broker_utc_offset(self) -> int:
        """
        Calculates broker server time offset from UTC in seconds.
        Blueberry Markets server time is UTC+3 in summer (+10800s).
        """
        import time
        if hasattr(self, '_cached_utc_offset') and self._cached_utc_offset is not None:
            if time.time() - getattr(self, '_last_offset_fetch', 0) < 3600:
                return self._cached_utc_offset

        if not self.connected:
            return 3 * 3600
        tick = mt5.symbol_info_tick("EURUSD.pi") or mt5.symbol_info_tick("EURUSD") or mt5.symbol_info_tick("EURUSD.p")
        if tick is None:
            return 3 * 3600
        from datetime import datetime, timezone
        now_utc_ts = datetime.now(timezone.utc).timestamp()
        offset_seconds = int(round((tick.time - now_utc_ts) / 3600.0) * 3600)
        
        self._cached_utc_offset = offset_seconds
        self._last_offset_fetch = time.time()
        return offset_seconds

    def get_15m_bars(self, symbol, count=100):
        if not self.connected:
            logging.error("Not connected to MT5")
            return pd.DataFrame()
            
        real_symbol = self.resolve_symbol(symbol)
        rates = mt5.copy_rates_from_pos(real_symbol, mt5.TIMEFRAME_M15, 0, count)
        if rates is None or len(rates) == 0:
            logging.error(f"Failed to fetch rates for {real_symbol} (original: {symbol}), error code = {mt5.last_error()}")
            return pd.DataFrame()
        
        df = pd.DataFrame(rates)
        offset = self.get_broker_utc_offset()
        # Convert broker server time to true UTC
        df['time_broker'] = df['time']
        df['time'] = df['time'] - offset
        df['datetime'] = pd.to_datetime(df['time'], unit='s', utc=True)
        return df

    def get_4h_bars(self, symbol, count=250):
        if not self.connected:
            logging.error("Not connected to MT5")
            return pd.DataFrame()
            
        real_symbol = self.resolve_symbol(symbol)
        rates = mt5.copy_rates_from_pos(real_symbol, mt5.TIMEFRAME_H4, 0, count)
        if rates is None or len(rates) == 0:
            logging.error(f"Failed to fetch 4H rates for {real_symbol} (original: {symbol}), error code = {mt5.last_error()}")
            return pd.DataFrame()
        
        df = pd.DataFrame(rates)
        offset = self.get_broker_utc_offset()
        # Convert broker server time to true UTC
        df['time_broker'] = df['time']
        df['time'] = df['time'] - offset
        df['datetime'] = pd.to_datetime(df['time'], unit='s', utc=True)
        return df
