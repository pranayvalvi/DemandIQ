import os
import joblib
import pandas as pd
import numpy as np

class PredictionService:
    def __init__(self):
        base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models")
        
        # Load best model (XGBoost)
        self.model = joblib.load(os.path.join(base_dir, "xgboost.joblib"))
        
        # Load encoders and configuration
        self.encoders = joblib.load(os.path.join(base_dir, "label_encoders.joblib"))
        self.config = joblib.load(os.path.join(base_dir, "feature_config.joblib"))
        
    def _encode_categorical(self, col_name, value):
        # Gracefully handle unseen categorical values by mapping to 0 or a safe default
        encoder = self.encoders.get(col_name, {})
        return encoder.get(value, 0)
        
    def predict_demand(self, data: dict) -> float:
        """
        Takes raw input dict, processes it, and returns the predicted demand.
        """
        # Feature extraction
        forecast_date = pd.to_datetime(data['forecast_date'])
        
        # Build features dataframe matching training exactly
        row = {
            'year': forecast_date.year,
            'month': forecast_date.month,
            'week': forecast_date.isocalendar().week,
            'day': forecast_date.day,
            'day_of_week': forecast_date.dayofweek,
            'is_weekend': int(forecast_date.dayofweek >= 5),
            'quarter': forecast_date.quarter,
            
            'Store': self._encode_categorical('Store', data['store']),
            'Product': self._encode_categorical('Product', data['product']),
            'Category': self._encode_categorical('Category', data['category']),
            
            'Price': data['price'],
            'Promotion': data['promotion'],
            'Holiday': data['holiday'],
            'Inventory': data['inventory'],
            
            'lag_1': data['lag_1'],
            'lag_7': data['lag_7'],
            'lag_14': data['lag_14'],
            'lag_28': data['lag_28'],
            
            'rolling_mean_7': data['rolling_mean_7'],
            'rolling_mean_14': data['rolling_mean_14'],
            'rolling_mean_28': data['rolling_mean_28'],
        }
        
        # Ensure column order matches the model training exactly
        df = pd.DataFrame([row])
        df = df[self.config['features']]
        
        # Predict and clamp negative values to 0
        prediction = self.model.predict(df)[0]
        return max(0.0, float(prediction))
        
prediction_service = PredictionService()
