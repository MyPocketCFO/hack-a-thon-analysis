import groq
import json

def generate_chatbot_response(report):
    # Convert report to a string format
    report_str = json.dumps(report, indent=4)
    
    # Example prompt
    prompt = f"""
    You are a highly skilled financial analyst with expertise in corporate finance, financial statement analysis, and business strategy. Your role is to analyze a company's financial statements—income statement, balance sheet, and cash flow statement—identifying key performance indicators, trends, and potential risks. Provide deep, specific insights on profitability, liquidity, efficiency, and solvency. Highlight strengths and pinpoint precise areas for improvement, offering actionable strategies to enhance financial health, optimize expenses, increase revenue, and improve overall business performance. Use industry benchmarks and financial ratios where relevant to support your analysis.

    Here is the financial analysis report:
    {report_str}
    """
    
    # Initialize Groq client
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    client = groq.Client(api_key="your_groq_api_key")
=======
    client = groq.Client(api_key="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")
>>>>>>> Stashed changes
=======
    client = groq.Client(api_key="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")
>>>>>>> Stashed changes
=======
    client = groq.Client(api_key="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")
>>>>>>> Stashed changes
=======
    client = groq.Client(api_key="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")
>>>>>>> Stashed changes
=======
    client = groq.Client(api_key="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")
>>>>>>> Stashed changes
    
    # Generate response
    response = client.generate(prompt)
    
    return response

if __name__ == "__main__":
    from analysis import generate_analysis_report
    from data_processing import main
    main_company, competitors = main()
    report = generate_analysis_report(main_company, competitors)
    chatbot_response = generate_chatbot_response(report)
    print(chatbot_response)