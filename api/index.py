from flask import Flask, render_template_string, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Beautiful Dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackathon Tracker | Live Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --success: #10b981;
            --danger: #ef4444;
            --dark: #1f2937;
            --light: #f3f4f6;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            background-attachment: fixed;
        }
        
        .container {
            max-width: 1300px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header */
        header {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            animation: slideDown 0.6s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .logo-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
        }
        
        h1 {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            color: #6b7280;
            font-size: 14px;
            margin-top: 5px;
        }
        
        .live-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--success);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 14px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .live-dot {
            width: 8px;
            height: 8px;
            background: white;
            border-radius: 50%;
            animation: blink 1.5s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            position: relative;
            overflow: hidden;
            transition: all 0.3s;
            animation: fadeIn 0.6s ease;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .stat-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-bottom: 15px;
        }
        
        .stat-number {
            font-size: 36px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #6b7280;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Filters */
        .filters {
            background: white;
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
        
        .filter-row {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .filter-group {
            flex: 1;
            min-width: 200px;
        }
        
        .filter-label {
            display: block;
            color: var(--dark);
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        input, select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 14px;
            transition: all 0.3s;
            background: white;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }
        
        /* Hackathon Grid */
        .hackathons-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .hackathon-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: all 0.3s;
            animation: cardSlide 0.6s ease;
        }
        
        @keyframes cardSlide {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hackathon-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            padding: 25px;
            position: relative;
        }
        
        .card-header::after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 0;
            right: 0;
            height: 30px;
            background: inherit;
            transform: skewY(-2deg);
        }
        
        .card-title {
            color: white;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        
        .card-tags {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .tag {
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            color: white;
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .card-body {
            padding: 35px 25px 25px;
        }
        
        .info-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            color: #4b5563;
            font-size: 14px;
        }
        
        .info-item i {
            color: var(--primary);
            width: 20px;
        }
        
        .prize-badge {
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            color: white;
            padding: 10px 15px;
            border-radius: 12px;
            font-weight: 700;
            margin: 15px 0;
            display: inline-block;
            font-size: 15px;
        }
        
        .btn-register {
            display: block;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            text-align: center;
            padding: 14px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            margin-top: 15px;
        }
        
        .btn-register:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
        }
        
        /* Loading State */
        .loading {
            text-align: center;
            padding: 100px 20px;
            color: white;
        }
        
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.2);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Empty State */
        .empty {
            background: white;
            border-radius: 20px;
            padding: 60px 20px;
            text-align: center;
            color: #6b7280;
        }
        
        .empty-icon {
            font-size: 60px;
            color: #e5e7eb;
            margin-bottom: 20px;
        }
        
        /* Footer */
        footer {
            background: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin-top: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 15px;
        }
        
        .footer-links a {
            color: var(--dark);
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s;
        }
        
        .footer-links a:hover {
            color: var(--primary);
        }
        
        @media (max-width: 768px) {
            .hackathons-grid {
                grid-template-columns: 1fr;
            }
            
            .header-content {
                flex-direction: column;
                text-align: center;
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
            <div class="header-content">
                <div class="logo-section">
                    <div class="logo-icon">
                        <i class="fas fa-rocket"></i>
                    </div>
                    <div>
                        <h1>Hackathon Tracker</h1>
                        <p class="subtitle">Live hackathons for CSE students & freshers</p>
                    </div>
                </div>
                <div class="live-badge">
                    <div class="live-dot"></div>
                    <span>LIVE DATA</span>
                </div>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🏆</div>
                <div class="stat-number" id="total">0</div>
                <div class="stat-label">Live Hackathons</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🌐</div>
                <div class="stat-number" id="platforms">0</div>
                <div class="stat-label">Platforms Tracked</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-number" id="freshers">0</div>
                <div class="stat-label">Fresher Friendly</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-number" id="total-prize">$500K+</div>
                <div class="stat-label">Total Prizes</div>
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-row">
                <div class="filter-group">
                    <label class="filter-label">🔍 Search</label>
                    <input type="text" id="search" placeholder="Search hackathons..." onkeyup="filterHackathons()">
                </div>
                <div class="filter-group">
                    <label class="filter-label">📍 Platform</label>
                    <select id="platform-filter" onchange="filterHackathons()">
                        <option value="">All Platforms</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">🌍 Mode</label>
                    <select id="mode-filter" onchange="filterHackathons()">
                        <option value="">All Modes</option>
                        <option value="Online">Online</option>
                        <option value="Offline">Offline</option>
                        <option value="Hybrid">Hybrid</option>
                    </select>
                </div>
            </div>
        </div>
        
        <div id="hackathons-container">
            <div class="loading">
                <div class="loading-spinner"></div>
                <p style="font-size: 18px;">Loading awesome hackathons...</p>
            </div>
        </div>
        
        <footer>
            <div class="footer-links">
                <a href="https://github.com/Swapnilpawar17/Hackathon-tracker" target="_blank">
                    <i class="fab fa-github"></i> GitHub
                </a>
                <a href="https://www.linkedin.com/in/swapnilpawar17" target="_blank">
                    <i class="fab fa-linkedin"></i> LinkedIn
                </a>
                <a href="mailto:swapnil@example.com">
                    <i class="fas fa-envelope"></i> Contact
                </a>
            </div>
            <p style="color: #6b7280; font-size: 14px;">Built with ❤️ by Swapnil Pawar</p>
            <p id="last-updated" style="color: #9ca3af; font-size: 13px; margin-top: 10px;">Last updated: Loading...</p>
        </footer>
    </div>
    
    <script>
        let allHackathons = [];
        let filteredHackathons = [];
        
        // Animated counter
        function animateValue(id, start, end, duration) {
            const obj = document.getElementById(id);
            const range = end - start;
            const increment = range / (duration / 16);
            let current = start;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= end) {
                    current = end;
                    clearInterval(timer);
                }
                obj.textContent = Math.floor(current);
            }, 16);
        }
        
        async function loadHackathons() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();
                
                allHackathons = data.hackathons || [];
                filteredHackathons = allHackathons;
                
                // Animate stats
                animateValue('total', 0, allHackathons.length, 1000);
                animateValue('platforms', 0, data.platform_count || 0, 1000);
                animateValue('freshers', 0, data.fresher_count || 0, 1000);
                
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
                    '<div class="empty"><i class="fas fa-exclamation-triangle empty-icon"></i><h3>Error loading hackathons</h3><p>Please refresh the page</p></div>';
            }
        }
        
        function renderHackathons(hackathons) {
            const container = document.getElementById('hackathons-container');
            
            if (hackathons.length === 0) {
                container.innerHTML = '<div class="empty"><i class="fas fa-inbox empty-icon"></i><h3>No hackathons found</h3><p>Try adjusting your filters</p></div>';
                return;
            }
            
            const html = hackathons.map((hack, index) => `
                <div class="hackathon-card" style="animation-delay: ${index * 0.05}s">
                    <div class="card-header">
                        <div class="card-title">${hack.name}</div>
                        <div class="card-tags">
                            <span class="tag">${hack.platform}</span>
                            <span class="tag">${hack.mode || 'Online'}</span>
                            <span class="tag">🔴 LIVE</span>
                        </div>
                    </div>
                    <div class="card-body">
                        ${hack.organizer ? `
                            <div class="info-item">
                                <i class="fas fa-building"></i>
                                <span>${hack.organizer}</span>
                            </div>
                        ` : ''}
                        ${hack.fresher_friendly ? `
                            <div class="info-item">
                                <i class="fas fa-check-circle" style="color: var(--success);"></i>
                                <span style="color: var(--success); font-weight: 600;">Fresher Friendly</span>
                            </div>
                        ` : ''}
                        ${hack.prize_pool && hack.prize_pool !== 'N/A' ? 
                            `<div class="prize-badge">🏆 ${hack.prize_pool}</div>` : ''}
                        ${hack.registration_link ? 
                            `<a href="${hack.registration_link}" target="_blank" class="btn-register">
                                Register Now <i class="fas fa-arrow-right" style="margin-left: 5px;"></i>
                            </a>` : ''}
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = `<div class="hackathons-grid">${html}</div>`;
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

# Get static hackathon data
def get_hackathon_data():
    return [
        {
            'name': 'Smart India Hackathon 2025',
            'platform': 'Government',
            'organizer': 'Government of India',
            'mode': 'Hybrid',
            'registration_link': 'https://www.sih.gov.in/',
            'prize_pool': '₹1,00,000 per team',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Google Solution Challenge 2025',
            'platform': 'Google',
            'organizer': 'Google Developer Student Clubs',
            'mode': 'Online',
            'registration_link': 'https://developers.google.com/community/gdsc-solution-challenge',
            'prize_pool': '$3,000 + Mentorship',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Microsoft Imagine Cup 2025',
            'platform': 'Microsoft',
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
            'registration_link': 'https://unstop.com/hackathons/flipkart-grid-60-software-development-track-flipkart-grid-60-flipkart-1024802',
            'prize_pool': '₹50,00,000',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'AWS DeepRacer Student League',
            'platform': 'AWS',
            'organizer': 'Amazon Web Services',
            'mode': 'Online',
            'registration_link': 'https://aws.amazon.com/deepracer/student/',
            'prize_pool': 'Scholarships + AWS Credits',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Schneider Go Green 2025',
            'platform': 'Unstop',
            'organizer': 'Schneider Electric',
            'mode': 'Online',
            'registration_link': 'https://unstop.com/hackathons/schneider-go-green-2025-schneider-electric-872499',
            'prize_pool': 'Trip to Paris + Jobs',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Wells Fargo Global Analytics Challenge',
            'platform': 'Unstop',
            'organizer': 'Wells Fargo',
            'mode': 'Online',
            'registration_link': 'https://unstop.com/competitions/wells-fargo-global-analytics-challenge-2025-wells-fargo-892631',
            'prize_pool': '₹2,00,000',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Global Hack Week: GenAI',
            'platform': 'MLH',
            'organizer': 'Major League Hacking',
            'mode': 'Hybrid',
            'registration_link': 'https://events.mlh.io/events/12402',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Codeforces Round (Div. 2)',
            'platform': 'Codeforces',
            'organizer': 'Codeforces',
            'mode': 'Online',
            'registration_link': 'https://codeforces.com/contests',
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
        },
        {
            'name': 'Red Bull Basement 2025',
            'platform': 'Red Bull',
            'organizer': 'Red Bull',
            'mode': 'Hybrid',
            'registration_link': 'https://www.redbull.com/basement',
            'prize_pool': 'Global Summit + Mentorship',
            'fresher_friendly': True,
            'status': 'Live'
        },
        {
            'name': 'Meta Hacker Cup 2025',
            'platform': 'Meta',
            'organizer': 'Meta (Facebook)',
            'mode': 'Online',
            'registration_link': 'https://www.facebook.com/codingcompetitions/hacker-cup',
            'prize_pool': '$20,000',
            'fresher_friendly': True,
            'status': 'Live'
        }
    ]

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/data')
def api_data():
    hackathons = get_hackathon_data()
    
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

# Vercel requires the app to be exposed
handler = app