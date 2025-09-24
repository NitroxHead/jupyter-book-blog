#!/usr/bin/env python3
"""
Script to automatically generate the recent posts section for the blog landing page.
Scans the book/ directory for markdown files and extracts metadata to create post listings.
"""

import os
import re
from datetime import datetime
from pathlib import Path

def extract_post_metadata(file_path):
    """Extract title, date, and description from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title (first # heading)
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else Path(file_path).stem.replace('-', ' ').title()

    # Extract date (look for *Published: DATE* or *DATE* patterns)
    date_match = re.search(r'\*(?:Published: )?(.+?)\*', content)
    date_str = date_match.group(1) if date_match else "Unknown date"

    # Extract description (first paragraph after title and date)
    # Split content into lines and find the first substantial paragraph
    lines = content.split('\n')
    description = ""

    # Skip title, date, and empty lines to find first paragraph
    start_looking = False
    for line in lines:
        line = line.strip()
        if start_looking and line and not line.startswith('#') and not line.startswith('*'):
            # Take first sentence or first 150 characters
            description = line
            if '.' in description:
                description = description.split('.')[0] + '.'
            elif len(description) > 150:
                description = description[:150] + '...'
            break
        elif line.startswith('# '):
            start_looking = True

    # If no description found, create a generic one
    if not description:
        description = f"Explore insights about {title.lower()}."

    return {
        'title': title,
        'date': date_str,
        'description': description,
        'file_path': file_path
    }

def parse_date(date_str):
    """Parse date string to datetime object for sorting."""
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except:
        return datetime.min

def generate_posts_section():
    """Generate the recent posts section markdown."""
    book_dir = Path('book')
    posts = []

    # Scan for markdown files in book directory
    for file_path in book_dir.glob('*.md'):
        if file_path.name != 'references.md':  # Skip reference files
            metadata = extract_post_metadata(file_path)
            posts.append(metadata)

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: parse_date(x['date']), reverse=True)

    # Generate markdown
    posts_md = "## Recent Posts\n\n"

    for post in posts:
        relative_path = f"book/{Path(post['file_path']).name}"
        posts_md += f"### [{post['title']}]({relative_path})\n"
        posts_md += f"*{post['date']}*\n\n"
        posts_md += f"{post['description']}\n\n"
        posts_md += "---\n\n"

    return posts_md.rstrip('---\n\n') + "\n\n"

def update_index_md():
    """Update index.md with automatically generated posts section."""
    index_path = Path('index.md')

    # Read current index.md
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate new posts section
    posts_section = generate_posts_section()

    # Find the first "## Recent Posts" and replace everything after it
    # Split at the first occurrence of "## Recent Posts"
    parts = content.split('## Recent Posts', 1)
    if len(parts) == 2:
        # Keep everything before the first "## Recent Posts"
        before_posts = parts[0].rstrip()
        new_content = before_posts + "\n\n" + posts_section
    else:
        # No existing posts section, append it
        new_content = content.rstrip() + "\n\n" + posts_section

    # Write updated content
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ Updated index.md with automatically generated posts section")

if __name__ == "__main__":
    update_index_md()