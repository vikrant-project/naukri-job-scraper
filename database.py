"""Database module for Naukri Job Scraper
Handles SQLite database operations for storing job listings
Author: Vikrant Rana
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_PATH = 'jobs.db'

class JobDatabase:
    """Manages SQLite database operations for job listings"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize database connection and create tables if not exist"""
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self):
        """Create and return a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def create_tables(self):
        """Create necessary database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                salary TEXT,
                experience TEXT,
                skills TEXT,
                description TEXT,
                job_url TEXT,
                scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Scraping history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                location TEXT,
                experience TEXT,
                jobs_found INTEGER DEFAULT 0,
                scrape_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_job(self, job_data: Dict) -> bool:
        """Insert a job into database, skip if duplicate
        
        Args:
            job_data: Dictionary containing job information
            
        Returns:
            True if inserted, False if duplicate
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO jobs (job_id, title, company, location, salary, 
                                experience, skills, description, job_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data.get('job_id'),
                job_data.get('title'),
                job_data.get('company'),
                job_data.get('location'),
                job_data.get('salary'),
                job_data.get('experience'),
                job_data.get('skills'),
                job_data.get('description'),
                job_data.get('job_url')
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Duplicate job_id
            return False
        finally:
            conn.close()
    
    def get_all_jobs(self, limit: Optional[int] = None) -> List[Dict]:
        """Retrieve all jobs from database
        
        Args:
            limit: Maximum number of jobs to retrieve
            
        Returns:
            List of job dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM jobs ORDER BY scraped_date DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        cursor.execute(query)
        jobs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jobs
    
    def search_jobs(self, keyword: str = '', location: str = '', 
                   experience: str = '', min_salary: str = '') -> List[Dict]:
        """Search jobs with filters
        
        Args:
            keyword: Search in title, company, skills
            location: Filter by location
            experience: Filter by experience
            min_salary: Filter by minimum salary
            
        Returns:
            List of matching job dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM jobs WHERE 1=1'
        params = []
        
        if keyword:
            query += ' AND (title LIKE ? OR company LIKE ? OR skills LIKE ?)'
            search_term = f'%{keyword}%'
            params.extend([search_term, search_term, search_term])
        
        if location:
            query += ' AND location LIKE ?'
            params.append(f'%{location}%')
        
        if experience:
            query += ' AND experience LIKE ?'
            params.append(f'%{experience}%')
        
        query += ' ORDER BY scraped_date DESC'
        
        cursor.execute(query, params)
        jobs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jobs
    
    def get_total_jobs_count(self) -> int:
        """Get total number of jobs in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM jobs')
        count = cursor.fetchone()['count']
        conn.close()
        return count
    
    def add_scraping_history(self, keyword: str, location: str, 
                            experience: str, jobs_found: int, 
                            status: str = 'completed'):
        """Add entry to scraping history
        
        Args:
            keyword: Search keyword used
            location: Location filter used
            experience: Experience filter used
            jobs_found: Number of jobs found
            status: Status of scraping operation
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scraping_history (keyword, location, experience, 
                                         jobs_found, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (keyword, location, experience, jobs_found, status))
        
        conn.commit()
        conn.close()
    
    def get_scraping_history(self, limit: int = 10) -> List[Dict]:
        """Get recent scraping history
        
        Args:
            limit: Number of recent entries to retrieve
            
        Returns:
            List of history dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM scraping_history 
            ORDER BY scrape_date DESC 
            LIMIT ?
        ''', (limit,))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return history
    
    def get_statistics(self) -> Dict:
        """Get database statistics
        
        Returns:
            Dictionary with various statistics
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total jobs
        cursor.execute('SELECT COUNT(*) as count FROM jobs')
        total_jobs = cursor.fetchone()['count']
        
        # Jobs today
        cursor.execute('''
            SELECT COUNT(*) as count FROM jobs 
            WHERE DATE(scraped_date) = DATE('now')
        ''')
        jobs_today = cursor.fetchone()['count']
        
        # Total companies
        cursor.execute('SELECT COUNT(DISTINCT company) as count FROM jobs')
        total_companies = cursor.fetchone()['count']
        
        # Total scrapes
        cursor.execute('SELECT COUNT(*) as count FROM scraping_history')
        total_scrapes = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_jobs': total_jobs,
            'jobs_today': jobs_today,
            'total_companies': total_companies,
            'total_scrapes': total_scrapes
        }
    
    def delete_all_jobs(self):
        """Delete all jobs from database (use with caution)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs')
        conn.commit()
        conn.close()
