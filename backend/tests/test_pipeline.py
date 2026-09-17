from pipeline.transform.transformer import DataTransformer
from pipeline.validation.schemas import ValidatedJob

def test_pipeline_validation_and_transformation():
    raw_input = [{
        "title": "Data Engineer",
        "company": "Absa Group",
        "location": "Johannesburg",
        "description": "ETL pipeline development",
        "source": "Test Source",
        "skills": ["Python", "Spark"]
    }]
    
    transformed = DataTransformer.transform_jobs(raw_input)
    assert len(transformed) == 1
    
    validated = ValidatedJob(**transformed[0])
    assert validated.title == "Data Engineer"
    assert "Python" in validated.skills