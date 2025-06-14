import streamlit as st
import pandas as pd
from stock_data import fetch_stock_data
from analyzer import analyze_stock
from gpt_helper import explain_recommendation
import plotly.graph_objs as go

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

                    # Candlestick chart
                    st.markdown("### 📉 Price Chart")
                    fig = go.Figure()
                    fig.add_trace(go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name='Price'))

                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df['Close'].rolling(20).mean(),
                        line=dict(color='orange', width=2),
                        name='20-day MA'))

                    fig.update_layout(xaxis_rangeslider_visible=False, height=500, template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)

                except Exception as e:
                    st.error(f"Error analyzing {ticker}: {e}")
