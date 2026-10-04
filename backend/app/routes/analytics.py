from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()

@router.get("/model-performance")
def get_model_performance():
    try:
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "results", "model_comparison.csv")
        df = pd.read_csv(path)
        return {"performance": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sales-summary")
def get_sales_summary():
    try:
        path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "data", "processed", "cleaned_grocery_sales.csv")
        df = pd.read_csv(path)
        
        return {
            "total_sales": int(df['Units Sold'].sum()),
            "total_revenue": float((df['Units Sold'] * df['Price']).sum()),
            "total_products": int(df['Product'].nunique()),
            "total_stores": int(df['Store'].nunique())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
