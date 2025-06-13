import openai
import os

# IMPORTANT: Set your OpenAI API Key in an environment variable
# or replace os.getenv("OPENAI_API_KEY") with your actual key
openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_stock_pick(ticker, reasons):
    prompt = f"Explain in simple terms why {ticker} is a good stock to consider based on these reasons: {', '.join(reasons)}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']