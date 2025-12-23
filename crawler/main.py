"""
Main entry point for Der Spiegel Bluesky crawler.

This script fetches posts from Der Spiegel's Bluesky account,
translates them to English, and generates Docusaurus documentation
with word-by-word vocabulary tables.
"""
import argparse
from bluesky_client import fetch_spiegel_posts, fetch_new_posts
from doc_generator import process_posts, save_post_as_doc


def run_crawl(limit: int = 50, new_only: bool = True):
    """
    Run the crawler and generate documentation.

    Args:
        limit: Maximum number of posts to fetch
        new_only: Only fetch posts not previously processed
    """
    print("Der Spiegel Bluesky Crawler")
    print("=" * 40)

    # Fetch posts
    if new_only:
        print("\nFetching new posts...")
        posts = fetch_new_posts()
    else:
        print(f"\nFetching up to {limit} posts...")
        posts = fetch_spiegel_posts(limit=limit)

    if not posts:
        print("No new posts found.")
        return

    print(f"Found {len(posts)} posts to process")

    # Process and generate docs
    print("\nProcessing posts and generating documentation...")
    saved_files = process_posts(posts)

    print(f"\n{'=' * 40}")
    print(f"Completed! Generated {len(saved_files)} documentation files.")
    print("\nTo view the documentation:")
    print("  cd docusaurus")
    print("  npm start")


def main():
    """Main entry point with CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Crawl Der Spiegel Bluesky posts and generate translated documentation"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of posts to fetch (default: 50)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fetch all posts, not just new ones"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run with a test post instead of fetching from Bluesky"
    )

    args = parser.parse_args()

    if args.test:
        print("Running in test mode with sample post...")
        sample_post = {
            "text": "Die Bundesregierung hat heute neue Maßnahmen zur Bekämpfung des Klimawandels angekündigt. Experten begrüßen die Initiative.",
            "created_at": "2024-12-23T10:00:00Z",
            "uri": "at://did:plc:test/app.bsky.feed.post/test123",
            "author": "derspiegel.bsky.social"
        }
        filepath = save_post_as_doc(sample_post)
        print(f"Generated test doc: {filepath}")
    else:
        run_crawl(limit=args.limit, new_only=not args.all)


if __name__ == "__main__":
    main()
