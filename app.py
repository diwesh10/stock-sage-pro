import streamlit as st
import pandas as pd
from stock_data import fetch_stock_data
from analyzer import analyze_stock
from gpt_helper import explain_recommendation
from telegram_alert import send_telegram_alert
from news_sentiment import fetch_news_and_sentiment  # NEW
import plotly.graph_objects as go  # For candlestick charts

st.set_page_config(page_title="Stock Sage Pro - AI Stock Recommender", layout="centered")
st.title("📈 Stock Sage Pro - AI Stock Recommender")
st.markdown("Enter stock tickers below and get AI-powered technical insights with explanations.")

input_tickers = st.text_input("Enter stock tickers (comma separated):", "AAPL, MSFT, TSLA")

if st.button("Analyze Stocks"):
    tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()]
    if not tickers:
        st.warning("Please enter valid stock tickers.")
    else:
        for ticker in tickers:
            with st.spinner(f"Analyzing {ticker}..."):
                try:
                    df = fetch_stock_data(ticker)
                    if df is None or df.empty:
                        st.warning(f"⚠️ Could not fetch data for {ticker}")
                        continue

                    result = analyze_stock(df)
                    explanation = explain_recommendation(ticker, result['reasons'])

                    st.subheader(f"📊 {ticker} Analysis")
                    st.markdown(f"**Recommendation:** {result['recommendation']}")
                    st.markdown(f"**Score:** {result['score']}/5")
                    st.markdown(f"**Reasoning:**")
                    for reason in result['reasons']:
                        st.markdown(f"- {reason}")

                    st.markdown("**AI Explanation:**")
                    st.success(explanation)

                    # Telegram Alert
                    if result['score'] >= 3:
                        message = f"📈 *Stock Sage Alert*\n\n💼 *{ticker}*\n✅ Recommendation: *{result['recommendation']}*\n📊 Score: *{result['score']}/5*\n💡 Summary: {', '.join(result['reasons'])}"
                        send_telegram_alert(message)

                    # Candlestick Chart
                    st.markdown("**📉 Candlestick Chart:**")
                    candle = go.Figure(data=[go.Candlestick(x=df.index,
                                                            open=df['Open'],
                                                            high=df['High'],
                                                            low=df['Low'],
                                                            close=df['Close'])])
                    candle.update_layout(height=400, xaxis_title='Date', yaxis_title='Price (USD)')
                    st.plotly_chart(candle, use_container_width=True)

                    # News & Sentiment
                    st.markdown("**📰 News & Sentiment Analysis:**")
                    news_items = fetch_news_and_sentiment(ticker)
                    if news_items:
                        for news in news_items:
                            st.markdown(f"- [{news['title']}]({news['url']}) - **{news['sentiment']}**")
                    else:
                        st.info("No recent news found.")

                except Exception as e:
                    st.error(f"Error analyzing {ticker}: {e}")
