import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scrapers.base import BaseScraper

class OpportunityScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="SA Learnerships & Graduate Portals")

    def extract(self) -> list:
        print(f"[{self.source_name}] Starting extraction of opportunities...")
        
        raw_opportunities = [
            {
                "title": "Systems Development Learnership NQF 5",
                "company": "WeThinkCode_",
                "type": "Learnership",
                "location": "Cape Town / Johannesburg",
                "description": "A 12-month intensive coding and software engineering learnership.",
                "requirements": "South African citizen, 18-35 years old, Matric with Maths.",
                "closing_date": "2026-11-30T23:59:59",
                "url": "https://example.com/opps/wethinkcode",
                "source": "WeThinkCode_ Portal"
            }
        ]

        self.save_raw_data(raw_opportunities, "raw_opportunities.json")
        return raw_opportunities

if __name__ == "__main__":
    scraper = OpportunityScraper()
    scraper.extract()