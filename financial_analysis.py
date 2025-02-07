from groq import Groq
import requests
import re
import os
import pandas as pd
import matplotlib.pyplot as plt

# Set up Groq API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
perplexity_api_key = os.environ.get("PERPLEXITY_API_KEY")

def generate_market_report_perplexity(company_name):
    url = "https://api.perplexity.ai/chat/completions"
    prompt = f"Do market research for the business named {company_name} in the CPG sector, and the Food & Beverage vertical.\
    Be specific and use specific examples and references.\
    Include the following information:\
    Company Summary\
    Product Offering\
    Market Opportunity\
    Target Markets and size\
    Similarly-sized Competitors\
    Sales and Growth\
    Distribution Channels\
    Customer Retention and Conversion\
    Financial Performance\
    Competitive Advantage\
    Also make recommendations for additional Target Markets, Distribution Channels, and general growth opportunities.\
    Be specific and provide specific examples while being precise and concise.\
    Keep in mind the company's size, financials, and industry position. Make the report credible and useful for assessing the company's standing in the market.\
"
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": f"You are an intelligent financial assistant. You answer the user's question based on the company's financial data.\
                And you always return the answer in proper Markdown format that can be parsed\
                with react-markdown and remark-gfm while avoiding using the h1 header in the markdown.\
                You will not add a header that is larger than h4 in the markdown. Do not include h1, h2, or h3 headers in the markdown.\
                Each markdown section should be separated by a blank line. All amounts should be denoted with a dollar sign (USD). The company is named {company_name} in the CPG sector, and the Food & Beverage vertical."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.01,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "response_format": None
    }

    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    result = response.json()["choices"][0]["message"]["content"]
        
    # Clean the text (remove unwanted characters and format)
    market_report = re.sub(r"[\*\#\-]", "", result)  # Remove *, #, -
    market_report = market_report.replace("\n", "\n")  # Ensure double line breaks for Markdown
    market_report = re.sub(r'\[\d+\]', '', market_report)
        
    return market_report

def calculate_averages_using_ai(documents, company_name):
    prompt = "Given the following income statements from different companies(consider them as the industry,dont mention the companies explicitily, consider them as the whole rest of the industry, extract the quarterly revenue, revenue growth trend, profit, expenses(breakdown if possible), and net income, operational and non-operational costs and incomes, cogs, for each, and then calculate the average for each metric. \n\n"
    
    for i, doc in enumerate(documents):
        prompt += f"Income Statement {i+2}: {doc}\n\n"  # Start from Company 2
    
    prompt += "Provide the average values. Consider all the compies provided as the industry, and give the averages like- here is the industry average. Do not mention number of companies or each compny, give the result as a whole. Make the report professional and look like a standard report of how this industry looks like based on all the companies provided. Don't provide the think part. Act like you are talking to a client and explaining what the industry averages look like."
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"You are an intelligent financial assistant.You answer the user's question based on the company's financial data.\
            And you always return the answer in proper Markdown format that can be parsed with react-markdown and remark-gfm while avoid using the h1 header in the markdown.\
            You will not add a header that is larger than h4 in the markdown. Do not include h1, h2, or h3 headers in the markdown. \
            Each markdown section should be separated by a blank line.And all amount as USD denoted with a dollar sign.The company is named {company_name} in the CPG sector, and the Food & Beverage vertical"
        },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="deepseek-r1-distill-llama-70b",
        stream=False,
        temperature=0.01,
        max_tokens=3000,
    )
    
    industry_averages = chat_completion.choices[0].message.content
    industry_averages = re.sub(r'<think>.*?</think>', '', industry_averages, flags=re.DOTALL)
    return industry_averages

