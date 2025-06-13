import yfinance as yf
import pandas as pd

def compute_indicators(df):
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df

def analyze_stock(ticker):
    df = yf.download(ticker, period='6mo', interval='1d')
    if df.empty or len(df) < 50:
        return None
    df = compute_indicators(df)
    latest = df.iloc[-1]
    reasons = []
    score = 0

    rsi_value = latest['RSI'].iloc[-1] if 'RSI' in latest and not latest['RSI'].isna().all() else None
    if rsi_value is not None and rsi_value < 30:
    reasons.append("RSI is below 30 (oversold)")
    score += 1
    def safe_get_indicator(latest, col):
        return latest[col].iloc[-1] if col in latest and not latest[col].isna().all() else None
    rsi = safe_get_indicator(latest, 'RSI')
    if rsi is not None and rsi < 30:
        reasons.append("RSI is below 30 (oversold)")
        score += 1
    return {
        'ticker': ticker,
        'score': score,
        'recommendation': "Buy" if score > 0 else "Hold/Sell",
        'reasons': reasons
    }
