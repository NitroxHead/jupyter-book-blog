#!/usr/bin/env python3
"""
Bibliography validation script for Jupyter Book blog.

Checks for common issues:
- Duplicate citation keys across .bib files
- Invalid BibTeX syntax
- Missing .bib files referenced in posts
- Orphaned citations (cited but not defined)
- Unused references (defined but not cited)
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, List, Tuple

try:
    import frontmatter
except ImportError:
    print("❌ Error: python-frontmatter package not found")
    print("Please install it: pip install python-frontmatter")
    sys.exit(1)


def load_config():
    """Load blog configuration."""
    try:
        with open('blog_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def find_bib_files():
    """Find all .bib files in the project."""
    bib_files = []

    # Check references/ directory
    refs_dir = Path('references')
    if refs_dir.exists():
        for bib_file in refs_dir.glob('**/*.bib'):
            if not bib_file.name.startswith('_'):
                bib_files.append(bib_file)

    # Check posts/ directory
    posts_dir = Path('posts')
    if posts_dir.exists():
        for bib_file in posts_dir.glob('*.bib'):
            if not bib_file.name.startswith('_'):
                bib_files.append(bib_file)

    return bib_files


def parse_bib_file(bib_file: Path) -> Dict[str, int]:
    """
    Parse a .bib file and extract citation keys.

    Returns:
        Dict mapping citation key to line number
    """
    keys = {}
    try:
        with open(bib_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                # Match BibTeX entry: @article{key, @book{key, etc.
                match = re.match(r'@\w+\s*\{\s*([^,\s]+)', line)
                if match:
                    key = match.group(1)
                    keys[key] = line_num
    except Exception as e:
        print(f"⚠️  Warning: Error parsing {bib_file}: {e}")

    return keys


def check_duplicate_keys() -> Tuple[bool, List[str]]:
    """
    Check for duplicate citation keys across all .bib files.

    Returns:
        (has_errors, warnings)
    """
    print("\n🔍 Checking for duplicate citation keys...")

    bib_files = find_bib_files()
    if not bib_files:
        print("⚠️  No bibliography files found")
        return False, []

    # Build mapping: key -> [(file, line_number), ...]
    key_locations = defaultdict(list)

    for bib_file in bib_files:
        keys = parse_bib_file(bib_file)
        for key, line_num in keys.items():
            key_locations[key].append((bib_file, line_num))

    # Find duplicates
    has_errors = False
    warnings = []
    duplicates_found = 0

    for key, locations in key_locations.items():
        if len(locations) > 1:
            duplicates_found += 1
            has_errors = True
            warning = f"⚠️  Duplicate key '{key}' found in:"
            warnings.append(warning)
            print(warning)
            for file_path, line_num in locations:
                location = f"   - {file_path}:{line_num}"
                warnings.append(location)
                print(location)

            # Suggest fix
            suggestion = f"   💡 Suggestion: Use unique keys like '{key}_topic1', '{key}_topic2'"
            warnings.append(suggestion)
            print(suggestion)

    if not has_errors:
        print("✅ No duplicate citation keys found")
    else:
        print(f"\n❌ Found {duplicates_found} duplicate citation key(s)")

    return has_errors, warnings


def check_bibtex_syntax() -> Tuple[bool, List[str]]:
    """
    Check for basic BibTeX syntax errors.

    Returns:
        (has_errors, warnings)
    """
    print("\n🔍 Checking BibTeX syntax...")

    bib_files = find_bib_files()
    has_errors = False
    warnings = []

    for bib_file in bib_files:
        try:
            with open(bib_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic syntax checks
            open_braces = content.count('{')
            close_braces = content.count('}')

            if open_braces != close_braces:
                has_errors = True
                warning = f"⚠️  {bib_file}: Mismatched braces ({{: {open_braces}, }}: {close_braces})"
                warnings.append(warning)
                print(warning)

            # Check for common issues
            if '@@' in content:
                has_errors = True
                warning = f"⚠️  {bib_file}: Double @@ found (possible typo)"
                warnings.append(warning)
                print(warning)

        except Exception as e:
            has_errors = True
            warning = f"❌ Error reading {bib_file}: {e}"
            warnings.append(warning)
            print(warning)

    if not has_errors:
        print("✅ No syntax errors found")

    return has_errors, warnings


def find_citations_in_posts() -> Dict[Path, Set[str]]:
    """
    Find all citations used in blog posts.

    Returns:
        Dict mapping post file to set of cited keys
    """
    citations = {}
    posts_dir = Path('posts')

    if not posts_dir.exists():
        return citations

    for post_file in posts_dir.glob('*.md'):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                content = post.content

            # Find all {cite}`key` and {cite:t}`key` patterns
            cite_pattern = r'\{cite(?::t)?\}`([^`]+)`'
            matches = re.findall(cite_pattern, content)

            # Split multiple citations: {cite}`key1,key2,key3`
            cited_keys = set()
            for match in matches:
                keys = [k.strip() for k in match.split(',')]
                cited_keys.update(keys)

            if cited_keys:
                citations[post_file] = cited_keys

        except Exception as e:
            print(f"⚠️  Warning: Error parsing {post_file}: {e}")

    return citations


def check_orphaned_citations() -> Tuple[bool, List[str]]:
    """
    Check for citations used in posts but not defined in any .bib file.

    Returns:
        (has_warnings, warnings)
    """
    print("\n🔍 Checking for orphaned citations...")

    # Get all defined keys
    bib_files = find_bib_files()
    defined_keys = set()
    for bib_file in bib_files:
        keys = parse_bib_file(bib_file)
        defined_keys.update(keys.keys())

    # Get all cited keys
    post_citations = find_citations_in_posts()

    # Find orphaned citations
    has_warnings = False
    warnings = []

    for post_file, cited_keys in post_citations.items():
        orphaned = cited_keys - defined_keys
        if orphaned:
            has_warnings = True
            warning = f"⚠️  {post_file} cites undefined keys:"
            warnings.append(warning)
            print(warning)
            for key in sorted(orphaned):
                key_warning = f"   - {key}"
                warnings.append(key_warning)
                print(key_warning)

    if not has_warnings:
        print("✅ All cited keys are defined")

    return has_warnings, warnings


def check_unused_references() -> Tuple[bool, List[str]]:
    """
    Check for references defined but never cited (informational only).

    Returns:
        (has_info, info_messages)
    """
    print("\n🔍 Checking for unused references...")

    # Get all defined keys
    bib_files = find_bib_files()
    defined_keys = {}  # key -> file
    for bib_file in bib_files:
        keys = parse_bib_file(bib_file)
        for key in keys.keys():
            defined_keys[key] = bib_file

    # Get all cited keys
    post_citations = find_citations_in_posts()
    cited_keys = set()
    for keys in post_citations.values():
        cited_keys.update(keys)

    # Find unused
    unused = set(defined_keys.keys()) - cited_keys

    has_info = len(unused) > 0
    info_messages = []

    if unused:
        info = f"ℹ️  Found {len(unused)} unused reference(s) (this is informational):"
        info_messages.append(info)
        print(info)

        # Show first 10
        for key in sorted(list(unused)[:10]):
            file_info = f"   - {key} in {defined_keys[key].name}"
            info_messages.append(file_info)
            print(file_info)

        if len(unused) > 10:
            more_info = f"   ... and {len(unused) - 10} more"
            info_messages.append(more_info)
            print(more_info)

        tip = "   💡 Unused references are not an error - they may be for future use"
        info_messages.append(tip)
        print(tip)
    else:
        print("✅ All defined references are cited")

    return has_info, info_messages


def check_missing_bib_files() -> Tuple[bool, List[str]]:
    """
    Check if posts reference .bib files that don't exist.

    Returns:
        (has_errors, warnings)
    """
    print("\n🔍 Checking for missing bibliography files...")

    posts_dir = Path('posts')
    if not posts_dir.exists():
        return False, []

    has_errors = False
    warnings = []

    for post_file in posts_dir.glob('*.md'):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            # Check if post specifies a bibliography file
            if 'bibliography' in post.metadata:
                bib_file = post.metadata['bibliography']
                bib_path = Path(bib_file)

                if not bib_path.exists():
                    has_errors = True
                    warning = f"⚠️  {post_file} references missing file: {bib_file}"
                    warnings.append(warning)
                    print(warning)

        except Exception as e:
            print(f"⚠️  Warning: Error parsing {post_file}: {e}")

    if not has_errors:
        print("✅ All referenced bibliography files exist")

    return has_errors, warnings


def main():
    """Run all validation checks."""
    print("📚 Bibliography Validation")
    print("=" * 50)

    config = load_config()
    if config.get('bibliography', {}).get('validation', {}).get('strict_mode'):
        print("ℹ️  Running in STRICT mode (all warnings are errors)\n")
        strict = True
    else:
        strict = False

    all_errors = []
    all_warnings = []

    # Run checks
    errors, warnings = check_duplicate_keys()
    if errors:
        all_errors.extend(warnings)
    else:
        all_warnings.extend(warnings)

    errors, warnings = check_bibtex_syntax()
    if errors:
        all_errors.extend(warnings)

    errors, warnings = check_missing_bib_files()
    if errors:
        all_errors.extend(warnings)

    errors, warnings = check_orphaned_citations()
    if errors:
        all_errors.extend(warnings)

    # Unused references is informational only
    _, info = check_unused_references()

    # Summary
    print("\n" + "=" * 50)
    print("📊 Validation Summary")
    print("=" * 50)

    if all_errors:
        print(f"❌ Found {len(all_errors)} error(s)")
        if strict:
            print("⚠️  STRICT MODE: Build may fail")
            sys.exit(1)
        else:
            print("⚠️  Please review and fix the errors above")
            sys.exit(1)
    elif all_warnings:
        print(f"⚠️  Found {len(all_warnings)} warning(s)")
        print("✅ No critical errors")
    else:
        print("✅ All checks passed!")
        print("📚 Your bibliography is well-formed")

    print()


if __name__ == "__main__":
    main()
