import os
import time
from datetime import datetime
from main import main

def run_scheduler():
    """Run the scraper periodically on Render"""
    print("\n" + "="*60)
    print("🤖 RENDER SCHEDULER STARTED")
    print("="*60 + "\n")
    
    while True:
        try:
            print(f"\n⏰ Running scheduled update at {datetime.now()}")
            
            # Run the main scraper
            main(send_notification=False)  # Disable browser notifications on server
            
            print(f"✅ Update completed at {datetime.now()}")
            
        except Exception as e:
            print(f"❌ Scheduler error: {e}")
        
        # Wait 6 hours before next run
        print(f"\n💤 Sleeping for 6 hours...")
        time.sleep(21600)  # 6 hours in seconds

if __name__ == "__main__":
    run_scheduler()