# DemandIQ: Project Documentation (Final Updated Version)

## 1. What is the Project?
**DemandIQ** is an end-to-end Machine Learning application designed to accurately forecast future grocery product demand based on historical sales data. 

Rather than stopping at just a trained model in a Jupyter Notebook, DemandIQ functions as a complete software product. It translates raw machine learning predictions into actionable **Inventory Intelligence**, allowing store managers to see expected shortages, safety stock requirements, and recommended reorder quantities before stockouts happen.

---

## 2. How Does It Work?

The system operates across three main layers: the ML Pipeline, the Backend API, and the Frontend Dashboard.

### A. The Machine Learning Pipeline
1. **Data Ingestion & Cleaning:** The system processes historical daily sales data containing information on pricing, promotions, and holidays.
2. **Feature Engineering:** To capture the time-series nature of the problem, the pipeline engineers specialized temporal features:
   - *Date Features:* Day of the week, weekends, month, quarter.
   - *Lag Features:* Demand from exactly 1 day, 7 days, 14 days, and 28 days prior.
   - *Rolling Averages:* Smoothed demand trends over the past week or month.
3. **Strict Evaluation Split:** To prevent "data leakage" (accidentally letting the model peek into the future), the dataset is split chronologically: the first 70% of time for training, the next 15% for tuning, and the final 15% strictly for final testing.
4. **Model Training & Baselines:** Four models are evaluated to prove the value of ML:
   - *Seasonal Naive Baseline:* A standard forecasting rule assuming "Demand today = Demand 7 days ago."
   - *Linear Regression:* Provides a simple mathematical baseline.
   - *Random Forest Regressor:* An ensemble of decision trees.
   - *XGBoost Regressor:* An advanced gradient boosting algorithm that ultimately won as the most accurate model.
5. **Serialization:** The winning model (XGBoost) and the data transformers (Label Encoders) are saved into `.joblib` files so they can be loaded instantly without retraining.

### B. The Backend Inference Engine (FastAPI)
1. **Always-On Engine:** When the server starts, it loads the trained `.joblib` ML model into memory.
2. **API Endpoints:** It opens REST endpoints (like `/api/predict` and `/api/dashboard-summary`). 
3. **Live Prediction & What-If Analysis:** When the frontend requests a forecast, the backend generates the required temporal features on the fly, passes it through the XGBoost model, and returns the numerical demand prediction. It even allows the frontend to run parallel "What-If" queries to calculate promotional uplift.
4. **Inventory Business Logic:** A dedicated mathematical service calculates a highly defensible safety stock using standard deviations: `Safety Stock = Z * Sigma * sqrt(Lead Time)`. It then calculates the exact recommended reorder quantities based on current physical stock.

### C. The Frontend Interface (React)
1. **Interactive Dashboard:** Users interact with a clean, responsive web interface showing KPIs, Demand Trends, and Category Mixes.
2. **Dynamic Forms:** Users can select different stores and products, toggle promotions, and instantly see a "What-If Analysis" showing the expected % uplift.
3. **Data Visualization:** The interface pulls historical ML metrics from the backend and plots beautiful comparison charts so stakeholders can trust the model's performance (proving XGBoost outperforms the Seasonal Naive baseline).

---

## 3. What Technologies Were Used?

### Machine Learning & Data Science
* **Python 3.11+:** The core programming language.
* **Pandas & NumPy:** Used heavily for data manipulation, cleaning, and mathematical feature engineering.
* **Scikit-learn:** Used for the Linear Regression baseline, Random Forest model, and calculating core error metrics (MAE, RMSE, R-Squared).
* **XGBoost:** The primary, high-performance gradient boosting library used for the final demand predictions and feature importance extraction.
* **Joblib:** Used to serialize (save) and deserialize (load) the trained ML models and data transformers to disk.

### Backend Development
* **FastAPI:** A modern, high-performance web framework used to build the REST API. Chosen for its speed and native Python type-hinting support.
* **Uvicorn:** The lightning-fast ASGI server used to host the FastAPI application.
* **Pydantic:** Used natively by FastAPI to validate that the data coming from the frontend exactly matches the expected schema.
* **Pytest:** Used to write automated test scripts ensuring the API behaves correctly (e.g., handling zero/negative stock).

### Frontend Development
* **React:** The core JavaScript UI library used to build the interactive dashboard.
* **Vite:** A next-generation frontend tooling system used to scaffold and serve the React app instantly.
* **Tailwind CSS (v4):** A utility-first CSS framework used to quickly style the dashboard, cards, and buttons with a clean, professional aesthetic.
* **Recharts:** A composable charting library built on React components used to render the bar charts and line graphs on the Dashboard and Model Performance pages.
* **Axios:** The HTTP client used to seamlessly send JSON requests from the React frontend to the Python backend.
* **Lucide React:** Used for the clean, SVG vector icons found throughout the dashboard.
