"""
Scheduler for daily crawling of Der Spiegel Bluesky posts.
"""
import schedule
import time
import subprocess
import sys
from pathlib import Path


def run_crawler():
    """Run the main crawler script."""
    print(f"\n{'='*50}")
    print(f"Running crawler at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*50)

    try:
        # Import and run the main crawler
        from main import run_crawl
        run_crawl()
        print("Crawler completed successfully!")
    except Exception as e:
        print(f"Crawler error: {e}")


def rebuild_docusaurus():
    """Rebuild the Docusaurus site after crawling."""
    docusaurus_path = Path(__file__).parent.parent / "docusaurus"

    if not docusaurus_path.exists():
        print("Docusaurus directory not found, skipping build")
        return

    print("Rebuilding Docusaurus site...")
    try:
        subprocess.run(
            ["npm", "run", "build"],
            cwd=str(docusaurus_path),
            check=True,
            shell=True
        )
        print("Docusaurus build completed!")
    except subprocess.CalledProcessError as e:
        print(f"Docusaurus build failed: {e}")
    except FileNotFoundError:
        print("npm not found, skipping Docusaurus build")


def daily_job():
    """Run the full daily job: crawl + rebuild."""
    run_crawler()
    rebuild_docusaurus()


def start_scheduler(run_time: str = "06:00"):
    """
    Start the daily scheduler.

    Args:
        run_time: Time to run daily job (HH:MM format, 24-hour)
    """
    print(f"Scheduling daily crawl at {run_time}")
    schedule.every().day.at(run_time).do(daily_job)

    print(f"Scheduler started. Next run at {run_time} daily.")
    print("Press Ctrl+C to stop.")

    # Run immediately on first start
    print("\nRunning initial crawl...")
    daily_job()

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Der Spiegel Bluesky Crawler Scheduler")
    parser.add_argument(
        "--time",
        type=str,
        default="06:00",
        help="Time to run daily (HH:MM format, default: 06:00)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (no scheduling)"
    )

    args = parser.parse_args()

    if args.once:
        print("Running single crawl...")
        daily_job()
    else:
        start_scheduler(args.time)
