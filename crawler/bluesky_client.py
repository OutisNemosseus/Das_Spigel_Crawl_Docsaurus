"""
Bluesky ATP client for fetching Der Spiegel posts.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from atproto import Client

# Der Spiegel's Bluesky handle
SPIEGEL_HANDLE = "derspiegel.bsky.social"

# File to track already fetched posts
FETCHED_POSTS_FILE = Path(__file__).parent / "fetched_posts.json"


def load_fetched_posts() -> set:
    """Load set of already fetched post URIs."""
    if FETCHED_POSTS_FILE.exists():
        with open(FETCHED_POSTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("uris", []))
    return set()


def save_fetched_posts(uris: set) -> None:
    """Save set of fetched post URIs."""
    with open(FETCHED_POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump({"uris": list(uris), "last_updated": datetime.now().isoformat()}, f)


def fetch_spiegel_posts(limit: int = 50) -> list[dict]:
    """
    Fetch posts from Der Spiegel's Bluesky account.

    Args:
        limit: Maximum number of posts to fetch

    Returns:
        List of post dictionaries with text, created_at, and uri
    """
    client = Client()

    # Get the profile to resolve the DID
    try:
        profile = client.get_profile(SPIEGEL_HANDLE)
        did = profile.did
    except Exception as e:
        print(f"Error fetching profile for {SPIEGEL_HANDLE}: {e}")
        return []

    # Fetch the author's feed
    posts = []
    fetched_uris = load_fetched_posts()
    cursor = None

    while len(posts) < limit:
        try:
            response = client.get_author_feed(
                actor=did,
                limit=min(50, limit - len(posts)),
                cursor=cursor
            )
        except Exception as e:
            print(f"Error fetching feed: {e}")
            break

        if not response.feed:
            break

        for feed_item in response.feed:
            post = feed_item.post
            post_uri = post.uri

            # Skip already fetched posts
            if post_uri in fetched_uris:
                continue

            # Extract post data
            record = post.record
            if hasattr(record, 'text') and record.text:
                post_data = {
                    "uri": post_uri,
                    "text": record.text,
                    "created_at": record.created_at if hasattr(record, 'created_at') else None,
                    "author": SPIEGEL_HANDLE,
                    "cid": post.cid
                }
                posts.append(post_data)
                fetched_uris.add(post_uri)

        cursor = response.cursor
        if not cursor:
            break

    # Save updated fetched posts
    save_fetched_posts(fetched_uris)

    return posts


def fetch_new_posts() -> list[dict]:
    """
    Fetch only new posts that haven't been processed yet.

    Returns:
        List of new post dictionaries
    """
    return fetch_spiegel_posts(limit=100)


if __name__ == "__main__":
    # Test fetching posts
    print(f"Fetching posts from {SPIEGEL_HANDLE}...")
    posts = fetch_spiegel_posts(limit=5)
    print(f"Fetched {len(posts)} posts")
    for post in posts:
        print(f"\n--- Post ---")
        print(f"Date: {post['created_at']}")
        print(f"Text: {post['text'][:200]}...")
