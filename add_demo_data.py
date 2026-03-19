"""Add demo data to database for testing dashboard
This script adds sample job listings to test the UI without running the scraper
Author: Vikrant Rana
"""

from database import JobDatabase
import hashlib
from datetime import datetime, timedelta
import random

def generate_job_id(title, company):
    """Generate unique job ID"""
    unique_string = f"{title}_{company}".lower().strip()
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]

def add_demo_jobs():
    """Add demo job listings to database"""
    db = JobDatabase()
    
    demo_jobs = [
        {
            'title': 'Python Developer',
            'company': 'Tech Solutions Pvt Ltd',
            'location': 'Delhi, India',
            'salary': '3-6 Lakh per annum',
            'experience': 'Fresher - 2 years',
            'skills': 'Python, Django, REST API, PostgreSQL, Git',
            'description': 'Looking for a passionate Python developer to join our team. Work on exciting projects with latest technologies.',
            'job_url': 'https://www.naukri.com/job-listings-python-developer'
        },
        {
            'title': 'Full Stack Developer',
            'company': 'Digital Innovations Ltd',
            'location': 'Noida, India',
            'salary': '5-8 Lakh per annum',
            'experience': '1-3 years',
            'skills': 'React, Node.js, MongoDB, Express, JavaScript',
            'description': 'Seeking a full stack developer with experience in MERN stack to build scalable web applications.',
            'job_url': 'https://www.naukri.com/job-listings-full-stack-developer'
        },
        {
            'title': 'Data Analyst',
            'company': 'Analytics Pro Solutions',
            'location': 'Gurgaon, India',
            'salary': '4-7 Lakh per annum',
            'experience': '0-2 years',
            'skills': 'Python, Pandas, SQL, Excel, Data Visualization',
            'description': 'Join our data analytics team to work on business intelligence and data-driven decision making.',
            'job_url': 'https://www.naukri.com/job-listings-data-analyst'
        },
        {
            'title': 'BCA Fresher - Software Developer',
            'company': 'CodeCraft Technologies',
            'location': 'Delhi NCR, India',
            'salary': '2.5-4 Lakh per annum',
            'experience': 'Fresher',
            'skills': 'Java, C++, Data Structures, Algorithms, Problem Solving',
            'description': 'Excellent opportunity for BCA freshers to kickstart their career in software development.',
            'job_url': 'https://www.naukri.com/job-listings-bca-fresher'
        },
        {
            'title': 'Frontend Developer',
            'company': 'UI Masters Inc',
            'location': 'Mumbai, India',
            'salary': '4-6 Lakh per annum',
            'experience': '1-2 years',
            'skills': 'React, HTML, CSS, JavaScript, Tailwind CSS',
            'description': 'Build beautiful and responsive user interfaces for modern web applications.',
            'job_url': 'https://www.naukri.com/job-listings-frontend-developer'
        },
        {
            'title': 'Backend Developer - Node.js',
            'company': 'Server Solutions Pvt Ltd',
            'location': 'Bangalore, India',
            'salary': '6-10 Lakh per annum',
            'experience': '2-4 years',
            'skills': 'Node.js, Express, MongoDB, Redis, AWS',
            'description': 'Develop robust and scalable backend services for high-traffic applications.',
            'job_url': 'https://www.naukri.com/job-listings-backend-nodejs'
        },
        {
            'title': 'DevOps Engineer',
            'company': 'Cloud Infrastructure Ltd',
            'location': 'Hyderabad, India',
            'salary': '8-12 Lakh per annum',
            'experience': '3-5 years',
            'skills': 'Docker, Kubernetes, AWS, CI/CD, Jenkins, Linux',
            'description': 'Manage cloud infrastructure and implement DevOps best practices.',
            'job_url': 'https://www.naukri.com/job-listings-devops-engineer'
        },
        {
            'title': 'UI/UX Designer',
            'company': 'Design Studio Pro',
            'location': 'Pune, India',
            'salary': 'Not disclosed',
            'experience': '1-3 years',
            'skills': 'Figma, Adobe XD, Sketch, Prototyping, User Research',
            'description': 'Create intuitive and engaging user experiences for web and mobile applications.',
            'job_url': 'https://www.naukri.com/job-listings-ui-ux-designer'
        },
        {
            'title': 'Machine Learning Engineer',
            'company': 'AI Innovations Ltd',
            'location': 'Delhi, India',
            'salary': '10-15 Lakh per annum',
            'experience': '2-5 years',
            'skills': 'Python, TensorFlow, PyTorch, ML Algorithms, Deep Learning',
            'description': 'Build and deploy machine learning models for real-world applications.',
            'job_url': 'https://www.naukri.com/job-listings-ml-engineer'
        },
        {
            'title': 'QA Automation Engineer',
            'company': 'Testing Solutions Inc',
            'location': 'Noida, India',
            'salary': '5-8 Lakh per annum',
            'experience': '2-4 years',
            'skills': 'Selenium, Python, Pytest, Test Automation, CI/CD',
            'description': 'Automate testing processes and ensure software quality.',
            'job_url': 'https://www.naukri.com/job-listings-qa-automation'
        }
    ]
    
    added_count = 0
    duplicate_count = 0
    
    for job in demo_jobs:
        job['job_id'] = generate_job_id(job['title'], job['company'])
        
        if db.insert_job(job):
            added_count += 1
            print(f"✓ Added: {job['title']} at {job['company']}")
        else:
            duplicate_count += 1
            print(f"⊘ Duplicate: {job['title']} at {job['company']}")
    
    # Add scraping history entries
    keywords = ['Python Developer', 'BCA Fresher', 'Full Stack Developer', 'Data Analyst']
    locations = ['Delhi', 'Noida', 'Gurgaon', '']
    
    for i in range(3):
        db.add_scraping_history(
            keyword=random.choice(keywords),
            location=random.choice(locations),
            experience='Fresher' if i % 2 == 0 else '1-3 years',
            jobs_found=random.randint(5, 20),
            status='completed'
        )
    
    print(f"\n✓ Demo data added successfully!")
    print(f"  - Jobs added: {added_count}")
    print(f"  - Duplicates skipped: {duplicate_count}")
    print(f"  - History entries: 3")
    
    stats = db.get_statistics()
    print(f"\nDatabase Statistics:")
    print(f"  - Total jobs: {stats['total_jobs']}")
    print(f"  - Total companies: {stats['total_companies']}")
    print(f"  - Total scrapes: {stats['total_scrapes']}")

if __name__ == '__main__':
    print("="*60)
    print("Adding Demo Data to Naukri Job Scraper")
    print("="*60)
    print()
    add_demo_jobs()
    print()
    print("="*60)
    print("You can now run the app to see the demo data:")
    print("  python app.py")
    print("="*60)
