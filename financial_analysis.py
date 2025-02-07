from groq import Groq
import requests
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Set up Groq API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
perplexity_api_key = os.environ.get("PERPLEXITY_API_KEY")

# Simple cache for market reports and industry averages
market_report_cache = {}
industry_averages_cache = {}

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def generate_market_report_perplexity(company_name):
    if company_name in market_report_cache:
        return market_report_cache[company_name]

    url = "https://api.perplexity.ai/chat/completions"
    prompt = f"""Generate a detailed and accurate market report for {company_name}, a company in the CPG sector and Food & Beverage vertical. Include:
    1. Company Overview
    2. Market Size and Growth (use specific numbers and growth rates)
    3. Target Market (be specific about demographics and psychographics)
    4. Competitive Landscape (name at least 3 major competitors)
    5. Key Trends (mention at least 3 industry-specific trends)
    6. SWOT Analysis (provide 2-3 points for each category)
    7. Future Outlook (include market projections for the next 3-5 years)
    Use data where possible, and format the report professionally. Ensure all financial figures are in USD."""

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": f"You are a financial analyst specializing in the CPG sector and Food & Beverage vertical. Provide accurate, data-driven insights for {company_name}. Use proper Markdown format, avoiding h1, h2, and h3 headers. Separate sections with blank lines. Denote all amounts in USD with a dollar sign. Do not make assumptions, instead call out clearly where you lack information or data."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": 3000,
        "temperature": 0.01,
        "top_p": 0.9,
    }

    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()["choices"][0]["message"]["content"]
    
    market_report = re.sub(r"[\*\#\-]", "", result)
    market_report = market_report.replace("\n", "\n\n")
    market_report = re.sub(r'\[\d+\]', '', market_report)
    
    market_report_cache[company_name] = market_report
    return market_report

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def calculate_averages_using_ai(documents, company_name):
    if company_name in industry_averages_cache:
        return industry_averages_cache[company_name]

    prompt = f"""Analyze the following income statements from different companies in the {company_name}'s industry. Calculate and provide accurate industry averages for:

    1. Quarterly "Total Income": Average of "Total Income" for each quarter across all companies
    2. Quarterly "Total Income" Growth:
       a. Calculate growth percentages: ((Q2 - Q1) / Q1) * 100, ((Q3 - Q2) / Q2) * 100, ((Q4 - Q3) / Q3) * 100
       b. Take the average of these three growth percentages
    3. Gross Margin: (("Gross Profit" / "Total Income") * 100) averaged across all companies
    4. "Total Expenses" Ratio: (("Total Expenses" / "Total Income") * 100) averaged across all companies
    5. Net Profit Margin: (("Net Profit" / "Total Income") * 100) averaged across all companies
    6. "Total Cost Of Goods Sold" as % of "Total Income": (("Total Cost Of Goods Sold" / "Total Income") * 100) averaged across all companies

    Income Statements:
    {documents}

    These industry averages should be calculated using data from synthetic_data_4.csv, synthetic_data_5.csv, and synthetic_data_6.csv files only.

    Provide the averages as "Industry Averages" without mentioning specific companies. Format the report professionally, using markdown tables where appropriate. Ensure all financial figures are in USD and use a dollar sign where applicable. Express all metrics as percentages where appropriate. Be extremely precise and consistent in your calculations, showing your work for each metric. """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a financial analyst specializing in the CPG sector and Food & Beverage vertical. Provide accurate, data-driven industry averages for {company_name}'s sector. Use proper Markdown format, avoiding h1, h2, and h3 headers. Separate sections with blank lines. Denote all amounts in USD with a dollar sign. Ensure consistency and precision in all calculations, showing your work for each metric.  Do not make assumptions, instead call out clearly where you lack information or data."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="deepseek-r1-distill-llama-70b",
        temperature=0.01,
        max_tokens=3000,
    )
    
    industry_averages = chat_completion.choices[0].message.content
    industry_averages = re.sub(r'<think>.*?</think>', '', industry_averages, flags=re.DOTALL)

    industry_averages_cache[company_name] = industry_averages
    return industry_averages

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
def analyze_company_standing(company_statement, industry_averages, market_report, company_name):
    prompt = f"""Analyze {company_name}'s performance compared to industry benchmarks. Provide a detailed analysis in the following format:

    1. Key Metrics vs. Industry Benchmarks
    Create a markdown table with the following columns:
    - Metric
    - {company_name} (calculate from the company data in original_data.csv)
    - Industry Average (use the provided industry averages)
    - Verdict (use "Outperforming", "On par", or "Underperforming")
    Include these metrics:
    - Quarterly "Total Income" Growth: Average of ((Q2 - Q1) / Q1) * 100, ((Q3 - Q2) / Q2) * 100, ((Q4 - Q3) / Q3) * 100
    - Gross Margin: ("Gross Profit" / "Total Income") * 100
    - Net Profit Margin: ("Net Profit" / "Total Income") * 100
    - "Total Expenses" Ratio: ("Total Expenses" / "Total Income") * 100
    - "Total Cost Of Goods Sold" as % of "Total Income": ("Total Cost Of Goods Sold" / "Total Income") * 100

    2. Operational Highlights
    - Strengths: List 3 top performing areas with specific data points
    - Weaknesses: List 3 areas needing improvement with specific data points

    3. Strategic Recommendations
    Provide 3 detailed, actionable recommendations based on the company's performance and market conditions.

    Use the following data for your analysis:
    Company Data: {company_statement}
    Industry Averages: {industry_averages}
    Market Report: {market_report}

    Format your response using markdown, with appropriate headers (h4 or smaller) and bullet points. Separate each section with a horizontal rule (---).
    Ensure all financial figures are in USD and use a dollar sign where applicable. Express all metrics as percentages where appropriate. Be specific and data-driven in your analysis. Maintain consistency and accuracy in all calculations and comparisons. Show your work for each metric calculation."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a financial analyst specializing in the CPG sector and Food & Beverage vertical. Provide an accurate, data-driven analysis of {company_name}'s performance compared to industry benchmarks. Use proper Markdown format, avoiding h1, h2, and h3 headers. Separate sections with blank lines. Denote all amounts in USD with a dollar sign. Ensure consistency and precision in all calculations and comparisons, showing your work for each metric.  Do not make assumptions, instead call out clearly where you lack information or data."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="deepseek-r1-distill-llama-70b",
        temperature=0.01,
        max_tokens=5000,
    )
    
    analysis = chat_completion.choices[0].message.content
    analysis = re.sub(r'<think>.*?</think>', '', analysis, flags=re.DOTALL)

    return analysis

def generate_visualizations():
    df = pd.read_csv("data/original_data.csv", header=0)
    df = df.drop(columns=["Total"])

    revenue = df[df["Name"] == "Total Income"].set_index("Name").T
    revenue.columns = ["Revenue"]
    revenue.index = pd.to_datetime(revenue.index)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(revenue.index, revenue["Revenue"], marker='o', linestyle='-', label="Revenue")
    ax1.set_xlabel("Months")
    ax1.set_ylabel("Revenue ($)")
    ax1.set_title("Monthly Revenue Trend")
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend()
    ax1.grid()

    quarterly_revenue = revenue.resample('Q').sum()
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(quarterly_revenue.index.strftime('%Y-Q%q'), quarterly_revenue["Revenue"], marker='o', linestyle='-', label="Quarterly Revenue")
    ax2.set_xlabel("Quarter")
    ax2.set_ylabel("Revenue ($)")
    ax2.set_title("Quarterly Revenue Trend")
    ax2.legend()
    ax2.grid()

    gross_profit = df[df["Name"] == "Gross Profit"].set_index("Name").T
    gross_profit.columns = ["Gross Profit"]
    gross_profit.index = pd.to_datetime(gross_profit.index)

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.bar(gross_profit.index.strftime('%Y-%m'), gross_profit["Gross Profit"], color='skyblue')
    ax3.set_xlabel("Months")
    ax3.set_ylabel("Gross Profit ($)")
    ax3.set_title("Monthly Gross Profit")
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis="y")

    return [fig1, fig2, fig3]

def main():
    st.title("Company Financial Analysis")

    company_name = st.text_input("Enter company name:", "B.T.R Nation")
    st.session_state.company_name = company_name

    if st.button("Generate Analysis"):
        with st.spinner("Generating market report..."):
            market_report = generate_market_report_perplexity(company_name)

        with st.spinner("Calculating industry averages..."):
            file_paths_companies_2_to_9 = [
                'data/synthetic_data_4.csv',
                'data/synthetic_data_5.csv',
                'data/synthetic_data_6.csv',
            ]
            documents_companies_2_to_9 = [open(file, 'r').read() for file in file_paths_companies_2_to_9]
            industry_averages = calculate_averages_using_ai(documents_companies_2_to_9, company_name)
        
        with st.spinner("Analyzing company standing..."):
            with open('data/original_data.csv', 'r') as f:
                company_1_statement_content = f.read()
            analysis = analyze_company_standing(company_1_statement_content, industry_averages, market_report, company_name)
        
        st.subheader("Market Report")
        st.markdown(market_report)

        st.subheader("Industry Averages")
        st.markdown(industry_averages)

        st.subheader("Analysis of Company's Standing")
        st.markdown(analysis)

        with st.spinner("Generating visualizations..."):
            figures = generate_visualizations()
            for fig in figures:
                st.pyplot(fig)

if __name__ == "__main__":
    main()
