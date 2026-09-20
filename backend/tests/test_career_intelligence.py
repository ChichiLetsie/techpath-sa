from app.services.career_intelligence import CareerIntelligenceService
from unittest.mock import MagicMock

def test_readiness_scoring_algorithm():
    # Mocking database session and query return
    mock_db = MagicMock()
    mock_career = MagicMock()
    
    sk1 = MagicMock()
    sk1.name = "Python"
    sk2 = MagicMock()
    sk2.name = "SQL"
    sk3 = MagicMock()
    sk3.name = "AWS"
    mock_career.skills = [sk1, sk2, sk3]
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_career

    result = CareerIntelligenceService.calculate_readiness(mock_db, "Data Engineer", ["Python", "SQL"])
    
    assert result["target_career"] == "Data Engineer"
    assert result["readiness_score_percentage"] == 66.7
    assert "Python" in result["matched_skills"]
    assert "AWS" in result["missing_skills"]
    assert len(result["your_next_move"]) > 0