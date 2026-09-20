from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_jobs_endpoint_with_filters():
    response = client.get("/api/jobs?location=Cape Town")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_skills_endpoints():
    response = client.get("/api/skills")
    assert response.status_code == 200
    
    top_response = client.get("/api/skills/top")
    assert top_response.status_code == 200

def test_opportunities_endpoint():
    response = client.get("/api/opportunities")
    assert response.status_code == 200

def test_recommendations_endpoint():
    response = client.get("/api/recommendations?career_name=Data+Engineer&user_skills=Python,SQL")
    assert response.status_code == 200
    data = response.json()
    assert data["target_career"] == "Data Engineer"
    assert "readiness_score_percentage" in data