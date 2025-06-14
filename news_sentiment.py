import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

API_KEY = "YOUR_NEWS_API_KEY"  # Replace or load from env/secrets
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def fetch_news(ticker, max_articles=5):
    try:
        url = f"{NEWS_ENDPOINT}?q={ticker}&sortBy=publishedAt&apiKey={API_KEY}&language=en&pageSize={max_articles}"
        response = requests.get(url)
        articles = response.json().get("articles", [])
        return articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def summarize_sentiment(articles):
    analyzer = SentimentIntensityAnalyzer()
    summaries = []
    total_score = 0

    for art in articles:
        title = art['title']
        score = analyzer.polarity_scores(title)['compound']
        total_score += score
        summaries.append((title, score))

    avg_score = total_score / len(articles) if articles else 0
    sentiment = "Neutral"
    if avg_score > 0.2:
        sentiment = "📈 Bullish"
    elif avg_score < -0.2:
        sentiment = "📉 Bearish"

    return sentiment, summaries
