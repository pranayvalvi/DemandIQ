import pandas as pd
import numpy as np
import os

def load_and_inspect_data(filepath):
    print(f"--- Loading Dataset: {filepath} ---")
    df = pd.read_csv(filepath)
    
    print("\n--- Basic Info ---")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    print("\n--- Data Types ---")
    print(df.dtypes)
    
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    
    print("\n--- Duplicate Rows ---")
    duplicates = df.duplicated().sum()
    print(f"Duplicates: {duplicates}")
    
    return df, duplicates

def preprocess_data(df, duplicates):
    print("\n--- Preprocessing Pipeline ---")
    
    # 1. Parse dates
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
        
    # 2. Handle duplicates
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"Dropped {duplicates} duplicate rows.")
        
    # 3. Handle missing values (if any)
    if df.isnull().sum().sum() > 0:
        print("Handling missing values...")
        # Since it's sales data, forward fill or impute median depending on context.
        # Our generated dataset has 0 missing, but we add this for completeness.
        df.fillna(method='ffill', inplace=True)
        
    # 4. Identify unique counts
    if 'Store' in df.columns:
        print(f"Number of stores: {df['Store'].nunique()}")
    if 'Product' in df.columns:
        print(f"Number of products: {df['Product'].nunique()}")
    if 'Category' in df.columns:
        print(f"Categories: {df['Category'].unique().tolist()}")
        
    # 5. Define variables
    target_variable = 'Units Sold'
    numerical_variables = ['Price', 'Inventory']
    categorical_variables = ['Store', 'Product', 'Category', 'Promotion', 'Holiday']
    
    print(f"Target Variable: {target_variable}")
    print(f"Numerical Variables: {numerical_variables}")
    print(f"Categorical Variables: {categorical_variables}")
    
    return df

def main():
    raw_path = os.path.join("ml", "data", "raw", "grocery_sales.csv")
    processed_dir = os.path.join("ml", "data", "processed")
    processed_path = os.path.join(processed_dir, "cleaned_grocery_sales.csv")
    
    os.makedirs(processed_dir, exist_ok=True)
    
    # Load and inspect
    df, duplicates = load_and_inspect_data(raw_path)
    
    # Preprocess
    df_clean = preprocess_data(df, duplicates)
    
    # Save cleaned data
    df_clean.to_csv(processed_path, index=False)
    print(f"\nSaved cleaned dataset to {processed_path}")
    print("Preprocessing completed successfully.")

if __name__ == "__main__":
    main()
