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
    """Detect if content already has Hugo frontmatter"""
    if content.startswith('---\n'):
        # Find the end of frontmatter
        end_match = re.search(r'\n---\n', content[4:])
        if end_match:
            frontmatter_end = end_match.end() + 4
            frontmatter = content[4:frontmatter_end-4]  # Extract frontmatter without --- delimiters
            body = content[frontmatter_end:]
            return True, frontmatter, body
    return False, "", content

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

def create_hugo_frontmatter(title, slug):
    """Generate Hugo frontmatter for the post"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    frontmatter = f"""---
title: "{title}"
summary: ""
author:
  - Jamal Hansen
date: {today}
lastmod: ""
tags:
  - 
categories:
  - 
featureimage: ""
cardimage: ""
draft: true
toc: false
series: ""
canonical_url: https://jamalhansen.com/blog/{slug}
slug: {slug}
layout: post
---

"""
    return frontmatter

def setup_post_directory(content_dir, slug, title):
    """Create the Hugo post directory structure"""
    post_dir = Path(content_dir) / "blog" / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    
    # Create index.md with frontmatter
    index_file = post_dir / "index.md"
    frontmatter = create_hugo_frontmatter(title, slug)
    
    return post_dir, frontmatter

def categorize_images(images):
    """Categorize images into feature/card images vs inline content images"""
    if not images:
        return [], []
    
    print(f"\n📸 Found {len(images)} images. Let's categorize them:")
    
    feature_images = []
    content_images = []
    
    # Show all images first
    for i, img in enumerate(images, 1):
        print(f"  {i}. {img}")
    
    print(f"\n💡 Image types:")
    print(f"   Feature/Card: Used for homepage cards, social sharing, post headers")
    print(f"   Content: Inline images within the post content")
    
    # Get feature/card image selections
    while True:
        try:
            feature_input = input(f"\n🎯 Enter numbers of FEATURE/CARD images (comma-separated, or 'none'): ").strip()
            
            if feature_input.lower() in ['none', '']:
                break
                
            feature_nums = [int(x.strip()) for x in feature_input.split(',')]
            
            # Validate numbers
            if all(1 <= num <= len(images) for num in feature_nums):
                feature_images = [images[num-1] for num in feature_nums]
                break
            else:
                print(f"❌ Please enter numbers between 1 and {len(images)}")
                
        except ValueError:
            print("❌ Please enter valid numbers separated by commas")
    
    # Rest are content images
    content_images = [img for img in images if img not in feature_images]
    
    print(f"\n📁 Categorization result:")
    if feature_images:
        print(f"   Feature/Card ({len(feature_images)}): {', '.join(feature_images)}")
    if content_images:
        print(f"   Content ({len(content_images)}): {', '.join(content_images)}")
    
    return feature_images, content_images

def copy_images_from_obsidian(vault_path, post_dir, slug, feature_images, content_images, script_dir):
    """Copy images from Obsidian vault to appropriate Hugo directories"""
    if not vault_path or not os.path.exists(vault_path):
        print(f"Warning: Vault path '{vault_path}' not found. You'll need to copy images manually.")
        return [], []
    
    vault = Path(vault_path)
    assets_dir = script_dir / "assets" / slug
    
    # Create directories
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    copied_feature = []
    copied_content = []
    
    # Copy feature/card images to assets
    if feature_images:
        print(f"\n📸 Copying feature/card images to /assets/{slug}/:")
        for image in feature_images:
            image_files = list(vault.rglob(image))
            
            if image_files:
                src_image = image_files[0]
                dst_image = assets_dir / image
                
                try:
                    shutil.copy2(src_image, dst_image)
                    copied_feature.append(image)
                    print(f"   ✓ {image}")
                except Exception as e:
                    print(f"   ✗ Failed to copy {image}: {e}")
            else:
                print(f"   ✗ Image not found in vault: {image}")
    
    # Copy content images to post directory  
    if content_images:
        print(f"\n📝 Copying content images to post directory:")
        for image in content_images:
            image_files = list(vault.rglob(image))
            
            if image_files:
                src_image = image_files[0]
                dst_image = post_dir / image
                
                try:
                    shutil.copy2(src_image, dst_image)
                    copied_content.append(image)
                    print(f"   ✓ {image}")
                except Exception as e:
                    print(f"   ✗ Failed to copy {image}: {e}")
            else:
                print(f"   ✗ Image not found in vault: {image}")
    
    return copied_feature, copied_content

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
        converted_content = convert_obsidian_to_hugo(content)
        frontmatter = create_hugo_frontmatter(title, slug)
        final_content = frontmatter + converted_content
    
    # Extract images from the body content (not frontmatter)
    images = extract_images_from_content(converted_body if has_frontmatter else convert_obsidian_to_hugo(content))
    
    # Setup Hugo post directory
    script_dir = Path(__file__).parent.parent
    content_dir = script_dir / "content"
    post_dir = Path(content_dir) / "blog" / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    
    # Categorize images if any exist
    feature_images, content_images = [], []
    if images and vault_path:
        feature_images, content_images = categorize_images(images)
    
    # Write the converted markdown
    index_file = post_dir / "index.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    # Copy images from Obsidian vault
    if images:
        if vault_path:
            copied_feature, copied_content = copy_images_from_obsidian(
                vault_path, post_dir, slug, feature_images, content_images, script_dir
            )
            
            total_copied = len(copied_feature) + len(copied_content)
            print(f"\n✅ Successfully copied {total_copied} images:")
            if copied_feature:
                print(f"   📸 Feature/Card: {len(copied_feature)} → /assets/{slug}/")
            if copied_content:
                print(f"   📝 Content: {len(copied_content)} → /content/blog/{slug}/")
        else:
            print(f"\nFound {len(images)} images:")
            for img in images:
                print(f"  - {img}")
            print("\nNo vault path provided. Copy these images manually.")
    
    print(f"\n🎉 Post created successfully!")
    print(f"📁 Location: {post_dir}")
    print(f"📝 File: {index_file}")
    print(f"\n💡 Next steps:")
    print(f"   1. Edit the frontmatter in {index_file}")
    if feature_images:
        print(f"   2. Update featureimage and/or cardimage in frontmatter:")
        for img in feature_images:
            print(f"      - {img}")
    print(f"   3. Set draft: false when ready to publish")
    print(f"   4. Add tags, categories, and summary")
    
    if not vault_path and images:
        print(f"   5. Copy images manually from your Obsidian vault")

if __name__ == "__main__":
    main()