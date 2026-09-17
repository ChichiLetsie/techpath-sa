import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database.session import SessionLocal
from app.models import models

class DataLoader:
    @staticmethod
    def load_jobs(cleaned_jobs: list):
        db = SessionLocal()
        loaded_count = 0
        try:
            for j in cleaned_jobs:
                # Check for existing record to prevent duplicates
                existing = db.query(models.Job).filter_by(
                    title=j["title"], 
                    company=j["company"], 
                    location=j["location"]
                ).first()
                
                if not existing:
                    job = models.Job(
                        title=j["title"],
                        company=j["company"],
                        location=j["location"],
                        description=j["description"],
                        employment_type=j["employment_type"],
                        experience_level=j["experience_level"],
                        qualification=j["qualification"],
                        url=j["url"],
                        source=j["source"]
                    )
                    
                    # Map skills
                    for skill_name in j.get("skills", []):
                        skill = db.query(models.Skill).filter_by(name=skill_name).first()
                        if not skill:
                            # Auto-create skill if missing in dictionary
                            skill = models.Skill(name=skill_name, category="General Tech")
                            db.add(skill)
                            db.commit()
                            db.refresh(skill)
                        job.skills.append(skill)

                    db.add(job)
                    db.commit()
                    loaded_count += 1
            print(f"[DataLoader] Successfully loaded {loaded_count} new job records into PostgreSQL.")
        except Exception as e:
            db.rollback()
            print(f"[DataLoader] Error loading jobs: {e}")
        finally:
            db.close()

    @staticmethod
    def load_opportunities(cleaned_opps: list):
        db = SessionLocal()
        loaded_count = 0
        try:
            for o in cleaned_opps:
                existing = db.query(models.Opportunity).filter_by(
                    title=o["title"], 
                    company=o["company"]
                ).first()
                
                if not existing:
                    opp = models.Opportunity(
                        title=o["title"],
                        company=o["company"],
                        type=o["type"],
                        location=o["location"],
                        description=o["description"],
                        requirements=o["requirements"],
                        url=o["url"],
                        source=o["source"]
                    )
                    for skill_name in o.get("skills", []):
                        skill = db.query(models.Skill).filter_by(name=skill_name).first()
                        if skill:
                            opp.skills.append(skill)

                    db.add(opp)
                    db.commit()
                    loaded_count += 1
            print(f"[DataLoader] Successfully loaded {loaded_count} new opportunity records into PostgreSQL.")
        except Exception as e:
            db.rollback()
            print(f"[DataLoader] Error loading opportunities: {e}")
        finally:
            db.close()