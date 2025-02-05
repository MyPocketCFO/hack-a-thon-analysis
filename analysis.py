import pandas as pd
import numpy as np
import os

# Load Main Company Financials
def load_main_company_data():
    main_company_df = pd.read_csv("data/main_company.csv")
    return main_company_df

# Load Competitor Financials (5 CSV Files)
def load_competitor_data():
    competitor_files = [
        "data/competitor1.csv", "data/competitor2.csv", 
        "data/competitor3.csv", "data/competitor4.csv", "data/competitor5.csv"
    ]
    competitor_dfs = [pd.read_csv(file) for file in competitor_files]
    return pd.concat(competitor_dfs, ignore_index=True)

# Calculate Industry Benchmarks
def calculate_industry_benchmark(competitors_df):
    return competitors_df.mean(numeric_only=True)

# Compare Main Company vs Industry Benchmark
def compare_with_benchmark(main_company_df, industry_benchmark):
    analysis_report = {}
    
    for column in main_company_df.columns[1:]:  # Exclude Year
        main_values = main_company_df[column].astype(float)
        benchmark_value = industry_benchmark[column]

        comparison = {
            "Main Company": main_values.tolist(),
            "Industry Average": benchmark_value,
            "Difference": [val - benchmark_value for val in main_values],
            "Status": ["Above Average" if val > benchmark_value else "Below Average" for val in main_values]
        }

        analysis_report[column] = comparison
    
    return analysis_report

# Generate Insights
def generate_insights(main_company_df, financial_analysis):
    insights = []
    
    for metric, data in financial_analysis.items():
        for i, year in enumerate(main_company_df["Year"]):
            diff = data["Difference"][i]
            status = data["Status"][i]

            if status == "Below Average":
                insights.append(
                    f"In {year}, the {metric} is below industry average by {abs(diff):.2f}. "
                    f"Consider strategies to improve this metric."
                )
            else:
                insights.append(
                    f"In {year}, the {metric} is above industry average by {diff:.2f}. "
                    f"Maintain the strong performance in this area."
                )
    
    return insights
