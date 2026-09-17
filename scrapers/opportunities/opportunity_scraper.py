import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scrapers.base import BaseScraper

class OpportunityScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            source_name="SA Learnership & Early Career Portals (Prosple ZA)",
            base_url="https://za.prosple.com"
        )

    def extract(self) -> list:
        print(f"[{self.source_name}] Initiating opportunity extraction...")
        
        raw_opportunities = [
            {
                "title": "Systems Development Learnership NQF 5",
                "company": "WeThinkCode_",
                "type": "Learnership",
                "location": "Cape Town / Johannesburg",
                "description": "Intensive 12-month tech learnership sponsored by industry partners.",
                "requirements": "South African citizen, ages 18-35, Matric with core Mathematics.",
                "closing_date": "2026-11-30T23:59:59",
                "url": "https://za.prosple.com/wethinkcode-learnership",
                "source": "Prosple ZA / Curated Seed"
            }
        ]

        self.save_raw_data(raw_opportunities, "raw_opportunities.json")
        return raw_opportunities

if __name__ == "__main__":
    OpportunityScraper().extract()