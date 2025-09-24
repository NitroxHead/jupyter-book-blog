#!/usr/bin/env python3
"""
Script to automatically update _toc.yml with all blog posts.
"""

import os
import re
from pathlib import Path
from datetime import datetime

def extract_post_metadata(file_path):
    """Extract title and date from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title (first # heading)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(file_path).stem.replace('-', ' ').title()

    # Extract date (look for *Published: DATE* or *DATE* patterns)
    date_match = re.search(r'\*(?:Published: )?(.+?)\*', content)
    date_str = date_match.group(1) if date_match else "Unknown date"

    return {
        'title': title,
        'date': date_str,
        'filename': Path(file_path).stem
    }

def parse_date(date_str):
    """Parse date string to datetime object for sorting."""
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except:
        return datetime.min

def update_toc():
    """Update _toc.yml with all blog posts."""
    book_dir = Path('book')
    posts = []

    # Scan for markdown files in book directory
    for file_path in book_dir.glob('*.md'):
        if file_path.name not in ['references.md']:  # Skip reference files
            metadata = extract_post_metadata(file_path)
            posts.append(metadata)

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: parse_date(x['date']), reverse=True)

    # Generate TOC content
    toc_content = """# Table of contents
# Learn more at https://jupyterbook.org/customize/toc.html

format: jb-book
root: index

parts:
  - caption: Quick Links
    chapters:
      - file: about
      - file: projects
      - file: contact
  - caption: Blog Posts
    chapters:
"""

    # Add all posts to TOC
    for post in posts:
        toc_content += f"      - file: book/{post['filename']}\n"

    # Write updated TOC
    with open('_toc.yml', 'w', encoding='utf-8') as f:
        f.write(toc_content)

    print(f"✅ Updated _toc.yml with {len(posts)} blog posts")
    print("Posts added (newest first):")
    for i, post in enumerate(posts[:10]):  # Show first 10
        print(f"  {i+1}. {post['title']} ({post['date']})")
    if len(posts) > 10:
        print(f"  ... and {len(posts) - 10} more posts")

if __name__ == "__main__":
    update_toc()