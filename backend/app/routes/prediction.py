from fastapi import APIRouter, HTTPException
from schemas.api_models import PredictionRequest, PredictionResponse, InventoryInsightResponse
from services.prediction_service import prediction_service
from services.inventory_service import calculate_inventory_insights

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        data = request.model_dump()
        pred = prediction_service.predict_demand(data)
        
        return PredictionResponse(
            predicted_demand=round(pred, 2),
            store=request.store,
            product=request.product,
            forecast_date=request.forecast_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inventory-insights", response_model=InventoryInsightResponse)
def get_inventory_insights(request: PredictionRequest):
    try:
        data = request.model_dump()
        pred = prediction_service.predict_demand(data)
        
        insights = calculate_inventory_insights(request.inventory, pred)
        
        return InventoryInsightResponse(
            product=request.product,
            current_stock=request.inventory,
            predicted_demand=round(pred, 2),
            expected_shortage=insights["expected_shortage"],
            stock_status=insights["stock_status"],
            suggested_reorder=insights["suggested_reorder"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
