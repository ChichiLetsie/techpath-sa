from fastapi.testclient import TestClient
from app.main import app
from pipeline.transform.transformer import DataTransformer
from pipeline.validation.schemas import ValidatedJob
from pipeline.load.loader import DataLoader

client = TestClient(app)

def test_end_to_end_pipeline_flow():
    # 1. Raw sample input
    raw_jobs = [{
        "title": "Data Engineering Intern",
        "company": "Discovery Limited",
        "location": "Sandton, Johannesburg",
        "description": "Python and SQL data engineering internship role.",
        "employment_type": "Internship",
        "experience_level": "Graduate",
        "source": "Integration Test",
        "skills": ["Python", "SQL", "AWS"]
    }]

    # 2. Transform stage
    cleaned = DataTransformer.transform_jobs(raw_jobs)
    assert len(cleaned) == 1
    assert cleaned[0]["location"] == "Johannesburg"

    # 3. Validation stage
    validated = ValidatedJob(**cleaned[0])
    assert validated.title == "Data Engineering Intern"

    # 4. Load stage (PostgreSQL insertion)
    DataLoader.load_jobs([validated.dict()])

    # 5. Verify via FastAPI endpoint
    response = client.get("/api/jobs?location=Johannesburg")
    assert response.status_code == 200
    jobs = response.json()
    assert any(j["title"] == "Data Engineering Intern" for j in jobs)