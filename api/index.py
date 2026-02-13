from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
from urllib.parse import urlparse

# Hackathon Data
HACKATHONS = [
    {
        "name": "Smart India Hackathon 2025",
        "platform": "Government",
        "organizer": "Government of India",
        "mode": "Hybrid",
        "registration_link": "https://www.sih.gov.in/",
        "prize_pool": "₹1,00,000 per team",
        "fresher_friendly": True
    },
    {
        "name": "Google Solution Challenge 2025",
        "platform": "Google",
        "organizer": "Google Developer Student Clubs",
        "mode": "Online",
        "registration_link": "https://developers.google.com/community/gdsc-solution-challenge",
        "prize_pool": "$3,000 + Mentorship",
        "fresher_friendly": True
    },
    {
        "name": "Microsoft Imagine Cup 2025",
        "platform": "Microsoft",
        "organizer": "Microsoft",
        "mode": "Online",
        "registration_link": "https://imaginecup.microsoft.com/",
        "prize_pool": "$100,000",
        "fresher_friendly": True
    },
    {
        "name": "Flipkart GRiD 6.0",
        "platform": "Unstop",
        "organizer": "Flipkart",
        "mode": "Online",
        "registration_link": "https://unstop.com/hackathons/flipkart-grid",
        "prize_pool": "₹50,00,000",
        "fresher_friendly": True
    },
    {
        "name": "AWS DeepRacer Student League",
        "platform": "AWS",
        "organizer": "Amazon Web Services",
        "mode": "Online",
        "registration_link": "https://aws.amazon.com/deepracer/student/",
        "prize_pool": "Scholarships + AWS Credits",
        "fresher_friendly": True
    },
    {
        "name": "Schneider Go Green 2025",
        "platform": "Unstop",
        "organizer": "Schneider Electric",
        "mode": "Online",
        "registration_link": "https://unstop.com",
        "prize_pool": "Trip to Paris + Jobs",
        "fresher_friendly": True
    },
    {
        "name": "Global Hack Week GenAI",
        "platform": "MLH",
        "organizer": "Major League Hacking",
        "mode": "Hybrid",
        "registration_link": "https://mlh.io",
        "prize_pool": "Swag + Experience",
        "fresher_friendly": True
    },
    {
        "name": "Codeforces Round",
        "platform": "Codeforces",
        "organizer": "Codeforces",
        "mode": "Online",
        "registration_link": "https://codeforces.com",
        "prize_pool": "Rating Points",
        "fresher_friendly": True
    },
    {
        "name": "GitHub Campus Expert",
        "platform": "GitHub",
        "organizer": "GitHub Education",
        "mode": "Online",
        "registration_link": "https://education.github.com/experts",
        "prize_pool": "Swag + Training",
        "fresher_friendly": True
    },
    {
        "name": "Meta Hacker Cup 2025",
        "platform": "Meta",
        "organizer": "Meta",
        "mode": "Online",
        "registration_link": "https://facebook.com/codingcompetitions",
        "prize_pool": "$20,000",
        "fresher_friendly": True
    }
]

def get_html():
    cards_html = ""
    for h in HACKATHONS:
        fresher_badge = '<div class="info" style="color:#10b981;">✅ Fresher Friendly</div>' if h.get('fresher_friendly') else ''
        prize_badge = f'<div class="prize">🏆 {h["prize_pool"]}</div>' if h.get('prize_pool') else ''
        
        cards_html += f'''
        <div class="card">
            <div class="card-header">
                <div class="card-title">{h["name"]}</div>
                <div class="tags">
                    <span class="tag">{h["platform"]}</span>
                    <span class="tag">{h["mode"]}</span>
                    <span class="tag">🔴 LIVE</span>
                </div>
            </div>
            <div class="card-body">
                <div class="info"><strong>Organizer:</strong> {h["organizer"]}</div>
                {fresher_badge}
                {prize_badge}
                <a href="{h["registration_link"]}" target="_blank" class="btn">Register Now →</a>
            </div>
        </div>
        '''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackathon Tracker</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Inter, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        h1 {{
            font-size: 32px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .subtitle {{ color: #666; }}
        .live-badge {{
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-top: 15px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }}
        .stat-number {{
            font-size: 36px;
            font-weight: 800;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}
        .card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: transform 0.3s;
        }}
        .card:hover {{ transform: translateY(-10px); }}
        .card-header {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 20px;
            color: white;
        }}
        .card-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .tags {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .tag {{
            background: rgba(255,255,255,0.2);
            padding: 4px 10px;
            border-radius: 5px;
            font-size: 12px;
        }}
        .card-body {{ padding: 20px; }}
        .info {{ margin-bottom: 10px; color: #555; font-size: 14px; }}
        .prize {{
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            color: white;
            padding: 8px 15px;
            border-radius: 10px;
            font-weight: 600;
            display: inline-block;
            margin: 10px 0;
        }}
        .btn {{
            display: block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-align: center;
            padding: 14px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.3s;
        }}
        .btn:hover {{ transform: scale(1.03); }}
        footer {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            margin-top: 30px;
            color: #666;
        }}
        footer a {{ color: #667eea; text-decoration: none; margin: 0 15px; }}
        @media (max-width: 768px) {{
            .grid {{ grid-template-columns: 1fr; }}
            h1 {{ font-size: 24px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Hackathon Tracker</h1>
            <p class="subtitle">Live hackathons for CSE students & freshers</p>
            <span class="live-badge">🔴 LIVE DATA</span>
        </header>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(HACKATHONS)}</div>
                <div class="stat-label">Live Hackathons</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(set(h["platform"] for h in HACKATHONS))}</div>
                <div class="stat-label">Platforms</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([h for h in HACKATHONS if h.get("fresher_friendly")])}</div>
                <div class="stat-label">Fresher Friendly</div>
            </div>
        </div>
        <div class="grid">
            {cards_html}
        </div>
        <footer>
            <p>Built with ❤️ by Swapnil Pawar</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/Swapnilpawar17" target="_blank">GitHub</a>
                <a href="https://linkedin.com/in/swapnilpawar17" target="_blank">LinkedIn</a>
            </p>
            <p style="margin-top: 10px; font-size: 12px; color: #999;">
                Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
            </p>
        </footer>
    </div>
</body>
</html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(get_html().encode())
        return