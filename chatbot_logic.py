import requests
import os
from analysis import load_main_company_data, load_competitor_data, calculate_industry_benchmark, compare_with_benchmark, generate_insights

# Set Groq API Key (Replace with your actual key)
GROQ_API_KEY = "your-groq-api-key"

# Load and Process Financial Data
main_company_df = load_main_company_data()
competitors_df = load_competitor_data()
industry_benchmark = calculate_industry_benchmark(competitors_df)
financial_analysis = compare_with_benchmark(main_company_df, industry_benchmark)
insights = generate_insights(main_company_df, financial_analysis)

# Function to Call Groq API
def chatbot_response(user_query):
    api_url = "https://api.groq.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": "You are a financial analysis chatbot."},
        {"role": "user", "content": f"{user_query}\n\nHere are financial insights:\n" + "\n".join(insights[:10])}
    ]

    payload = {
        "model": "groq-model-name",  # Replace with the correct Groq model name
        "messages": messages,
        "max_tokens": 500
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"
