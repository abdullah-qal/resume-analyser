import logging
from typing import Optional

import requests
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _first_text(soup, selectors: list[tuple[str, dict]], default: str = "") -> str:
    for tag, attrs in selectors:
        el = soup.find(tag, attrs=attrs)
        if el and el.get_text(strip=True):
            return el.get_text(strip=True)
    return default


def parse_linkedin_job_posting(job_url: str) -> Optional[dict]:
    """
    Parses a LinkedIn job posting URL and extracts relevant details.

    Uses defensive selectors and headers to reduce failures when LinkedIn tweaks markup.
    """
    try:
        response = requests.get(job_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as exc:
        LOGGER.warning("Failed to fetch LinkedIn job posting: %s", exc)
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    job_title = _first_text(
        soup,
        [
            ("h1", {"class": "top-card-layout__title"}),
            ("h1", {"class": "t-24"}),
            ("h1", {}),
        ],
        default="Unknown title",
    )
    company_name = _first_text(
        soup,
        [
            ("a", {"class": "topcard__org-name-link"}),
            ("span", {"class": "topcard__flavor"}),
            ("a", {"data-tracking-control-name": "public_jobs_topcard-org-name"}),
        ],
        default="Unknown company",
    )
    job_location = _first_text(
        soup,
        [
            ("span", {"class": "topcard__flavor--bullet"}),
            ("span", {"class": "topcard__flavor"}),
        ],
        default="Unknown location",
    )
    job_description = _first_text(
        soup,
        [
            ("div", {"class": "show-more-less-html__markup"}),
            ("section", {"class": "description"}),
            ("div", {"id": "job-details"}),
        ],
        default="",
    )

    if not job_description:
        LOGGER.warning("LinkedIn job description not found for %s", job_url)
        return None

    return {
        "job_title": job_title,
        "company_name": company_name,
        "job_location": job_location,
        "job_description": job_description,
    }
