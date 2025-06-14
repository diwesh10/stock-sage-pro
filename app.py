import streamlit as st
import pandas as pd
from stock_data import fetch_stock_data
from analyzer import analyze_stock
from gpt_helper import explain_recommendation
from telegram_alert import send_telegram_alert  # NEW

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

                    # Send Telegram alert if score >= 3
                    if result['score'] >= 3:
                        message = f"📈 *Stock Sage Alert*\n\n💼 *{ticker}*\n✅ Recommendation: *{result['recommendation']}*\n📊 Score: *{result['score']}/5*\n💡 Summary: {', '.join(result['reasons'])}"
                        send_telegram_alert(message)

                except Exception as e:
                    st.error(f"Error analyzing {ticker}: {e}")
