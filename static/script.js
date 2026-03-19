// Naukri Job Scraper - Dashboard JavaScript
// Author: Vikrant Rana

// Show scrape modal
function showScrapeModal() {
    const modal = document.getElementById('scrapeModal');
    modal.classList.add('active');
}

// Close scrape modal
function closeScrapeModal() {
    const modal = document.getElementById('scrapeModal');
    modal.classList.remove('active');
    
    // Reset progress
    const progressDiv = document.getElementById('scrapeProgress');
    if (progressDiv) {
        progressDiv.style.display = 'none';
    }
    
    // Enable button
    const startBtn = document.getElementById('startScrapeBtn');
    if (startBtn) {
        startBtn.disabled = false;
        startBtn.innerHTML = '<i class="fas fa-rocket"></i> Start Scraping';
    }
}

// Start scraping
async function startScrape() {
    const keyword = document.getElementById('keyword').value;
    const location = document.getElementById('location').value;
    const experience = document.getElementById('experience').value;
    const maxPages = document.getElementById('maxPages').value;
    
    if (!keyword) {
        alert('Please enter a job keyword');
        return;
    }
    
    // Disable button and show progress
    const startBtn = document.getElementById('startScrapeBtn');
    startBtn.disabled = true;
    startBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scraping...';
    
    const progressDiv = document.getElementById('scrapeProgress');
    progressDiv.style.display = 'flex';
    
    const progressText = document.getElementById('progressText');
    progressText.textContent = 'Initializing scraper...';
    
    try {
        // Start scraping
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keyword: keyword,
                location: location,
                experience: experience,
                max_pages: parseInt(maxPages)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            progressText.textContent = 'Scraping started successfully! This may take a few minutes...';
            
            // Poll for status updates
            const statusInterval = setInterval(async () => {
                const statusResponse = await fetch('/api/scrape/status');
                const statusData = await statusResponse.json();
                
                progressText.textContent = statusData.progress || 'Scraping in progress...';
                
                if (!statusData.is_running) {
                    clearInterval(statusInterval);
                    
                    // Show completion message
                    progressText.textContent = statusData.progress || 'Scraping completed!';
                    
                    // Wait 2 seconds then reload
                    setTimeout(() => {
                        window.location.reload();
                    }, 2000);
                }
            }, 3000);
        } else {
            progressText.textContent = 'Error: ' + data.message;
            startBtn.disabled = false;
            startBtn.innerHTML = '<i class="fas fa-rocket"></i> Start Scraping';
        }
    } catch (error) {
        console.error('Error:', error);
        progressText.textContent = 'Error starting scraper. Please try again.';
        startBtn.disabled = false;
        startBtn.innerHTML = '<i class="fas fa-rocket"></i> Start Scraping';
    }
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('scrapeModal');
    if (event.target === modal) {
        closeScrapeModal();
    }
}

// Auto-refresh statistics every 30 seconds
if (window.location.pathname === '/') {
    setInterval(async () => {
        try {
            const response = await fetch('/api/statistics');
            const stats = await response.json();
            
            // Update stat values if elements exist
            const statValues = document.querySelectorAll('.stat-value');
            if (statValues.length >= 4) {
                statValues[0].textContent = stats.total_jobs;
                statValues[1].textContent = stats.jobs_today;
                statValues[2].textContent = stats.total_companies;
                statValues[3].textContent = stats.total_scrapes;
            }
        } catch (error) {
            console.error('Error fetching statistics:', error);
        }
    }, 30000);
}

// Console welcome message
console.log('%c Naukri Job Scraper ', 'background: #3b82f6; color: white; font-size: 16px; font-weight: bold; padding: 10px;');
console.log('%c Developed by Vikrant Rana ', 'background: #18181b; color: #a1a1aa; font-size: 12px; padding: 5px;');
console.log('%c BCA Aspirant, Delhi ', 'background: #18181b; color: #22c55e; font-size: 12px; padding: 5px;');
