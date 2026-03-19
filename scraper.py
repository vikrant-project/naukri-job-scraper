"""Naukri.com Job Scraper
Scrapes job listings from Naukri.com using Selenium and BeautifulSoup
Author: Vikrant Rana
"""

import time
import random
import hashlib
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
from database import JobDatabase

# List of user agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
]

class NaukriScraper:
    """Scraper class for Naukri.com job listings"""
    
    def __init__(self, headless: bool = True):
        """Initialize the scraper with Chrome options
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.db = JobDatabase()
        self.driver = None
    
    def get_driver(self):
        """Create and configure Chrome WebDriver with anti-detection measures"""
        chrome_options = Options()
        
        # Random user agent
        user_agent = random.choice(USER_AGENTS)
        chrome_options.add_argument(f'user-agent={user_agent}')
        
        # Headless mode
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        # Anti-detection options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # Remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def random_delay(self, min_seconds: float = 2.0, max_seconds: float = 5.0):
        """Add random delay between requests
        
        Args:
            min_seconds: Minimum delay in seconds
            max_seconds: Maximum delay in seconds
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def generate_job_id(self, title: str, company: str) -> str:
        """Generate unique job ID from title and company
        
        Args:
            title: Job title
            company: Company name
            
        Returns:
            MD5 hash as job ID
        """
        unique_string = f"{title}_{company}".lower().strip()
        return hashlib.md5(unique_string.encode()).hexdigest()[:16]
    
    def build_search_url(self, keyword: str, location: str = '', 
                        experience: str = '') -> str:
        """Build Naukri search URL with parameters
        
        Args:
            keyword: Job search keyword
            location: Location filter
            experience: Experience level filter
            
        Returns:
            Complete search URL
        """
        base_url = 'https://www.naukri.com/'
        keyword_encoded = keyword.replace(' ', '-').lower()
        
        url = f'{base_url}{keyword_encoded}-jobs'
        
        params = []
        if location:
            location_encoded = location.replace(' ', '-').lower()
            url += f'-in-{location_encoded}'
        
        # Experience parameters (example: fresher, 0-3 years, etc.)
        if experience and 'fresher' in experience.lower():
            params.append('experience=0')
        elif experience:
            # Parse experience range if provided
            pass
        
        if params:
            url += '?' + '&'.join(params)
        
        return url
    
    def extract_job_data(self, job_element) -> Dict:
        """Extract job data from a job card element
        
        Args:
            job_element: BeautifulSoup job element
            
        Returns:
            Dictionary with job information
        """
        job_data = {
            'title': '',
            'company': '',
            'location': '',
            'salary': 'Not disclosed',
            'experience': '',
            'skills': '',
            'description': '',
            'job_url': ''
        }
        
        try:
            # Job title
            title_elem = job_element.find('a', class_='title')
            if not title_elem:
                title_elem = job_element.find('a', {'class': lambda x: x and 'title' in x})
            if title_elem:
                job_data['title'] = title_elem.get_text(strip=True)
                job_data['job_url'] = title_elem.get('href', '')
            
            # Company name
            company_elem = job_element.find('a', class_='comp-name')
            if not company_elem:
                company_elem = job_element.find('a', {'class': lambda x: x and 'comp' in str(x).lower()})
            if company_elem:
                job_data['company'] = company_elem.get_text(strip=True)
            
            # Experience
            exp_elem = job_element.find('span', class_='exp')
            if not exp_elem:
                exp_elem = job_element.find('span', {'class': lambda x: x and 'exp' in str(x).lower()})
            if exp_elem:
                job_data['experience'] = exp_elem.get_text(strip=True)
            
            # Salary
            salary_elem = job_element.find('span', class_='sal')
            if not salary_elem:
                salary_elem = job_element.find('span', {'class': lambda x: x and 'sal' in str(x).lower()})
            if salary_elem:
                job_data['salary'] = salary_elem.get_text(strip=True)
            
            # Location
            loc_elem = job_element.find('span', class_='loc')
            if not loc_elem:
                loc_elem = job_element.find('span', {'class': lambda x: x and 'loc' in str(x).lower()})
            if loc_elem:
                job_data['location'] = loc_elem.get_text(strip=True)
            
            # Skills
            skills_elem = job_element.find('ul', class_='tags')
            if skills_elem:
                skills = [li.get_text(strip=True) for li in skills_elem.find_all('li')]
                job_data['skills'] = ', '.join(skills)
            
            # Job description snippet
            desc_elem = job_element.find('div', class_='job-desc')
            if desc_elem:
                job_data['description'] = desc_elem.get_text(strip=True)[:500]
            
            # Generate unique job ID
            job_data['job_id'] = self.generate_job_id(
                job_data['title'], 
                job_data['company']
            )
            
        except Exception as e:
            print(f"Error extracting job data: {e}")
        
        return job_data
    
    def scrape_jobs(self, keyword: str, location: str = '', 
                   experience: str = '', max_pages: int = 3) -> Dict:
        """Scrape jobs from Naukri.com
        
        Args:
            keyword: Search keyword
            location: Location filter
            experience: Experience filter
            max_pages: Maximum number of pages to scrape
            
        Returns:
            Dictionary with scraping results
        """
        print(f"Starting scrape: {keyword} in {location or 'All India'}")
        
        results = {
            'jobs_found': 0,
            'jobs_saved': 0,
            'duplicates_skipped': 0,
            'status': 'in_progress'
        }
        
        try:
            # Initialize driver
            self.driver = self.get_driver()
            
            # Build search URL
            search_url = self.build_search_url(keyword, location, experience)
            print(f"Search URL: {search_url}")
            
            # Load the page
            self.driver.get(search_url)
            self.random_delay(3, 6)
            
            # Check for CAPTCHA or blocks
            page_source = self.driver.page_source
            if 'captcha' in page_source.lower() or 'blocked' in page_source.lower():
                print("WARNING: Possible CAPTCHA or blocking detected")
                results['status'] = 'captcha_detected'
                return results
            
            # Scrape multiple pages
            for page in range(max_pages):
                print(f"Scraping page {page + 1}...")
                
                # Get page source and parse with BeautifulSoup
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find job cards (Naukri uses various class names)
                job_cards = soup.find_all('article', class_='jobTuple')
                if not job_cards:
                    job_cards = soup.find_all('div', {'class': lambda x: x and 'job' in str(x).lower() and 'tuple' in str(x).lower()})
                
                print(f"Found {len(job_cards)} job cards on page {page + 1}")
                
                if not job_cards:
                    print("No job cards found, stopping...")
                    break
                
                # Extract and save jobs
                for job_card in job_cards:
                    job_data = self.extract_job_data(job_card)
                    
                    if job_data['title'] and job_data['company']:
                        results['jobs_found'] += 1
                        
                        # Save to database
                        if self.db.insert_job(job_data):
                            results['jobs_saved'] += 1
                            print(f"Saved: {job_data['title']} at {job_data['company']}")
                        else:
                            results['duplicates_skipped'] += 1
                            print(f"Duplicate: {job_data['title']} at {job_data['company']}")
                
                # Try to go to next page
                if page < max_pages - 1:
                    try:
                        # Look for next button
                        next_button = self.driver.find_element(By.CLASS_NAME, 'fright')
                        next_button.click()
                        self.random_delay(3, 6)
                    except Exception as e:
                        print(f"Could not navigate to next page: {e}")
                        break
            
            results['status'] = 'completed'
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            results['status'] = 'error'
            results['error'] = str(e)
        
        finally:
            # Close driver
            if self.driver:
                self.driver.quit()
        
        # Save scraping history
        self.db.add_scraping_history(
            keyword=keyword,
            location=location,
            experience=experience,
            jobs_found=results['jobs_found'],
            status=results['status']
        )
        
        print(f"Scraping completed: {results['jobs_saved']} jobs saved, {results['duplicates_skipped']} duplicates skipped")
        return results

if __name__ == '__main__':
    # Test the scraper
    scraper = NaukriScraper(headless=True)
    results = scraper.scrape_jobs(
        keyword='Python Developer',
        location='Delhi',
        experience='Fresher',
        max_pages=2
    )
    print(results)
