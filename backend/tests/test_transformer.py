from pipeline.transform.skills import normalise_skill, normalise_location
from pipeline.transform.transformer import DataTransformer

def test_skill_normalisation():
    assert normalise_skill("Amazon Web Services") == "AWS"
    assert normalise_skill("python 3") == "Python"
    assert normalise_skill("Postgresql") == "PostgreSQL"

def test_location_normalisation():
    assert normalise_location("cape town cbd") == "Cape Town"
    assert normalise_location("johannesburg, south africa") == "Johannesburg"

def test_job_deduplication():
    raw_jobs = [
        {"title": "Junior Data Engineer", "company": "Capitec", "location": "Cape Town", "skills": ["Aws Cloud"]},
        {"title": "Junior Data Engineer", "company": "Capitec", "location": "Cape Town", "skills": ["AWS"]} # Duplicate
    ]
    transformed = DataTransformer.transform_jobs(raw_jobs)
    assert len(transformed) == 1
    assert transformed[0]["skills"][0] == "AWS"