#!/usr/bin/env python3
"""
Interactive setup script for customizing your Jupyter Book blog.
Run this after forking the template to personalize your blog.
"""

import json
from pathlib import Path

def get_user_input(prompt, default=""):
    """Get user input with optional default value"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def yes_no_prompt(prompt, default=True):
    """Ask a yes/no question"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{default_str}]: ").strip().lower()

    if not response:
        return default
    return response.startswith('y')

def setup_blog():
    """Interactive setup for blog configuration"""
    print("🚀 Welcome to Jupyter Book Blog Setup!")
    print("=" * 50)
    print("This script will help you customize your blog.")
    print("Press Enter to use default values shown in brackets.\n")

    # Load existing config if it exists
    config_path = Path('blog_config.json')
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("📝 Found existing configuration. You can update the values below.\n")
    else:
        config = {}

    # Get blog information
    print("📖 BLOG INFORMATION")
    print("-" * 20)

    blog_title = get_user_input(
        "Blog title",
        config.get('blog', {}).get('title', 'My Technical Blog')
    )

    blog_description = get_user_input(
        "Blog description",
        config.get('blog', {}).get('description', 'A technical blog powered by Jupyter Book')
    )

    author_name = get_user_input(
        "Author name",
        config.get('blog', {}).get('author', 'Your Name')
    )

    print(f"\n🔗 REPOSITORY INFORMATION")
    print("-" * 25)

    github_username = get_user_input(
        "GitHub username",
        config.get('social', {}).get('github', 'yourusername')
    )

    repo_name = get_user_input(
        "Repository name",
        'jupyter-book-blog'
    )

    repository_url = f"https://github.com/{github_username}/{repo_name}"
    website_url = f"https://{github_username}.github.io/{repo_name}"

    print(f"\n📧 CONTACT INFORMATION (optional)")
    print("-" * 33)

    email = get_user_input(
        "Email",
        config.get('social', {}).get('email', '')
    )

    twitter = get_user_input(
        "Twitter username (without @)",
        config.get('social', {}).get('twitter', '')
    )

    linkedin = get_user_input(
        "LinkedIn profile",
        config.get('social', {}).get('linkedin', '')
    )

    print(f"\n🏠 HOMEPAGE SETTINGS")
    print("-" * 19)

    welcome_text = get_user_input(
        "Welcome message",
        config.get('homepage', {}).get('welcome_text',
                  f"Welcome to {blog_title}! This is where I share my thoughts, experiences, and insights on various topics.")
    )

    print(f"\n📝 POST SETTINGS")
    print("-" * 16)

    max_posts = get_user_input(
        "Max posts on homepage (0 = all)",
        str(config.get('posts', {}).get('max_posts_on_homepage', 0))
    )

    try:
        max_posts = int(max_posts)
    except ValueError:
        max_posts = 0

    print(f"\n🚀 DEPLOYMENT SETTINGS")
    print("-" * 21)

    github_actions_enabled = yes_no_prompt(
        "Enable GitHub Actions automatic deployment?",
        config.get('deployment', {}).get('github_actions', {}).get('enabled', False)
    )

    # Build configuration
    new_config = {
        "_comment": "Blog Configuration - Customize your Jupyter Book blog settings",
        "_schema_version": "1.0",
        "blog": {
            "title": blog_title,
            "description": blog_description,
            "author": author_name,
            "copyright": f"© 2024 {author_name}. All rights reserved.",
            "logo": "images/general/logo.png",
            "favicon": "images/general/logo.png"
        },
        "urls": {
            "repository": repository_url,
            "website": website_url,
            "branch": "main"
        },
        "social": {
            "_comment": "Social links - leave empty string if not used",
            "github": github_username,
            "twitter": twitter,
            "linkedin": linkedin,
            "email": email
        },
        "navigation": {
            "_comment": "Configure navigation structure - Quick Links section",
            "quick_links": [
                {"title": "About", "file": "about"},
                {"title": "Projects", "file": "projects"},
                {"title": "Contact", "file": "contact"}
            ],
            "blog_section_title": "Blog Posts"
        },
        "homepage": {
            "welcome_text": welcome_text,
            "show_banner": True,
            "banner_image": "images/general/banner.jpg",
            "footer_note": "*Add your own posts to the `book/` directory and run `python scripts/generate_posts.py` to update this page automatically.*"
        },
        "posts": {
            "_comment": "Blog post settings",
            "max_posts_on_homepage": max_posts,
            "description_length": 150,
            "date_format": "%B %d, %Y",
            "sort_order": "newest_first",
            "supported_date_formats": [
                "%B %d, %Y",
                "%Y-%m-%d",
                "%d/%m/%Y",
                "%m/%d/%Y"
            ]
        },
        "features": {
            "github_buttons": {
                "repository": True,
                "issues": True,
                "edit": True,
                "download": True
            },
            "search": True,
            "mermaid_diagrams": True,
            "math_equations": True
        },
        "deployment": {
            "_comment": "Deployment settings",
            "github_actions": {
                "enabled": github_actions_enabled,
                "_comment": "Set to false to disable GitHub Actions deployment"
            }
        },
        "build": {
            "_comment": "Build settings",
            "exclude_patterns": [
                "_build",
                "Thumbs.db",
                ".DS_Store",
                "**.ipynb_checkpoints"
            ],
            "execute_notebooks": "auto"
        }
    }

    # Save configuration
    with open('blog_config.json', 'w', encoding='utf-8') as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Configuration saved to blog_config.json")

    # Ask if user wants to apply changes
    if yes_no_prompt("\n🔄 Apply configuration to all files now?", True):
        print("\n📋 Applying configuration...")

        import subprocess
        import sys

        try:
            # Run sync script
            result = subprocess.run([sys.executable, 'scripts/sync_config.py'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Configuration synced successfully!")
            else:
                print(f"❌ Error syncing configuration: {result.stderr}")

            # Run update scripts
            subprocess.run([sys.executable, 'scripts/update_toc.py'])
            subprocess.run([sys.executable, 'scripts/generate_posts.py'])

            print("\n🎉 Setup complete! Your blog is now customized.")
            print("\nNext steps:")
            print("1. Review your blog_config.json file")
            print("2. Build your site: jupyter-book build .")
            print("3. Add your own posts to the book/ directory")

        except Exception as e:
            print(f"❌ Error applying configuration: {e}")
            print("You can manually run: python scripts/sync_config.py")

    else:
        print("\n📝 Configuration saved but not applied.")
        print("Run 'python scripts/sync_config.py' when ready to apply changes.")

if __name__ == "__main__":
    setup_blog()