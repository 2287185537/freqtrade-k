"""
Download OHLCV data using python-binance library
This provides an alternative to Binance Vision archive and direct REST API access
"""

import logging
from datetime import datetime, timedelta
from typing import Any

import pandas as pd
from pandas import DataFrame

from freqtrade.enums import CandleType
from freqtrade.util.datetime_helpers import dt_from_ts, dt_ts


logger = logging.getLogger(__name__)


def download_ohlcv_with_python_binance(
    pair: str,
    timeframe: str,
    since_ms: int,
    until_ms: int | None,
    candle_type: CandleType,
    markets: dict[str, Any],
) -> DataFrame:
    """
    Download OHLCV data using python-binance library.
    
    This method uses the python-binance library which provides a simpler interface
    to Binance API. It doesn't require API keys for public market data.
    
    :param pair: Symbol name in CCXT convention (e.g., "BTC/USDT:USDT")
    :param timeframe: Timeframe (e.g., "1h", "15m")
    :param since_ms: Start timestamp in milliseconds
    :param until_ms: End timestamp in milliseconds (None for current time)
    :param candle_type: SPOT or FUTURES
    :param markets: CCXT markets dict
    :return: DataFrame with OHLCV data
    """
    try:
        # Import python-binance library
        try:
            from binance.client import Client
        except ImportError:
            logger.error(
                "python-binance library is not installed. "
                "Install it with: pip install python-binance"
            )
            return DataFrame()
        
        # Get Binance symbol name
        symbol = markets[pair]["id"]
        
        # Convert timeframe to Binance format
        binance_interval = _convert_timeframe_to_binance(timeframe)
        if not binance_interval:
            logger.error(f"Unsupported timeframe: {timeframe}")
            return DataFrame()
        
        # Convert timestamps to datetime strings
        start_time = dt_from_ts(since_ms)
        end_time = dt_from_ts(until_ms) if until_ms else datetime.now()
        
        # Format for Binance API
        start_str = start_time.strftime("%d %b %Y %H:%M:%S")
        end_str = end_time.strftime("%d %b %Y %H:%M:%S")
        
        logger.info(
            f"Downloading {pair} ({symbol}) data using python-binance library: "
            f"{start_str} to {end_str}, interval: {binance_interval}"
        )
        
        # Initialize Binance client (no API key needed for public data)
        client = Client()
        
        # Choose the appropriate API based on candle type
        if candle_type == CandleType.SPOT:
            klines = client.get_historical_klines(
                symbol, binance_interval, start_str, end_str
            )
        elif candle_type == CandleType.FUTURES:
            klines = client.futures_historical_klines(
                symbol, binance_interval, start_str, end_str
            )
        else:
            logger.error(f"Unsupported candle type: {candle_type}")
            return DataFrame()
        
        if not klines:
            logger.warning(f"No data received for {pair}")
            return DataFrame()
        
        # Convert to DataFrame
        # Binance klines format: [Open time, Open, High, Low, Close, Volume, 
        #                         Close time, Quote asset volume, Number of trades,
        #                         Taker buy base asset volume, Taker buy quote asset volume, Ignore]
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
        
        # Convert timestamp to datetime
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Convert numeric columns
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Select and reorder columns to match Freqtrade format
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        
        # Remove any rows with NaN values
        df = df.dropna()
        
        logger.info(f"Successfully downloaded {len(df)} candles for {pair}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error downloading data with python-binance: {e}", exc_info=True)
        return DataFrame()


def _convert_timeframe_to_binance(timeframe: str) -> str | None:
    """
    Convert Freqtrade timeframe to Binance interval format.
    
    :param timeframe: Freqtrade timeframe (e.g., "1h", "15m")
    :return: Binance interval string or None if unsupported
    """
    # Binance uses the same format for most common timeframes
    # Valid intervals: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    valid_intervals = {
        '1m', '3m', '5m', '15m', '30m',
        '1h', '2h', '4h', '6h', '8h', '12h',
        '1d', '3d', '1w', '1M'
    }
    
    if timeframe in valid_intervals:
        return timeframe
    
    # Handle some alternative formats
    timeframe_map = {
        '1min': '1m',
        '5min': '5m', 
        '15min': '15m',
        '30min': '30m',
        '1hour': '1h',
        '4hour': '4h',
        '1day': '1d',
        '1week': '1w',
        '1month': '1M',
    }
    
    return timeframe_map.get(timeframe)
