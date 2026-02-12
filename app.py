import os
from flask import Flask, render_template_string, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Simplified HTML - Faster Loading
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackathon Tracker | Live Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 16px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 36px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .filters {
            background: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .filter-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        input, select {
            padding: 10px 15px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            flex: 1;
            min-width: 200px;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .hackathons {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .hackathon-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .hackathon-card:hover {
            transform: translateY(-10px);
        }
        
        .card-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: white;
        }
        
        .card-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .tags {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .tag {
            background: rgba(255,255,255,0.2);
            padding: 4px 10px;
            border-radius: 5px;
            font-size: 12px;
        }
        
        .card-body {
            padding: 20px;
        }
        
        .info {
            margin-bottom: 10px;
            color: #666;
            font-size: 14px;
        }
        
        .info strong {
            color: #333;
        }
        
        .prize {
            background: #fef3c7;
            color: #92400e;
            padding: 8px 12px;
            border-radius: 8px;
            font-weight: 600;
            margin: 10px 0;
            display: inline-block;
        }
        
        .btn {
            display: block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 12px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.3s;
        }
        
        .btn:hover {
            transform: scale(1.05);
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: white;
            font-size: 18px;
        }
        
        .empty {
            text-align: center;
            padding: 50px;
            background: white;
            border-radius: 15px;
            color: #666;
        }
        
        footer {
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: #666;
            margin-top: 30px;
        }
        
        @media (max-width: 768px) {
            .hackathons {
                grid-template-columns: 1fr;
            }
            
            h1 {
                font-size: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Hackathon Tracker</h1>
            <p class="subtitle">Live hackathons for CSE students & freshers</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total">0</div>
                <div class="stat-label">Live Hackathons</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="platforms">0</div>
                <div class="stat-label">Platforms</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="freshers">0</div>
                <div class="stat-label">Fresher Friendly</div>
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <input type="text" id="search" placeholder="Search hackathons..." onkeyup="filterHackathons()">
                <select id="platform-filter" onchange="filterHackathons()">
                    <option value="">All Platforms</option>
                </select>
                <select id="mode-filter" onchange="filterHackathons()">
                    <option value="">All Modes</option>
                    <option value="Online">Online</option>
                    <option value="Offline">Offline</option>
                    <option value="Hybrid">Hybrid</option>
                </select>
            </div>
        </div>
        
        <div id="hackathons-container">
            <div class="loading">Loading hackathons...</div>
        </div>
        
        <footer>
            <p>Built by Swapnil Pawar | <a href="https://github.com/Swapnilpawar17/Hackathon-tracker" target="_blank">GitHub</a></p>
            <p id="last-updated">Last updated: Loading...</p>
        </footer>
    </div>
    
    <script>
        let allHackathons = [];
        let filteredHackathons = [];
        
        async function loadHackathons() {
            try {
                const response = await fetch('/api/hackathons');
                const data = await response.json();
                
                allHackathons = data.hackathons || [];
                filteredHackathons = allHackathons;
                
                // Update stats
                document.getElementById('total').textContent = allHackathons.length;
                document.getElementById('platforms').textContent = data.platform_count || 0;
                document.getElementById('freshers').textContent = data.fresher_count || 0;
                
                // Update platform filter
                const platforms = [...new Set(allHackathons.map(h => h.platform))];
                const select = document.getElementById('platform-filter');
                platforms.forEach(platform => {
                    const option = document.createElement('option');
                    option.value = platform;
                    option.textContent = platform;
                    select.appendChild(option);
                });
                
                // Render hackathons
                renderHackathons(allHackathons);
                
                // Update time
                document.getElementById('last-updated').textContent = 
                    `Last updated: ${new Date(data.last_updated).toLocaleString()}`;
                    
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('hackathons-container').innerHTML = 
                    '<div class="empty">Error loading hackathons. Please refresh.</div>';
            }
        }
        
        function renderHackathons(hackathons) {
            const container = document.getElementById('hackathons-container');
            
            if (hackathons.length === 0) {
                container.innerHTML = '<div class="empty">No hackathons found</div>';
                return;
            }
            
            const html = hackathons.map(hack => `
                <div class="hackathon-card">
                    <div class="card-header">
                        <div class="card-title">${hack.name}</div>
                        <div class="tags">
                            <span class="tag">${hack.platform}</span>
                            <span class="tag">${hack.mode || 'Online'}</span>
                            <span class="tag">LIVE</span>
                        </div>
                    </div>
                    <div class="card-body">
                        ${hack.organizer ? `<div class="info"><strong>Organizer:</strong> ${hack.organizer}</div>` : ''}
                        ${hack.fresher_friendly ? '<div class="info"><strong>✅ Fresher Friendly</strong></div>' : ''}
                        ${hack.prize_pool && hack.prize_pool !== 'N/A' ? 
                            `<div class="prize">🏆 ${hack.prize_pool}</div>` : ''}
                        ${hack.registration_link ? 
                            `<a href="${hack.registration_link}" target="_blank" class="btn">Register Now →</a>` : ''}
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = `<div class="hackathons">${html}</div>`;
        }
        
        function filterHackathons() {
            const search = document.getElementById('search').value.toLowerCase();
            const platform = document.getElementById('platform-filter').value;
            const mode = document.getElementById('mode-filter').value;
            
            filteredHackathons = allHackathons.filter(hack => {
                const matchSearch = !search || 
                    hack.name.toLowerCase().includes(search) ||
                    (hack.organizer && hack.organizer.toLowerCase().includes(search));
                const matchPlatform = !platform || hack.platform === platform;
                const matchMode = !mode || hack.mode === mode;
                
                return matchSearch && matchPlatform && matchMode;
            });
            
            renderHackathons(filteredHackathons);
        }
        
        // Load on start
        loadHackathons();
    </script>
</body>
</html>
"""

# Simple API endpoint
@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/hackathons')
def api_hackathons():
    """Return static hackathon data for now"""
    
    # Static data - no heavy processing
    hackathons = [
        {
            'name': 'Smart India Hackathon 2025',
            'platform': 'Other',
            'organizer': 'Government of India',
            'mode': 'Hybrid',
            'registration_link': 'https://www.sih.gov.in/',
            'prize_pool': '₹1,00,000 per team',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Google Solution Challenge 2025',
            'platform': 'Other',
            'organizer': 'Google Developer Student Clubs',
            'mode': 'Online',
            'registration_link': 'https://developers.google.com/community/gdsc-solution-challenge',
            'prize_pool': '$3,000 + Mentorship',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Microsoft Imagine Cup 2025',
            'platform': 'Other',
            'organizer': 'Microsoft',
            'mode': 'Online',
            'registration_link': 'https://imaginecup.microsoft.com/',
            'prize_pool': '$100,000',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Flipkart GRiD 6.0',
            'platform': 'Unstop',
            'organizer': 'Flipkart',
            'mode': 'Online',
            'registration_link': 'https://unstop.com/hackathons/flipkart-grid',
            'prize_pool': '₹50,00,000',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'AWS DeepRacer Student League',
            'platform': 'Other',
            'organizer': 'Amazon',
            'mode': 'Online',
            'registration_link': 'https://aws.amazon.com/deepracer/student/',
            'prize_pool': 'Scholarships + Credits',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Schneider Go Green 2025',
            'platform': 'Unstop',
            'organizer': 'Schneider Electric',
            'mode': 'Online',
            'registration_link': 'https://unstop.com',
            'prize_pool': 'Trip to Paris',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Wells Fargo Analytics Challenge',
            'platform': 'Unstop',
            'organizer': 'Wells Fargo',
            'mode': 'Online',
            'registration_link': 'https://unstop.com',
            'prize_pool': '₹2,00,000',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Global Hack Week: GenAI',
            'platform': 'MLH',
            'organizer': 'Major League Hacking',
            'mode': 'Hybrid',
            'registration_link': 'https://mlh.io',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Codeforces Round',
            'platform': 'Codeforces',
            'organizer': 'Codeforces',
            'mode': 'Online',
            'registration_link': 'https://codeforces.com',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'GitHub Campus Expert Program',
            'platform': 'GitHub',
            'organizer': 'GitHub Education',
            'mode': 'Online',
            'registration_link': 'https://education.github.com/experts',
            'fresher_friendly': True,
            'status': 'Live'
        }
    ]
    
    # Calculate stats
    platforms = set(h['platform'] for h in hackathons)
    fresher_count = len([h for h in hackathons if h.get('fresher_friendly')])
    
    return jsonify({
        'hackathons': hackathons,
        'total': len(hackathons),
        'platform_count': len(platforms),
        'fresher_count': fresher_count,
        'last_updated': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)