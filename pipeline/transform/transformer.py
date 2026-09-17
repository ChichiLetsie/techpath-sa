import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pipeline.transform.skills import normalise_skill, normalise_location, normalise_company

class DataTransformer:
    @staticmethod
    def transform_jobs(raw_jobs: list) -> list:
        cleaned_jobs = []
        seen = set()

        for job in raw_jobs:
            title = job.get("title", "").strip()
            company = normalise_company(job.get("company", ""))
            location = normalise_location(job.get("location", ""))
            
            # Deduplication key based on title + company + location
            dedup_key = (title.lower(), company.lower(), location.lower())
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            transformed_job = {
                "title": title,
                "company": company,
                "location": location,
                "description": job.get("description", "").strip(),
                "employment_type": job.get("employment_type", "Full-time").strip(),
                "experience_level": job.get("experience_level", "Junior").strip(),
                "qualification": job.get("qualification", "Not Specified").strip(),
                "url": job.get("url", ""),
                "date_posted": job.get("date_posted"),
                "source": job.get("source", "Unknown"),
                "skills": [normalise_skill(s) for s in job.get("skills", [])]
            }
            cleaned_jobs.append(transformed_job)

        return cleaned_jobs

    @staticmethod
    def transform_opportunities(raw_opps: list) -> list:
        cleaned_opps = []
        seen = set()

        for opp in raw_opps:
            title = opp.get("title", "").strip()
            company = normalise_company(opp.get("company", ""))
            
            dedup_key = (title.lower(), company.lower())
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            transformed_opp = {
                "title": title,
                "company": company,
                "type": opp.get("type", "Learnership").strip(),
                "location": normalise_location(opp.get("location", "")),
                "description": opp.get("description", "").strip(),
                "requirements": opp.get("requirements", "").strip(),
                "closing_date": opp.get("closing_date"),
                "url": opp.get("url", ""),
                "source": opp.get("source", "Unknown"),
                "skills": [normalise_skill(s) for s in opp.get("skills", [])]
            }
            cleaned_opps.append(transformed_opp)

        return cleaned_opps