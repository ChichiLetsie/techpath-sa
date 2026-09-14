from fastapi import FastAPI
from app.api import health

app = FastAPI(
    title="TechPath SA API",
    description="South African technology career intelligence platform API",
    version="0.1.0"
)

app.include_router(health.api_router if hasattr(health, 'api_router') else health.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to TechPath SA API. Visit /docs for documentation."}