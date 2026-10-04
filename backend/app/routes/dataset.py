from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()

def get_data_path():
    return os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "data", "processed", "cleaned_grocery_sales.csv")

@router.get("/products")
def get_products():
    try:
        df = pd.read_csv(get_data_path())
        return {"products": df['Product'].unique().tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
def get_categories():
    try:
        df = pd.read_csv(get_data_path())
        return {"categories": df['Category'].unique().tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stores")
def get_stores():
    try:
        df = pd.read_csv(get_data_path())
        return {"stores": df['Store'].unique().tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
