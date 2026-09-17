import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scrapers.base import BaseScraper

class CourseScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="SA & Global Training Providers")

    def extract(self) -> list:
        print(f"[{self.source_name}] Starting extraction of courses & certifications...")
        
        raw_courses = [
            {
                "name": "AWS Certified Cloud Practitioner",
                "provider": "Amazon Web Services",
                "technology": "AWS",
                "level": "Beginner",
                "cost": 1600.0,
                "currency": "ZAR",
                "duration": "4 weeks",
                "delivery_mode": "Online",
                "url": "https://example.com/courses/aws",
                "source": "AWS Training"
            }
        ]

        self.save_raw_data(raw_courses, "raw_courses.json")
        return raw_courses

if __name__ == "__main__":
    scraper = CourseScraper()
    scraper.extract()