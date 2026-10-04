import pandas as pd
import numpy as np
from datetime import timedelta

np.random.seed(42)
start_date = pd.to_datetime('2021-01-01')
end_date = pd.to_datetime('2023-12-31')
dates = pd.date_range(start_date, end_date)

stores = ['Store_A', 'Store_B', 'Store_C', 'Store_D', 'Store_E']
categories = {'Produce': ['Apples', 'Bananas', 'Carrots', 'Potatoes'],
              'Dairy': ['Milk', 'Cheese', 'Yogurt', 'Butter'],
              'Bakery': ['Bread', 'Bagels', 'Muffins', 'Croissants'],
              'Beverages': ['Water', 'Soda', 'Juice', 'Coffee']}

data = []
for date in dates:
    is_weekend = date.weekday() >= 5
    month_factor = 1.0 + 0.2 * np.sin(2 * np.pi * date.month / 12)
    is_holiday = np.random.choice([0, 1], p=[0.95, 0.05])
    
    for store in stores:
        store_factor = {'Store_A': 1.2, 'Store_B': 0.9, 'Store_C': 1.0, 'Store_D': 1.5, 'Store_E': 0.8}[store]
        
        for cat, prods in categories.items():
            for prod in prods:
                base_price = np.random.uniform(1.0, 10.0)
                is_promotion = np.random.choice([0, 1], p=[0.85, 0.15])
                price = base_price * 0.8 if is_promotion else base_price
                
                # Base demand
                base_demand = np.random.poisson(30)
                
                # Adjustments
                demand = base_demand * store_factor * month_factor
                if is_weekend:
                    demand *= 1.3
                if is_holiday:
                    demand *= 1.5
                if is_promotion:
                    demand *= 1.4
                    
                demand = int(max(0, np.round(demand + np.random.normal(0, 5))))
                
                inventory = int(demand + np.random.randint(5, 30))
                
                data.append([
                    date, store, prod, cat, demand, round(price, 2), is_promotion, is_holiday, inventory
                ])

df = pd.DataFrame(data, columns=['Date', 'Store', 'Product', 'Category', 'Units Sold', 'Price', 'Promotion', 'Holiday', 'Inventory'])
df.to_csv('ml/data/raw/grocery_sales.csv', index=False)
print(f"Generated {len(df)} rows of data.")
