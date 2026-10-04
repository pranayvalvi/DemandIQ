from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class PredictionRequest(BaseModel):
    store: str
    product: str
    category: str
    forecast_date: date
    price: float
    promotion: int
    holiday: int
    inventory: int
    # Previous demand features required by the model
    lag_1: float
    lag_7: float
    lag_14: float
    lag_28: float
    rolling_mean_7: float
    rolling_mean_14: float
    rolling_mean_28: float

class PredictionResponse(BaseModel):
    predicted_demand: float
    store: str
    product: str
    forecast_date: date

class InventoryInsightResponse(BaseModel):
    product: str
    current_stock: int
    predicted_demand: float
    expected_shortage: float
    stock_status: str
    suggested_reorder: float
