#!/usr/bin/env python3
"""
Script to sync blog_config.json settings with _config.yml and other files.
Run this after updating blog_config.json to apply changes throughout the site.
"""

import json
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def load_blog_config() -> Optional[Dict[str, Any]]:
    """Load blog configuration from blog_config.json"""
    config_path = Path('blog_config.json')

    if not config_path.exists():
        print("❌ Error: blog_config.json not found")
        print("Please make sure blog_config.json exists in the root directory")
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Loaded blog_config.json")
        return config
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in blog_config.json: {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading blog_config.json: {e}")
        return None


def get_nested_value(config: Dict[str, Any], *keys, default=None):
    """Safely get nested dictionary values"""
    value = config
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, default)
        else:
            return default
    return value if value is not None else default


def discover_bib_files(config: Dict[str, Any]) -> list:
    """
    Discover .bib files based on bibliography configuration mode.

    Supports three modes:
    - 'global': Use only global.bib
    - 'per-post': Look for matching .bib files per post
    - 'all-files': Use all .bib files in references/
    - 'auto': Smart detection with fallbacks (default)
    """
    bib_config = get_nested_value(config, 'bibliography', default={})
    mode = bib_config.get('mode', 'auto')
    global_file = bib_config.get('global_file', 'references/global.bib')

    bib_files = []

    if mode == 'global':
        # Simple: use only the global file
        if Path(global_file).exists():
            bib_files.append(global_file)
        else:
            print(f"⚠️  Warning: Global bibliography file {global_file} not found")

    elif mode == 'per-post':
        # Scan for matching .bib files in posts/
        posts_dir = Path('posts')
        if posts_dir.exists():
            for bib_file in posts_dir.glob('*.bib'):
                if not bib_file.name.startswith('_'):
                    bib_files.append(str(bib_file))
        # Fallback to global if no per-post files found
        if not bib_files and Path(global_file).exists():
            bib_files.append(global_file)

    elif mode == 'all-files':
        # Discover all .bib files based on scan patterns
        scan_patterns = bib_config.get('discovery', {}).get('scan_patterns',
                                                             ['references/*.bib', 'posts/*.bib'])
        exclude_patterns = bib_config.get('discovery', {}).get('exclude_patterns', [])

        for pattern in scan_patterns:
            for bib_file in Path('.').glob(pattern):
                # Check if file should be excluded
                should_exclude = False
                for exclude_pattern in exclude_patterns:
                    if Path('.').glob(exclude_pattern):
                        # Simple check: if filename starts with _ or matches exclude
                        if bib_file.name.startswith('_') or 'backup' in bib_file.name.lower():
                            should_exclude = True
                            break

                if not should_exclude and bib_file.is_file():
                    bib_files.append(str(bib_file))

    else:  # mode == 'auto' or default
        # Auto mode: Try to find the best match
        # Priority: per-post files > all files in references/ > global file

        # Check for per-post .bib files
        posts_dir = Path('posts')
        if posts_dir.exists():
            for bib_file in posts_dir.glob('*.bib'):
                if not bib_file.name.startswith('_'):
                    bib_files.append(str(bib_file))

        # Check for files in references/ directory
        refs_dir = Path('references')
        if refs_dir.exists():
            for bib_file in refs_dir.glob('*.bib'):
                if not bib_file.name.startswith('_'):
                    bib_files.append(str(bib_file))

        # Fallback to global file if nothing found
        if not bib_files and Path(global_file).exists():
            bib_files.append(global_file)

    # Remove duplicates while preserving order
    seen = set()
    unique_bib_files = []
    for f in bib_files:
        if f not in seen:
            seen.add(f)
            unique_bib_files.append(f)

    if unique_bib_files:
        print(f"📚 Discovered {len(unique_bib_files)} bibliography file(s):")
        for f in unique_bib_files[:5]:  # Show first 5
            print(f"   - {f}")
        if len(unique_bib_files) > 5:
            print(f"   ... and {len(unique_bib_files) - 5} more")
    else:
        print("⚠️  Warning: No bibliography files found")
        # Return at least the default path so config doesn't break
        unique_bib_files = ['references/global.bib']

    return unique_bib_files


