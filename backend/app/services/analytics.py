from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import models

class SkillAnalyticsService:
    @staticmethod
    def get_top_skills(db: Session, limit: int = 10):
        total_jobs = db.query(models.Job).count()
        if total_jobs == 0:
            return []

        results = (
            db.query(
                models.Skill.name,
                models.Skill.category,
                func.count(models.job_skills.c.job_id).label("job_count")
            )
            .join(models.job_skills, models.Skill.id == models.job_skills.c.skill_id)
            .group_by(models.Skill.id, models.Skill.name, models.Skill.category)
            .order_by(func.count(models.job_skills.c.job_id).desc())
            .limit(limit)
            .all()
        )

        analytics = []
        for r in results:
            percentage = round((r.job_count / total_jobs) * 100, 1)
            analytics.append({
                "skill": r.name,
                "category": r.category,
                "job_count": r.job_count,
                "total_analyzed_jobs": total_jobs,
                "demand_percentage": percentage
            })
        return analytics

    @staticmethod
    def get_skills_by_location(db: Session, location: str):
        results = (
            db.query(models.Skill.name, func.count(models.job_skills.c.job_id).label("count"))
            .join(models.job_skills, models.Skill.id == models.job_skills.c.skill_id)
            .join(models.Job, models.Job.id == models.job_skills.c.job_id)
            .filter(models.Job.location.ilike(f"%{location}%"))
            .group_by(models.Skill.name)
            .order_by(func.count(models.job_skills.c.job_id).desc())
            .all()
        )
        return [{"skill": r.name, "job_count": r.count} for r in results]