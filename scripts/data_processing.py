import pandas as pd
import os

def load_data(file_name):
    # Get the absolute path to the data directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from scripts/
    file_path = os.path.join(base_dir, 'data', file_name)
    print(f"Loading file from: {file_path}")  # Debugging: Print the resolved file path
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Transpose the DataFrame so that rows become columns and vice versa
    df = df.set_index('Name').transpose()
    
    # Convert all columns to numeric, handling non-numeric values
    df = df.apply(pd.to_numeric, errors='coerce')
    
    print("Columns in the DataFrame:", df.columns.tolist())  # Debugging: Print column names
    return df

def calculate_metrics(df):
    # Calculate Gross Profit if the required rows exist
<<<<<<< Updated upstream
    if 'Gross Profit' in df.columns and 'Total Income' in df.columns:
        df['Gross Margin'] = (df['Gross Profit'] / df['Total Income']) * 100
    else:
        print("Warning: 'Gross Profit' or 'Total Income' column not found. Skipping Gross Margin calculation.")
    
    # Calculate Net Profit Margin if the required rows exist
    if 'Net Profit' in df.columns and 'Total Income' in df.columns:
        df['Net Profit Margin'] = (df['Net Profit'] / df['Total Income']) * 100
    else:
        print("Warning: 'Net Profit' or 'Total Income' column not found. Skipping Net Profit Margin calculation.")
=======
    if 'Gross Profit' in df.columns:
        df['Gross Margin'] = (df['Gross Profit'] / df['Total Income']) * 100
    else:
        print("Warning: 'Gross Profit' column not found. Skipping Gross Margin calculation.")
>>>>>>> Stashed changes
    
    # Add more metrics as needed
    return df

def main():
    # Load and preprocess data
    main_company = load_data('main_company.csv')
    main_company = calculate_metrics(main_company)
    
    # Load competitor data
    competitors = []
    for i in range(1, 6):
        competitor = load_data(f'competitor_{i}.csv')
        competitor = calculate_metrics(competitor)
        competitors.append(competitor)
    
    return main_company, competitors

if __name__ == "__main__":
    main_company, competitors = main()