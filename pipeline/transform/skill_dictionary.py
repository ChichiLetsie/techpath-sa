import re

CONTROLLED_SKILLS = {
    "Python": {"category": "Programming", "aliases": ["python 3", "python programming"]},
    "Java": {"category": "Programming", "aliases": ["java se", "java enterprise"]},
    "JavaScript": {"category": "Programming", "aliases": ["js", "ecmascript"]},
    "SQL": {"category": "Data", "aliases": ["sql server", "tsql", "plsql"]},
    "PostgreSQL": {"category": "Data", "aliases": ["postgres", "postgresql"]},
    "AWS": {"category": "Cloud", "aliases": ["amazon web services", "aws cloud"]},
    "Docker": {"category": "DevOps", "aliases": ["docker containerisation", "docker containers"]},
    "Git": {"category": "DevOps", "aliases": ["github", "gitlab", "git/github"]},
    "Spark": {"category": "Data", "aliases": ["apache spark", "pyspark"]},
    "Linux": {"category": "DevOps", "aliases": ["ubuntu", "debian", "redhat"]}
}

def extract_skills_from_text(text: str) -> list:
    """Scans text using regex word boundaries to prevent substring mismatches."""
    if not text:
        return []
    
    found_skills = set()
    text_lower = text.lower()

    for canonical_name, info in CONTROLLED_SKILLS.items():
        # Check canonical name
        pattern = r'\b' + re.escape(canonical_name.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(canonical_name)
            continue
            
        # Check aliases
        for alias in info["aliases"]:
            alias_pattern = r'\b' + re.escape(alias.lower()) + r'\b'
            if re.search(alias_pattern, text_lower):
                found_skills.add(canonical_name)
                break

    return list(found_skills)