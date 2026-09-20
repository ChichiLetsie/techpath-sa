from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models import models
from app.services.analytics import SkillAnalyticsService
from app.schemas.responses import JobResponse, CourseResponse, OpportunityResponse, CareerResponse, SkillResponse

router = APIRouter(prefix="/api", tags=["TechPath SA Career Intelligence"])

@router.get("/jobs", response_model=List[JobResponse], summary="List and filter job postings")
def get_jobs(
    skill: Optional[str] = None,
    location: Optional[str] = None,
    experience: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.Job)
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    if experience:
        query = query.filter(models.Job.experience_level.ilike(f"%{experience}%"))
    if skill:
        query = query.join(models.Job.skills).filter(models.Skill.name.ilike(f"%{skill}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/jobs/{job_id}", response_model=JobResponse, summary="Get job details by ID")
def get_job_detail(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return job

@router.get("/skills", response_model=List[SkillResponse], summary="List all technical skills")
def get_skills(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Skill).offset(skip).limit(limit).all()

@router.get("/skills/top", summary="Get top demanded skills with percentages")
def get_top_skills(limit: int = 10, db: Session = Depends(get_db)):
    return SkillAnalyticsService.get_top_skills(db, limit=limit)

@router.get("/skills/{skill_name}", summary="Get specific skill detail and related jobs")
def get_skill_detail(skill_name: str, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.name.ilike(skill_name)).first()
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")
    return {
        "skill": skill.name,
        "category": skill.category,
        "job_count": len(skill.jobs),
        "jobs": [{"id": j.id, "title": j.title, "company": j.company} for j in skill.jobs]
    }

@router.get("/courses", response_model=List[CourseResponse], summary="List courses and training providers")
def get_courses(technology: Optional[str] = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    query = db.query(models.Course)
    if technology:
        query = query.filter(models.Course.technology.ilike(f"%{technology}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/certifications", summary="List professional certifications")
def get_certifications(technology: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Certification)
    if technology:
        query = query.filter(models.Certification.technology.ilike(f"%{technology}%"))
    return query.all()

@router.get("/opportunities", response_model=List[OpportunityResponse], summary="List career opportunities (Internships/Learnerships/Grad programs)")
def get_opportunities(
    type: Optional[str] = None, 
    closing_soon: bool = False, 
    skip: int = 0, 
    limit: int = 20, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Opportunity)
    if type:
        query = query.filter(models.Opportunity.type.ilike(f"%{type}%"))
    if closing_soon:
        threshold = datetime.utcnow() + timedelta(days=30)
        query = query.filter(models.Opportunity.closing_date <= threshold, models.Opportunity.closing_date >= datetime.utcnow())
    return query.offset(skip).limit(limit).all()

@router.get("/careers", response_model=List[CareerResponse], summary="List target tech career paths")
def get_careers(db: Session = Depends(get_db)):
    return db.query(models.Career).all()

@router.get("/analytics/skills", summary="Skill demand analytics by location")
def get_analytics_skills(location: Optional[str] = None, db: Session = Depends(get_db)):
    if location:
        return SkillAnalyticsService.get_skills_by_location(db, location)
    return SkillAnalyticsService.get_top_skills(db, limit=20)

@router.get("/analytics/trends", summary="Skill demand trend analysis")
def get_analytics_trends():
    return {
        "status": "insufficient_historical_data",
        "message": "Trend analysis requires additional historical accumulation over time. Data collection active."
    }

@router.get("/recommendations", summary="Career readiness & next move recommendations")
def get_recommendations(career_name: str = "Data Engineer", user_skills: str = "Python,SQL"):
    user_skill_set = {s.strip().title() for s in user_skills.split(",")}
    career_requirements = {"Python", "SQL", "Git", "Linux", "AWS", "Docker", "Spark"}
    
    matched = user_skill_set.intersection(career_requirements)
    missing = career_requirements.difference(user_skill_set)
    score = round((len(matched) / len(career_requirements)) * 100, 1)

    return {
        "target_career": career_name,
        "readiness_score_percentage": score,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "your_next_move": [
            f"Complete a practical course in {next(iter(missing))}" if missing else "You match all core requirements! Apply for junior roles.",
            "Build an end-to-end portfolio project showcasing these tools.",
            "Review active South African graduate opportunities matching your profile."
        ]
    }