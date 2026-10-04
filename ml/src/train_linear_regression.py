import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from utils import load_split_data, calculate_metrics

def main():
    print("--- Training Linear Regression ---")
    X_train, y_train, X_val, y_val, X_test, y_test = load_split_data()
    
    # Train
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate on Val
    val_preds = model.predict(X_val)
    val_metrics = calculate_metrics(y_val, val_preds)
    print(f"Validation Metrics: {val_metrics}")
    
    # Evaluate on Test
    test_preds = model.predict(X_test)
    test_metrics = calculate_metrics(y_test, test_preds)
    print(f"Test Metrics: {test_metrics}")
    
    # Save Model
    model_dir = os.path.join("ml", "models")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "linear_regression.joblib"))
    
    # Save Metrics
    results_dir = os.path.join("ml", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    metrics_df = pd.DataFrame([test_metrics])
    metrics_df['Model'] = 'Linear Regression'
    metrics_df.to_csv(os.path.join(results_dir, "lr_metrics.csv"), index=False)
    print("Model and metrics saved successfully.")

if __name__ == "__main__":
    main()
