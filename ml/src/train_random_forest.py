import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from utils import load_split_data, calculate_metrics

def main():
    print("--- Training Random Forest ---")
    X_train, y_train, X_val, y_val, X_test, y_test = load_split_data()
    
    # Simple Hyperparameter Tuning using Validation set
    param_grid = [
        {'n_estimators': 50, 'max_depth': 10, 'min_samples_split': 5},
        {'n_estimators': 100, 'max_depth': 15, 'min_samples_split': 5},
        {'n_estimators': 100, 'max_depth': 20, 'min_samples_split': 2},
    ]
    
    best_model = None
    best_val_rmse = float('inf')
    best_params = None
    
    print("Tuning hyperparameters on validation set...")
    for params in param_grid:
        model = RandomForestRegressor(
            random_state=42,
            n_jobs=-1,
            **params
        )
        model.fit(X_train, y_train)
        val_preds = model.predict(X_val)
        metrics = calculate_metrics(y_val, val_preds)
        
        print(f"Params: {params} -> Val RMSE: {metrics['RMSE']:.4f}")
        if metrics['RMSE'] < best_val_rmse:
            best_val_rmse = metrics['RMSE']
            best_model = model
            best_params = params
            
    print(f"\nBest Params Selected: {best_params}")
    
    # Evaluate final model on Test
    test_preds = best_model.predict(X_test)
    test_metrics = calculate_metrics(y_test, test_preds)
    print(f"Test Metrics: {test_metrics}")
    
    # Save Model
    model_dir = os.path.join("ml", "models")
    joblib.dump(best_model, os.path.join(model_dir, "random_forest.joblib"))
    
    # Save Metrics
    results_dir = os.path.join("ml", "results")
    metrics_df = pd.DataFrame([test_metrics])
    metrics_df['Model'] = 'Random Forest'
    metrics_df.to_csv(os.path.join(results_dir, "rf_metrics.csv"), index=False)
    print("Model and metrics saved successfully.")

if __name__ == "__main__":
    main()
