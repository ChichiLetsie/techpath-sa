from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

# Association tables for Many-to-Many relationships
job_skills = Table(
    'job_skills',
    Base.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id', ondelete="CASCADE"), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id', ondelete="CASCADE"), primary_key=True)
)

opportunity_skills = Table(
    'opportunity_skills',
    Base.metadata,
    Column('opportunity_id', Integer, ForeignKey('opportunities.id', ondelete="CASCADE"), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id', ondelete="CASCADE"), primary_key=True)
)

career_skills = Table(
    'career_skills',
    Base.metadata,
    Column('career_id', Integer, ForeignKey('careers.id', ondelete="CASCADE"), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id', ondelete="CASCADE"), primary_key=True),
    Column('importance', String(50), default="Required")
)

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    employment_type = Column(String(50), default="Full-time")
    experience_level = Column(String(50), default="Entry-level")
    qualification = Column(String(255), nullable=True)
    url = Column(String(500), nullable=True)
    date_posted = Column(DateTime, nullable=True)
    date_scraped = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100), nullable=False)
    status = Column(String(20), default="ACTIVE")

    skills = relationship("Skill", secondary=job_skills, back_populates="jobs")

class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False) # e.g., Programming, Data, Cloud

    jobs = relationship("Job", secondary=job_skills, back_populates="skills")
    opportunities = relationship("Opportunity", secondary=opportunity_skills, back_populates="skills")
    careers = relationship("Career", secondary=career_skills, back_populates="skills")

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(150), nullable=False)
    technology = Column(String(100), nullable=False)
    level = Column(String(50), default="Beginner")
    cost = Column(Float, default=0.0)
    currency = Column(String(10), default="ZAR")
    duration = Column(String(50), nullable=True)
    delivery_mode = Column(String(50), default="Online")
    url = Column(String(500), nullable=True)
    source = Column(String(100), nullable=False)
    date_scraped = Column(DateTime, default=datetime.utcnow)

class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    provider = Column(String(150), nullable=False)
    technology = Column(String(100), nullable=False)
    level = Column(String(50), default="Associate")
    cost = Column(Float, nullable=True)
    url = Column(String(500), nullable=True)
    source = Column(String(100), nullable=False)

class Opportunity(Base):
    __tablename__ = 'opportunities'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False) # Internship, Learnership, Graduate Programme
    location = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    closing_date = Column(DateTime, nullable=True)
    url = Column(String(500), nullable=True)
    source = Column(String(100), nullable=False)
    date_scraped = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="ACTIVE")

    skills = relationship("Skill", secondary=opportunity_skills, back_populates="opportunities")

class Career(Base):
    __tablename__ = 'careers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    skills = relationship("Skill", secondary=career_skills, back_populates="careers")