def update_jupyter_book_config(config: Dict[str, Any]) -> bool:
    """Update _config.yml with values from blog_config.json using proper YAML parsing"""
    config_path = Path('_config.yml')

    if not config_path.exists():
        print("❌ Error: _config.yml not found")
        return False

    try:
        # Read current config as YAML
        with open(config_path, 'r', encoding='utf-8') as f:
            jb_config = yaml.safe_load(f)

        if jb_config is None:
            jb_config = {}

        # Update title and author
        jb_config['title'] = get_nested_value(config, 'blog', 'title', default='My Blog')
        jb_config['author'] = get_nested_value(config, 'blog', 'author', default='Blog Author')

        # Handle logo (can be text or image)
        logo_config = get_nested_value(config, 'blog', 'logo', default={})
        if isinstance(logo_config, dict):
            logo_type = logo_config.get('type', 'image')
            logo_value = logo_config.get('value', 'images/general/logo.png')
            if logo_type == 'text':
                # For text logos, we still need an image file for Jupyter Book
                # User should provide a simple text image or we use default
                jb_config['logo'] = logo_value if logo_value and not logo_value.isspace() else ''
            else:  # image or URL
                jb_config['logo'] = logo_value
        else:
            # Backward compatibility: if logo is just a string
            jb_config['logo'] = logo_config

        # Update repository settings
        if 'repository' not in jb_config:
            jb_config['repository'] = {}
        jb_config['repository']['url'] = get_nested_value(config, 'urls', 'repository',
                                                           default='https://github.com/yourusername/repo')
        jb_config['repository']['branch'] = get_nested_value(config, 'urls', 'branch', default='main')

        # Update HTML settings
        if 'html' not in jb_config:
            jb_config['html'] = {}

        jb_config['html']['favicon'] = get_nested_value(config, 'blog', 'favicon',
                                                         default='images/general/logo.png')
        jb_config['html']['baseurl'] = get_nested_value(config, 'urls', 'website',
                                                          default='https://yourusername.github.io/repo')

        # Update GitHub buttons
        features = get_nested_value(config, 'features', 'github_buttons', default={})
        jb_config['html']['use_repository_button'] = features.get('repository', True)
        jb_config['html']['use_issues_button'] = features.get('issues', True)
        jb_config['html']['use_edit_page_button'] = features.get('edit', True)
        jb_config['html']['use_download_button'] = features.get('download', True)

        # Update sphinx config for theme options
        if 'sphinx' not in jb_config:
            jb_config['sphinx'] = {}
        if 'config' not in jb_config['sphinx']:
            jb_config['sphinx']['config'] = {}

        if 'html_theme_options' not in jb_config['sphinx']['config']:
            jb_config['sphinx']['config']['html_theme_options'] = {}

        theme_options = jb_config['sphinx']['config']['html_theme_options']
        theme_options['repository_url'] = get_nested_value(config, 'urls', 'repository',
                                                             default='https://github.com/yourusername/repo')
        theme_options['use_repository_button'] = features.get('repository', True)
        theme_options['use_issues_button'] = features.get('issues', True)
        theme_options['use_edit_page_button'] = features.get('edit', True)
        theme_options['use_download_button'] = features.get('download', True)

        # Update copyright in footer
        copyright_text = get_nested_value(config, 'blog', 'copyright',
                                          default='© 2024 Blog Author. All rights reserved.')
        theme_options['extra_footer'] = f"<p>\n{copyright_text}\n</p>"

        # Update exclude patterns
        exclude_patterns = get_nested_value(config, 'build', 'exclude_patterns',
                                             default=['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints'])
        jb_config['exclude_patterns'] = exclude_patterns

        # Update execute notebooks setting
        if 'execute' not in jb_config:
            jb_config['execute'] = {}
        execute_notebooks = get_nested_value(config, 'build', 'execute_notebooks', default='auto')
        jb_config['execute']['execute_notebooks'] = execute_notebooks

        # Update bibliography settings
        bib_config = get_nested_value(config, 'bibliography', default={})
        if bib_config:
            # Discover .bib files based on mode
            bib_files = discover_bib_files(config)
            jb_config['bibtex_bibfiles'] = bib_files

            # Set citation style
            citation_style = bib_config.get('citation_style', 'author_year')
            # Handle custom styles (e.g., "custom:ieee" -> "ieee")
            if citation_style.startswith('custom:'):
                citation_style = citation_style.split(':', 1)[1]

            jb_config['sphinx']['config']['bibtex_reference_style'] = citation_style

        # Write updated config back to file
        # First read the original file to preserve comments at the top
        with open(config_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Extract the comment header (lines starting with #)
        lines = original_content.split('\n')
        header_lines = []
        for line in lines:
            if line.strip().startswith('#'):
                header_lines.append(line)
            else:
                break

        # Write header + updated YAML
        with open(config_path, 'w', encoding='utf-8') as f:
            if header_lines:
                f.write('\n'.join(header_lines) + '\n\n')
            yaml.dump(jb_config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print("✅ Updated _config.yml")
        return True

    except yaml.YAMLError as e:
        print(f"❌ Error parsing _config.yml: {e}")
        return False
    except Exception as e:
        print(f"❌ Error updating _config.yml: {e}")
        return False


def update_index_page(config: Dict[str, Any]) -> bool:
    """Update index.md with values from blog_config.json"""
    index_path = Path('index.md')

    if not index_path.exists():
        print("❌ Error: index.md not found")
        return False

    try:
        # Read current index
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')

        # Update title (first line if it starts with #)
        blog_title = get_nested_value(config, 'blog', 'title', default='My Blog')
        if lines and lines[0].startswith('# '):
            lines[0] = f'# {blog_title}'

        # Handle banner (can be image, URL, text, or none)
        banner_config = get_nested_value(config, 'homepage', 'banner', default={})
        banner_type = banner_config.get('type', 'none') if isinstance(banner_config, dict) else 'none'
        banner_value = banner_config.get('value', '') if isinstance(banner_config, dict) else ''
        banner_alt = banner_config.get('alt_text', 'Banner') if isinstance(banner_config, dict) else 'Banner'

        # Generate banner line based on type
        banner_line = ''
        if banner_type == 'image' or banner_type == 'url':
            banner_line = f'![{banner_alt}]({banner_value})'
        elif banner_type == 'text':
            banner_line = f'**{banner_value}**'
        # else: banner_type == 'none', banner_line stays empty

        # Find and update/remove existing banner
        banner_found = False
        for i, line in enumerate(lines):
            if line.startswith('![') or (i > 0 and i < 5 and line.startswith('**') and line.endswith('**')):
                if banner_line:
                    lines[i] = banner_line
                else:
                    lines[i] = ''
                banner_found = True
                break

        # Add banner if not found and should be shown
        if not banner_found and banner_line and len(lines) > 1:
            lines.insert(1, '')
            lines.insert(2, banner_line)

        # Update welcome text (line that starts with "Welcome to")
        welcome_text = get_nested_value(config, 'homepage', 'welcome_text',
                                        default='Welcome to my technical blog!')
        for i, line in enumerate(lines):
            if line.startswith('Welcome to'):
                lines[i] = welcome_text
                break

        # Write updated index
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        print("✅ Updated index.md")
        return True

    except Exception as e:
        print(f"❌ Error updating index.md: {e}")
        return False


def main():
    """Main function to sync all configurations"""
    print("🔄 Syncing blog configuration...")
    print()

    # Load blog config
    config = load_blog_config()
    if not config:
        sys.exit(1)

    # Update files
    success = True
    success &= update_jupyter_book_config(config)
    success &= update_index_page(config)

    print()
    if success:
        print("✅ Configuration sync completed successfully!")
        print("\nNext steps:")
        print("1. Run: python scripts/update_toc.py")
        print("2. Run: python scripts/generate_posts.py")
        print("3. Build: jupyter-book build .")
    else:
        print("❌ Configuration sync completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()