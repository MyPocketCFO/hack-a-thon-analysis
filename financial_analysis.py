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
                "content": f"You are a financial analyst specializing in the CPG sector and Food & Beverage vertical. Provide accurate, data-driven insights for {company_name}. Use proper Markdown format, avoiding h1, h2, and h3 headers. Separate sections with blank lines. Denote all amounts in USD with a dollar sign."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": 2000,
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

    These industry averages should be calculated using data from synthetic_data_1.csv, synthetic_data_5.csv, and synthetic_data_6.csv files only.

    Provide the averages as "Industry Averages" without mentioning specific companies. Format the report professionally, using markdown tables where appropriate. Ensure all financial figures are in USD and use a dollar sign where applicable. Express all metrics as percentages where appropriate. Be extremely precise and consistent in your calculations, showing your work for each metric. DON'T MAKE STUFF UP. USE THE VALUES ONLY PROVIDED. MAKE SURE THE INDUSTRY AVERAGES AND THE COMPANY AVERAGES ARE DIFFERENT PLEASE!"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a financial analyst specializing in the CPG sector and Food & Beverage vertical. Provide accurate, data-driven industry averages for {company_name}'s sector. Use proper Markdown format, avoiding h1, h2, and h3 headers. Separate sections with blank lines. Denote all amounts in USD with a dollar sign. Ensure consistency and precision in all calculations, showing your work for each metric. DON'T MAKE STUFF UP. USE THE VALUES ONLY PROVIDED. MAKE SURE THE INDUSTRY AVERAGES AND THE COMPANY AVERAGES ARE DIFFERENT PLEASE!"
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
    Ensure all financial figures are in USD and use a dollar sign where applicable. Express all metrics as percentages where appropriate. Be specific and data-driven in your analysis. Maintain consistency and accuracy in all calculations and comparisons. Show your work for each metric calculation. DON'T MAKE STUFF UP. USE THE VALUES ONLY PROVIDED. MAKE SURE THE INDUSTRY AVERAGES AND THE COMPANY AVERAGES ARE DIFFERENT PLEASE!"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are a financial analyst specializing in the CPG sector and Food & Beverage vertical. Provide an accurate, data-driven analysis of {company_name}'s performance compared to industry benchmarks. Use proper Markdown format, avoiding h1, h2, and h3 headers. Separate sections with blank lines. Denote all amounts in USD with a dollar sign. Ensure consistency and precision in all calculations and comparisons, showing your work for each metric. DON'T MAKE STUFF UP. USE THE VALUES ONLY PROVIDED. MAKE SURE THE INDUSTRY AVERAGES AND THE COMPANY AVERAGES ARE DIFFERENT PLEASE!"
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
    # Load main revenue data
    df = pd.read_csv("data/original_data.csv")
    # Extract revenue for 'Total Income'
    revenue = df[df["Name"] == "Total Income"].set_index("Name")
    # Define monthly columns
    monthly_columns = [
        "Jan 2024", "Feb 2024", "Mar 2024",
        "Apr 2024", "May 2024", "Jun 2024",
        "Jul 2024", "Aug 2024", "Sep 2024",
        "Oct 2024", "Nov 2024", "Dec 2024"
    ]
    revenue = revenue[monthly_columns]
    # Define quarters
    quarters = {
        "Q1 2024": ["Jan 2024", "Feb 2024", "Mar 2024"],
        "Q2 2024": ["Apr 2024", "May 2024", "Jun 2024"],
        "Q3 2024": ["Jul 2024", "Aug 2024", "Sep 2024"],
        "Q4 2024": ["Oct 2024", "Nov 2024", "Dec 2024"]
    }
    # Calculate quarterly revenue
    quarterly_revenue = {q: revenue[months].sum(axis=1).values[0] for q, months in quarters.items()}
    # Convert to DataFrame
    quarterly_df = pd.DataFrame(list(quarterly_revenue.items()), columns=["Quarter", "Revenue"])
    # Load industry benchmark data from three CSV files
    industry_files = ["data/synthetic_data_1.csv", "data/synthetic_data_5.csv", "data/synthetic_data_6.csv"]
    # Initialize empty DataFrame for industry averages
    industry_data = []
    for file in industry_files:
        industry_df = pd.read_csv(file)
        industry_revenue = industry_df[industry_df["Name"] == "Total Income"].set_index("Name")
        industry_revenue = industry_revenue[monthly_columns]
        # Calculate industry quarterly revenue
        industry_quarterly = {q: industry_revenue[months].sum(axis=1).values[0] for q, months in quarters.items()}
        industry_data.append(industry_quarterly)
    # Compute the industry benchmark as the average across the three files
    industry_avg = {q: sum(d[q] for d in industry_data) / len(industry_data) for q in quarters.keys()}
    # Convert industry benchmark to DataFrame
    industry_df = pd.DataFrame(list(industry_avg.items()), columns=["Quarter", "Industry Avg"])
    # Merge both DataFrames
    final_df = quarterly_df.merge(industry_df, on="Quarter")
    # Plot Quarterly Revenue
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(final_df["Quarter"], final_df["Revenue"], marker='o', linestyle='-', label="Company Revenue", color='b')
    ax.plot(final_df["Quarter"], final_df["Industry Avg"], marker='s', linestyle='--', label="Industry Avg", color='r')
    # Formatting
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Revenue")
    ax.set_title("Quarterly Revenue vs. Industry Benchmark")
    ax.legend()
    ax.grid()
    return [fig]

def main():
    st.title("Company Financial Analysis")

    company_name = st.text_input("Enter company name:", "B.T.R Nation")
    st.session_state.company_name = company_name

    if st.button("Generate Analysis"):
        with st.spinner("Generating market report..."):
            market_report = generate_market_report_perplexity(company_name)

        with st.spinner("Calculating industry averages..."):
            file_paths_companies_2_to_9 = [
                'data/synthetic_data_1.csv',
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
