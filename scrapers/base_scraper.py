import json
import os
from datetime import datetime
import httpx

class BaseScraper:
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.headers = {
            "User-Agent": "TechPathSA-Bot/1.0 (Educational Career Intelligence Platform; South Africa)"
        }

    def fetch_url(self, url: str) -> str | None:
        try:
            with httpx.Client(headers=self.headers, timeout=10.0, follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"[{self.source_name}] Error fetching {url}: {e}")
            return None

    def save_raw_data(self, data: list | dict, filename: str):
        raw_dir = "data/raw"
        os.makedirs(raw_dir, exist_ok=True)
        filepath = os.path.join(raw_dir, filename)
        
        payload = {
            "source": self.source_name,
            "scraped_at": datetime.utcnow().isoformat(),
            "data": data
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"[{self.source_name}] Saved raw data to {filepath}")