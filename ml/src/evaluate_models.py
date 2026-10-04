import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("--- Evaluating and Comparing Models ---")
    results_dir = os.path.join("ml", "results")
    
    # Load all metrics
    lr_df = pd.read_csv(os.path.join(results_dir, "lr_metrics.csv"))
    rf_df = pd.read_csv(os.path.join(results_dir, "rf_metrics.csv"))
    xgb_df = pd.read_csv(os.path.join(results_dir, "xgb_metrics.csv"))
    
    # Combine
    comparison_df = pd.concat([lr_df, rf_df, xgb_df], ignore_index=True)
    comparison_df = comparison_df[['Model', 'MAE', 'RMSE', 'MAPE', 'R2']] # Reorder
    
    print("\nModel Comparison Table:")
    print(comparison_df.to_string(index=False))
    
    # Save comparison table
    comparison_df.to_csv(os.path.join(results_dir, "model_comparison.csv"), index=False)
    
    # Generate Charts
    sns.set_theme(style="whitegrid")
    metrics = ['MAE', 'RMSE', 'MAPE', 'R2']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Model Performance Comparison', fontsize=16)
    
    for idx, metric in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]
        sns.barplot(data=comparison_df, x='Model', y=metric, ax=ax, palette='viridis')
        ax.set_title(metric)
        ax.set_xlabel('')
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(results_dir, "model_comparison_charts.png"))
    plt.close()
    
    # Select best model (lowest RMSE)
    best_model_idx = comparison_df['RMSE'].idxmin()
    best_model_name = comparison_df.loc[best_model_idx, 'Model']
    print(f"\nBest model based on RMSE is: {best_model_name}")
    
    print(f"Results saved to {results_dir}")

if __name__ == "__main__":
    main()
