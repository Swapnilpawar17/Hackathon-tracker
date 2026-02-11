import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Notion client
notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DATABASE_ID")

def add_test_hackathon():
    """Add a test hackathon to verify everything works"""
    
    print("\n" + "="*50)
    print("🚀 ADDING TEST HACKATHON TO NOTION")
    print("="*50 + "\n")
    
    try:
        # Create a new page in the database
        new_page = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "Test Hackathon 2025 - Google Challenge"
                            }
                        }
                    ]
                },
                "Platform": {
                    "select": {
                        "name": "Other"
                    }
                },
                "Mode": {
                    "select": {
                        "name": "Online"
                    }
                },
                "Status": {
                    "select": {
                        "name": "Live"
                    }
                },
                "Fresher Friendly": {
                    "checkbox": True
                },
                "Registration Link": {
                    "url": "https://developers.google.com/community/gdsc-solution-challenge"
                },
                "Organizer": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Google Developer Student Clubs"
                            }
                        }
                    ]
                },
                "Prize Pool": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "$3000 + Mentorship"
                            }
                        }
                    ]
                },
                "Last Updated": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }
        )
        
        print("✅ Test hackathon added successfully!")
        print(f"📊 Hackathon Name: Test Hackathon 2025 - Google Challenge")
        print(f"🔗 View in Notion: {new_page['url']}\n")
        
        print("="*50)
        print("✨ SUCCESS! Check your Notion database! ✨")
        print("="*50 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding hackathon: {e}\n")
        print("="*50)
        print("❌ FAILED TO ADD HACKATHON")
        print("="*50 + "\n")
        return False

# Run the function
if __name__ == "__main__":
    add_test_hackathon()