import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime
from scrapers import HackathonScraper
from india_scrapers import IndiaHackathonScraper
from manual_sources import get_manual_hackathons
from filters import apply_all_filters, get_statistics
from simple_notifier import SimpleNotifier
import time

# Load environment variables
load_dotenv()

class NotionUpdater:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")
    
    def get_existing_hackathons(self):
        """Get existing hackathons to avoid duplicates"""
        try:
            # Updated for notion-client 2.x
            results = self.notion.databases.query(**{"database_id": self.database_id})
            existing = {}
            
            for page in results.get('results', []):
                try:
                    # Get name from title
                    name_prop = page['properties'].get('Name', {})
                    if name_prop.get('title'):
                        name = name_prop['title'][0]['text']['content']
                    else:
                        continue
                    
                    # Get registration link
                    link_prop = page['properties'].get('Registration Link', {})
                    link = link_prop.get('url', '') if link_prop else ''
                    
                    # Create unique key
                    key = f"{name}||{link}"
                    existing[key] = page['id']
                except:
                    continue
            
            print(f"📊 Found {len(existing)} existing hackathons in database\n")
            return existing
            
        except Exception as e:
            print(f"⚠️  Note: Could not check for duplicates ({e})")
            print(f"   Continuing with fresh import...\n")
            return {}
    
    def create_hackathon_page(self, hackathon):
        """Add a single hackathon to Notion"""
        try:
            # Build properties
            properties = {
                "Name": {
                    "title": [{"text": {"content": hackathon.get('name', 'Unnamed')[:100]}}]
                },
                "Platform": {
                    "select": {"name": hackathon.get('platform', 'Other')}
                },
                "Mode": {
                    "select": {"name": hackathon.get('mode', 'Online')}
                },
                "Status": {
                    "select": {"name": hackathon.get('status', 'Live')}
                },
                "Fresher Friendly": {
                    "checkbox": hackathon.get('fresher_friendly', True)
                },
                "Last Updated": {
                    "date": {"start": datetime.now().isoformat()}
                }
            }
            
            # Add optional fields
            if hackathon.get('registration_link'):
                properties["Registration Link"] = {"url": hackathon['registration_link']}
            
            if hackathon.get('organizer'):
                properties["Organizer"] = {
                    "rich_text": [{"text": {"content": str(hackathon['organizer'])[:2000]}}]
                }
            
            if hackathon.get('prize_pool'):
                properties["Prize Pool"] = {
                    "rich_text": [{"text": {"content": str(hackathon['prize_pool'])[:2000]}}]
                }
            
            # Create page
            self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def update_database(self, hackathons):
        """Update Notion with all hackathons"""
        print("\n" + "="*60)
        print("📝 UPDATING NOTION DATABASE")
        print("="*60 + "\n")
        
        existing = self.get_existing_hackathons()
        
        added = 0
        skipped = 0
        failed = 0
        new_hackathons = []
        
        for hackathon in hackathons:
            # Create unique identifier
            key = f"{hackathon.get('name', '')}||{hackathon.get('registration_link', '')}"
            
            # Check if exists
            if key in existing:
                skipped += 1
                continue
            
            # Try to add
            if self.create_hackathon_page(hackathon):
                added += 1
                new_hackathons.append(hackathon)
                print(f"✅ Added: {hackathon.get('name', 'Unknown')[:60]}")
            else:
                failed += 1
                print(f"❌ Failed: {hackathon.get('name', 'Unknown')[:60]}")
            
            time.sleep(0.3)  # Rate limiting
        
        # Summary
        print("\n" + "="*60)
        print("📊 UPDATE SUMMARY")
        print("="*60)
        print(f"✅ New hackathons added: {added}")
        print(f"⏭️  Duplicates skipped: {skipped}")
        print(f"❌ Failed to add: {failed}")
        print(f"📊 Total in database: {len(existing) + added}")
        print("="*60 + "\n")
        
        return added, skipped, failed, new_hackathons


def main(send_notification=True):
    """Main execution"""
    print("\n" + "🎯"*30)
    print("   HACKATHON SCRAPER & NOTION UPDATER")
    print("🎯"*30 + "\n")
    
    # Step 1: Scrape international hackathons
    print("STEP 1: Scraping international hackathon platforms...\n")
    scraper = HackathonScraper()
    hackathons = scraper.get_all_hackathons()
    
    # Step 2: Scrape India-specific platforms
    print("\nSTEP 2: Scraping India-specific platforms...\n")
    india_scraper = IndiaHackathonScraper()
    india_hackathons = india_scraper.get_all_india_hackathons()
    hackathons.extend(india_hackathons)
    
    # Step 3: Add manual hackathons (only LIVE ones)
    print("\nSTEP 3: Adding manually curated LIVE hackathons...\n")
    manual_hacks = get_manual_hackathons()
    print(f"➕ Added {len(manual_hacks)} manually curated LIVE hackathons")
    hackathons.extend(manual_hacks)
    
    # Show statistics before filtering
    print(f"\n📊 Total hackathons found (before filtering): {len(hackathons)}")
    
    # Step 4: Apply filters - ONLY LIVE HACKATHONS
    print("\nSTEP 4: Filtering for LIVE hackathons only...\n")
    
    # Get stats before filtering
    stats_before = get_statistics(hackathons)
    print(f"   Before filtering: {stats_before['live']} Live, {stats_before['upcoming']} Upcoming")
    
    # Apply strict LIVE filter
    hackathons = apply_all_filters(hackathons, live_only=True, fresher_only=False, remove_dupes=True)
    
    print(f"📊 Total LIVE hackathons after filtering: {len(hackathons)}\n")
    
    if not hackathons:
        print("⚠️  No LIVE hackathons found from any source.")
        print("💡 TIP: Check if any hackathons are currently accepting registrations!\n")
        return
    
    # Step 5: Update Notion
    print("\nSTEP 5: Adding LIVE hackathons to Notion...\n")
    updater = NotionUpdater()
    added, skipped, failed, new_hackathons = updater.update_database(hackathons)
    
    # Step 6: Platform breakdown
    print("\n📊 PLATFORM BREAKDOWN (LIVE HACKATHONS):\n")
    platform_counts = {}
    for hack in hackathons:
        platform = hack.get('platform', 'Unknown')
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    for platform, count in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {platform}: {count} LIVE hackathons")
    
    # Step 7: Send notification
    if send_notification and new_hackathons:
        print("\n\nSTEP 7: Sending notification...\n")
        notifier = SimpleNotifier()
        notifier.send_notification(new_hackathons)
    
    # Step 8: Show highlights
    if added > 0:
        print("\n🌟 TOP NEWLY ADDED LIVE HACKATHONS:\n")
        for i, hack in enumerate(new_hackathons[:5], 1):
            print(f"{i}. {hack['name']}")
            print(f"   Platform: {hack['platform']} | Mode: {hack.get('mode', 'N/A')}")
            print(f"   Prize: {hack.get('prize_pool', 'N/A')}")
            print(f"   🔗 {hack.get('registration_link', 'N/A')}\n")
    
    print("✨ Process completed successfully!")
    print("📊 Your Notion database now contains only LIVE hackathons!")
    print("🔗 Check your Notion database now!\n")


if __name__ == "__main__":
    main()