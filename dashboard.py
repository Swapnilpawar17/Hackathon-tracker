from flask import Flask, render_template_string, jsonify, request
from scrapers import HackathonScraper
from india_scrapers import IndiaHackathonScraper
from manual_sources import get_manual_hackathons
from filters import apply_all_filters
from datetime import datetime
import json

app = Flask(__name__)

# Store hackathons in memory
cached_hackathons = []
last_updated = None

def get_all_hackathons():
    """Fetch all hackathons from all sources"""
    global cached_hackathons, last_updated
    
    hackathons = []
    
    # Scrape international
    scraper = HackathonScraper()
    hackathons.extend(scraper.get_all_hackathons())
    
    # Scrape India
    india_scraper = IndiaHackathonScraper()
    hackathons.extend(india_scraper.get_all_india_hackathons())
    
    # Add manual
    hackathons.extend(get_manual_hackathons())
    
    # Apply filters
    hackathons = apply_all_filters(hackathons)
    
    cached_hackathons = hackathons
    last_updated = datetime.now()
    
    return hackathons

# HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Hackathon Tracker Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
        }
        
        .navbar {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .logo {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-actions {
            display: flex;
            gap: 15px;
        }
        
        .btn {
            padding: 10px 20px;
            border-radius: 25px;
            border: none;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .stat-number {
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            margin-top: 5px;
        }
        
        .filters {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
        }
        
        .filter-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .filter-label {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.7);
        }
        
        select, input[type="text"] {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 10px 15px;
            color: white;
            font-size: 14px;
            outline: none;
        }
        
        select option {
            background: #1a1a2e;
        }
        
        .hackathon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }
        
        .hackathon-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s;
        }
        
        .hackathon-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            border-color: #667eea;
        }
        
        .card-header {
            padding: 20px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        
        .card-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .tag {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .tag-platform {
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        
        .tag-mode {
            background: rgba(40, 167, 69, 0.3);
            border: 1px solid #28a745;
        }
        
        .tag-status {
            background: rgba(220, 53, 69, 0.3);
            border: 1px solid #dc3545;
        }
        
        .tag-status.upcoming {
            background: rgba(255, 193, 7, 0.3);
            border: 1px solid #ffc107;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .card-info {
            margin-bottom: 15px;
        }
        
        .info-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        .info-item i {
            width: 20px;
            color: #667eea;
        }
        
        .card-actions {
            display: flex;
            gap: 10px;
        }
        
        .card-btn {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .card-btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .card-btn-primary:hover {
            transform: scale(1.02);
        }
        
        .loading {
            text-align: center;
            padding: 50px;
        }
        
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .no-results {
            text-align: center;
            padding: 50px;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .last-updated {
            text-align: center;
            color: rgba(255, 255, 255, 0.5);
            font-size: 14px;
            margin-top: 30px;
        }
        
        @media (max-width: 768px) {
            .navbar {
                flex-direction: column;
                gap: 15px;
            }
            
            .filters {
                flex-direction: column;
            }
            
            .hackathon-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo">🚀 Hackathon Tracker</div>
        <div class="nav-actions">
            <button class="btn btn-secondary" onclick="refreshData()">
                <i class="fas fa-sync-alt"></i> Refresh
            </button>
            <a href="https://notion.so" target="_blank" class="btn btn-primary">
                <i class="fas fa-external-link-alt"></i> Open Notion
            </a>
        </div>
    </nav>
    
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-number" id="total-count">-</div>
                <div class="stat-label">Total Hackathons</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔴</div>
                <div class="stat-number" id="live-count">-</div>
                <div class="stat-label">Live Now</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🌐</div>
                <div class="stat-number" id="platform-count">-</div>
                <div class="stat-label">Platforms</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👶</div>
                <div class="stat-number" id="fresher-count">-</div>
                <div class="stat-label">Fresher Friendly</div>
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <label class="filter-label">Platform:</label>
                <select id="platform-filter" onchange="applyFilters()">
                    <option value="">All Platforms</option>
                </select>
            </div>
            <div class="filter-group">
                <label class="filter-label">Mode:</label>
                <select id="mode-filter" onchange="applyFilters()">
                    <option value="">All Modes</option>
                    <option value="Online">Online</option>
                    <option value="Offline">Offline</option>
                    <option value="Hybrid">Hybrid</option>
                </select>
            </div>
            <div class="filter-group">
                <label class="filter-label">Status:</label>
                <select id="status-filter" onchange="applyFilters()">
                    <option value="">All</option>
                    <option value="Live">Live</option>
                    <option value="Upcoming">Upcoming</option>
                </select>
            </div>
            <div class="filter-group">
                <label class="filter-label">Search:</label>
                <input type="text" id="search-input" placeholder="Search hackathons..." oninput="applyFilters()">
            </div>
        </div>
        
        <div id="hackathon-container" class="hackathon-grid">
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>Loading hackathons...</p>
            </div>
        </div>
        
        <p class="last-updated" id="last-updated"></p>
    </div>
    
    <script>
        let allHackathons = [];
        
        // Fetch hackathons from API
        async function fetchHackathons() {
            try {
                const response = await fetch('/api/hackathons');
                const data = await response.json();
                allHackathons = data.hackathons;
                updateStats(data);
                populateFilters();
                renderHackathons(allHackathons);
                document.getElementById('last-updated').textContent = 
                    `Last updated: ${new Date(data.last_updated).toLocaleString()}`;
            } catch (error) {
                console.error('Error fetching hackathons:', error);
                document.getElementById('hackathon-container').innerHTML = `
                    <div class="no-results">
                        <p>Error loading hackathons. Please try refreshing.</p>
                    </div>
                `;
            }
        }
        
        // Update stats
        function updateStats(data) {
            document.getElementById('total-count').textContent = data.total;
            document.getElementById('live-count').textContent = data.live_count;
            document.getElementById('platform-count').textContent = data.platform_count;
            document.getElementById('fresher-count').textContent = data.fresher_count;
        }
        
        // Populate platform filter
        function populateFilters() {
            const platforms = [...new Set(allHackathons.map(h => h.platform))].sort();
            const select = document.getElementById('platform-filter');
            platforms.forEach(platform => {
                const option = document.createElement('option');
                option.value = platform;
                option.textContent = platform;
                select.appendChild(option);
            });
        }
        
        // Render hackathons
        function renderHackathons(hackathons) {
            const container = document.getElementById('hackathon-container');
            
            if (hackathons.length === 0) {
                container.innerHTML = `
                    <div class="no-results">
                        <p>No hackathons found matching your criteria.</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = hackathons.map(hack => `
                <div class="hackathon-card">
                    <div class="card-header">
                        <h3 class="card-title">${hack.name}</h3>
                        <div class="card-tags">
                            <span class="tag tag-platform">${hack.platform}</span>
                            <span class="tag tag-mode">${hack.mode}</span>
                            <span class="tag tag-status ${hack.status.toLowerCase()}">${hack.status}</span>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="card-info">
                            ${hack.organizer ? `<div class="info-item"><i class="fas fa-building"></i> ${hack.organizer}</div>` : ''}
                            ${hack.prize_pool && hack.prize_pool !== 'N/A' ? `<div class="info-item"><i class="fas fa-trophy"></i> ${hack.prize_pool}</div>` : ''}
                            ${hack.fresher_friendly ? `<div class="info-item"><i class="fas fa-check-circle"></i> Fresher Friendly</div>` : ''}
                        </div>
                        <div class="card-actions">
                            <a href="${hack.registration_link}" target="_blank" class="card-btn card-btn-primary">
                                Register Now <i class="fas fa-arrow-right"></i>
                            </a>
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        // Apply filters
        function applyFilters() {
            const platform = document.getElementById('platform-filter').value;
            const mode = document.getElementById('mode-filter').value;
            const status = document.getElementById('status-filter').value;
            const search = document.getElementById('search-input').value.toLowerCase();
            
            let filtered = allHackathons;
            
            if (platform) {
                filtered = filtered.filter(h => h.platform === platform);
            }
            
            if (mode) {
                filtered = filtered.filter(h => h.mode === mode);
            }
            
            if (status) {
                filtered = filtered.filter(h => h.status === status);
            }
            
            if (search) {
                filtered = filtered.filter(h => 
                    h.name.toLowerCase().includes(search) ||
                    h.platform.toLowerCase().includes(search) ||
                    (h.organizer && h.organizer.toLowerCase().includes(search))
                );
            }
            
            renderHackathons(filtered);
        }
        
        // Refresh data
        async function refreshData() {
            document.getElementById('hackathon-container').innerHTML = `
                <div class="loading">
                    <div class="loading-spinner"></div>
                    <p>Refreshing hackathons...</p>
                </div>
            `;
            
            try {
                const response = await fetch('/api/refresh', { method: 'POST' });
                const data = await response.json();
                allHackathons = data.hackathons;
                updateStats(data);
                renderHackathons(allHackathons);
                document.getElementById('last-updated').textContent = 
                    `Last updated: ${new Date().toLocaleString()}`;
            } catch (error) {
                console.error('Error refreshing:', error);
            }
        }
        
        // Initial load
        fetchHackathons();
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Render the dashboard"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/hackathons')
def get_hackathons_api():
    """API endpoint to get hackathons"""
    global cached_hackathons, last_updated
    
    if not cached_hackathons:
        hackathons = get_all_hackathons()
    else:
        hackathons = cached_hackathons
    
    # Calculate stats
    platforms = set(h.get('platform', '') for h in hackathons)
    live_count = len([h for h in hackathons if h.get('status', '').lower() == 'live'])
    fresher_count = len([h for h in hackathons if h.get('fresher_friendly', False)])
    
    return jsonify({
        'hackathons': hackathons,
        'total': len(hackathons),
        'platform_count': len(platforms),
        'live_count': live_count,
        'fresher_count': fresher_count,
        'last_updated': last_updated.isoformat() if last_updated else datetime.now().isoformat()
    })

@app.route('/api/refresh', methods=['POST'])
def refresh_hackathons():
    """Refresh hackathons from all sources"""
    hackathons = get_all_hackathons()
    
    platforms = set(h.get('platform', '') for h in hackathons)
    live_count = len([h for h in hackathons if h.get('status', '').lower() == 'live'])
    fresher_count = len([h for h in hackathons if h.get('fresher_friendly', False)])
    
    return jsonify({
        'hackathons': hackathons,
        'total': len(hackathons),
        'platform_count': len(platforms),
        'live_count': live_count,
        'fresher_count': fresher_count,
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    global cached_hackathons
    
    if not cached_hackathons:
        return jsonify({'error': 'No data loaded'})
    
    platform_counts = {}
    for hack in cached_hackathons:
        platform = hack.get('platform', 'Unknown')
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    return jsonify({
        'total': len(cached_hackathons),
        'by_platform': platform_counts,
        'by_mode': {
            'Online': len([h for h in cached_hackathons if h.get('mode') == 'Online']),
            'Offline': len([h for h in cached_hackathons if h.get('mode') == 'Offline']),
            'Hybrid': len([h for h in cached_hackathons if h.get('mode') == 'Hybrid'])
        }
    })

def run_dashboard(debug=True, port=5000):
    """Run the dashboard server"""
    print("\n" + "="*60)
    print("🌐 HACKATHON TRACKER DASHBOARD")
    print("="*60)
    print(f"\n🚀 Starting dashboard server...")
    print(f"📍 Open in browser: http://localhost:{port}")
    print(f"📍 Or: http://127.0.0.1:{port}")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    app.run(debug=debug, port=port, host='0.0.0.0')

if __name__ == '__main__':
    run_dashboard()