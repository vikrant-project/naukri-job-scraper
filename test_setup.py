"""Test script to verify Naukri Job Scraper setup
Run this to ensure all components are working correctly
Author: Vikrant Rana
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import flask
        print("✓ Flask installed")
        
        import selenium
        print("✓ Selenium installed")
        
        import bs4
        print("✓ BeautifulSoup4 installed")
        
        import pandas
        print("✓ Pandas installed")
        
        from apscheduler.schedulers.background import BackgroundScheduler
        print("✓ APScheduler installed")
        
        print("\n✓ All required packages are installed!\n")
        return True
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_database():
    """Test database initialization"""
    print("Testing database...")
    try:
        from database import JobDatabase
        db = JobDatabase()
        stats = db.get_statistics()
        print(f"✓ Database initialized successfully")
        print(f"  - Total jobs: {stats['total_jobs']}")
        print(f"  - Total companies: {stats['total_companies']}")
        print(f"  - Total scrapes: {stats['total_scrapes']}")
        print()
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_scraper_module():
    """Test scraper module initialization"""
    print("Testing scraper module...")
    try:
        from scraper import NaukriScraper
        scraper = NaukriScraper(headless=True)
        print("✓ Scraper module loaded successfully")
        print()
        return True
    except Exception as e:
        print(f"✗ Scraper error: {e}")
        return False

def test_flask_app():
    """Test Flask app initialization"""
    print("Testing Flask application...")
    try:
        from app import app
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Flask app initialized successfully")
                print("✓ Dashboard route working")
                print()
                return True
            else:
                print(f"✗ Dashboard returned status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ Flask app error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("Testing file structure...")
    required_files = [
        'app.py',
        'scraper.py',
        'database.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
        'static/style.css',
        'static/script.js',
        'templates/index.html',
        'templates/jobs.html'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING!")
            all_exist = False
    
    print()
    return all_exist

def main():
    """Run all tests"""
    print("="*60)
    print("Naukri Job Scraper - Setup Verification")
    print("="*60)
    print()
    
    results = []
    
    results.append(("File Structure", test_file_structure()))
    results.append(("Python Packages", test_imports()))
    results.append(("Database", test_database()))
    results.append(("Scraper Module", test_scraper_module()))
    results.append(("Flask Application", test_flask_app()))
    
    print("="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for test_name, result in results:
        status = "PASS ✓" if result else "FAIL ✗"
        print(f"{test_name}: {status}")
    
    print("="*60)
    
    if all(result for _, result in results):
        print("\n✓ ALL TESTS PASSED!")
        print("\nYou can now run the application:")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        print("\nPlease fix the errors above before running the application.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