def analyze_company_standing(company_statement, industry_averages, market_report, company_name):
    prompt = f"""Analyze {company_name}'s performance compared to industry benchmarks. Provide a detailed analysis in the following format:
    1. Create a markdown table titled "Key Metrics vs. Industry Benchmarks" with the following columns:
       - Metric
       - {company_name}
       - Industry Average
       - Verdict (use "Outperforming", "On par", or "Underperforming")
       Include the following metrics:
       - Quarterly Revenue Growth
       - Gross Margin
       - Net Profit Margin
    2. Under an "Operational Highlights" section, list key strengths and weaknesses:
       - Strengths: List 2-3 top performing areas
       - Weaknesses: List 2-3 areas needing improvement
    3. Provide 3 strategic recommendations under a "Strategic Recommendations" section
    Use the following data for your analysis:
    Company Data: {company_statement}
    Industry Averages: {industry_averages}
    Market Report: {market_report}
    Format your response using markdown, with appropriate headers (h4 or smaller) and bullet points. Separate each section with a horizontal rule (---).
    Ensure all financial figures are in USD and use a dollar sign where appropriate.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"You are an intelligent financial assistant.You answer the user's question based on the company's financial data.\
            And you always return the answer in proper Markdown format that can be parsed with react-markdown and remark-gfm while avoid using the h1 header in the markdown.\
            You will not add a header that is larger than h4 in the markdown. Do not include h1, h2, or h3 headers in the markdown. \
            Each markdown section should be separated by a blank line.And all amount as USD denoted with a dollar sign.The company is named {company_name} in the CPG sector, and the Food & Beverage vertical"
        },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="deepseek-r1-distill-llama-70b",
        stream=False,
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
    
    # Convert index to datetime
    revenue.index = pd.to_datetime(revenue.index)

    # Monthly Revenue Trend
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(revenue.index, revenue["Revenue"], marker='o', linestyle='-', label="Revenue")
    ax1.axhline(y=554200, color='r', linestyle='--', label="Industry Average quarterly revenue")
    ax1.set_xlabel("Months")
    ax1.set_ylabel("Revenue")
    ax1.set_title("Monthly Revenue Trend")
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend()
    ax1.grid()

    # Quarterly Revenue Trend
    quarterly_revenue = revenue.resample('Q').sum()
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(quarterly_revenue.index.strftime('%Y-Q%q'), quarterly_revenue["Revenue"], marker='o', linestyle='-', label="Quarterly Revenue")
    ax2.axhline(y=554200*3, color='r', linestyle='--', label="Industry Avg Quarterly Revenue")
    ax2.set_xlabel("Quarter")
    ax2.set_ylabel("Revenue")
    ax2.set_title("Quarterly Revenue Trend")
    ax2.legend()
    ax2.grid()

    # Monthly Gross Profit
    gross_profit = df[df["Name"] == "Gross Profit"].set_index("Name").T
    gross_profit.columns = ["Gross Profit"]
    gross_profit.index = pd.to_datetime(gross_profit.index)

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.bar(gross_profit.index.strftime('%Y-%m'), gross_profit["Gross Profit"], color='skyblue')
    ax3.axhline(y=32500, color='r', linestyle='--', label="Industry Average Gross profit")
    ax3.set_xlabel("Months")
    ax3.set_ylabel("Gross Profit")
    ax3.set_title("Monthly Gross Profit")
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis="y")

    return [fig1, fig2, fig3]


def main():
    # This function can be used for testing or running the analysis independently
    company_name = "B.T.R Nation"
    market_report = generate_market_report_perplexity(company_name)

    file_paths_companies_2_to_9 = [
        'data/synthetic_data_4.csv',
        'data/synthetic_data_5.csv',
        'data/synthetic_data_6.csv',
    ]
    documents_companies_2_to_9 = [open(file, 'r').read() for file in file_paths_companies_2_to_9]
    
    industry_averages = calculate_averages_using_ai(documents_companies_2_to_9, company_name)
    
    with open('data/original_data.csv', 'r') as f:
        company_1_statement_content = f.read()
    
    analysis = analyze_company_standing(company_1_statement_content, industry_averages, market_report, company_name)
    
    print("Market Report:")
    print(market_report)
    print("\nIndustry Averages:")
    print(industry_averages)
    print("\nAnalysis of Company's Standing:")
    print(analysis)

    figures = generate_visualizations()
    for fig in figures:
        plt.show()

if __name__ == "__main__":
    main()

