import yfinance as yf
import pandas as pd
import ta

def fetch_stock_data(ticker):
    try:
        data = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if data.empty:
            return None

        # Add technical indicators
        data['RSI'] = ta.momentum.RSIIndicator(close=data['Close']).rsi()
        macd = ta.trend.MACD(close=data['Close'])
        data['MACD'] = macd.macd()
        data['MACD_Signal'] = macd.macd_signal()

        return data.dropna()
    except Exception as e:
        print(f"Data fetch error for {ticker}: {e}")
        return None
