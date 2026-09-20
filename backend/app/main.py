from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from app.api import health, router

app = FastAPI(
    title="TechPath SA API",
    description="South African technology career intelligence platform API",
    version="0.1.0"
)

app.include_router(health.router, prefix="/api")
app.include_router(router.router)

@app.get("/", response_class=HTMLResponse)
def root():
    index_path = "/app/frontend/index.html"
    if not os.path.exists(index_path):
        index_path = "frontend/index.html"
    
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return {"message": "Welcome to TechPath SA API. Visit /docs for Swagger documentation."}