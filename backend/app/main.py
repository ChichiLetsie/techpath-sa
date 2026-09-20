from fastapi import FastAPI
from app.api import health, router

app = FastAPI(
    title="TechPath SA API",
    description="South African technology career intelligence platform API",
    version="0.1.0"
)

app.include_router(health.router, prefix="/api")
app.include_router(router.router)  # router.py already has prefix="/api" defined internally

@app.get("/")
def root():
    return {"message": "Welcome to TechPath SA API. Visit /docs for documentation."}