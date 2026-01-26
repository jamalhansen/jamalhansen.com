#!/usr/bin/env python3
"""
Convert Obsidian markdown to Hugo-compatible markdown with page bundle setup
Usage: python obsidian-to-hugo.py input.md post-slug [obsidian-vault-path]
"""
import sys
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

def detect_existing_frontmatter(content):
    """Detect if content already has Hugo frontmatter.
    Returns (has_frontmatter: bool, frontmatter: str, body: str).
    """
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', content, flags=re.DOTALL)
    if m:
        frontmatter = m.group(1)
        body = m.group(2)
        return True, frontmatter, body
    return False, "", content

def clean_obsidian_links_from_frontmatter(frontmatter):
    """Remove Obsidian wiki-link syntax [[]] from frontmatter values"""
    # Remove [[ and ]] from frontmatter values (e.g., series: "[[SQL for Python]]" -> series: "SQL for Python")
    frontmatter = re.sub(r'\[\[([^\]]+)\]\]', r'\1', frontmatter)
    return frontmatter

def normalize_frontmatter_fields(frontmatter):
    """Normalize frontmatter field names to PaperMod theme conventions"""
    # Change summary: to description: (PaperMod uses description)
    frontmatter = re.sub(r'^summary:', 'description:', frontmatter, flags=re.MULTILINE)

    # Remove # prefix from tags (e.g., #python -> python, #sql -> sql)
    def remove_tag_hashes(match):
        tags_section = match.group(0)
        tags_section = re.sub(r'- ["\']*#([^"\'\n]+)["\']*', r'- \1', tags_section)
        return tags_section

    frontmatter = re.sub(
        r'^tags:\s*\n(?:  - [^\n]+\n)*',
        remove_tag_hashes,
        frontmatter,
        flags=re.MULTILINE
    )

    # Convert simple image: field to cover: block for PaperMod
    image_match = re.search(r'^image:\s*["\']?([^"\'\n]+)["\']?\s*$', frontmatter, re.MULTILINE)
    if image_match:
        image_value = image_match.group(1).strip()
        if image_value:
            cover_block = f'''cover:
  image: "{image_value}"
  alt: ""
  caption: ""
  relative: true'''
            frontmatter = re.sub(r'^image:\s*["\']?[^"\'\n]*["\']?\s*$', cover_block, frontmatter, flags=re.MULTILINE)
        else:
            # Remove empty image: field
            frontmatter = re.sub(r'^image:\s*["\']?["\']?\s*\n', '', frontmatter, flags=re.MULTILINE)

    # Convert toc: to ShowToc: (PaperMod convention)
    frontmatter = re.sub(r'^toc:\s*true', 'ShowToc: true\nTocOpen: false', frontmatter, flags=re.MULTILINE)
    frontmatter = re.sub(r'^toc:\s*false', 'ShowToc: false', frontmatter, flags=re.MULTILINE)

    # Remove fields not used by PaperMod
    frontmatter = re.sub(r'^canonical_url:.*\n', '', frontmatter, flags=re.MULTILINE)
    frontmatter = re.sub(r'^layout:.*\n', '', frontmatter, flags=re.MULTILINE)
    frontmatter = re.sub(r'^slug:.*\n', '', frontmatter, flags=re.MULTILINE)
    frontmatter = re.sub(r'^lastmod:\s*["\']?["\']?\s*\n', '', frontmatter, flags=re.MULTILINE)

    return frontmatter

def convert_obsidian_to_hugo(content):
    """Convert Obsidian syntax to Hugo-compatible markdown"""
    # Convert ![[image.jpg]] to ![Image](image.jpg)
    content = re.sub(r'!\[\[([^\]]+)\]\]', r'![Image](\1)', content)
    
    # Convert ![[image.jpg|alt text]] to ![alt text](image.jpg)
    content = re.sub(r'!\[\[([^\]|]+)\|([^\]]+)\]\]', r'![\2](\1)', content)
    
    # Convert [[Link]] to [Link](link) - remove if you don't want this
    # content = re.sub(r'\[\[([^\]]+)\]\]', r'[\1](\1)', content)
    
    return content

def extract_images_from_content(content):
    """Extract all image references from markdown content"""
    # Match ![any](image.ext) patterns
    image_pattern = r'!\[.*?\]\(([^)]+)\)'
    images = re.findall(image_pattern, content)
    return images

# extract_frontmatter_images removed — frontmatter image promotion is no longer performed.

def create_hugo_frontmatter(title):
    """Generate Hugo frontmatter for PaperMod theme"""
    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = f"""---
title: "{title}"
date: {today}
draft: true
description: ""
tags: []
categories: []
series: []
cover:
  image: ""
  alt: ""
  caption: ""
  relative: true
ShowToc: true
TocOpen: false
---

"""
    return frontmatter

