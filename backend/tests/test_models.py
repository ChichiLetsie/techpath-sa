from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models import models

client = TestClient(app)

def test_database_connection_and_models():
    db = SessionLocal()
    try:
        # Check if skills table exists and can query
        skills_count = db.query(models.Skill).count()
        assert skills_count >= 0
    finally:
        db.close()