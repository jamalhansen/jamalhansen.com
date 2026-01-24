#!/usr/bin/env python3
"""
Convert blog posts from qubt theme image format to PaperMod cover format.
"""

import re
import sys
from pathlib import Path


def convert_file(filepath):
    """Convert a single markdown file from qubt to PaperMod format."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split front matter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"Skipping {filepath}: No valid front matter found")
        return False
    
    front_matter = parts[1]
    body = parts[2]
    
    # Extract title, featureimage, and cardimage
    title_match = re.search(r'^title:\s*(.+)$', front_matter, re.MULTILINE)
    feature_match = re.search(r'^featureimage:\s*(.*)$', front_matter, re.MULTILINE)
    card_match = re.search(r'^cardimage:\s*(.*)$', front_matter, re.MULTILINE)
    
    if not feature_match and not card_match:
        print(f"Skipping {filepath}: No featureimage or cardimage found")
        return False
    
    # Get the values
    title = title_match.group(1).strip().strip('"\'') if title_match else "Featured Image"
    feature_image = feature_match.group(1).strip() if feature_match else None
    card_image = card_match.group(1).strip() if card_match else None
    
    # Use featureimage if it has a value, otherwise use cardimage
    # Skip if both are empty
    if feature_image and feature_image != '':
        image_to_use = feature_image
    elif card_image and card_image != '':
        image_to_use = card_image
    else:
        print(f"Skipping {filepath}: Both featureimage and cardimage are empty")
        return False
    
    # Create the cover block
    cover_block = f"""cover:
    image: {image_to_use}
    alt: "{title}"
    relative: true"""
    
    # Remove featureimage and cardimage lines
    new_front_matter = front_matter
    if feature_match:
        new_front_matter = re.sub(r'^featureimage:.*$\n?', '', new_front_matter, flags=re.MULTILINE)
    if card_match:
        new_front_matter = re.sub(r'^cardimage:.*$\n?', '', new_front_matter, flags=re.MULTILINE)
    
    # Find the best location to insert the cover block (after categories or tags)
    # Look for categories or tags line to insert after
    insert_match = re.search(r'^(categories:.*?\n(?:(?:  - .+\n)*)?)', new_front_matter, re.MULTILINE)
    if not insert_match:
        insert_match = re.search(r'^(tags:.*?\n(?:(?:  - .+\n)*)?)', new_front_matter, re.MULTILINE)
    
    if insert_match:
        # Insert after categories/tags
        insert_pos = insert_match.end()
        new_front_matter = (
            new_front_matter[:insert_pos] + 
            cover_block + '\n' +
            new_front_matter[insert_pos:]
        )
    else:
        # Just append before draft if possible, otherwise at the end
        draft_match = re.search(r'^draft:', new_front_matter, re.MULTILINE)
        if draft_match:
            insert_pos = draft_match.start()
            new_front_matter = (
                new_front_matter[:insert_pos] + 
                cover_block + '\n' +
                new_front_matter[insert_pos:]
            )
        else:
            new_front_matter = new_front_matter.rstrip() + '\n' + cover_block + '\n'
    
    # Reconstruct the file
    new_content = '---' + new_front_matter + '---' + body
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Converted: {filepath}")
    print(f"  Image: {image_to_use}")
    print(f"  Alt: {title}")
    return True


def main():
    """Main function to process all blog posts."""
    blog_dir = Path('/Users/jamalhansen/projects/jamalhansen.com/content/blog')
    
    if not blog_dir.exists():
        print(f"Error: Blog directory not found: {blog_dir}")
        sys.exit(1)
    
    # Find all index.md files
    index_files = list(blog_dir.glob('*/index.md'))
    
    if not index_files:
        print("No index.md files found")
        sys.exit(1)
    
    print(f"Found {len(index_files)} blog posts\n")
    
    converted = 0
    skipped = 0
    
    for filepath in sorted(index_files):
        if convert_file(filepath):
            converted += 1
        else:
            skipped += 1
        print()
    
    print(f"\nSummary:")
    print(f"  Converted: {converted}")
    print(f"  Skipped: {skipped}")
    print(f"  Total: {len(index_files)}")


if __name__ == '__main__':
    main()
