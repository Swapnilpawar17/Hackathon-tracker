import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime
from scrapers import HackathonScraper
from manual_sources import get_manual_hackathons
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
        
        return added, skipped, failed


def main():
    """Main execution"""
    print("\n" + "🎯"*30)
    print("   HACKATHON SCRAPER & NOTION UPDATER")
    print("🎯"*30 + "\n")
    
    # Step 1: Scrape hackathons
    print("STEP 1: Scraping hackathons from web...\n")
    scraper = HackathonScraper()
    hackathons = scraper.get_all_hackathons()
    
    # Step 1.5: Add manual hackathons
    print("\nSTEP 1.5: Adding manually curated hackathons...\n")
    manual_hacks = get_manual_hackathons()
    print(f"➕ Added {len(manual_hacks)} manually curated hackathons")
    hackathons.extend(manual_hacks)
    print(f"📊 Total hackathons to process: {len(hackathons)}\n")
    
    if not hackathons:
        print("⚠️  No hackathons found from scraping.")
        print("💡 TIP: You can add manual hackathons in the next step!\n")
        return
    
    # Step 2: Update Notion
    print("\nSTEP 2: Adding hackathons to Notion...\n")
    updater = NotionUpdater()
    added, skipped, failed = updater.update_database(hackathons)
    
    # Step 3: Show highlights
    if added > 0:
        print("\n🌟 TOP FRESHLY ADDED HACKATHONS:\n")
        fresher_friendly = [h for h in hackathons if h.get('fresher_friendly', False)]
        for i, hack in enumerate(fresher_friendly[:5], 1):
            print(f"{i}. {hack['name']}")
            print(f"   Platform: {hack['platform']} | Mode: {hack.get('mode', 'N/A')}")
            print(f"   🔗 {hack.get('registration_link', 'N/A')}\n")
    
    print("✨ Process completed successfully!")
    print("🔗 Check your Notion database now!\n")


if __name__ == "__main__":
    main()