def copy_images_from_obsidian(vault_path, post_dir, feature_images, content_images):
    """Copy images from Obsidian vault to post directory (Hugo page bundle structure).
    Matching is done by filename (basename) to avoid glob/path issues.
    """
    if not vault_path or not os.path.exists(vault_path):
        print(f"Warning: Vault path '{vault_path}' not found. You'll need to copy images manually.")
        return [], []

    vault = Path(vault_path)
    copied_feature = []
    copied_content = []

    all_images = feature_images + content_images
    if not all_images:
        return copied_feature, copied_content

    print(f"\n📸 Copying images to post directory:")
    for image in all_images:
        src_candidates = list(vault.rglob(Path(image).name))
        if not src_candidates:
            print(f"   ✗ Image not found in vault: {image}")
            continue

        src_image = src_candidates[0]
        dst_image = post_dir / Path(image).name
        dst_image.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src_image, dst_image)
            if image in feature_images:
                copied_feature.append(image)
                print(f"   ✓ {image} (cover image)")
            else:
                copied_content.append(image)
                print(f"   ✓ {image}")
        except Exception as e:
            print(f"   ✗ Failed to copy {image}: {e}")

    return copied_feature, copied_content

def copy_all_images_from_source_folder(input_file, post_dir):
    """Copy all image files from the source markdown's folder to the post directory.
    This ensures cover images and any other images in the folder are included.
    """
    source_dir = Path(input_file).parent
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.avif'}

    copied_images = []

    for file in source_dir.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:
            dst_image = post_dir / file.name
            try:
                shutil.copy2(file, dst_image)
                copied_images.append(file.name)
                print(f"   ✓ {file.name}")
            except Exception as e:
                print(f"   ✗ Failed to copy {file.name}: {e}")

    return copied_images

def main():
    if len(sys.argv) < 3:
        print("Usage: python obsidian-to-hugo.py input.md post-slug [obsidian-vault-path]")
        print("\nExample:")
        print("  python obsidian-to-hugo.py ~/my-post.md my-awesome-post ~/Documents/ObsidianVault")
        sys.exit(1)
    
    input_file = sys.argv[1]
    slug = sys.argv[2]
    vault_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Read the Obsidian markdown file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Check if content already has Hugo frontmatter
    has_frontmatter, existing_frontmatter, body_content = detect_existing_frontmatter(content)

    if has_frontmatter:
        print("✅ Detected existing Hugo frontmatter - preserving it")
        # Clean Obsidian wiki-links from frontmatter
        existing_frontmatter = clean_obsidian_links_from_frontmatter(existing_frontmatter)
        # Normalize field names (description -> summary, featured_image -> featureimage, thumbnail -> cardimage)
        existing_frontmatter = normalize_frontmatter_fields(existing_frontmatter)
        # Use existing frontmatter, just convert the body content
        converted_body = convert_obsidian_to_hugo(body_content)
        final_content = f"---\n{existing_frontmatter}\n---\n{converted_body}"

        # Extract title from existing frontmatter
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', existing_frontmatter, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip('"\'')
        else:
            title = Path(input_file).stem.replace('-', ' ').title()
    else:
        print("ℹ️  No existing frontmatter found - creating new Hugo frontmatter")
        # Extract title from first heading or use filename
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = Path(input_file).stem.replace('-', ' ').title()

        # Convert content and create new frontmatter
        converted_body = convert_obsidian_to_hugo(content)
        frontmatter = create_hugo_frontmatter(title)
        final_content = frontmatter + converted_body

    # Extract images from the body content (all images are handled from content)
    body_images = extract_images_from_content(converted_body)

    # Setup Hugo post directory
    script_dir = Path(__file__).parent.parent
    content_dir = script_dir / "content"
    post_dir = Path(content_dir) / "blog" / slug
    post_dir.mkdir(parents=True, exist_ok=True)

    # All images come from content. No interactive categorization — treat all as content images.
    feature_images, content_images = [], body_images[:]
    if body_images and not vault_path:
        print(f"\n📸 Found {len(body_images)} images, but no vault path provided.")
        print("Images will not be copied automatically; copy them manually into the post directory.")

    # No separate frontmatter image extraction — keep feature_images as chosen from body images.

    # Write the converted markdown
    index_file = post_dir / "index.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    # Copy all images from the source folder (covers, content images, etc.)
    print(f"\n📸 Copying all images from source folder:")
    copied_from_folder = copy_all_images_from_source_folder(input_file, post_dir)

    if copied_from_folder:
        print(f"\n✅ Successfully copied {len(copied_from_folder)} images from source folder")
    else:
        # Fall back to vault-wide search for images referenced in content
        all_images = body_images
        if all_images:
            if vault_path:
                copied_feature, copied_content = copy_images_from_obsidian(
                    vault_path, post_dir, feature_images, content_images
                )

                total_copied = len(copied_feature) + len(copied_content)
                if total_copied > 0:
                    print(f"\n✅ Successfully copied {total_copied} images from vault:")
                    if copied_feature:
                        print(f"   📸 Cover image: {len(copied_feature)}")
                    if copied_content:
                        print(f"   📝 Content images: {len(copied_content)}")
                else:
                    print(f"\n⚠️  No images found in source folder or vault")
            else:
                print(f"\nFound {len(all_images)} images referenced:")
                for img in all_images:
                    print(f"  - {img}")
                print("\nNo vault path provided. Copy these images manually.")
    
    print(f"\n🎉 Post created successfully!")
    print(f"📁 Location: {post_dir}")
    print(f"📝 File: {index_file}")
    print(f"\n💡 Next steps:")
    print(f"   1. Edit the frontmatter in {index_file}")
    if copied_from_folder:
        print(f"   2. Set cover.image in frontmatter to one of:")
        for img in copied_from_folder:
            print(f"      - {img}")
    print(f"   3. Add tags, categories, and summary")
    print(f"   4. Set draft: false when ready to publish")

if __name__ == "__main__":
    main()