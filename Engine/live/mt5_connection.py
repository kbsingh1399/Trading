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
        
    def get_15m_bars(self, symbol, count=100):
        if not self.connected:
            logging.error("Not connected to MT5")
            return pd.DataFrame()
            
        real_symbol = self.resolve_symbol(symbol)
        # mt5.TIMEFRAME_M15 is 15 minutes
        rates = mt5.copy_rates_from_pos(real_symbol, mt5.TIMEFRAME_M15, 0, count)
        if rates is None or len(rates) == 0:
            logging.error(f"Failed to fetch rates for {real_symbol} (original: {symbol}), error code = {mt5.last_error()}")
            return pd.DataFrame()
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
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
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
