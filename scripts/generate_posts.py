#!/usr/bin/env python3
"""
Script to automatically generate the recent posts section for the blog landing page.
Scans the book/ directory for markdown files and extracts metadata to create post listings.
Supports both frontmatter and legacy format.
"""

import json
import sys
import re
from datetime import datetime
from pathlib import Path
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
            "homepage": {
                "welcome_text": "Welcome to my blog!",
                "footer_note": "*Add posts to update automatically.*"
            },
            "posts": {
                "max_posts_on_homepage": 0,
                "description_length": 150,
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
    """Extract title, date, and description from a markdown file with frontmatter support."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Try to get metadata from frontmatter first
        title = post.get('title')
        date_str = post.get('date')
        description = post.get('description')

        # Fallback to content parsing if frontmatter is missing
        content = post.content

        # Extract title if not in frontmatter
        if not title:
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else file_path.stem.replace('-', ' ').title()

        # Extract date if not in frontmatter (legacy format: *DATE*)
        if not date_str:
            date_match = re.search(r'\*(?:Published: )?(.+?)\*', content)
            date_str = date_match.group(1) if date_match else None

        if not date_str:
            print(f"⚠️  Warning: No date found in {file_path.name}, skipping post")
            return None

        # Convert date to string if it's a datetime object
        if isinstance(date_str, datetime):
            date_str = date_str.strftime("%B %d, %Y")
        else:
            date_str = str(date_str)

        # Extract description if not in frontmatter
        if not description:
            description_length = get_nested_value(config, 'posts', 'description_length', default=150)
            lines = content.split('\n')

            # Skip title, date, and empty lines to find first paragraph
            start_looking = False
            for line in lines:
                line = line.strip()
                if start_looking and line and not line.startswith('#') and not line.startswith('*') and not line.startswith('```'):
                    # Take first sentence or configured length
                    description = line
                    if '.' in description:
                        description = description.split('.')[0] + '.'
                    elif len(description) > description_length:
                        description = description[:description_length] + '...'
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

    except Exception as e:
        print(f"❌ Error processing {file_path.name}: {e}")
        return None


def parse_date(date_str: str, config: Dict[str, Any]) -> datetime:
    """Parse date string to datetime object for sorting, supports multiple formats."""
    supported_formats = get_nested_value(
        config, 'posts', 'supported_date_formats',
        default=["%B %d, %Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]
    )

    for date_format in supported_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue

    # If no format matches, print warning and return min date
    print(f"⚠️  Warning: Could not parse date '{date_str}' with any supported format")
    return datetime.min


def generate_posts_section(config: Dict[str, Any]) -> str:
    """Generate the recent posts section markdown."""
    posts_dir = Path('posts')

    if not posts_dir.exists():
        print(f"❌ Error: posts/ directory not found")
        return "## Recent Posts\n\n*No posts found.*\n\n"

    posts = []

    # Scan for markdown files in posts directory
    for file_path in posts_dir.glob('*.md'):
        if file_path.name not in ['references.md', 'README.md']:  # Skip reference files
            metadata = extract_post_metadata(file_path, config)
            if metadata:  # Only add if extraction succeeded
                posts.append(metadata)

    if not posts:
        print("⚠️  Warning: No valid posts found in posts/ directory")
        return "## Recent Posts\n\n*No posts found. Add markdown files with dates to the posts/ directory.*\n\n"

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: parse_date(x['date'], config), reverse=True)

    # Limit posts if configured
    max_posts = get_nested_value(config, 'posts', 'max_posts_on_homepage', default=0)
    if max_posts > 0:
        posts = posts[:max_posts]

    # Generate markdown
    posts_md = "## Recent Posts\n\n"

    for post in posts:
        relative_path = f"posts/{post['file_path'].name}"
        posts_md += f"### [{post['title']}]({relative_path})\n"
        posts_md += f"*{post['date']}*\n\n"
        posts_md += f"{post['description']}\n\n"
        posts_md += "---\n\n"

    return posts_md.rstrip('---\n\n') + "\n\n"


def update_index_md():
    """Update index.md with automatically generated posts section."""
    # Load configuration
    config = load_config()

    index_path = Path('index.md')

    if not index_path.exists():
        print("❌ Error: index.md not found")
        sys.exit(1)

    try:
        # Read current index.md
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate new posts section
        posts_section = generate_posts_section(config)

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

    except Exception as e:
        print(f"❌ Error updating index.md: {e}")
        sys.exit(1)


if __name__ == "__main__":
    update_index_md()
