import pandas as pd
import numpy as np
import os
import joblib

def create_date_features(df):
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['week'] = df['Date'].dt.isocalendar().week.astype(int)
    df['day'] = df['Date'].dt.day
    df['day_of_week'] = df['Date'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['quarter'] = df['Date'].dt.quarter
    return df

def create_lag_and_rolling_features(df, target='Units Sold'):
    # Sort to ensure chronological order per group
    df = df.sort_values(by=['Store', 'Product', 'Date']).copy()
    
    # Lag features
    lags = [1, 7, 14, 28]
    for lag in lags:
        df[f'lag_{lag}'] = df.groupby(['Store', 'Product'])[target].shift(lag)
        
    # Rolling features (shift by 1 to prevent data leakage)
    windows = [7, 14, 28]
    for window in windows:
        df[f'rolling_mean_{window}'] = (
            df.groupby(['Store', 'Product'])[target]
            .transform(lambda x: x.shift(1).rolling(window=window).mean())
        )
        
    # Drop rows with NaN values created by lag/rolling
    df.dropna(inplace=True)
    return df

def chronological_split(df):
    # Sort strictly by date for splitting
    df = df.sort_values('Date').reset_index(drop=True)
    
    n = len(df)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)
    
    train_df = df.iloc[:train_end]
    val_df = df.iloc[train_end:val_end]
    test_df = df.iloc[val_end:]
    
    print(f"Train set: {len(train_df)} rows ({train_df['Date'].min().date()} to {train_df['Date'].max().date()})")
    print(f"Validation set: {len(val_df)} rows ({val_df['Date'].min().date()} to {val_df['Date'].max().date()})")
    print(f"Test set: {len(test_df)} rows ({test_df['Date'].min().date()} to {test_df['Date'].max().date()})")
    
    return train_df, val_df, test_df

def main():
    print("--- Starting Feature Engineering ---")
    input_path = os.path.join("ml", "data", "processed", "cleaned_grocery_sales.csv")
    output_dir = os.path.join("ml", "data", "processed")
    
    df = pd.read_csv(input_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 1. Date Features
    df = create_date_features(df)
    
    # 2. Lag and Rolling Features
    df = create_lag_and_rolling_features(df, target='Units Sold')
    
    # 3. Categorical encoding (Basic Label Encoding for tree models, leaving as is for XGB/RF can be fine, 
    # but let's map them to integers to be safe and compatible with both Linear Regression and trees)
    # We will save the encoders
    categorical_cols = ['Store', 'Product', 'Category']
    encoders = {}
    
    for col in categorical_cols:
        unique_vals = df[col].unique()
        mapping = {val: i for i, val in enumerate(unique_vals)}
        df[col] = df[col].map(mapping)
        encoders[col] = mapping
        
    # Save encoders for prediction pipeline
    os.makedirs(os.path.join("ml", "models"), exist_ok=True)
    joblib.dump(encoders, os.path.join("ml", "models", "label_encoders.joblib"))
    
    # 4. Train/Val/Test Split
    train_df, val_df, test_df = chronological_split(df)
    
    # Save datasets
    train_df.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    val_df.to_csv(os.path.join(output_dir, "val.csv"), index=False)
    test_df.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    
    features = list(train_df.columns)
    features.remove('Units Sold')
    features.remove('Date') # Usually dropped before training
    
    # Save feature configuration
    config = {
        'target': 'Units Sold',
        'features': features
    }
    joblib.dump(config, os.path.join("ml", "models", "feature_config.joblib"))
    
    print("Feature engineering completed and data split into train, val, test.")

if __name__ == "__main__":
    main()
