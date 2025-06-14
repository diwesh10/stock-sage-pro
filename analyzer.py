def analyze_stock(df):
    latest = df.iloc[-1]
    score = 0
    reasons = []

    # RSI logic
    if latest['RSI'] < 30:
        score += 2
        reasons.append("RSI < 30 → Oversold, potential bounce.")
    elif latest['RSI'] > 70:
        reasons.append("RSI > 70 → Overbought, risky entry.")

    # MACD logic
    if latest['MACD'] > latest['MACD_Signal']:
        score += 2
        reasons.append("MACD crossover → Bullish signal.")
    else:
        reasons.append("MACD below signal → Weak trend.")

    # Price trend logic
    if latest['Close'] > df['Close'].rolling(20).mean().iloc[-1]:
        score += 1
        reasons.append("Price above 20-day MA → Uptrend.")
    else:
        reasons.append("Price below 20-day MA → Caution advised.")

    # Final recommendation
    if score >= 4:
        recommendation = "✅ Strong Buy"
    elif score >= 2:
        recommendation = "⚠️ Watchlist / Hold"
    else:
        recommendation = "❌ Avoid"

    return {
        "score": score,
        "reasons": reasons,
        "recommendation": recommendation
    }
