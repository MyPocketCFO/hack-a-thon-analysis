import pandas as pd
import numpy as np

# Configure pandas to display the full table without truncation
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Load the original CSV file
original_data = pd.read_csv('original_data.csv', index_col=0)

# Function to generate synthetic data by multiplying the entire dataset by a random value
def generate_synthetic_data(data, lower_bound, upper_bound):
    random_factor = np.random.uniform(lower_bound, upper_bound)  # Random factor within the specified range
    synthetic_data = data.apply(lambda x: np.round(x * random_factor, 2) if np.issubdtype(x.dtype, np.number) else x)
    return synthetic_data

# Function to calculate metrics
def calculate_metrics(data):
    metrics = {}
    
    # Gross Profit
    metrics['Gross Profit'] = np.round(data.loc['Total Income'] - data.loc['Total Cost Of Goods Sold'], 2)
    
    # Operating Income
    metrics['Operating Income'] = np.round(metrics['Gross Profit'] - data.loc['Total Expenses'], 2)
    
    # Net Income
    metrics['Net Income'] = np.round(metrics['Operating Income'] + data.loc['Total Other Income'] - data.loc['Total Other Expenses'], 2)
    
    # Liquidity Metrics (if data is available)
    if 'Cash' in data.index and 'Cash Burn' in data.index:
        metrics['Cash Runway'] = np.where(metrics['Net Income'] > 0, 'Cash Flow Positive', 
                                         np.round((data.loc['Cash'] / data.loc['Cash Burn']) * -1, 2))
    else:
        metrics['Cash Runway'] = 'N/A'
    
    if 'AR' in data.index and 'Current Liabilities' in data.index:
        metrics['Quick Ratio'] = np.round((data.loc['AR'] + data.loc['Cash']) / data.loc['Current Liabilities'], 2)
    else:
        metrics['Quick Ratio'] = 'N/A'
    
    if 'Current Assets' in data.index and 'Current Liabilities' in data.index:
        metrics['Current Ratio'] = np.round(data.loc['Current Assets'] / data.loc['Current Liabilities'], 2)
    else:
        metrics['Current Ratio'] = 'N/A'
    
    # Cash Efficiency Metrics (if data is available)
    if 'T3M Average AR' in data.index and 'YTD Total Net Sales' in data.index and '# of Days in YTD Period' in data.index:
        metrics['DSO'] = np.round(((data.loc['T3M Average AR'] / data.loc['YTD Total Net Sales']) / data.loc['# of Days in YTD Period']) * 365, 2)
    else:
        metrics['DSO'] = 'N/A'
    
    if 'T3M Average Period Inventory' in data.index and 'YTD Total Cost of Sales' in data.index and '# of Days in YTD Period' in data.index:
        metrics['DIO'] = np.round(((data.loc['T3M Average Period Inventory'] / data.loc['YTD Total Cost of Sales']) / data.loc['# of Days in YTD Period']) * 365, 2)
    else:
        metrics['DIO'] = 'N/A'
    
    if 'T3M Average AP' in data.index and 'YTD Total Cost of Sales' in data.index and '# of Days in YTD Period' in data.index:
        metrics['DPO'] = np.round(((data.loc['T3M Average AP'] / data.loc['YTD Total Cost of Sales']) / data.loc['# of Days in YTD Period']) * 365, 2)
    else:
        metrics['DPO'] = 'N/A'
    
    if metrics['DSO'] != 'N/A' and metrics['DIO'] != 'N/A' and metrics['DPO'] != 'N/A':
        metrics['CCC'] = np.round(metrics['DSO'] + metrics['DIO'] - metrics['DPO'], 2)
    else:
        metrics['CCC'] = 'N/A'
    
    # Aging Data Metrics (if data is available)
    if 'Total AR Aged > 90 Days' in data.index and 'Total AR' in data.index:
        metrics['AR Aging'] = np.round(data.loc['Total AR Aged > 90 Days'] / data.loc['Total AR'], 2)
    else:
        metrics['AR Aging'] = 'N/A'
    
    if 'Total AP Aged > 120 Days' in data.index and 'Total AP' in data.index:
        metrics['AP Aging'] = np.round(data.loc['Total AP Aged > 120 Days'] / data.loc['Total AP'], 2)
    else:
        metrics['AP Aging'] = 'N/A'
    
    if 'Total Inventory Aged > 180 Days' in data.index and 'Total Inventory' in data.index:
        metrics['Inv Aging'] = np.round(data.loc['Total Inventory Aged > 180 Days'] / data.loc['Total Inventory'], 2)
    else:
        metrics['Inv Aging'] = 'N/A'
    
    # Solvency & Leverage Metrics (if data is available)
    if 'Total Liabilities' in data.index and 'Total Assets' in data.index:
        metrics['Debt Ratio'] = np.round(data.loc['Total Liabilities'] / data.loc['Total Assets'], 2)
    else:
        metrics['Debt Ratio'] = 'N/A'
    
    if 'Debt' in data.index and 'Monthly Net Revenue' in data.index:
        metrics['Debt / Monthly Revenue'] = np.round(data.loc['Debt'] / data.loc['Monthly Net Revenue'], 2)
    else:
        metrics['Debt / Monthly Revenue'] = 'N/A'
    
    if 'Intangible Assets' in data.index and 'Total Assets' in data.index:
        metrics['Intangible Assets as % of Total Assets'] = np.round(data.loc['Intangible Assets'] / data.loc['Total Assets'], 2)
    else:
        metrics['Intangible Assets as % of Total Assets'] = 'N/A'
    
    if 'Equity' in data.index and 'Intangible Assets' in data.index:
        metrics['TNW'] = np.round(data.loc['Equity'] - data.loc['Intangible Assets'], 2)
    else:
        metrics['TNW'] = 'N/A'
    
    # Growth & Stability of Revenue Metrics (if data is available)
    if 'Net Sales Current Period' in data.index and 'Net Sales Prior Year Period' in data.index:
        metrics['Revenue Growth'] = np.round((data.loc['Net Sales Current Period'] - data.loc['Net Sales Prior Year Period']) / data.loc['Net Sales Current Period'], 2)
    else:
        metrics['Revenue Growth'] = 'N/A'
    
    if 'Monthly Net Revenue' in data.index:
        metrics['Revenue Variability'] = np.round(data.loc['Monthly Net Revenue'].std() / data.loc['Monthly Net Revenue'].mean(), 2)
    else:
        metrics['Revenue Variability'] = 'N/A'
    
    if 'Gross Sales' in data.index and 'Net Sales' in data.index:
        metrics['Revenue Discounting + Returns'] = np.round((data.loc['Gross Sales'] - data.loc['Net Sales']) / data.loc['Gross Sales'], 2)
    else:
        metrics['Revenue Discounting + Returns'] = 'N/A'
    
    # Revenue Diversification Metrics (if data is available)
    if 'Gross Revenue eComm' in data.index and 'Total Gross Revenue' in data.index:
        metrics['Channel Distribution - eComm'] = np.round(data.loc['Gross Revenue eComm'] / data.loc['Total Gross Revenue'], 2)
    else:
        metrics['Channel Distribution - eComm'] = 'N/A'
    
    if 'Gross Revenue Wholesale' in data.index and 'Total Gross Revenue' in data.index:
        metrics['Channel Distribution - Wholesale'] = np.round(data.loc['Gross Revenue Wholesale'] / data.loc['Total Gross Revenue'], 2)
    else:
        metrics['Channel Distribution - Wholesale'] = 'N/A'
    
    if 'Revenue Largest Customer' in data.index and 'Total Revenue All Customers' in data.index:
        metrics['Revenue Concentration'] = np.round(data.loc['Revenue Largest Customer'] / data.loc['Total Revenue All Customers'], 2)
    else:
        metrics['Revenue Concentration'] = 'N/A'
    
    # Unit Economics Metrics (if data is available)
    if 'Gross Profit' in metrics and 'Net Sales' in data.index:
        metrics['Gross Margin'] = np.round(metrics['Gross Profit'] / data.loc['Net Sales'], 2)
    else:
        metrics['Gross Margin'] = 'N/A'
    
    if 'Gross Profit' in metrics and 'Advertising' in data.index and 'Marketing Expense' in data.index and 'Net Sales' in data.index:
        metrics['Contribution Margin'] = np.round((metrics['Gross Profit'] - (data.loc['Advertising'] + data.loc['Marketing Expense'])) / data.loc['Net Sales'], 2)
    else:
        metrics['Contribution Margin'] = 'N/A'
    
    if 'Net Profit' in data.index and 'Net Revenue' in data.index:
        metrics['Net Profit Margin'] = np.round(data.loc['Net Profit'] / data.loc['Net Revenue'], 2)
    else:
        metrics['Net Profit Margin'] = 'N/A'
    
    # Expense Efficiency Metrics (if data is available)
    if 'Advertising' in data.index and 'Marketing Expense' in data.index and 'Net Sales' in data.index:
        metrics['S&M as % of Revenue'] = np.round((data.loc['Advertising'] + data.loc['Marketing Expense']) / data.loc['Net Sales'], 2)
    else:
        metrics['S&M as % of Revenue'] = 'N/A'
    
    if 'Payroll Expense' in data.index and 'Net Sales' in data.index:
        metrics['Payroll as % of Revenue'] = np.round(data.loc['Payroll Expense'] / data.loc['Net Sales'], 2)
    else:
        metrics['Payroll as % of Revenue'] = 'N/A'
    
    if 'Credit Cards' in data.index and 'Monthly Operating Expenses' in data.index:
        metrics['Credit Card as % of OpEx'] = np.round(data.loc['Credit Cards'] / data.loc['Monthly Operating Expenses'], 2)
    else:
        metrics['Credit Card as % of OpEx'] = 'N/A'
    
    return metrics

