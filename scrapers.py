import requests
from bs4 import BeautifulSoup
import time

class HackathonScraper:
    def __init__(self):
        self.hackathons = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_devpost(self):
        """Scrape Devpost hackathons"""
        print("🔍 Scraping Devpost...")
        try:
            url = "https://devpost.com/api/hackathons"
            params = {
                'status[]': 'upcoming',
                'order_by': 'submission-period-end'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                hackathons_data = data.get('hackathons', [])
                
                for hack in hackathons_data[:10]:  # Get first 10
                    hackathon = {
                        'name': hack.get('title', 'N/A'),
                        'platform': 'Devpost',
                        'registration_link': hack.get('url', ''),
                        'organizer': hack.get('displayed_location', {}).get('location', 'N/A'),
                        'mode': 'Online' if hack.get('open_state') == 'online' else 'Hybrid',
                        'prize_pool': f"${hack.get('prize_amount', 'N/A')}" if hack.get('prize_amount') else 'N/A',
                        'fresher_friendly': True,
                        'status': 'Upcoming'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {hackathon['name'][:50]}")
                
                print(f"✅ Devpost: Found {len(hackathons_data[:10])} hackathons\n")
            else:
                print(f"⚠️  Devpost returned status code: {response.status_code}\n")
                
        except Exception as e:
            print(f"❌ Devpost error: {e}\n")
    
    def scrape_mlh(self):
        """Scrape MLH (Major League Hacking) events"""
        print("🔍 Scraping MLH...")
        try:
            url = "https://mlh.io/seasons/2025/events"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # MLH uses event cards
            events = soup.find_all('div', class_='event', limit=10)
            
            for event in events:
                try:
                    name_elem = event.find('h3')
                    name = name_elem.text.strip() if name_elem else "MLH Event"
                    
                    link_elem = event.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    
                    date_elem = event.find('p', class_='event-date')
                    date = date_elem.text.strip() if date_elem else ''
                    
                    hackathon = {
                        'name': name,
                        'platform': 'MLH',
                        'registration_link': link,
                        'organizer': 'Major League Hacking',
                        'mode': 'Hybrid',
                        'event_date': date,
                        'fresher_friendly': True,
                        'status': 'Upcoming'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {name[:50]}")
                except:
                    continue
            
            mlh_count = len([h for h in self.hackathons if h['platform'] == 'MLH'])
            print(f"✅ MLH: Found {mlh_count} hackathons\n")
            
        except Exception as e:
            print(f"❌ MLH error: {e}\n")
    
    def scrape_unstop(self):
        """Scrape Unstop hackathons"""
        print("🔍 Scraping Unstop...")
        try:
            # Unstop's public listings
            url = "https://unstop.com/hackathons"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find competition cards (structure may vary)
            cards = soup.find_all('div', class_='opportunity-card', limit=10)
            
            if not cards:
                # Try alternative selectors
                cards = soup.find_all('div', attrs={'data-type': 'hackathon'}, limit=10)
            
            for card in cards:
                try:
                    title_elem = card.find('h3') or card.find('h2') or card.find('a')
                    name = title_elem.text.strip() if title_elem else "Unstop Hackathon"
                    
                    link_elem = card.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = f"https://unstop.com{link}"
                    
                    hackathon = {
                        'name': name,
                        'platform': 'Unstop',
                        'registration_link': link,
                        'mode': 'Hybrid',
                        'fresher_friendly': True,
                        'status': 'Live'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {name[:50]}")
                except:
                    continue
            
            unstop_count = len([h for h in self.hackathons if h['platform'] == 'Unstop'])
            print(f"✅ Unstop: Found {unstop_count} hackathons\n")
            
        except Exception as e:
            print(f"❌ Unstop error: {e}\n")
    
    def get_all_hackathons(self):
        """Run all scrapers"""
        print("\n" + "="*60)
        print("🚀 STARTING HACKATHON SCRAPING PROCESS")
        print("="*60 + "\n")
        
        self.scrape_devpost()
        time.sleep(2)  # Be polite to servers
        
        self.scrape_mlh()
        time.sleep(2)
        
        self.scrape_unstop()
        
        print("="*60)
        print(f"✅ SCRAPING COMPLETE: Found {len(self.hackathons)} total hackathons")
        print("="*60 + "\n")
        
        return self.hackathons


# Test the scraper independently
if __name__ == "__main__":
    scraper = HackathonScraper()
    hackathons = scraper.get_all_hackathons()
    
    print("\n📋 SAMPLE RESULTS:\n")
    for i, hack in enumerate(hackathons[:5], 1):
        print(f"{i}. {hack['name']}")
        print(f"   Platform: {hack['platform']}")
        print(f"   Link: {hack.get('registration_link', 'N/A')}")
        print(f"   Status: {hack.get('status', 'N/A')}\n")