from pipeline.transform.skill_dictionary import extract_skills_from_text

def test_skill_extraction_with_boundaries():
    # Should match Python and AWS, but NOT substring matching issues
    text = "We are looking for a developer experienced in Python 3 and Amazon Web Services. Knowledge of Javascript is a bonus."
    skills = extract_skills_from_text(text)
    
    assert "Python" in skills
    assert "AWS" in skills
    assert "JavaScript" in skills