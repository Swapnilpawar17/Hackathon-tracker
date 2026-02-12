import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class EmailNotifier:
    def __init__(self):
        # Email configuration - Update these in your .env file
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.sender_password = os.getenv("EMAIL_PASSWORD")  # App password for Gmail
        self.recipient_email = os.getenv("EMAIL_RECIPIENT")
    
    def create_hackathon_html(self, hackathons):
        """Create beautiful HTML email for hackathons"""
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 700px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 28px;
                }
                .header p {
                    margin: 10px 0 0 0;
                    opacity: 0.9;
                }
                .content {
                    padding: 30px;
                }
                .stats {
                    display: flex;
                    justify-content: space-around;
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin-bottom: 25px;
                }
                .stat {
                    text-align: center;
                }
                .stat-number {
                    font-size: 32px;
                    font-weight: bold;
                    color: #667eea;
                }
                .stat-label {
                    color: #666;
                    font-size: 14px;
                }
                .hackathon-card {
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 15px;
                    transition: box-shadow 0.3s;
                }
                .hackathon-card:hover {
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }
                .hackathon-name {
                    font-size: 18px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                .hackathon-details {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin-bottom: 15px;
                }
                .detail {
                    background-color: #f0f0f0;
                    padding: 5px 12px;
                    border-radius: 15px;
                    font-size: 13px;
                    color: #555;
                }
                .platform {
                    background-color: #667eea;
                    color: white;
                }
                .mode {
                    background-color: #28a745;
                    color: white;
                }
                .status-live {
                    background-color: #dc3545;
                    color: white;
                }
                .register-btn {
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 10px 25px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 14px;
                }
                .footer {
                    background-color: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #666;
                    font-size: 13px;
                }
                .divider {
                    height: 1px;
                    background-color: #e0e0e0;
                    margin: 25px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 New Hackathons Found!</h1>
                    <p>Your weekly hackathon digest is here</p>
                </div>
                <div class="content">
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">""" + str(len(hackathons)) + """</div>
                            <div class="stat-label">New Hackathons</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">""" + str(len(set(h.get('platform', '') for h in hackathons))) + """</div>
                            <div class="stat-label">Platforms</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">""" + str(len([h for h in hackathons if h.get('fresher_friendly')])) + """</div>
                            <div class="stat-label">Fresher Friendly</div>
                        </div>
                    </div>
                    
                    <h2 style="color: #333; margin-bottom: 20px;">📋 Latest Hackathons</h2>
        """
        
        # Add hackathon cards
        for hack in hackathons[:10]:  # Limit to 10 in email
            html += f"""
                    <div class="hackathon-card">
                        <div class="hackathon-name">{hack.get('name', 'Unknown Hackathon')}</div>
                        <div class="hackathon-details">
                            <span class="detail platform">{hack.get('platform', 'Unknown')}</span>
                            <span class="detail mode">{hack.get('mode', 'Online')}</span>
                            <span class="detail status-live">{hack.get('status', 'Live')}</span>
                        </div>
            """
            
            if hack.get('organizer'):
                html += f'<p style="color: #666; margin: 5px 0;">🏢 Organizer: {hack.get("organizer")}</p>'
            
            if hack.get('prize_pool') and hack.get('prize_pool') != 'N/A':
                html += f'<p style="color: #666; margin: 5px 0;">🏆 Prize: {hack.get("prize_pool")}</p>'
            
            if hack.get('registration_link'):
                html += f'''
                        <a href="{hack.get('registration_link')}" class="register-btn">Register Now →</a>
                '''
            
            html += """
                    </div>
            """
        
        # Footer
        html += """
                    <div class="divider"></div>
                    <p style="text-align: center; color: #666;">
                        Want to see all hackathons? Check your Notion database!
                    </p>
                </div>
                <div class="footer">
                    <p>🎯 Hackathon Tracker | Built for CSE Freshers 2025</p>
                    <p>This email was automatically generated on """ + datetime.now().strftime('%B %d, %Y at %I:%M %p') + """</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def create_plain_text(self, hackathons):
        """Create plain text version of email"""
        text = f"""
🚀 NEW HACKATHONS FOUND!
========================
Date: {datetime.now().strftime('%B %d, %Y')}
Total New Hackathons: {len(hackathons)}

📋 HACKATHON LIST:
------------------
"""
        for i, hack in enumerate(hackathons[:10], 1):
            text += f"""
{i}. {hack.get('name', 'Unknown')}
   Platform: {hack.get('platform', 'Unknown')}
   Mode: {hack.get('mode', 'Online')}
   Status: {hack.get('status', 'Live')}
   Link: {hack.get('registration_link', 'N/A')}
"""
        
        text += """
------------------
Check your Notion database for the complete list!

🎯 Hackathon Tracker - Built for CSE Freshers 2025
"""
        return text
    
    def send_notification(self, hackathons, subject=None):
        """Send email notification with new hackathons"""
        
        if not self.sender_email or not self.sender_password or not self.recipient_email:
            print("⚠️  Email not configured. Set EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT in .env")
            return False
        
        if not hackathons:
            print("ℹ️  No new hackathons to notify about.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject or f"🚀 {len(hackathons)} New Hackathons Found! - {datetime.now().strftime('%b %d, %Y')}"
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            # Attach both plain text and HTML versions
            plain_text = self.create_plain_text(hackathons)
            html_content = self.create_hackathon_html(hackathons)
            
            part1 = MIMEText(plain_text, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            print("📧 Sending email notification...")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
            
            print(f"✅ Email sent successfully to {self.recipient_email}!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Email authentication failed. Check your email and app password.")
            print("💡 For Gmail, use App Password: https://myaccount.google.com/apppasswords")
            return False
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False


# Test email
if __name__ == "__main__":
    notifier = EmailNotifier()
    
    # Test with sample hackathons
    test_hackathons = [
        {
            'name': 'Test Hackathon 2025',
            'platform': 'Devpost',
            'mode': 'Online',
            'status': 'Live',
            'organizer': 'Test Org',
            'prize_pool': '$10,000',
            'registration_link': 'https://example.com',
            'fresher_friendly': True
        }
    ]
    
    notifier.send_notification(test_hackathons)