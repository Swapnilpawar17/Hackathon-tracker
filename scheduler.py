import schedule
import time
from datetime import datetime
from main import main

def scheduled_job():
    """Run the scraper on schedule"""
    print("\n" + "="*70)
    print(f"⏰ SCHEDULED RUN - {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    print("="*70 + "\n")
    
    try:
        main()
        print(f"\n✅ Scheduled run completed successfully at {datetime.now().strftime('%I:%M %p')}\n")
    except Exception as e:
        print(f"\n❌ Scheduled run failed: {e}\n")

def run_scheduler():
    """Set up and run the scheduler"""
    print("\n" + "🤖"*35)
    print("   HACKATHON SCRAPER - AUTOMATED SCHEDULER")
    print("🤖"*35 + "\n")
    
    # Choose your schedule (uncomment the one you want):
        # TEST: Run once immediately
    print("🧪 Running test scrape now...\n")
    scheduled_job()
    print("\n✅ Test complete! Now waiting for scheduled time...")
    
    print("📅 Scheduled: Every Monday at 9:00 AM")
    
    # Option 1: Run every Monday at 9:00 AM
    schedule.every().monday.at("09:00").do(scheduled_job)
    print("📅 Scheduled: Every Monday at 9:00 AM")
    
    # Option 2: Run every 7 days (uncomment to use)
    # schedule.every(7).days.do(scheduled_job)
    # print("📅 Scheduled: Every 7 days")
    
    # Option 3: Run every day at 10:00 AM (uncomment to use)
    # schedule.every().day.at("10:00").do(scheduled_job)
    # print("📅 Scheduled: Daily at 10:00 AM")
    
    # Option 4: Run every 3 hours (for testing - uncomment to use)
    # schedule.every(3).hours.do(scheduled_job)
    # print("📅 Scheduled: Every 3 hours")
    
    print("⏱️  Scheduler is now running...")
    print("💡 Press Ctrl+C to stop\n")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n⚠️  Scheduler stopped by user")
        print("👋 Goodbye!\n")

if __name__ == "__main__":
    run_scheduler()