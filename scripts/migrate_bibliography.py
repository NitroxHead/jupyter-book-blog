#!/usr/bin/env python3
"""
Migration script for updating to the new bibliography system.

Helps users migrate from the old book/references.bib structure
to the new references/ directory structure.
"""

import sys
from pathlib import Path
import shutil


def migrate_bibliography():
    """Interactive migration to new bibliography structure."""
    print("📚 Bibliography Migration Tool")
    print("=" * 50)
    print()
    print("This script will help you migrate to the new bibliography system.")
    print()

    # Check if old structure exists
    old_bib = Path('book/references.bib')
    old_posts = Path('book')
    new_refs_dir = Path('references')
    new_posts = Path('posts')

    if not old_bib.exists() and not old_posts.exists():
        print("✅ No migration needed - you're already using the new structure!")
        return

    print("📋 Found old structure to migrate:")
    if old_bib.exists():
        print(f"   - {old_bib}")
    if old_posts.exists() and list(old_posts.glob('*.md')):
        print(f"   - {old_posts}/*.md files")
    print()

    # Ask user for confirmation
    response = input("Proceed with migration? [Y/n]: ").strip().lower()
    if response and not response.startswith('y'):
        print("❌ Migration cancelled")
        return

    print()
    print("🔄 Starting migration...")
    print()

    # Create new directories
    new_refs_dir.mkdir(exist_ok=True)
    new_posts.mkdir(exist_ok=True)
    print(f"✅ Created {new_refs_dir}/")
    print(f"✅ Created {new_posts}/")

    # Migrate references.bib
    if old_bib.exists():
        new_bib = new_refs_dir / 'global.bib'
        if new_bib.exists():
            backup = new_refs_dir / 'global.bib.backup'
            shutil.copy(new_bib, backup)
            print(f"📦 Backed up existing {new_bib} to {backup}")

        shutil.copy(old_bib, new_bib)
        print(f"✅ Migrated {old_bib} → {new_bib}")

    # Migrate blog posts
    if old_posts.exists():
        md_files = list(old_posts.glob('*.md'))
        bib_files = list(old_posts.glob('*.bib'))

        for md_file in md_files:
            if md_file.name not in ['README.md', 'references.md']:
                new_file = new_posts / md_file.name
                if new_file.exists():
                    backup = new_posts / f"{md_file.stem}.backup.md"
                    shutil.copy(new_file, backup)
                    print(f"📦 Backed up {new_file} to {backup}")

                shutil.copy(md_file, new_file)
                print(f"✅ Migrated {md_file} → {new_file}")

        for bib_file in bib_files:
            if bib_file.name != 'references.bib':
                new_file = new_posts / bib_file.name
                shutil.copy(bib_file, new_file)
                print(f"✅ Migrated {bib_file} → {new_file}")

    print()
    print("=" * 50)
    print("✅ Migration completed successfully!")
    print()
    print("📋 Next steps:")
    print("1. Review migrated files in references/ and posts/")
    print("2. Run: python scripts/sync_config.py")
    print("3. Run: python scripts/update_toc.py")
    print("4. Run: python scripts/generate_posts.py")
    print("5. Build: jupyter-book build .")
    print()
    print("💡 The old book/ directory is preserved for safety.")
    print("   You can delete it once you've verified the migration.")


if __name__ == "__main__":
    migrate_bibliography()
