# analyser/utils/linkedin_parser.py
import requests
from bs4 import BeautifulSoup

def parse_linkedin_job_posting(job_url):
    """
    Parses a LinkedIn job posting URL and extracts relevant details.
    """
    try:
        # Send a GET request to the job URL
        response = requests.get(job_url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract job title
        job_title = soup.find('h1', class_='top-card-layout__title').get_text(strip=True)

        # Extract company name
        company_name = soup.find('a', class_='topcard__org-name-link').get_text(strip=True)

        # Extract job location
        job_location = soup.find('span', class_='topcard__flavor--bullet').get_text(strip=True)

        # Extract job description
        job_description = soup.find('div', class_='show-more-less-html__markup').get_text(strip=True)

        # Return the extracted data
        return {
            'job_title': job_title,
            'company_name': company_name,
            'job_location': job_location,
            'job_description': job_description,
        }
    except Exception as e:
        print(f"Error parsing LinkedIn job posting: {e}")
        return None