#!/usr/bin/env python3
"""
Convert Obsidian markdown to Hugo-compatible markdown with page bundle setup.
Usage: python obsidian-to-hugo.py input.md post-slug [obsidian-vault-path]
"""
import sys
import re
import shutil
import unicodedata
from pathlib import Path
from datetime import datetime

def slugify(text):
    """
    Convert to ASCII. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Strip leading and trailing whitespace.
    """
    text = str(text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def detect_existing_frontmatter(content):
    """Detect if content already has Hugo/Obsidian frontmatter.
    Returns (has_frontmatter: bool, frontmatter: str, body: str).
    """
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', content, flags=re.DOTALL)
    if m:
        return True, m.group(1), m.group(2)
    return False, "", content

def yaml_str(value):
    """Escape a value for embedding in a YAML double-quoted string."""
    return value.replace('\\', '\\\\').replace('"', '\\"')

def clean_obsidian_links_from_frontmatter(frontmatter):
    """Remove Obsidian wiki-link syntax [[]] from frontmatter values"""
    return re.sub(r'\[\[([^\]]+)\]\]', r'\1', frontmatter)

def normalize_frontmatter_fields(frontmatter):
    """Normalize frontmatter field names to PaperMod theme conventions"""
    # Change summary: to description: (PaperMod uses description)
    frontmatter = re.sub(r'^summary:', 'description:', frontmatter, flags=re.MULTILINE)
    
    # PaperMod uses ShowToc instead of toc
    frontmatter = re.sub(r'^toc:\s*true', 'ShowToc: true\nTocOpen: false', frontmatter, flags=re.MULTILINE)
    frontmatter = re.sub(r'^toc:\s*false', 'ShowToc: false', frontmatter, flags=re.MULTILINE)

    # Clean up tags (remove # hashes and empty entries)
    def remove_tag_hashes(match):
        cleaned = re.sub(r'- ["\']*#([^"\'\n]+)["\']*', r'- \1', match.group(0))
        cleaned = re.sub(r'  -\s*\n', '', cleaned)
        return cleaned

    frontmatter = re.sub(r'^tags:\s*\n(?:  - [^\n]+\n)*', remove_tag_hashes, frontmatter, flags=re.MULTILINE)

    # Process Unsplash credit and Cover images
    unsplash_data = {
        'name': re.search(r'^unsplash_name:\s*["\']?([^"\'\n]+)["\']?\s*$', frontmatter, re.MULTILINE),
        'user': re.search(r'^unsplash_user:\s*["\']?([^"\'\n]+)["\']?\s*$', frontmatter, re.MULTILINE),
        'id': re.search(r'^unsplash_id:\s*["\']?([^"\'\n]+)["\']?\s*$', frontmatter, re.MULTILINE)
    }
    
    credit_info = {k: v.group(1).strip() for k, v in unsplash_data.items() if v}
    
    # Remove raw unsplash fields
    for field in ['unsplash_name', 'unsplash_user', 'unsplash_id']:
        frontmatter = re.sub(rf'^{field}:[^\n]*\n?', '', frontmatter, flags=re.MULTILINE)

    # Build credit block
    credit_block = ""
    if credit_info:
        credit_block = "\n  credit:"
        if 'name' in credit_info: credit_block += f'\n    name: "{yaml_str(credit_info["name"])}"'
        if 'user' in credit_info: credit_block += f'\n    username: "{yaml_str(credit_info["user"])}"'
        if 'id' in credit_info: credit_block += f'\n    photo_id: "{yaml_str(credit_info["id"])}"'

    # Convert simple image: to PaperMod cover:
    image_match = re.search(r'^image:\s*["\']?([^"\'\n]+)["\']?\s*$', frontmatter, re.MULTILINE)
    if image_match:
        img = image_match.group(1).strip()
        if img:
            cover_block = f'cover:\n  image: "{yaml_str(img)}"\n  alt: ""\n  caption: ""\n  relative: true{credit_block}'
            frontmatter = re.sub(r'^image:[^\n]*\n?', cover_block + '\n', frontmatter, flags=re.MULTILINE)
        else:
            frontmatter = re.sub(r'^image:[^\n]*\n?', '', frontmatter, flags=re.MULTILINE)
    elif credit_block:
        # Inject credit into existing cover if possible
        if 'cover:' in frontmatter:
            frontmatter = re.sub(r'(relative:\s*true)', r'\1' + credit_block, frontmatter)

    # Clean up redundant or theme-clashing fields
    for field in ['canonical_url', 'layout', 'slug', 'status', 'created',
                  'published_date', 'Category', 'promo_file', 'series_position']:
        frontmatter = re.sub(rf'^{field}:[^\n]*\n?', '', frontmatter, flags=re.MULTILINE)

    # Strip empty weight field
    frontmatter = re.sub(r'^weight:\s*\n?', '', frontmatter, flags=re.MULTILINE)

    # Convert series scalar string to Hugo array format; strip if empty
    series_scalar = re.search(r'^series:\s*(\S[^\n]*?)\s*$', frontmatter, re.MULTILINE)
    already_array = re.search(r'^series:\s*\n\s+-', frontmatter, re.MULTILINE)
    if series_scalar and not already_array:
        raw = series_scalar.group(1).strip()
        if raw in ('[]', ''):
            frontmatter = re.sub(r'^series:[^\n]*\n?', '', frontmatter, flags=re.MULTILINE)
        else:
            # Strip surrounding quotes of any style (handles 'value', "value", '"value"')
            value = raw.strip("'\"").strip("'\"")
            if value:
                frontmatter = re.sub(r'^series:[^\n]*\n?', f'series:\n  - "{value}"\n', frontmatter, flags=re.MULTILINE)
            else:
                frontmatter = re.sub(r'^series:[^\n]*\n?', '', frontmatter, flags=re.MULTILINE)

    return frontmatter.strip()

def convert_body_syntax(content):
    """Convert Obsidian-specific syntax to Hugo-compatible markdown"""
    # ![[image.jpg]] -> ![Image](image.jpg)
    content = re.sub(r'!\[\[([^\]|]+)\]\]', r'![Image](\1)', content)
    # ![[image.jpg|alt]] -> ![alt](image.jpg)
    content = re.sub(r'!\[\[([^\]|]+)\|([^\]]+)\]\]', r'![\2](\1)', content)
    # Obsidian callouts [!info] -> Hugo/Goldmark blockquotes (basic support)
    content = re.sub(r'^>\s+\[!(\w+)\]\+?\s*(.*)', r'> **\1**: \2', content, flags=re.MULTILINE | re.IGNORECASE)
    return content

def main():
    if len(sys.argv) < 3:
        print("Usage: python obsidian-to-hugo.py input.md post-slug [vault-path]")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    # Optimization: Ensure the slug is always clean (dashes, lowercase)
    slug = slugify(sys.argv[2])
    vault_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found")
        sys.exit(1)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    has_fm, fm, body = detect_existing_frontmatter(content)
    
    if has_fm:
        print("✅ Found existing frontmatter")
        fm = clean_obsidian_links_from_frontmatter(fm)
        fm = normalize_frontmatter_fields(fm)
        # Extract title from FM if possible
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
        title = title_match.group(1).strip('"\'') if title_match else input_path.stem.replace('-', ' ').title()
        # Inject author if missing
        if not re.search(r'^author:', fm, re.MULTILINE):
            fm = re.sub(r'^(date:[^\n]*)', r'\1\nauthor:\n  - Jamal Hansen', fm, count=1, flags=re.MULTILINE)
    else:
        print("ℹ️  Creating new frontmatter")
        # Extract title from first H1 or filename
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = h1_match.group(1).strip() if h1_match else input_path.stem.replace('-', ' ').title()
        fm = f'title: "{title}"\ndate: {datetime.now().strftime("%Y-%m-%d")}\nauthor:\n  - Jamal Hansen\ndraft: true\ndescription: ""\ntags: []\ncategories: []\nseries: []\ncover:\n  image: ""\n  alt: ""\n  caption: ""\n  relative: true\nShowToc: true\nTocOpen: false'

    converted_body = convert_body_syntax(body if has_fm else content)
    final_content = f"---\n{fm}\n---\n\n{converted_body}"

    # Setup Directory
    base_dir = Path(__file__).parent.parent
    blog_dir = base_dir / "content" / "blog" / slug
    blog_dir.mkdir(parents=True, exist_ok=True)
    
    # Write Post
    (blog_dir / "index.md").write_text(final_content, encoding='utf-8')
    
    # Image Handling
    print(f"\n📸 Copying images to: {blog_dir.relative_to(base_dir)}")
    
    # 1. Copy from source directory (if it's a page bundle or attachment in same folder)
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    source_dir = input_path.parent
    for img_file in source_dir.iterdir():
        if img_file.is_file() and img_file.suffix.lower() in image_exts:
            shutil.copy2(img_file, blog_dir / img_file.name)
            print(f"   ✓ {img_file.name}")

    # 2. Search vault for referenced images if not in source dir
    if vault_path and vault_path.exists():
        referenced_images = re.findall(r'!\[.*?\]\(([^)]+)\)', converted_body)
        blog_dir_resolved = blog_dir.resolve()
        for img_name in referenced_images:
            dest = (blog_dir / img_name).resolve()
            if not dest.is_relative_to(blog_dir_resolved):
                print(f"   ⚠️  Skipped suspicious image path: {img_name}")
                continue
            if not dest.exists():
                # Search vault (rglob can be slow on huge vaults, but works for most)
                matches = list(vault_path.rglob(img_name))
                if matches:
                    shutil.copy2(matches[0], dest)
                    print(f"   ✓ {img_name} (from vault)")

    print(f"\n🎉 Done! Folder created: {slug}")

if __name__ == "__main__":
    main()
