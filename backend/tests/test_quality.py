from datetime import datetime, timedelta
from pipeline.transform.quality import classify_opportunity_status, sanitize_missing_values

def test_opportunity_expiration_classifier():
    past_date = (datetime.utcnow() - timedelta(days=5)).isoformat()
    future_date = (datetime.utcnow() + timedelta(days=10)).isoformat()
    
    assert classify_opportunity_status(past_date) == "EXPIRED"
    assert classify_opportunity_status(future_date) == "ACTIVE"
    assert classify_opportunity_status(None) == "ACTIVE"

def test_sanitize_missing_values():
    raw_record = {"title": "Junior Developer", "company": "Absa"}
    sanitized = sanitize_missing_values(raw_record)
    
    assert sanitized["experience_level"] == "Entry-level / Junior"
    assert sanitized["qualification"] == "Not Specified"
    assert sanitized["location"] == "South Africa (Remote / National)"