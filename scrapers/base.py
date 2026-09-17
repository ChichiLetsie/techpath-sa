import json
import os
import time
from datetime import datetime
from urllib.parse import urlparse
from urllib import robotparser
import httpx

class BaseScraper:
    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.headers = {
            "User-Agent": "TechPathSA-Bot/1.0 (+https://github.com/techpath-sa; Educational Career Intelligence Platform)"
        }
        self.delay = 1.5  # Polite delay between requests

    def check_robots(self, target_url: str) -> bool:
        """Parses robots.txt to ensure scraping is permitted."""
        try:
            parsed = urlparse(target_url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            rp = robotparser.RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            allowed = rp.can_fetch(self.headers["User-Agent"], target_url)
            return allowed
        except Exception:
            # If robots.txt cannot be reached, default to cautious allowance or fallback datasets
            return True

    def fetch_page(self, url: str) -> str | None:
        """Fetches a page politely with rate limiting and safety checks."""
        if not self.check_robots(url):
            print(f"[{self.source_name}] Blocked by robots.txt: {url}")
            return None

        try:
            time.sleep(self.delay)
            with httpx.Client(headers=self.headers, timeout=15.0, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"[{self.source_name}] Network error fetching {url}: {e}")
            return None

    def save_raw_data(self, data: list | dict, filename: str):
        """Persists raw extracted artifacts with source metadata."""
        os.makedirs("data/raw", exist_ok=True)
        filepath = os.path.join("data/raw", filename)
        
        payload = {
            "source": self.source_name,
            "scraped_at": datetime.utcnow().isoformat(),
            "record_count": len(data) if isinstance(data, list) else 1,
            "data": data
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"[{self.source_name}] Successfully saved raw payload to {filepath}")