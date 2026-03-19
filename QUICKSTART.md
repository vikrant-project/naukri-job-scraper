# Quick Start Guide - Naukri Job Scraper

## Installation (5 minutes)

### Step 1: Clone Repository
```bash
git clone https://github.com/vikrant-project/naukri-job-scraper.git
cd naukri-job-scraper
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Setup
```bash
python test_setup.py
```

You should see:
```
✓ ALL TESTS PASSED!
```

### Step 4: Run Application
```bash
python app.py
```

### Step 5: Open Dashboard
Open your browser and go to:
```
http://localhost:5000
```

## First Scrape

1. Click **"Start Scraping"** button
2. Enter job details:
   - Keyword: `Python Developer`
   - Location: `Delhi`
   - Experience: `Fresher`
   - Pages: `2`
3. Click **"Start Scraping"**
4. Wait 2-3 minutes
5. View results in **"All Jobs"**

## Export Data

- Click **"Export to Excel"** button
- File saved in `exports/` folder
- Opens automatically for download

## Troubleshooting

### Chrome not found
```bash
# Install Google Chrome
# The app will auto-download ChromeDriver
```

### Permission denied
```bash
sudo chmod +x app.py
```

### Port already in use
```bash
# Change port in app.py (line: app.run(port=5000))
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Need Help?

Email: vikrantranahome@gmail.com
GitHub Issues: https://github.com/vikrant-project/naukri-job-scraper/issues
