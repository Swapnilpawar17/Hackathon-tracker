import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
notion_token = os.getenv("NOTION_TOKEN")
database_id = os.getenv("NOTION_DATABASE_ID")

# Initialize Notion client
notion = Client(auth=notion_token)

def test_connection():
    """Test if we can connect to Notion"""
    print("\n" + "="*50)
    print("🔍 TESTING NOTION CONNECTION")
    print("="*50 + "\n")
    
    # Check if credentials are loaded
    if not notion_token:
        print("❌ ERROR: NOTION_TOKEN not found in .env file")
        return False
    
    if not database_id:
        print("❌ ERROR: NOTION_DATABASE_ID not found in .env file")
        return False
    
    print("✅ Credentials loaded from .env file")
    print(f"   Token starts with: {notion_token[:20]}...")
    print(f"   Database ID: {database_id}\n")
    
    # Try to connect to Notion
    try:
        print("🔄 Attempting to connect to Notion...")
        database = notion.databases.retrieve(database_id=database_id)
        
        print("✅ Successfully connected to Notion!")
        print(f"📊 Database Name: {database['title'][0]['text']['content']}")
        print(f"🎯 Database ID verified: {database['id']}\n")
        
        print("="*50)
        print("✨ CONNECTION TEST PASSED! ✨")
        print("="*50 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed!")
        print(f"   Error: {e}\n")
        print("="*50)
        print("❌ CONNECTION TEST FAILED")
        print("="*50 + "\n")
        return False

# Run the test
if __name__ == "__main__":
    test_connection()