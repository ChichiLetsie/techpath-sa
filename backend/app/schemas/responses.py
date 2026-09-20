from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class SkillResponse(BaseModel):
    id: int
    name: str
    category: str

    class Config:
        from_attributes = True

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    employment_type: str
    experience_level: str
    qualification: Optional[str] = None
    url: Optional[str] = None
    source: str
    status: str
    skills: List[SkillResponse] = []

    class Config:
        from_attributes = True

class CourseResponse(BaseModel):
    id: int
    name: str
    provider: str
    technology: str
    level: str
    cost: float
    currency: str
    duration: Optional[str] = None
    delivery_mode: str
    url: Optional[str] = None
    source: str

    class Config:
        from_attributes = True

class OpportunityResponse(BaseModel):
    id: int
    title: str
    company: str
    type: str
    location: str
    description: str
    requirements: Optional[str] = None
    closing_date: Optional[datetime] = None
    url: Optional[str] = None
    source: str
    status: str
    skills: List[SkillResponse] = []

    class Config:
        from_attributes = True

class CareerResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    skills: List[SkillResponse] = []

    class Config:
        from_attributes = True