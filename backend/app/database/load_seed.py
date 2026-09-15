import json
import os
from datetime import datetime
from app.database.session import SessionLocal
from app.models import models

def load_json(filename):
    path = os.path.join("/app/data/seed", filename)
    if not os.path.exists(path):
        # fallback for local execution outside container if needed
        path = os.path.join("data/seed", filename)
    with open(path, "r") as f:
        return json.load(f)

def run_seed():
    db = SessionLocal()
    try:
        print("Starting seed data loading...")

        # 1. Skills
        skills_data = load_json("skills.json")
        skill_map = {}
        for s in skills_data:
            skill = db.query(models.Skill).filter_by(name=s["name"]).first()
            if not skill:
                skill = models.Skill(name=s["name"], category=s["category"])
                db.add(skill)
                db.commit()
                db.refresh(skill)
            skill_map[skill.name] = skill

        # 2. Jobs
        jobs_data = load_json("jobs.json")
        for j in jobs_data:
            existing = db.query(models.Job).filter_by(title=j["title"], company=j["company"]).first()
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
                for sk_name in j.get("skills", []):
                    if sk_name in skill_map:
                        job.skills.append(skill_map[sk_name])
                db.add(job)
                db.commit()

        # 3. Courses
        courses_data = load_json("courses.json")
        for c in courses_data:
            existing = db.query(models.Course).filter_by(name=c["name"], provider=c["provider"]).first()
            if not existing:
                course = models.Course(**c)
                db.add(course)
                db.commit()

        # 4. Opportunities
        opps_data = load_json("opportunities.json")
        for o in opps_data:
            existing = db.query(models.Opportunity).filter_by(title=o["title"], company=o["company"]).first()
            if not existing:
                closing = datetime.fromisoformat(o["closing_date"]) if o.get("closing_date") else None
                opp = models.Opportunity(
                    title=o["title"],
                    company=o["company"],
                    type=o["type"],
                    location=o["location"],
                    description=o["description"],
                    requirements=o["requirements"],
                    closing_date=closing,
                    url=o["url"],
                    source=o["source"]
                )
                for sk_name in o.get("skills", []):
                    if sk_name in skill_map:
                        opp.skills.append(skill_map[sk_name])
                db.add(opp)
                db.commit()

        # 5. Careers
        careers_data = load_json("careers.json")
        for car in careers_data:
            existing = db.query(models.Career).filter_by(name=car["name"]).first()
            if not existing:
                career = models.Career(name=car["name"], description=car["description"])
                for sk_info in car.get("skills", []):
                    sk_obj = skill_map.get(sk_info["name"])
                    if sk_obj:
                        career.skills.append(sk_obj)
                db.add(career)
                db.commit()

        print("Seed data loaded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error loading seed data: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()