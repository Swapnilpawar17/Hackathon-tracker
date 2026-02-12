import webbrowser
import json
from datetime import datetime

class SimpleNotifier:
    """Simple notification system without email passwords"""
    
    def __init__(self):
        self.log_file = "hackathon_notifications.json"
    
    def save_notification(self, hackathons):
        """Save new hackathons to a JSON file"""
        notification_data = {
            "timestamp": datetime.now().isoformat(),
            "count": len(hackathons),
            "hackathons": hackathons[:20]  # Save top 20
        }
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(notification_data, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Notification saved to {self.log_file}")
        return True
    
    def create_html_report(self, hackathons):
        """Create an HTML file and open it in browser"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🚀 LIVE Hackathons - {datetime.now().strftime('%B %d, %Y')}</title>
            <meta charset="utf-8">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px;
                    text-align: center;
                }}
                
                .header h1 {{
                    font-size: 36px;
                    margin-bottom: 10px;
                }}
                
                .header p {{
                    font-size: 18px;
                    opacity: 0.95;
                }}
                
                .stats {{
                    display: flex;
                    justify-content: space-around;
                    padding: 30px;
                    background: #f8f9fa;
                    border-bottom: 2px solid #e9ecef;
                }}
                
                .stat-box {{
                    text-align: center;
                }}
                
                .stat-number {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #667eea;
                    display: block;
                }}
                
                .stat-label {{
                    font-size: 14px;
                    color: #6c757d;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .content {{
                    padding: 30px;
                }}
                
                .hackathon-card {{
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    border-radius: 10px;
                    padding: 25px;
                    margin-bottom: 20px;
                    transition: transform 0.3s, box-shadow 0.3s;
                }}
                
                .hackathon-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                }}
                
                .hackathon-name {{
                    font-size: 22px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 15px;
                }}
                
                .hackathon-details {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-bottom: 15px;
                }}
                
                .tag {{
                    display: inline-block;
                    padding: 6px 15px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                
                .tag-platform {{
                    background: #667eea;
                    color: white;
                }}
                
                .tag-mode {{
                    background: #28a745;
                    color: white;
                }}
                
                .tag-status {{
                    background: #dc3545;
                    color: white;
                }}
                
                .info-row {{
                    margin: 10px 0;
                    color: #495057;
                    font-size: 15px;
                }}
                
                .info-row strong {{
                    color: #2c3e50;
                }}
                
                .register-btn {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 15px;
                    transition: transform 0.3s, box-shadow 0.3s;
                    margin-top: 10px;
                }}
                
                .register-btn:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
                }}
                
                .footer {{
                    background: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    color: #6c757d;
                    font-size: 14px;
                }}
                
                .badge-live {{
                    display: inline-block;
                    background: #dc3545;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: bold;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    animation: pulse 2s infinite;
                    margin-left: 10px;
                }}
                
                @keyframes pulse {{
                    0% {{ opacity: 1; }}
                    50% {{ opacity: 0.7; }}
                    100% {{ opacity: 1; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 LIVE Hackathons Found!</h1>
                    <p>Active competitions accepting registrations now</p>
                </div>
                
                <div class="stats">
                    <div class="stat-box">
                        <span class="stat-number">{len(hackathons)}</span>
                        <span class="stat-label">Live Hackathons</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-number">{len(set(h.get('platform', '') for h in hackathons))}</span>
                        <span class="stat-label">Platforms</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-number">{len([h for h in hackathons if h.get('fresher_friendly')])}</span>
                        <span class="stat-label">Fresher Friendly</span>
                    </div>
                </div>
                
                <div class="content">
                    <h2 style="color: #2c3e50; margin-bottom: 25px;">
                        📋 Active Hackathons 
                        <span class="badge-live">LIVE</span>
                    </h2>
        """
        
        # Add hackathon cards
        for i, hack in enumerate(hackathons[:20], 1):  # Show up to 20
            prize = hack.get('prize_pool', 'N/A')
            if prize == 'N/A' or not prize:
                prize = 'Prizes to be announced'
            
            html_content += f"""
                    <div class="hackathon-card">
                        <div class="hackathon-name">
                            {i}. {hack.get('name', 'Unknown Hackathon')}
                        </div>
                        <div class="hackathon-details">
                            <span class="tag tag-platform">{hack.get('platform', 'Unknown')}</span>
                            <span class="tag tag-mode">{hack.get('mode', 'Online')}</span>
                            <span class="tag tag-status">LIVE NOW</span>
                        </div>
            """
            
            if hack.get('organizer'):
                html_content += f'<div class="info-row"><strong>🏢 Organizer:</strong> {hack.get("organizer")}</div>'
            
            if prize:
                html_content += f'<div class="info-row"><strong>🏆 Prize Pool:</strong> {prize}</div>'
            
            if hack.get('fresher_friendly'):
                html_content += f'<div class="info-row"><strong>✅ Fresher Friendly:</strong> Perfect for beginners!</div>'
            
            if hack.get('registration_link'):
                html_content += f'''
                        <a href="{hack.get('registration_link')}" target="_blank" class="register-btn">
                            Register Now →
                        </a>
                '''
            
            html_content += """
                    </div>
            """
        
        # Footer
        html_content += f"""
                </div>
                <div class="footer">
                    <p><strong>🎯 Hackathon Tracker - For CSE Freshers 2025</strong></p>
                    <p>Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p style="margin-top: 15px; font-size: 12px;">
                        All hackathons shown are currently LIVE and accepting registrations.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save HTML file
        filename = f"live_hackathons_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Open in browser
        webbrowser.open(filename)
        
        print(f"✅ Report opened in browser: {filename}")
        return filename
    
    def send_notification(self, hackathons):
        """Main notification method"""
        if not hackathons:
            print("ℹ️ No new hackathons to notify about.")
            return False
        
        print(f"\n📢 NOTIFICATION: {len(hackathons)} new LIVE hackathons found!\n")
        
        # Save to JSON
        self.save_notification(hackathons)
        
        # Create and open HTML report
        self.create_html_report(hackathons)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 NEW LIVE HACKATHONS SUMMARY")
        print("="*60)
        
        for i, hack in enumerate(hackathons[:5], 1):
            print(f"\n{i}. {hack.get('name', 'Unknown')}")
            print(f"   Platform: {hack.get('platform', 'Unknown')}")
            print(f"   Mode: {hack.get('mode', 'Online')}")
            print(f"   Prize: {hack.get('prize_pool', 'N/A')}")
            print(f"   Link: {hack.get('registration_link', 'N/A')}")
        
        if len(hackathons) > 5:
            print(f"\n   ... and {len(hackathons) - 5} more LIVE hackathons!")
        
        print("\n" + "="*60 + "\n")
        
        return True

# Test
if __name__ == "__main__":
    notifier = SimpleNotifier()
    
    test_hackathons = [
        {
            'name': 'Test Hackathon 2025',
            'platform': 'Unstop',
            'mode': 'Online',
            'status': 'Live',
            'organizer': 'Test Org',
            'prize_pool': '₹50,000',
            'registration_link': 'https://unstop.com',
            'fresher_friendly': True
        }
    ]
    
    notifier.send_notification(test_hackathons)