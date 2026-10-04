def calculate_inventory_insights(current_stock: int, predicted_demand: float) -> dict:
    """
    Calculates inventory intelligence metrics based on demand and current stock.
    Safety stock is assumed to be 20% of predicted demand.
    """
    expected_shortage = max(0.0, predicted_demand - current_stock)
    
    safety_stock = predicted_demand * 0.20
    target_inventory = predicted_demand + safety_stock
    
    suggested_reorder = max(0.0, target_inventory - current_stock)
    
    # Determine Status
    if expected_shortage > 0:
        status = "LOW STOCK"
    elif current_stock > target_inventory * 1.5:
        status = "HIGH STOCK"
    else:
        status = "SUFFICIENT STOCK"
        
    return {
        "expected_shortage": round(expected_shortage, 2),
        "suggested_reorder": round(suggested_reorder, 2),
        "stock_status": status
    }
