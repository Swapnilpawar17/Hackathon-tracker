import requests
from bs4 import BeautifulSoup
import time

class HackathonScraper:
    def __init__(self):
        self.hackathons = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_devpost(self):
        """Scrape Devpost hackathons - using HTML instead of API"""
        print("🔍 Scraping Devpost...")
        try:
            url = "https://devpost.com/hackathons"
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find hackathon cards
                cards = soup.find_all('div', class_='hackathon-tile')
                
                if not cards:
                    # Try alternative selector
                    cards = soup.find_all('article')
                
                for card in cards[:10]:
                    try:
                        # Find title
                        title_elem = card.find('h2') or card.find('h3') or card.find('a', class_='title')
                        name = title_elem.text.strip() if title_elem else None
                        
                        if not name:
                            continue
                        
                        # Find link
                        link_elem = card.find('a')
                        link = link_elem.get('href', '') if link_elem else ''
                        if link and not link.startswith('http'):
                            link = f"https://devpost.com{link}"
                        
                        hackathon = {
                            'name': name,
                            'platform': 'Devpost',
                            'registration_link': link,
                            'mode': 'Online',
                            'fresher_friendly': True,
                            'status': 'Live'
                        }
                        self.hackathons.append(hackathon)
                        print(f"   ✓ Found: {name[:50]}")
                    except:
                        continue
                
                devpost_count = len([h for h in self.hackathons if h['platform'] == 'Devpost'])
                print(f"✅ Devpost: Found {devpost_count} hackathons\n")
            else:
                print(f"⚠️  Devpost: Status code {response.status_code}\n")
                
        except Exception as e:
            print(f"❌ Devpost error: {e}\n")
    
    def scrape_mlh(self):
        """Scrape MLH events"""
        print("🔍 Scraping MLH...")
        try:
            # MLH Season page
            url = "https://mlh.io/seasons/2025/events"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all event containers
            events = soup.find_all('div', class_='event')
            
            if not events:
                # Try finding by different selector
                events = soup.find_all('a', href=lambda x: x and 'mlh.io' in str(x))
            
            for event in events[:10]:
                try:
                    # Get event name
                    name_elem = event.find('h3') or event.find('h2')
                    if name_elem:
                        name = name_elem.text.strip()
                    else:
                        name_elem = event.find('img', alt=True)
                        name = name_elem.get('alt', 'MLH Event') if name_elem else 'MLH Event'
                    
                    # Get link
                    link = event.get('href', '') if event.name == 'a' else ''
                    if not link:
                        link_elem = event.find('a')
                        link = link_elem.get('href', '') if link_elem else ''
                    
                    if name and name != 'MLH Event':
                        hackathon = {
                            'name': name,
                            'platform': 'MLH',
                            'registration_link': link,
                            'organizer': 'Major League Hacking',
                            'mode': 'Hybrid',
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
    
    def scrape_hackerearth(self):
        """Scrape HackerEarth challenges"""
        print("🔍 Scraping HackerEarth...")
        try:
            url = "https://www.hackerearth.com/challenges/"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find challenge cards
            challenges = soup.find_all('div', class_='challenge-card')
            
            for challenge in challenges[:5]:
                try:
                    title_elem = challenge.find('div', class_='challenge-name') or challenge.find('h5')
                    name = title_elem.text.strip() if title_elem else None
                    
                    if not name or 'hiring' in name.lower():
                        continue
                    
                    link_elem = challenge.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = f"https://www.hackerearth.com{link}"
                    
                    hackathon = {
                        'name': name,
                        'platform': 'HackerEarth',
                        'registration_link': link,
                        'mode': 'Online',
                        'fresher_friendly': True,
                        'status': 'Live'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {name[:50]}")
                except:
                    continue
            
            he_count = len([h for h in self.hackathons if h['platform'] == 'HackerEarth'])
            print(f"✅ HackerEarth: Found {he_count} hackathons\n")
            
        except Exception as e:
            print(f"❌ HackerEarth error: {e}\n")
    
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
    
    def scrape_codechef(self):
        """Scrape CodeChef hackathons and contests"""
        print("🔍 Scraping CodeChef...")
        try:
            url = "https://www.codechef.com/contests"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find contest tables
            contest_tables = soup.find_all('table', class_='dataTable')
            
            for table in contest_tables[:2]:  # Future and Present contests
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows[:5]:  # Limit to 5 per table
                    try:
                        cols = row.find_all('td')
                        if len(cols) >= 4:
                            # Extract contest info
                            code = cols[0].text.strip()
                            name = cols[1].text.strip()
                            
                            # Skip if not a hackathon (filter by keywords)
                            hackathon_keywords = ['hack', 'thon', 'challenge', 'fest', 'build']
                            if not any(keyword in name.lower() for keyword in hackathon_keywords):
                                continue
                            
                            link = cols[1].find('a')
                            link_url = f"https://www.codechef.com{link.get('href', '')}" if link else ''
                            
                            start_date = cols[2].text.strip()
                            end_date = cols[3].text.strip()
                            
                            hackathon = {
                                'name': name,
                                'platform': 'CodeChef',
                                'registration_link': link_url,
                                'mode': 'Online',
                                'event_date': f"{start_date} - {end_date}",
                                'fresher_friendly': True,
                                'status': 'Upcoming' if 'Future' in str(table) else 'Live'
                            }
                            self.hackathons.append(hackathon)
                            print(f"   ✓ Found: {name[:50]}")
                    except:
                        continue
            
            cc_count = len([h for h in self.hackathons if h['platform'] == 'CodeChef'])
            print(f"✅ CodeChef: Found {cc_count} hackathons\n")
            
        except Exception as e:
            print(f"❌ CodeChef error: {e}\n")
    
    def scrape_kaggle(self):
        """Scrape Kaggle competitions suitable for students"""
        print("🔍 Scraping Kaggle...")
        try:
            # Kaggle competitions API endpoint
            url = "https://www.kaggle.com/competitions"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find competition cards
            competitions = soup.find_all('div', class_='competition-tile')
            
            if not competitions:
                # Alternative selector
                competitions = soup.find_all('a', href=lambda x: x and '/competitions/' in str(x))[:10]
            
            for comp in competitions[:10]:
                try:
                    # Extract competition details
                    title_elem = comp.find('div', class_='competition-tile__title') or comp
                    title = title_elem.text.strip() if hasattr(title_elem, 'text') else str(title_elem)
                    
                    # Get link
                    link_elem = comp if comp.name == 'a' else comp.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = f"https://www.kaggle.com{link}"
                    
                    # Prize info
                    prize_elem = comp.find('div', class_='competition-tile__prize')
                    prize = prize_elem.text.strip() if prize_elem else 'Knowledge & Experience'
                    
                    hackathon = {
                        'name': f"Kaggle: {title[:100]}",
                        'platform': 'Kaggle',
                        'registration_link': link,
                        'mode': 'Online',
                        'prize_pool': prize,
                        'fresher_friendly': True,
                        'status': 'Live',
                        'organizer': 'Kaggle'
                    }
                    
                    # Only add if it seems relevant
                    if title and link:
                        self.hackathons.append(hackathon)
                        print(f"   ✓ Found: {title[:50]}")
                except:
                    continue
            
            kaggle_count = len([h for h in self.hackathons if h['platform'] == 'Kaggle'])
            print(f"✅ Kaggle: Found {kaggle_count} competitions\n")
            
        except Exception as e:
            print(f"❌ Kaggle error: {e}\n")
    
    def scrape_leetcode(self):
        """Scrape LeetCode contests and hackathons"""
        print("🔍 Scraping LeetCode...")
        try:
            # LeetCode contest page
            url = "https://leetcode.com/contest/"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find upcoming contests
            contest_cards = soup.find_all('div', class_='contest-card')
            
            for card in contest_cards[:5]:
                try:
                    # Extract contest name
                    name_elem = card.find('div', class_='contest-title')
                    name = name_elem.text.strip() if name_elem else "LeetCode Contest"
                    
                    # Time info
                    time_elem = card.find('div', class_='contest-time')
                    time_info = time_elem.text.strip() if time_elem else ""
                    
                    hackathon = {
                        'name': name,
                        'platform': 'LeetCode',
                        'registration_link': 'https://leetcode.com/contest/',
                        'mode': 'Online',
                        'event_date': time_info,
                        'fresher_friendly': True,
                        'status': 'Upcoming',
                        'organizer': 'LeetCode'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {name}")
                except:
                    continue
            
            lc_count = len([h for h in self.hackathons if h['platform'] == 'LeetCode'])
            print(f"✅ LeetCode: Found {lc_count} contests\n")
            
        except Exception as e:
            print(f"❌ LeetCode error: {e}\n")
    
    def scrape_codeforces(self):
        """Scrape Codeforces contests"""
        print("🔍 Scraping Codeforces...")
        try:
            # Codeforces API
            url = "https://codeforces.com/api/contest.list"
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK':
                    contests = data['result']
                    
                    # Filter upcoming contests
                    for contest in contests[:10]:
                        if contest['phase'] == 'BEFORE':  # Upcoming contests
                            hackathon = {
                                'name': contest['name'],
                                'platform': 'Codeforces',
                                'registration_link': f"https://codeforces.com/contest/{contest['id']}",
                                'mode': 'Online',
                                'event_date': time.strftime('%Y-%m-%d %H:%M', time.gmtime(contest['startTimeSeconds'])),
                                'fresher_friendly': True,
                                'status': 'Upcoming',
                                'organizer': 'Codeforces'
                            }
                            self.hackathons.append(hackathon)
                            print(f"   ✓ Found: {contest['name'][:50]}")
                    
                    cf_count = len([h for h in self.hackathons if h['platform'] == 'Codeforces'])
                    print(f"✅ Codeforces: Found {cf_count} contests\n")
            
        except Exception as e:
            print(f"❌ Codeforces error: {e}\n")
    
    def scrape_github(self):
        """Scrape GitHub for hackathon repositories"""
        print("🔍 Scraping GitHub Hackathons...")
        try:
            # Search GitHub for recent hackathon repos
            url = "https://api.github.com/search/repositories"
            params = {
                'q': 'hackathon 2025 OR hackathon 2026',
                'sort': 'updated',
                'order': 'desc',
                'per_page': 10
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                for repo in data.get('items', []):
                    # Filter for actual hackathon events
                    if 'hackathon' in repo['name'].lower() or 'hackathon' in repo.get('description', '').lower():
                        hackathon = {
                            'name': repo['name'].replace('-', ' ').replace('_', ' ').title(),
                            'platform': 'GitHub',
                            'registration_link': repo['html_url'],
                            'mode': 'Online',
                            'organizer': repo['owner']['login'],
                            'fresher_friendly': True,
                            'status': 'Live'
                        }
                        self.hackathons.append(hackathon)
                        print(f"   ✓ Found: {repo['name'][:50]}")
                
                gh_count = len([h for h in self.hackathons if h['platform'] == 'GitHub'])
                print(f"✅ GitHub: Found {gh_count} hackathons\n")
            
        except Exception as e:
            print(f"❌ GitHub error: {e}\n")
    
    def scrape_gfg(self):
        """Scrape GeeksforGeeks contests and hackathons"""
        print("🔍 Scraping GeeksforGeeks...")
        try:
            url = "https://practice.geeksforgeeks.org/events"
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find event cards
            events = soup.find_all('div', class_='event_card')
            
            for event in events[:8]:
                try:
                    # Extract event details
                    title_elem = event.find('div', class_='event_head')
                    title = title_elem.text.strip() if title_elem else "GFG Event"
                    
                    # Get link
                    link_elem = event.find('a')
                    link = link_elem.get('href', '') if link_elem else ''
                    if link and not link.startswith('http'):
                        link = f"https://practice.geeksforgeeks.org{link}"
                    
                    # Date info
                    date_elem = event.find('div', class_='event_timings')
                    date_info = date_elem.text.strip() if date_elem else ""
                    
                    hackathon = {
                        'name': title,
                        'platform': 'GeeksforGeeks',
                        'registration_link': link,
                        'mode': 'Online',
                        'event_date': date_info,
                        'fresher_friendly': True,
                        'status': 'Upcoming',
                        'organizer': 'GeeksforGeeks'
                    }
                    self.hackathons.append(hackathon)
                    print(f"   ✓ Found: {title[:50]}")
                except:
                    continue
            
            gfg_count = len([h for h in self.hackathons if h['platform'] == 'GeeksforGeeks'])
            print(f"✅ GeeksforGeeks: Found {gfg_count} events\n")
            
        except Exception as e:
            print(f"❌ GeeksforGeeks error: {e}\n")
    
    def get_all_hackathons(self):
        """Run all scrapers"""
        print("\n" + "="*60)
        print("🚀 STARTING HACKATHON SCRAPING PROCESS")
        print("="*60 + "\n")
        
        # Existing scrapers
        self.scrape_devpost()
        time.sleep(2)
        
        self.scrape_mlh()
        time.sleep(2)
        
        self.scrape_hackerearth()
        time.sleep(2)
        
        self.scrape_unstop()
        time.sleep(2)
        
        # NEW SCRAPERS
        self.scrape_codechef()
        time.sleep(2)
        
        self.scrape_kaggle()
        time.sleep(2)
        
        self.scrape_leetcode()
        time.sleep(2)
        
        self.scrape_codeforces()
        time.sleep(2)
        
        self.scrape_github()
        time.sleep(2)
        
        self.scrape_gfg()
        
        print("="*60)
        print(f"✅ SCRAPING COMPLETE: Found {len(self.hackathons)} total hackathons")
        print("="*60 + "\n")
        
        return self.hackathons


# Test the scraper
if __name__ == "__main__":
    scraper = HackathonScraper()
    hackathons = scraper.get_all_hackathons()
    
    if hackathons:
        print("\n📋 SAMPLE RESULTS:\n")
        for i, hack in enumerate(hackathons[:5], 1):
            print(f"{i}. {hack['name']}")
            print(f"   Platform: {hack['platform']}")
            print(f"   Link: {hack.get('registration_link', 'N/A')}\n")
    else:
        print("⚠️  No hackathons found. This can happen if:")
        print("   - Websites are blocking requests")
        print("   - No live hackathons at the moment")
        print("   - Website structure changed")
        print("\n✅ Don't worry! We'll add manual sources next.\n")