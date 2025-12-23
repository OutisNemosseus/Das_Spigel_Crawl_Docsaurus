"""
Docusaurus markdown generator for translated posts.
"""
import os
import re
from datetime import datetime
from pathlib import Path
from translator import translate_german_to_english
from word_parser import parse_text_to_vocabulary, vocabulary_to_markdown_table


# Path to Docusaurus docs folder
DOCS_PATH = Path(__file__).parent.parent / "docusaurus" / "docs" / "posts"


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    Create a safe filename from text.

    Args:
        text: Text to convert to filename
        max_length: Maximum filename length

    Returns:
        Safe filename string
    """
    # Remove special characters
    safe = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace whitespace with hyphens
    safe = re.sub(r'[\s]+', '-', safe)
    # Truncate
    return safe[:max_length].strip('-')


def generate_post_markdown(post: dict) -> str:
    """
    Generate Docusaurus markdown for a single post.

    Args:
        post: Post dictionary with text, created_at, uri, author

    Returns:
        Markdown string
    """
    german_text = post.get("text", "")
    created_at = post.get("created_at", "")
    uri = post.get("uri", "")

    # Parse date
    if created_at:
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            date_str = dt.strftime("%B %d, %Y")
            date_iso = dt.strftime("%Y-%m-%d")
        except Exception:
            date_str = created_at
            date_iso = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = "Unknown date"
        date_iso = datetime.now().strftime("%Y-%m-%d")

    # Translate the full text
    english_text = translate_german_to_english(german_text)

    # Parse vocabulary
    vocabulary = parse_text_to_vocabulary(german_text, include_stopwords=True)
    vocab_table = vocabulary_to_markdown_table(vocabulary)

    # Generate title from first words
    title_words = german_text.split()[:6]
    title = " ".join(title_words)
    if len(german_text.split()) > 6:
        title += "..."

    # Build markdown
    markdown = f"""---
title: "{title}"
date: {date_iso}
tags: [der-spiegel, german, translation]
---

# Post from {date_str}

## Original German

{german_text}

## English Translation

{english_text}

## Vocabulary Table

{vocab_table}

---

*Source: Der Spiegel on Bluesky*
*Post URI: {uri}*
"""
    return markdown


def save_post_as_doc(post: dict) -> str:
    """
    Generate and save a post as a Docusaurus markdown file.

    Args:
        post: Post dictionary

    Returns:
        Path to saved file
    """
    # Ensure docs directory exists
    DOCS_PATH.mkdir(parents=True, exist_ok=True)

    # Generate markdown
    markdown = generate_post_markdown(post)

    # Create filename from date and content
    created_at = post.get("created_at", "")
    if created_at:
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            date_prefix = dt.strftime("%Y-%m-%d")
        except Exception:
            date_prefix = datetime.now().strftime("%Y-%m-%d")
    else:
        date_prefix = datetime.now().strftime("%Y-%m-%d")

    text_slug = sanitize_filename(post.get("text", "post")[:30])
    filename = f"{date_prefix}-{text_slug}.md"
    filepath = DOCS_PATH / filename

    # Write file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Saved: {filepath}")
    return str(filepath)


def generate_index_page(posts: list[dict]) -> None:
    """
    Generate an index page for all posts.

    Args:
        posts: List of post dictionaries
    """
    DOCS_PATH.mkdir(parents=True, exist_ok=True)

    content = """---
sidebar_position: 1
---

# Der Spiegel Bluesky Posts

Welcome to the Der Spiegel Bluesky translation archive. This site automatically fetches posts from Der Spiegel's Bluesky account, translates them to English, and provides word-by-word vocabulary tables for German learners.

## Latest Posts

"""
    # Add links to recent posts
    for post in posts[:10]:
        created_at = post.get("created_at", "")
        text = post.get("text", "")[:60] + "..."

        if created_at:
            try:
                dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                date_str = dt.strftime("%Y-%m-%d")
                date_prefix = date_str
            except Exception:
                date_str = "Unknown"
                date_prefix = datetime.now().strftime("%Y-%m-%d")
        else:
            date_str = "Unknown"
            date_prefix = datetime.now().strftime("%Y-%m-%d")

        text_slug = sanitize_filename(text[:30])
        filename = f"{date_prefix}-{text_slug}"

        content += f"- [{date_str}] [{text}](./{filename})\n"

    content += """

## How to Use This Site

1. **Read the German text** - Try to understand it first
2. **Check the English translation** - Compare with your understanding
3. **Study the vocabulary table** - Learn individual words with their translations and grammatical notes

## About

This documentation is automatically generated by a Python crawler that:
- Fetches posts from @derspiegel.bsky.social on Bluesky
- Translates the content from German to English
- Creates word-by-word vocabulary breakdowns

Happy learning! 🇩🇪 → 🇬🇧
"""

    index_path = DOCS_PATH / "intro.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated index: {index_path}")


def process_posts(posts: list[dict]) -> list[str]:
    """
    Process multiple posts and save them as Docusaurus docs.

    Args:
        posts: List of post dictionaries

    Returns:
        List of saved file paths
    """
    saved_files = []
    for post in posts:
        try:
            filepath = save_post_as_doc(post)
            saved_files.append(filepath)
        except Exception as e:
            print(f"Error processing post: {e}")

    # Generate index page
    if posts:
        generate_index_page(posts)

    return saved_files


if __name__ == "__main__":
    # Test with sample post
    sample_post = {
        "text": "Die Bundesregierung hat neue Maßnahmen zur Bekämpfung des Klimawandels angekündigt.",
        "created_at": "2024-12-23T10:00:00Z",
        "uri": "at://did:plc:example/app.bsky.feed.post/123",
        "author": "derspiegel.bsky.social"
    }

    print("Testing doc generator...")
    filepath = save_post_as_doc(sample_post)
    print(f"\nGenerated: {filepath}")

    # Read and display the generated file
    with open(filepath, "r", encoding="utf-8") as f:
        print("\n--- Generated Content ---")
        print(f.read())
