import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

def load_split_data():
    base_dir = os.path.join("ml", "data", "processed")
    train = pd.read_csv(os.path.join(base_dir, "train.csv"))
    val = pd.read_csv(os.path.join(base_dir, "val.csv"))
    test = pd.read_csv(os.path.join(base_dir, "test.csv"))
    
    # Exclude non-feature columns
    drop_cols = ['Units Sold', 'Date']
    
    X_train = train.drop(columns=drop_cols)
    y_train = train['Units Sold']
    
    X_val = val.drop(columns=drop_cols)
    y_val = val['Units Sold']
    
    X_test = test.drop(columns=drop_cols)
    y_test = test['Units Sold']
    
    return X_train, y_train, X_val, y_val, X_test, y_test

def calculate_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    # Safe MAPE calculation handling zeros
    # If y_true is 0, we can use max(1, y_true) to prevent infinite inflation
    mape = np.mean(np.abs((y_true - y_pred) / np.maximum(1, y_true))) * 100
    
    return {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'R2': r2
    }
