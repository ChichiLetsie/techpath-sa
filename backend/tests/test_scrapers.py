from unittest.mock import patch
from scrapers.jobs.job_scraper import JobScraper
from scrapers.opportunities.opportunity_scraper import OpportunityScraper
from scrapers.courses.course_scraper import CourseScraper

@patch("scrapers.base.BaseScraper.fetch_page")
def test_job_scraper_extraction(mock_fetch):
    mock_fetch.return_value = "<html>Mocked HTML</html>"
    scraper = JobScraper()
    jobs = scraper.extract()
    assert isinstance(jobs, list)
    assert len(jobs) > 0
    assert jobs[0]["title"] == "Junior Data Engineer"

@patch("scrapers.base.BaseScraper.fetch_page")
def test_opportunity_scraper_extraction(mock_fetch):
    mock_fetch.return_value = "<html>Mocked HTML</html>"
    scraper = OpportunityScraper()
    opps = scraper.extract()
    assert isinstance(opps, list)
    assert len(opps) > 0
    assert opps[0]["type"] == "Learnership"

@patch("scrapers.base.BaseScraper.fetch_page")
def test_course_scraper_extraction(mock_fetch):
    mock_fetch.return_value = "<html>Mocked HTML</html>"
    scraper = CourseScraper()
    courses = scraper.extract()
    assert isinstance(courses, list)
    assert len(courses) > 0
    assert courses[0]["technology"] == "AWS"