from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ValidatedJob(BaseModel):
    title: str
    company: str
    location: str
    description: str
    employment_type: str = "Full-time"
    experience_level: str = "Junior"
    qualification: Optional[str] = "Not Specified"
    url: Optional[str] = None
    date_posted: Optional[str] = None
    source: str
    skills: List[str] = []

class ValidatedOpportunity(BaseModel):
    title: str
    company: str
    type: str
    location: str
    description: str
    requirements: Optional[str] = None
    closing_date: Optional[str] = None
    url: Optional[str] = None
    source: str
    skills: List[str] = []