import re

def normalise_skill(raw_skill: str) -> str:
    """Standardises skill names into clean, controlled dictionary terms."""
    if not raw_skill:
        return "Unknown"
    
    cleaned = raw_skill.strip().title()
    
    mapping = {
        "Python 3": "Python",
        "Python Programming": "Python",
        "Aws": "AWS",
        "Amazon Web Services": "AWS",
        "Aws Cloud": "AWS",
        "Javascript": "JavaScript",
        "Postgresql": "PostgreSQL",
        "Postgres": "PostgreSQL",
        "Git/Github": "Git",
        "Github": "Git",
        "Docker Containerisation": "Docker",
        "Apache Spark": "Spark",
        "Sql": "SQL"
    }
    
    return mapping.get(cleaned, cleaned)

def normalise_location(raw_location: str) -> str:
    """Standardises South African locations into primary metros / remote options."""
    if not raw_location:
        return "South Africa (Remote)"
    
    loc = raw_location.lower()
    if "cape town" in loc:
        return "Cape Town"
    elif "johannesburg" in loc or "joburg" in loc:
        return "Johannesburg"
    elif "pretoria" in loc or "tshwane" in loc:
        return "Pretoria"
    elif "durban" in loc:
        return "Durban"
    elif "stellenbosch" in loc:
        return "Stellenbosch"
    elif "remote" in loc:
        return "Remote / South Africa"
    
    return raw_location.strip().title()

def normalise_company(raw_company: str) -> str:
    """Cleans company naming artifacts."""
    if not raw_company:
        return "Unknown Company"
    return raw_company.replace("(Pty) Ltd", "").replace("Limited", "").strip()