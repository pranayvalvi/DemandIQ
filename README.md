# DemandIQ: Grocery Store Demand Forecasting & Inventory Intelligence

DemandIQ is a machine learning application designed to predict future grocery product demand using historical sales data. It features a complete ML pipeline, a FastAPI prediction backend, and a modern React dashboard.

## Technology Stack
- **Machine Learning:** Python (Pandas, Scikit-learn, XGBoost, Joblib)
- **Backend:** FastAPI, Uvicorn
- **Frontend:** React, Vite, Tailwind CSS, Recharts

## Project Architecture
```text
DemandIQ/
├── backend/          # FastAPI server and ML services
├── frontend/         # React dashboard
└── ml/               # Machine learning pipeline (preprocessing, models, EDA)
```

## Setup and Installation

### 1. Machine Learning & Backend
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Train the models: `python ml/train.py`
5. Start the backend: `python backend/app/main.py`
   - The API will be available at `http://localhost:8000`

### 2. Frontend Dashboard
1. Open a new terminal and navigate to the `frontend/` directory.
2. Install dependencies: `npm install`
3. Start the dashboard: `npm run dev`
   - The UI will be available at `http://localhost:5173`

## Features & Results
- **EDA Pipeline:** Evaluates overall sales, demand distribution, and impacts of pricing/promotions/holidays.
- **Model Evaluation:** Compares Linear Regression, Random Forest, and XGBoost.
- **Winning Model:** **XGBoost** achieved the best predictive performance (Lowest RMSE, Highest R²).
- **Inventory Intelligence:** Translates raw demand forecasts into actionable insights (Expected Shortage, Stock Status, Reorder Quantities).
