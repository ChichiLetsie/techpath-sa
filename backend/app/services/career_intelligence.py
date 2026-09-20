from sqlalchemy.orm import Session
from app.models import models

class CareerIntelligenceService:
    @staticmethod
    def calculate_readiness(db: Session, career_name: str, user_skills: list[str]):
        # Fetch target career from DB
        career = db.query(models.Career).filter(models.Career.name.ilike(career_name)).first()
        if not career:
            # Fallback definition if unseeded
            required_skills = {"Python", "SQL", "Git", "Linux", "AWS", "Docker", "Spark"}
        else:
            required_skills = {s.name for s in career.skills}

        user_skill_set = {s.strip().title() for s in user_skills}
        
        matched = user_skill_set.intersection(required_skills)
        missing = required_skills.difference(user_skill_set)
        
        total_required = len(required_skills) if required_skills else 1
        score = round((len(matched) / total_required) * 100, 1)

        # Generate "Your Next Move" actions
        next_moves = []
        if missing:
            next_move_skill = next(iter(missing))
            next_moves.append(f"Learn {next_move_skill} — frequently requested in analyzed South African tech roles.")
            next_moves.append(f"Complete a practical foundational course or project involving {next_move_skill}.")
        else:
            next_moves.append("You match all core required skills! Focus on building an end-to-end portfolio project.")
            
        next_moves.append("Apply for matching junior or graduate opportunities listed on TechPath SA.")

        return {
            "target_career": career_name,
            "readiness_score_percentage": score,
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing)),
            "your_next_move": next_moves
        }

    @staticmethod
    def match_opportunities(db: Session, user_skills: list[str]):
        user_skill_set = {s.strip().title() for s in user_skills}
        opportunities = db.query(models.Opportunity).all()
        
        matches = []
        for opp in opportunities:
            opp_skills = {s.name for s in opp.skills}
            if not opp_skills:
                match_percentage = 50.0  # Default general match if no specific tags
                matched = []
                missing = []
            else:
                matched = user_skill_set.intersection(opp_skills)
                missing = opp_skills.difference(user_skill_set)
                match_percentage = round((len(matched) / len(opp_skills)) * 100, 1)

            matches.append({
                "opportunity_id": opp.id,
                "title": opp.title,
                "company": opp.company,
                "type": opp.type,
                "location": opp.location,
                "match_percentage": match_percentage,
                "matched_skills": list(matched),
                "missing_skills": list(missing),
                "url": opp.url
            })
            
        # Sort by highest match percentage
        matches.sort(key=lambda x: x["match_percentage"], reverse=True)
        return matches