from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.prediction import router as prediction_router
from routes.dataset import router as dataset_router
from routes.analytics import router as analytics_router

app = FastAPI(title="DemandIQ API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "DemandIQ API is running."}

# Include Routers
app.include_router(prediction_router, prefix="/api")
app.include_router(dataset_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
