import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scrapers.jobs.job_scraper import JobScraper
from scrapers.opportunities.opportunity_scraper import OpportunityScraper
from scrapers.courses.course_scraper import CourseScraper
from pipeline.transform.transformer import DataTransformer
from pipeline.validation.schemas import ValidatedJob, ValidatedOpportunity
from pipeline.load.loader import DataLoader

from scrapers.jobs.live_job_scraper import LiveJobScraper

def run_complete_pipeline():
    print("==================================================")
    print("🚀 Starting TechPath SA Data Engineering Pipeline")
    print("==================================================")

    # 1. EXTRACT (with per-source isolation)
    raw_jobs = []
    raw_opps = []
    raw_courses = []

    try:
        print("\n--- Phase 1: Extract ---")
        raw_jobs = LiveJobScraper().extract()
        #raw_jobs = JobScraper().extract()
        if not raw_jobs:
            # Fallback to secondary source if live API throttles
            raw_jobs = JobScraper().extract()
    except Exception as e:
        print(f"❌ Live job extraction failed, falling back: {e}")
        raw_jobs = JobScraper().extract()
        #print(f"❌ Job extraction failed (isolated): {e}")

    try:
        raw_opps = OpportunityScraper().extract()
    except Exception as e:
        print(f"❌ Opportunity extraction failed (isolated): {e}")

    try:
        raw_courses = CourseScraper().extract()
    except Exception as e:
        print(f"❌ Course extraction failed (isolated): {e}")

    # 2. TRANSFORM
    print("\n--- Phase 2: Transform ---")
    cleaned_jobs = DataTransformer.transform_jobs(raw_jobs) if raw_jobs else []
    cleaned_opps = DataTransformer.transform_opportunities(raw_opps) if raw_opps else []
    print(f"Cleaned {len(cleaned_jobs)} jobs and {len(cleaned_opps)} opportunities.")

    # 3. VALIDATE
    print("\n--- Phase 3: Validate ---")
    validated_jobs = []
    for j in cleaned_jobs:
        try:
            v_job = ValidatedJob(**j)
            validated_jobs.append(v_job.dict())
        except Exception as err:
            print(f"Validation error on job record: {err}")

    validated_opps = []
    for o in cleaned_opps:
        try:
            v_opp = ValidatedOpportunity(**o)
            validated_opps.append(v_opp.dict())
        except Exception as err:
            print(f"Validation error on opportunity record: {err}")

    print(f"Validated {len(validated_jobs)} jobs and {len(validated_opps)} opportunities successfully.")

    # 4. LOAD
    print("\n--- Phase 4: Load into PostgreSQL ---")
    if validated_jobs:
        DataLoader.load_jobs(validated_jobs)
    if validated_opps:
        DataLoader.load_opportunities(validated_opps)

    print("\n==================================================")
    print("✨ TechPath SA Pipeline Execution Complete")
    print("==================================================")

if __name__ == "__main__":
    run_complete_pipeline()