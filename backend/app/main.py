from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(title="AI News Aggregator")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI News Aggregator API"}
