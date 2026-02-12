import requests
from bs4 import BeautifulSoup
import time

class IndiaHackathonScraper:
    """Scraper specifically for Indian hackathon platforms"""
    
    def __init__(self):
        self.hackathons = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_techgig(self):
        """Scrape TechGig hackathons"""
        print("🔍 Scraping TechGig...")
        try:
            url = "https://www.techgig.com/challenge"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            challenges = soup.find_all('div', class_='challenge-card')
            
            for challenge in challenges[:10]:
                try:
                    title_elem = challenge.find('h3') or challenge.find('h4')
                    title = title_elem.text.strip() if title_elem else "TechGig Challenge"
                    
                    link_elem = challenge.find('a')
                    link = link_elem['href'] if link_elem else ''
                    if not link.startswith('http'):
                        link = f"https://www.techgig.com{link}"
                    
                    hackathon = {
                        'name': title,
                        'platform': 'TechGig',
                        'registration_link': link,
                        'mode': 'Online',
                        'fresher_friendly': True,
                        'status': 'Live',
                        'organizer': 'TechGig'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {title[:50]}")
                except:
                    continue
            
            print(f"✅ TechGig: Found {len([h for h in self.hackathons if h['platform'] == 'TechGig'])} hackathons\n")
            
        except Exception as e:
            print(f"❌ TechGig error: {e}\n")
    
    def scrape_hackerrank(self):
        """Scrape HackerRank contests"""
        print("🔍 Scraping HackerRank...")
        try:
            url = "https://www.hackerrank.com/contests"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find contest sections
            contest_sections = soup.find_all('div', class_='contest-card')
            
            if not contest_sections:
                # Alternative: find by links
                contest_links = soup.find_all('a', href=lambda x: x and '/contests/' in str(x))
                for link in contest_links[:10]:
                    try:
                        name = link.text.strip() or "HackerRank Contest"
                        href = link['href']
                        if not href.startswith('http'):
                            href = f"https://www.hackerrank.com{href}"
                        
                        hackathon = {
                            'name': name,
                            'platform': 'HackerRank',
                            'registration_link': href,
                            'mode': 'Online',
                            'fresher_friendly': True,
                            'status': 'Live'
                        }
                        self.hackathons.append(hackathon)
                        print(f"   ✓ Found: {name[:50]}")
                    except:
                        continue
            
            print(f"✅ HackerRank: Found {len([h for h in self.hackathons if h['platform'] == 'HackerRank'])} contests\n")
            
        except Exception as e:
            print(f"❌ HackerRank error: {e}\n")
    
    def scrape_skillenza(self):
        """Scrape Skillenza challenges"""
        print("🔍 Scraping Skillenza...")
        try:
            url = "https://skillenza.com/challenges"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find challenge items
            challenges = soup.find_all('div', class_='challenge-item')
            
            if not challenges:
                # Alternative selector
                challenges = soup.find_all('div', class_='card')[:10]
            
            for challenge in challenges[:8]:
                try:
                    title_elem = challenge.find('h3') or challenge.find('h4') or challenge.find('a')
                    title = title_elem.text.strip() if title_elem else "Skillenza Challenge"
                    
                    link = "https://skillenza.com/challenges"
                    
                    hackathon = {
                        'name': title,
                        'platform': 'Skillenza',
                        'registration_link': link,
                        'mode': 'Online',
                        'fresher_friendly': True,
                        'status': 'Live'
                    }
                    if title != "Skillenza Challenge":
                        self.hackathons.append(hackathon)
                        print(f"   ✓ Found: {title[:50]}")
                except:
                    continue
            
            print(f"✅ Skillenza: Found {len([h for h in self.hackathons if h['platform'] == 'Skillenza'])} challenges\n")
            
        except Exception as e:
            print(f"❌ Skillenza error: {e}\n")
    
    def scrape_dphi(self):
        """Scrape DPhi data science hackathons"""
        print("🔍 Scraping DPhi...")
        try:
            url = "https://dphi.tech/challenges/"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            challenges = soup.find_all('div', class_='challenge-card')
            
            for challenge in challenges[:8]:
                try:
                    title = challenge.find('h3').text.strip()
                    link = "https://dphi.tech/challenges/"
                    
                    hackathon = {
                        'name': f"DPhi: {title}",
                        'platform': 'DPhi',
                        'registration_link': link,
                        'mode': 'Online',
                        'fresher_friendly': True,
                        'status': 'Live',
                        'organizer': 'DPhi Tech'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {title[:50]}")
                except:
                    continue
            
            print(f"✅ DPhi: Found {len([h for h in self.hackathons if h['platform'] == 'DPhi'])} challenges\n")
            
        except Exception as e:
            print(f"❌ DPhi error: {e}\n")
    
    def get_all_india_hackathons(self):
        """Run all India-specific scrapers"""
        print("\n🇮🇳 Scraping India-specific platforms...\n")
        
        self.scrape_techgig()
        time.sleep(2)
        
        self.scrape_hackerrank()
        time.sleep(2)
        
        self.scrape_skillenza()
        time.sleep(2)
        
        self.scrape_dphi()
        
        print(f"✅ India scrapers: Found {len(self.hackathons)} total\n")
        return self.hackathons