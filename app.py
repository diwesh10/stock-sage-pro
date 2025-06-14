import streamlit as st
import pandas as pd
from stock_data import fetch_stock_data, fetch_crypto_data
from analyzer import analyze_stock
from gpt_helper import explain_recommendation, predict_price_target
from telegram_alert import send_telegram_alert
from news_sentiment import fetch_news_and_sentiment
import plotly.graph_objects as go
from streamlit_authenticator import Authenticate  # NEW
import yaml
from yaml.loader import SafeLoader

# --- User Auth Config ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.set_page_config(page_title="Stock Sage Pro - AI Stock Recommender", layout="centered")
    authenticator.logout("Logout", "sidebar")
    st.title("📈 Stock Sage Pro - AI Stock Recommender")
    st.markdown("Enter stock tickers or crypto symbols (comma separated). Example: AAPL, BTC")

    input_tickers = st.text_input("Enter tickers/symbols:", "AAPL, MSFT, BTC")

    if st.button("Analyze"):
        tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()]
        if not tickers:
            st.warning("Please enter valid tickers.")
        else:
            for ticker in tickers:
                with st.spinner(f"Analyzing {ticker}..."):
                    try:
                        df = fetch_stock_data(ticker)
                        if df is None or df.empty:
                            df = fetch_crypto_data(ticker)

                        if df is None or df.empty:
                            st.warning(f"⚠️ Could not fetch data for {ticker}")
                            continue

                        result = analyze_stock(df)
                        explanation = explain_recommendation(ticker, result['reasons'])
                        price_target = predict_price_target(ticker, df)

                        st.subheader(f"📊 {ticker} Analysis")
                        st.markdown(f"**Recommendation:** {result['recommendation']}")
                        st.markdown(f"**Score:** {result['score']}/5")
                        st.markdown(f"**Reasoning:**")
                        for reason in result['reasons']:
                            st.markdown(f"- {reason}")

                        st.markdown("**AI Explanation:**")
                        st.success(explanation)

                        st.markdown("**🎯 AI-Based Price Target:**")
                        st.info(price_target)

                        if result['score'] >= 3:
                            message = f"📈 *Stock Sage Alert*\n\n💼 *{ticker}*\n✅ Recommendation: *{result['recommendation']}*\n📊 Score: *{result['score']}/5*\n🎯 Target: {price_target}\n💡 Summary: {', '.join(result['reasons'])}"
                            send_telegram_alert(message)

                        st.markdown("**📉 Candlestick Chart:**")
                        candle = go.Figure(data=[go.Candlestick(x=df.index,
                                                                open=df['Open'],
                                                                high=df['High'],
                                                                low=df['Low'],
                                                                close=df['Close'])])
                        candle.update_layout(height=400, xaxis_title='Date', yaxis_title='Price')
                        st.plotly_chart(candle, use_container_width=True)

                        st.markdown("**📰 News & Sentiment Analysis:**")
                        news_items = fetch_news_and_sentiment(ticker)
                        if news_items:
                            for news in news_items:
                                st.markdown(f"- [{news['title']}]({news['url']}) - **{news['sentiment']}**")
                        else:
                            st.info("No recent news found.")

                    except Exception as e:
                        st.error(f"Error analyzing {ticker}: {e}")

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