# Generate 6 synthetic datasets
synthetic_datasets = []
for i in range(3):  # First 3 datasets with multiplication factor between 0.5 and 1
    synthetic_datasets.append(generate_synthetic_data(original_data, 0.5, 1))
for i in range(3):  # Next 3 datasets with multiplication factor between 1.1 and 2
    synthetic_datasets.append(generate_synthetic_data(original_data, 1.1, 2))

# Calculate metrics for original data
original_metrics = calculate_metrics(original_data)

# Calculate metrics for synthetic datasets
synthetic_metrics_list = [calculate_metrics(data) for data in synthetic_datasets]

# Create a comparison table
comparison_table = pd.DataFrame({
    'Metric': list(original_metrics.keys()),
    'Original Data': list(original_metrics.values())
})

for i, synthetic_metrics in enumerate(synthetic_metrics_list, start=1):
    comparison_table[f'Synthetic Data {i}'] = list(synthetic_metrics.values())

# Print the comparison table
print("Comparison of Metrics: Original Data vs Synthetic Datasets")
print(comparison_table.to_string())

# Save synthetic datasets to separate CSV files
for i, synthetic_data in enumerate(synthetic_datasets, start=1):
    synthetic_data.to_csv(f'synthetic_data_{i}.csv', index=True)

print("\nSynthetic datasets saved to 'synthetic_data_1.csv' to 'synthetic_data_6.csv'.")