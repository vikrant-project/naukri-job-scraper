# Naukri Job Scraper 🚀

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.16-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A powerful web scraping tool to extract job listings from Naukri.com with a beautiful dark-themed dashboard**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots) • [Tech Stack](#tech-stack)

</div>

---

## 📋 Overview

Naukri Job Scraper is a comprehensive Python-based web scraping application that automatically extracts job listings from Naukri.com and presents them in a modern, user-friendly dashboard. Perfect for job seekers, recruiters, and data analysts looking to aggregate job market data.

## ✨ Features

### Core Scraping Features
- 🔍 **Smart Job Search** - Search by keyword (Python Developer, BCA Fresher, etc.)
- 📍 **Location Filtering** - Filter jobs by city (Delhi, Noida, Gurgaon, etc.)
- 💼 **Experience Filtering** - Filter by experience level (Fresher, 1-3 years, etc.)
- 🎯 **Comprehensive Data Extraction** - Extracts:
  - Job title and description
  - Company name
  - Salary range
  - Location
  - Experience requirements
  - Required skills
  - Direct job URL

### Data Management
- 💾 **SQLite Database** - Persistent storage for all scraped jobs
- 🗑️ **Auto Duplicate Removal** - Intelligent duplicate detection
- 📊 **Excel Export** - One-click export to `.xlsx` format with timestamps
- 📈 **Scraping History** - Track all scraping activities with date/time stamps
- 📉 **Statistics Dashboard** - Real-time metrics and analytics

### Dashboard Features
- 🎨 **Modern Dark Theme** - Eye-friendly professional interface
- 🃏 **Job Cards** - Beautiful card layout with company logo placeholders
- 🎨 **Color-Coded Salaries** - Visual salary range indicators
- 🔎 **Advanced Search** - Filter and search scraped jobs instantly
- 📱 **Fully Responsive** - Works seamlessly on mobile, tablet, and desktop
- ⚡ **Real-Time Updates** - Live statistics and status monitoring

### Anti-Detection Features
- 🕐 **Random Delays** - 2-5 second delays between requests
- 🔄 **User Agent Rotation** - Pool of 10+ realistic user agents
- 🕶️ **Headless Mode** - Stealthy browser automation
- 🛡️ **CAPTCHA Detection** - Graceful handling of blocks

### Automation
- ⏰ **Scheduled Scraping** - Automatic scraping every 6 hours (configurable)
- 🎛️ **Manual Trigger** - On-demand scraping via dashboard button
- 🧵 **Background Processing** - Non-blocking scraper execution

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Google Chrome browser (latest version)
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/vikrant-project/naukri-job-scraper.git
cd naukri-job-scraper
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- Selenium (Browser automation)
- BeautifulSoup4 (HTML parsing)
- Pandas (Data processing)
- APScheduler (Task scheduling)
- All other required packages

### Step 3: Verify Chrome Installation
Make sure Google Chrome is installed on your system. The scraper uses ChromeDriver which will be automatically downloaded on first run.

---

## 📖 Usage

### Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser and navigate to:**
```
http://localhost:5000
```

3. **You'll see the dashboard with:**
   - Statistics cards showing job counts
   - Recent scraping activity
   - Navigation to view all jobs

### Starting a Scrape

1. Click the **"Start Scraping"** button on the dashboard
2. Fill in the scrape parameters:
   - **Keyword**: Job title (e.g., "Python Developer", "BCA Fresher")
   - **Location**: City name (optional)
   - **Experience**: Select experience level (optional)
   - **Pages**: Number of pages to scrape (1-10)
3. Click **"Start Scraping"** and wait for completion
4. The scraper runs in the background and shows progress
5. Page automatically refreshes when scraping completes

### Viewing Jobs

1. Click **"All Jobs"** in the sidebar
2. Use the search bar to filter by title, company, or skills
3. Apply filters for location and experience
4. Click **"View Job"** on any job card to open the Naukri listing

### Exporting Data

Click the **"Export to Excel"** button to download all jobs as an Excel file with timestamp:
- Format: `naukri_jobs_YYYYMMDD_HHMMSS.xlsx`
- Saved to: `exports/` folder
- Includes all job details

---

## 📸 Screenshots

### Dashboard
- Clean statistics overview
- Recent scraping activity
- One-click scraping

### Jobs Listing
- Beautiful card layout
- Advanced filtering
- Color-coded salaries
- Skill tags

### Scraping Modal
- Intuitive form
- Real-time progress
- Status updates

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| **Python 3.8+** | Core programming language |
| **Flask 3.0** | Web framework for dashboard |
| **Selenium 4.16** | Browser automation for scraping |
| **BeautifulSoup4** | HTML parsing and data extraction |
| **SQLite3** | Lightweight database for storage |
| **Pandas** | Data processing and Excel export |
| **APScheduler** | Automated scheduled scraping |
| **HTML5 + CSS3** | Modern responsive UI |
| **JavaScript (Vanilla)** | Dynamic dashboard interactions |

---

## 📁 Project Structure

```
naukri-job-scraper/
├── app.py                  # Flask web application
├── scraper.py              # Selenium scraping logic
├── database.py             # SQLite database operations
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore rules
├── jobs.db                 # SQLite database (auto-created)
├── static/
│   ├── style.css           # Dashboard styles
│   └── script.js           # Dashboard JavaScript
├── templates/
│   ├── index.html          # Main dashboard page
│   └── jobs.html           # Jobs listing page
└── exports/                # Excel export folder (auto-created)
```

---

## 🎯 How It Works

1. **User Input**: User provides search criteria via dashboard
2. **URL Construction**: System builds Naukri.com search URL
3. **Browser Automation**: Selenium opens headless Chrome
4. **Anti-Detection**: Random delays and user agent rotation applied
5. **Page Scraping**: BeautifulSoup extracts job data from HTML
6. **Data Processing**: Extracted data cleaned and structured
7. **Duplicate Check**: Jobs checked against database
8. **Storage**: New jobs saved to SQLite database
9. **History Logging**: Scraping activity recorded
10. **Dashboard Update**: Statistics refreshed automatically

---

## ⚙️ Configuration

### Modify Scraping Schedule

In `app.py`, find the scheduler configuration:

```python
scheduler.add_job(
    func=scheduled_scrape,
    trigger='interval',
    hours=6,  # Change this value
    id='scheduled_scrape',
    replace_existing=True
)
```

### Adjust Delay Times

In `scraper.py`, modify the `random_delay` function:

```python
def random_delay(self, min_seconds: float = 2.0, max_seconds: float = 5.0):
    # Adjust min_seconds and max_seconds
```

### Change Default Search Parameters

In `app.py`, modify the `scheduled_scrape` function:

```python
def scheduled_scrape():
    scraper = NaukriScraper(headless=True)
    results = scraper.scrape_jobs(
        keyword='Python Developer',  # Change default keyword
        location='Delhi',             # Change default location
        experience='',                # Change default experience
        max_pages=2                   # Change default pages
    )
```

---

## 🚨 Important Notes

### Legal Disclaimer

⚠️ **This tool is for EDUCATIONAL PURPOSES ONLY**

- Always respect Naukri.com's Terms of Service
- Do not use for commercial purposes without permission
- Implement reasonable scraping delays (already included)
- Do not overload Naukri's servers with excessive requests
- The developer is not responsible for misuse of this tool
- Use at your own risk

### Ethical Web Scraping

✅ **Best Practices Followed:**
- Respects `robots.txt`
- Implements polite delays (2-5 seconds)
- Uses single-threaded scraping
- Does not bypass paywalls
- Handles rate limiting gracefully

❌ **Do Not:**
- Run scraper continuously without breaks
- Scrape more than necessary
- Share scraped data commercially
- Use scraped data to harm Naukri or users

---

## 🐛 Troubleshooting

### ChromeDriver Issues
**Error**: "chromedriver not found"
**Solution**: Install webdriver-manager (included in requirements)
```bash
pip install webdriver-manager
```

### Database Locked
**Error**: "database is locked"
**Solution**: Close any other connections to `jobs.db`

### No Jobs Found
**Possible Causes**:
- CAPTCHA detected (check console output)
- Search keyword too specific
- Naukri's HTML structure changed
- Network connectivity issues

### Scraping Stuck
**Solution**: 
- Check console for error messages
- Reduce `max_pages` parameter
- Increase delay times in `scraper.py`

---

## 🔮 Future Enhancements

- [ ] Email alerts for new matching jobs
- [ ] Advanced analytics and charts
- [ ] Support for other job portals (Indeed, LinkedIn)
- [ ] Job application tracking
- [ ] Resume parsing and matching
- [ ] Salary trend analysis
- [ ] Company reviews integration
- [ ] Telegram/WhatsApp notifications
- [ ] Docker containerization
- [ ] API endpoints for integration

---

## 👨‍💻 About the Developer

**Name**: Vikrant Rana  
**Profile**: BCA Aspirant  
**Location**: Delhi, India  
**GitHub**: [@vikrant-project](https://github.com/vikrant-project)  
**Email**: vikrantranahome@gmail.com

*Passionate about web scraping, automation, and building practical tools that solve real-world problems.*

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Naukri.com for providing the job listing platform
- Selenium and BeautifulSoup communities
- Flask framework developers
- All open-source contributors

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Contact: vikrantranahome@gmail.com

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star on GitHub! ⭐**

Made with ❤️ by Vikrant Rana

</div>
