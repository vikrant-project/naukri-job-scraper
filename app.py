"""Flask Web Dashboard for Naukri Job Scraper
Provides web interface for viewing and managing scraped jobs
Author: Vikrant Rana
"""

from flask import Flask, render_template, request, jsonify, send_file
from database import JobDatabase
from scraper import NaukriScraper
import pandas as pd
from datetime import datetime
import os
import threading
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'naukri-scraper-secret-key-2024'

# Initialize database
db = JobDatabase()

# Scraping status tracker
scraping_status = {
    'is_running': False,
    'current_keyword': '',
    'progress': ''
}

# Scheduler for automatic scraping
scheduler = BackgroundScheduler()
scheduler.start()

def scheduled_scrape():
    """Function to run scheduled scraping"""
    print("Running scheduled scrape...")
    # Default search parameters for scheduled scraping
    scraper = NaukriScraper(headless=True)
    results = scraper.scrape_jobs(
        keyword='Python Developer',
        location='Delhi',
        experience='',
        max_pages=2
    )
    print(f"Scheduled scrape completed: {results}")

# Schedule scraping every 6 hours
scheduler.add_job(
    func=scheduled_scrape,
    trigger='interval',
    hours=6,
    id='scheduled_scrape',
    replace_existing=True
)

@app.route('/')
def index():
    """Main dashboard page"""
    stats = db.get_statistics()
    recent_history = db.get_scraping_history(limit=5)
    return render_template('index.html', stats=stats, history=recent_history)

@app.route('/jobs')
def jobs():
    """Jobs listing page"""
    # Get filter parameters
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    experience = request.args.get('experience', '')
    
    # Get jobs from database
    if keyword or location or experience:
        jobs_list = db.search_jobs(keyword, location, experience)
    else:
        jobs_list = db.get_all_jobs(limit=100)
    
    return render_template('jobs.html', jobs=jobs_list)

@app.route('/api/scrape', methods=['POST'])
def start_scraping():
    """API endpoint to start scraping"""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({
            'success': False,
            'message': 'Scraping is already in progress'
        }), 400
    
    data = request.json
    keyword = data.get('keyword', 'Python Developer')
    location = data.get('location', '')
    experience = data.get('experience', '')
    max_pages = int(data.get('max_pages', 3))
    
    # Run scraping in background thread
    def scrape_in_background():
        global scraping_status
        scraping_status['is_running'] = True
        scraping_status['current_keyword'] = keyword
        scraping_status['progress'] = 'Starting...'
        
        try:
            scraper = NaukriScraper(headless=True)
            results = scraper.scrape_jobs(keyword, location, experience, max_pages)
            scraping_status['progress'] = f"Completed: {results['jobs_saved']} jobs saved"
        except Exception as e:
            scraping_status['progress'] = f"Error: {str(e)}"
        finally:
            scraping_status['is_running'] = False
    
    thread = threading.Thread(target=scrape_in_background)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Scraping started successfully'
    })

@app.route('/api/scrape/status')
def scrape_status():
    """Get current scraping status"""
    return jsonify(scraping_status)

@app.route('/api/jobs')
def get_jobs_api():
    """API endpoint to get jobs with filters"""
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    experience = request.args.get('experience', '')
    
    if keyword or location or experience:
        jobs_list = db.search_jobs(keyword, location, experience)
    else:
        jobs_list = db.get_all_jobs(limit=100)
    
    return jsonify({
        'success': True,
        'count': len(jobs_list),
        'jobs': jobs_list
    })

@app.route('/api/statistics')
def get_statistics():
    """API endpoint for statistics"""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/export/excel')
def export_excel():
    """Export all jobs to Excel file"""
    jobs_list = db.get_all_jobs()
    
    if not jobs_list:
        return jsonify({
            'success': False,
            'message': 'No jobs to export'
        }), 400
    
    # Create DataFrame
    df = pd.DataFrame(jobs_list)
    
    # Select columns to export
    columns_to_export = ['title', 'company', 'location', 'salary', 
                        'experience', 'skills', 'job_url', 'scraped_date']
    df = df[columns_to_export]
    
    # Create exports directory if not exists
    os.makedirs('exports', exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'naukri_jobs_{timestamp}.xlsx'
    filepath = os.path.join('exports', filename)
    
    # Export to Excel
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    # Send file
    return send_file(
        filepath,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/history')
def get_history():
    """Get scraping history"""
    limit = request.args.get('limit', 10, type=int)
    history = db.get_scraping_history(limit)
    return jsonify({
        'success': True,
        'history': history
    })

if __name__ == '__main__':
    print("="*50)
    print("Naukri Job Scraper Dashboard")
    print("Author: Vikrant Rana")
    print("="*50)
    print("Starting Flask server...")
    print("Dashboard: http://localhost:5000")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
