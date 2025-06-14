import openai
import os

# Load your OpenAI key from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_recommendation(ticker, reasons):
    try:
        prompt = (
            f"You are an AI stock advisor. The analysis of the stock {ticker} shows:\n\n"
            + "\n".join(f"- {r}" for r in reasons)
            + "\n\nExplain this in clear, easy-to-understand terms for a retail investor, "
              "and suggest whether it's a good idea to consider investing in it."
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're a financial expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Could not generate explanation: {e}"
