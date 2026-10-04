import os
import joblib
import pandas as pd
from xgboost import XGBRegressor
from utils import load_split_data, calculate_metrics

def main():
    print("--- Training XGBoost ---")
    X_train, y_train, X_val, y_val, X_test, y_test = load_split_data()
    
    # Train with early stopping on the validation set
    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=20
    )
    
    print("Training and tuning via early stopping...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=50
    )
    
    print(f"\nBest iteration: {model.best_iteration}")
    
    # Evaluate final model on Test
    test_preds = model.predict(X_test)
    test_metrics = calculate_metrics(y_test, test_preds)
    print(f"Test Metrics: {test_metrics}")
    
    # Save Model
    model_dir = os.path.join("ml", "models")
    joblib.dump(model, os.path.join(model_dir, "xgboost.joblib"))
    
    # Save Metrics
    results_dir = os.path.join("ml", "results")
    metrics_df = pd.DataFrame([test_metrics])
    metrics_df['Model'] = 'XGBoost'
    metrics_df.to_csv(os.path.join(results_dir, "xgb_metrics.csv"), index=False)
    print("Model and metrics saved successfully.")

if __name__ == "__main__":
    main()
