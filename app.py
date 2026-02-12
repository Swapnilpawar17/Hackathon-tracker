import os
from flask import Flask, render_template_string, jsonify
from scrapers import HackathonScraper
from india_scrapers import IndiaHackathonScraper
from manual_sources import get_manual_hackathons
from filters import apply_all_filters
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Store hackathons in memory
cached_hackathons = []
last_updated = None

def update_hackathons():
    """Background job to update hackathons"""
    global cached_hackathons, last_updated
    
    while True:
        try:
            print(f"🔄 Updating hackathons at {datetime.now()}")
            
            # Scrape all sources
            hackathons = []
            
            # International platforms
            scraper = HackathonScraper()
            hackathons.extend(scraper.get_all_hackathons())
            
            # India platforms
            india_scraper = IndiaHackathonScraper()
            hackathons.extend(india_scraper.get_all_india_hackathons())
            
            # Manual sources
            hackathons.extend(get_manual_hackathons())
            
            # Apply filters - LIVE only
            hackathons = apply_all_filters(hackathons, live_only=True)
            
            cached_hackathons = hackathons
            last_updated = datetime.now()
            
            print(f"✅ Updated: {len(hackathons)} live hackathons found")
            
        except Exception as e:
            print(f"❌ Update error: {e}")
        
        # Wait 6 hours before next update
        time.sleep(21600)

# Start background thread
update_thread = threading.Thread(target=update_hackathons, daemon=True)
update_thread.start()

# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Live Hackathon Tracker</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        h1 {
            color: #667eea;
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 18px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .stat-number {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }
        
        .hackathon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .hackathon-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }
        
        .hackathon-card:hover {
            transform: translateY(-5px);
        }
        
        .hackathon-name {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        
        .tags {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .tag {
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: 500;
            color: white;
        }
        
        .tag-platform {
            background: #667eea;
        }
        
        .tag-mode {
            background: #28a745;
        }
        
        .tag-live {
            background: #dc3545;
        }
        
        .info {
            color: #666;
            font-size: 14px;
            margin: 5px 0;
        }
        
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 10px;
            transition: transform 0.3s;
        }
        
        .btn:hover {
            transform: scale(1.05);
        }
        
        .last-updated {
            text-align: center;
            color: white;
            margin-top: 30px;
            font-size: 14px;
        }
        
        @media (max-width: 768px) {
            .hackathon-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Live Hackathon Tracker</h1>
            <p class="subtitle">Real-time tracking of active hackathons for CSE students</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-count">-</div>
                <div class="stat-label">Live Hackathons</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="platform-count">-</div>
                <div class="stat-label">Platforms</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="fresher-count">-</div>
                <div class="stat-label">Fresher Friendly</div>
            </div>
        </div>
        
        <div id="hackathon-container" class="hackathon-grid">
            <div style="grid-column: 1/-1; text-align: center; color: white; padding: 50px;">
                Loading hackathons...
            </div>
        </div>
        
        <p class="last-updated" id="last-updated"></p>
    </div>
    
    <script>
        async function fetchHackathons() {
            try {
                const response = await fetch('/api/hackathons');
                const data = await response.json();
                
                // Update stats
                document.getElementById('total-count').textContent = data.total;
                document.getElementById('platform-count').textContent = data.platform_count;
                document.getElementById('fresher-count').textContent = data.fresher_count;
                
                // Update hackathon grid
                const container = document.getElementById('hackathon-container');
                
                if (data.hackathons.length === 0) {
                    container.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: white; padding: 50px;">No live hackathons found. Check back later!</div>';
                    return;
                }
                
                container.innerHTML = data.hackathons.map(hack => `
                    <div class="hackathon-card">
                        <div class="hackathon-name">${hack.name}</div>
                        <div class="tags">
                            <span class="tag tag-platform">${hack.platform}</span>
                            <span class="tag tag-mode">${hack.mode || 'Online'}</span>
                            <span class="tag tag-live">LIVE</span>
                        </div>
                        ${hack.organizer ? `<div class="info">🏢 ${hack.organizer}</div>` : ''}
                        ${hack.prize_pool && hack.prize_pool !== 'N/A' ? `<div class="info">🏆 ${hack.prize_pool}</div>` : ''}
                        ${hack.fresher_friendly ? '<div class="info">✅ Fresher Friendly</div>' : ''}
                        ${hack.registration_link ? `<a href="${hack.registration_link}" target="_blank" class="btn">Register Now →</a>` : ''}
                    </div>
                `).join('');
                
                // Update last updated
                document.getElementById('last-updated').textContent = 
                    `Last updated: ${new Date(data.last_updated).toLocaleString()}`;
                
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('hackathon-container').innerHTML = 
                    '<div style="grid-column: 1/-1; text-align: center; color: white; padding: 50px;">Error loading hackathons. Please refresh.</div>';
            }
        }
        
        // Fetch on load
        fetchHackathons();
        
        // Refresh every 5 minutes
        setInterval(fetchHackathons, 300000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/hackathons')
def api_hackathons():
    """API endpoint for hackathons"""
    global cached_hackathons, last_updated
    
    if not cached_hackathons:
        # Initial load if cache is empty
        hackathons = []
        
        try:
            scraper = HackathonScraper()
            hackathons.extend(scraper.get_all_hackathons())
            
            india_scraper = IndiaHackathonScraper()
            hackathons.extend(india_scraper.get_all_india_hackathons())
            
            hackathons.extend(get_manual_hackathons())
            hackathons = apply_all_filters(hackathons, live_only=True)
            
            cached_hackathons = hackathons
            last_updated = datetime.now()
        except:
            pass
    
    # Calculate stats
    platforms = set(h.get('platform', '') for h in cached_hackathons)
    fresher_count = len([h for h in cached_hackathons if h.get('fresher_friendly', False)])
    
    return jsonify({
        'hackathons': cached_hackathons,
        'total': len(cached_hackathons),
        'platform_count': len(platforms),
        'fresher_count': fresher_count,
        'last_updated': last_updated.isoformat() if last_updated else datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'time': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)