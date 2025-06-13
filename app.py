import streamlit as st
from recommender import analyze_stock
from gpt_explainer import explain_stock_pick

st.set_page_config(page_title="Stock Sage Pro", layout="centered")
st.title("📈 Stock Sage Pro - AI Stock Recommender")

tickers = st.text_input("Enter stock tickers (comma separated):", "AAPL, MSFT, TSLA")
tickers = [t.strip().upper() for t in tickers.split(",")]

if st.button("Analyze Stocks"):
    for ticker in tickers:
        result = analyze_stock(ticker)
        if not result:
            st.warning(f"Not enough data for {ticker}")
            continue
        st.subheader(f"{ticker}: {result['recommendation']}")
        st.write("Reasons:")
        for reason in result['reasons']:
            st.markdown(f"- {reason}")
        if st.checkbox(f"🧠 Explain {ticker}", key=ticker):
            with st.spinner("Generating explanation..."):
                explanation = explain_stock_pick(ticker, result['reasons'])
                st.success(explanation)