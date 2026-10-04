# DemandIQ: Project Documentation

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
4. **Model Training:** Three models are trained to compare performance:
   - *Linear Regression* (Provides a simple mathematical baseline)
   - *Random Forest Regressor* (An ensemble of decision trees)
   - *XGBoost Regressor* (An advanced gradient boosting algorithm that ultimately won as the most accurate model)
5. **Serialization:** The winning model (XGBoost) and the data transformers (Label Encoders) are saved into `.joblib` files so they can be loaded instantly without retraining.

### B. The Backend Inference Engine (FastAPI)
1. **Always-On Engine:** When the server starts, it loads the trained `.joblib` ML model into memory.
2. **API Endpoints:** It opens REST endpoints (like `/api/predict`). 
3. **Live Prediction:** When the frontend requests a forecast, the backend takes the raw user input (store, product, date, price, etc.), safely encodes the categories, generates the required temporal features on the fly, passes it through the XGBoost model, and returns the numerical demand prediction.
4. **Inventory Business Logic:** A dedicated service sits on top of the ML predictions to calculate if a product is in `LOW STOCK`, calculates a 20% safety stock margin, and suggests exact reorder quantities.

### C. The Frontend Interface (React)
1. **Interactive Dashboard:** Users interact with a clean, responsive web interface.
2. **Dynamic Forms:** Users can select different stores and products, input hypothetical scenarios (like "what if we put this on promotion tomorrow?"), and click "Generate Forecast".
3. **Data Visualization:** The interface pulls historical ML metrics from the backend and plots beautiful comparison charts so stakeholders can trust the model's performance.

---

## 3. What Technologies Were Used?

The project was built using a modern, industry-standard technology stack.

### Machine Learning & Data Science
* **Python 3.11+:** The core programming language.
* **Pandas & NumPy:** Used heavily for data manipulation, cleaning, and mathematical feature engineering.
* **Scikit-learn:** Used for the Linear Regression baseline, Random Forest model, and calculating core error metrics (MAE, RMSE, R²).
* **XGBoost:** The primary, high-performance gradient boosting library used for the final demand predictions.
* **Joblib:** Used to serialize (save) and deserialize (load) the trained ML models and data transformers to disk.

### Backend Development
* **FastAPI:** A modern, high-performance web framework used to build the REST API. Chosen for its speed and native Python type-hinting support.
* **Uvicorn:** The lightning-fast ASGI server used to host the FastAPI application.
* **Pydantic:** Used natively by FastAPI to validate that the data coming from the frontend exactly matches the expected schema.

### Frontend Development
* **React:** The core JavaScript UI library used to build the interactive dashboard.
* **Vite:** A next-generation frontend tooling system used to scaffold and serve the React app instantly.
* **Tailwind CSS (v4):** A utility-first CSS framework used to quickly style the dashboard, cards, and buttons with a clean, professional aesthetic.
* **Recharts:** A composable charting library built on React components used to render the bar charts on the Model Performance page.
* **Axios:** The HTTP client used to seamlessly send JSON requests from the React frontend to the Python backend.
* **Lucide React:** Used for the clean, SVG vector icons found throughout the dashboard (boxes, trending arrows, warning symbols).
