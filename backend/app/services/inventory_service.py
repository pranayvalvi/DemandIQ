import math

def calculate_inventory_insights(current_stock: int, predicted_demand: float) -> dict:
    """
    Calculates inventory intelligence metrics based on demand and current stock.
    Formula: SafetyStock = Z * sigma_demand * sqrt(LeadTime)
    """
    # Assumptions for academic demonstration:
    Z = 1.65 # 95% service level factor
    lead_time_days = 2
    sigma_demand = predicted_demand * 0.25 # Assuming Coefficient of Variation is 0.25
    
    safety_stock = Z * sigma_demand * math.sqrt(lead_time_days)
    target_inventory = predicted_demand + safety_stock
    
    expected_shortage = max(0.0, predicted_demand - current_stock)
    suggested_reorder = max(0.0, target_inventory - current_stock)
    
    # Determine Status
    if current_stock <= target_inventory * 0.8:
        status = "LOW STOCK"
    elif current_stock > target_inventory * 1.5:
        status = "HIGH STOCK"
    else:
        status = "SUFFICIENT STOCK"
        
    return {
        "expected_shortage": round(expected_shortage, 0),
        "safety_stock": round(safety_stock, 0),
        "target_inventory": round(target_inventory, 0),
        "suggested_reorder": round(suggested_reorder, 0),
        "stock_status": status
    }
