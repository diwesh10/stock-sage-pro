import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(ticker, recommendation, score, reasons):
    try:
        if not BOT_TOKEN or not CHAT_ID:
            return "Missing Telegram credentials."

        reason_text = "\\n".join(f"- {r}" for r in reasons)
        message = (
            f"📢 Stock Sage Pro Alert\n\n"
            f"📈 {ticker} Recommendation: {recommendation}\n"
            f"⭐ Score: {score}/5\n"
            f"🔍 Reasons:\n{reason_text}"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        return "✅ Alert sent!" if response.status_code == 200 else f"❌ Failed: {response.text}"

    except Exception as e:
        return f"Error sending alert: {e}"
