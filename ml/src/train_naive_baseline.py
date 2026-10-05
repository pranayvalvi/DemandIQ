import os
import pandas as pd
from utils import load_split_data, calculate_metrics

def main():
    print("--- Training Seasonal Naive Baseline ---")
    _, _, X_val, y_val, X_test, y_test = load_split_data()
    
    # Seasonal Naive: Predicted demand today = demand 7 days ago (lag_7)
    # Since we already have lag_7 in our features, we just use it directly!
    
    # Evaluate on Val
    val_preds = X_val['lag_7']
    val_metrics = calculate_metrics(y_val, val_preds)
    print(f"Validation Metrics: {val_metrics}")
    
    # Evaluate on Test
    test_preds = X_test['lag_7']
    test_metrics = calculate_metrics(y_test, test_preds)
    print(f"Test Metrics: {test_metrics}")
    
    # Save Metrics
    results_dir = os.path.join("ml", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    metrics_df = pd.DataFrame([test_metrics])
    metrics_df['Model'] = 'Seasonal Naive'
    metrics_df.to_csv(os.path.join(results_dir, "naive_metrics.csv"), index=False)
    print("Naive Baseline metrics saved successfully.")

if __name__ == "__main__":
    main()
