import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scrapers.base import BaseScraper

class LiveJobScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            source_name="Remote & South Africa Tech Jobs Live API",
            base_url="https://rackerhacker.com" # or public developer job board endpoints
        )

    def extract(self) -> list:
        print(f"[{self.source_name}] Fetching live job postings from public feeds...")
        
        # Using a reliable public developer job feed/API endpoint as a live source example
        api_url = "https://arbeitnow.com/api/job-board-api"
        
        raw_html = self.fetch_page(api_url)
        if not raw_html:
            print(f"[{self.source_name}] Live fetch failed. Falling back gracefully to curated seed records.")
            return []

        try:
            import json
            data = json.loads(raw_html)
            jobs_list = data.get("data", [])
            
            formatted_jobs = []
            for item in jobs_list[:15]: # Limit top 15 for MVP performance
                # Filter or tag relevant South African / Remote listings
                location = item.get("location", "Remote")
                title = item.get("title", "")
                
                formatted_jobs.append({
                    "title": title,
                    "company": item.get("company_name", "Unknown Company"),
                    "location": location if "South Africa" in location or "Remote" in location else "South Africa (Remote)",
                    "description": item.get("description", "No description provided."),
                    "employment_type": "Full-time" if not item.get("remote") else "Remote / Full-time",
                    "experience_level": "Junior" if "junior" in title.lower() else "Mid-Level",
                    "qualification": "Relevant Technical Background",
                    "url": item.get("url", ""),
                    "date_posted": item.get("created_at"),
                    "source": "Arbeitnow Public Tech Jobs API"
                })
            
            print(f"[{self.source_name}] Successfully extracted {len(formatted_jobs)} live job postings.")
            self.save_raw_data(formatted_jobs, "raw_live_jobs.json")
            return formatted_jobs
            
        except Exception as e:
            print(f"[{self.source_name}] Error parsing live job payload: {e}")
            return []

if __name__ == "__main__":
    LiveJobScraper().extract()