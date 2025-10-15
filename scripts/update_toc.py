#!/usr/bin/env python3
"""
Script to automatically update _toc.yml with all blog posts.
Reads navigation structure from blog_config.json.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

try:
    import frontmatter
except ImportError:
    print("❌ Error: python-frontmatter package not found")
    print("Please install it: pip install python-frontmatter")
    sys.exit(1)


def load_config() -> Dict[str, Any]:
    """Load blog configuration from blog_config.json"""
    try:
        with open('blog_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("⚠️  Warning: blog_config.json not found, using default values")
        return {
            "blog": {"title": "Your Blog"},
            "navigation": {
                "quick_links": [
                    {"title": "About", "file": "about"},
                    {"title": "Projects", "file": "projects"},
                    {"title": "Contact", "file": "contact"}
                ],
                "blog_section_title": "Blog Posts"
            },
            "posts": {
                "supported_date_formats": ["%B %d, %Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
            }
        }
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in blog_config.json: {e}")
        sys.exit(1)


def get_nested_value(config: Dict[str, Any], *keys, default=None):
    """Safely get nested dictionary values"""
    value = config
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, default)
        else:
            return default
    return value if value is not None else default


def extract_post_metadata(file_path: Path, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract title and date from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Try to get metadata from frontmatter first
        title = post.get('title')
        date_str = post.get('date')

        # Fallback to content parsing
        content = post.content

        # Extract title if not in frontmatter
        if not title:
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else file_path.stem.replace('-', ' ').title()

        # Extract date if not in frontmatter (legacy format)
        if not date_str:
            date_match = re.search(r'\*(?:Published: )?(.+?)\*', content)
            date_str = date_match.group(1) if date_match else None

        if not date_str:
            print(f"⚠️  Warning: No date found in {file_path.name}, skipping")
            return None

        # Convert date to string if it's a datetime object
        if isinstance(date_str, datetime):
            date_str = date_str.strftime("%B %d, %Y")
        else:
            date_str = str(date_str)

        return {
            'title': title,
            'date': date_str,
            'filename': file_path.stem
        }

    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
        return None


def parse_date(date_str: str, config: Dict[str, Any]) -> datetime:
    """Parse date string to datetime object for sorting."""
    supported_formats = get_nested_value(
        config, 'posts', 'supported_date_formats',
        default=["%B %d, %Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
    )

    for date_format in supported_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue

    print(f"⚠️  Warning: Could not parse date '{date_str}'")
    return datetime.min


def update_toc():
    """Update _toc.yml with all blog posts using config-driven navigation."""
    # Load configuration
    config = load_config()

    posts_dir = Path('posts')
    posts = []

    # Scan for markdown files in posts directory
    if posts_dir.exists():
        for file_path in posts_dir.glob('*.md'):
            if file_path.name not in ['references.md', 'README.md']:
                metadata = extract_post_metadata(file_path, config)
                if metadata:
                    posts.append(metadata)

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: parse_date(x['date'], config), reverse=True)

    # Generate TOC content
    toc_content = """# Table of contents
# Learn more at https://jupyterbook.org/customize/toc.html

format: jb-book
root: index

parts:
"""

    # Add Quick Links section from config
    quick_links = get_nested_value(config, 'navigation', 'quick_links', default=[])
    if quick_links:
        toc_content += "  - caption: Quick Links\n"
        toc_content += "    chapters:\n"
        for link in quick_links:
            file_name = link.get('file', '')
            if file_name:
                toc_content += f"      - file: {file_name}\n"

    # Add Blog Posts section
    blog_section_title = get_nested_value(config, 'navigation', 'blog_section_title', default='Blog Posts')
    toc_content += f"  - caption: {blog_section_title}\n"
    toc_content += "    chapters:\n"

    # Add all posts to TOC
    for post in posts:
        toc_content += f"      - file: posts/{post['filename']}\n"

    # Write updated TOC
    try:
        with open('_toc.yml', 'w', encoding='utf-8') as f:
            f.write(toc_content)

        print(f"✅ Updated _toc.yml with {len(posts)} blog posts")
        if posts:
            print("Posts added (newest first):")
            for i, post in enumerate(posts[:10]):  # Show first 10
                print(f"  {i+1}. {post['title']} ({post['date']})")
            if len(posts) > 10:
                print(f"  ... and {len(posts) - 10} more posts")

    except Exception as e:
        print(f"❌ Error writing _toc.yml: {e}")
        sys.exit(1)


if __name__ == "__main__":
    update_toc()
