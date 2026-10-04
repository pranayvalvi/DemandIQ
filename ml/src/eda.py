import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def perform_eda(filepath, output_dir):
    print(f"--- Performing EDA on {filepath} ---")
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    # 1. Overall sales/demand over time
    plt.figure(figsize=(15, 6))
    daily_sales = df.groupby('Date')['Units Sold'].sum().reset_index()
    sns.lineplot(data=daily_sales, x='Date', y='Units Sold')
    plt.title('Overall Demand Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Units Sold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '1_overall_demand_over_time.png'))
    plt.close()
    print("Generated: Overall demand over time")

    # 2. Demand by product
    plt.figure(figsize=(12, 6))
    product_sales = df.groupby('Product')['Units Sold'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=product_sales, x='Units Sold', y='Product', palette='viridis')
    plt.title('Total Demand by Product')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_demand_by_product.png'))
    plt.close()
    print("Generated: Demand by product")

    # 3. Demand by category
    plt.figure(figsize=(10, 6))
    category_sales = df.groupby('Category')['Units Sold'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=category_sales, x='Category', y='Units Sold', palette='Set2')
    plt.title('Total Demand by Category')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '3_demand_by_category.png'))
    plt.close()
    print("Generated: Demand by category")

    # 4. Demand by store
    plt.figure(figsize=(10, 6))
    store_sales = df.groupby('Store')['Units Sold'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=store_sales, x='Store', y='Units Sold', palette='pastel')
    plt.title('Total Demand by Store')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '4_demand_by_store.png'))
    plt.close()
    print("Generated: Demand by store")

    # 5. Distribution of demand
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Units Sold'], bins=30, kde=True, color='purple')
    plt.title('Distribution of Demand (Units Sold)')
    plt.xlabel('Units Sold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_distribution_of_demand.png'))
    plt.close()
    print("Generated: Distribution of demand")

    # 6. Price vs demand
    if 'Price' in df.columns:
        plt.figure(figsize=(10, 6))
        # Random sample to avoid overplotting if data is large
        sample_df = df.sample(min(10000, len(df)), random_state=42)
        sns.scatterplot(data=sample_df, x='Price', y='Units Sold', alpha=0.5)
        plt.title('Price vs Demand (Sampled)')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, '6_price_vs_demand.png'))
        plt.close()
        print("Generated: Price vs demand")

    # 7. Promotion vs demand
    if 'Promotion' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, x='Promotion', y='Units Sold', palette='Set1')
        plt.title('Promotion vs Demand')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, '7_promotion_vs_demand.png'))
        plt.close()
        print("Generated: Promotion vs demand")

    # 8. Holiday vs demand
    if 'Holiday' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.boxplot(data=df, x='Holiday', y='Units Sold', palette='Set3')
        plt.title('Holiday vs Demand')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, '8_holiday_vs_demand.png'))
        plt.close()
        print("Generated: Holiday vs demand")
        
    print("\nEDA pipeline completed successfully. All visualizations saved to:", output_dir)

def main():
    processed_path = os.path.join("ml", "data", "processed", "cleaned_grocery_sales.csv")
    eda_output_dir = os.path.join("ml", "results", "eda")
    perform_eda(processed_path, eda_output_dir)

if __name__ == "__main__":
    main()
