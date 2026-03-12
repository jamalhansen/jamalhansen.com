#!/usr/bin/env python3
"""
Convert Obsidian finds to Hugo-compatible markdown page bundles.
Usage: python finds-to-hugo.py input.md
"""
import sys
import re
import json
import unicodedata
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime


def slugify(text):
    text = str(text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


def detect_existing_frontmatter(content):
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', content, flags=re.DOTALL)
    if m:
        return True, m.group(1), m.group(2)
    return False, "", content


def extract_scalar(frontmatter, field):
    """Extract a single-line scalar value from YAML frontmatter."""
    m = re.search(rf'^{field}:\s*["\']?([^"\'\n]*?)["\']?\s*$', frontmatter, re.MULTILINE)
    return m.group(1).strip() if m else ""


def extract_list(frontmatter, field):
    """Extract a YAML list field. Returns a list of strings."""
    # Block style: field:\n  - item
    m = re.search(rf'^{field}:\s*\n((?:[ \t]+-[ \t]+[^\n]+\n?)*)', frontmatter, re.MULTILINE)
    if m:
        items = re.findall(r'[ \t]+-[ \t]+(.+)', m.group(1))
        return [i.strip().strip('"\'').lstrip('#').strip() for i in items if i.strip()]
    # Flow style: field: [a, b]
    m2 = re.search(rf'^{field}:\s*\[([^\]]*)\]', frontmatter, re.MULTILINE)
    if m2 and m2.group(1).strip():
        return [i.strip().strip('"\'') for i in m2.group(1).split(',') if i.strip()]
    return []


def fetch_oembed_html(platform, url):
    """Fetch pre-rendered embed HTML from the platform's oEmbed API.
    Returns the HTML string, or None on failure."""
    clean_url = re.sub(r'\?.*$', '', url)
    try:
        if platform == 'x':
            api = f"https://publish.twitter.com/oembed?url={urllib.parse.quote(clean_url)}&theme=dark&dnt=true&omit_script=false"
        elif platform == 'bluesky':
            api = f"https://embed.bsky.app/oembed?url={urllib.parse.quote(url)}"
        else:
            return None
        req = urllib.request.Request(api, headers={'User-Agent': 'finds-to-hugo/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get('html', '').strip()
    except Exception as e:
        print(f"⚠️  oEmbed fetch failed for {platform}: {e}")
        return None


def detect_social_platform(url):
    """Return 'x', 'bluesky', 'mastodon', or None based on URL pattern."""
    if not url:
        return None
    if re.search(r'(twitter\.com|x\.com)/\w+/status/\d+', url):
        return 'x'
    if re.search(r'bsky\.app/profile/.+/post/', url):
        return 'bluesky'
    if re.search(r'/@[\w]+/\d+$', url):
        return 'mastodon'
    return None


def yaml_str(value):
    """Escape a value for embedding in a YAML double-quoted string."""
    return value.replace('\\', '\\\\').replace('"', '\\"')


def extract_description_from_body(body, max_len=160):
    """Pull the first meaningful paragraph from commentary for meta description."""
    # Strip headings
    text = re.sub(r'^#+\s+.*$', '', body, flags=re.MULTILINE).strip()
    if not text:
        return ""
    first_para = re.split(r'\n\n', text)[0].strip()
    if len(first_para) <= max_len:
        return first_para
    return first_para[:max_len].rsplit(' ', 1)[0] + "..."


def main():
    if len(sys.argv) < 2:
        print("Usage: python finds-to-hugo.py input.md")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found")
        sys.exit(1)

    content = input_path.read_text(encoding='utf-8')
    has_fm, fm, body = detect_existing_frontmatter(content)

    if not has_fm:
        print("Error: No frontmatter found. Finds must have frontmatter.")
        sys.exit(1)

    # Extract Obsidian fields
    source_title  = extract_scalar(fm, 'source_title')
    source_url    = extract_scalar(fm, 'source_url')
    source_author = extract_scalar(fm, 'source_author')
    source_type   = extract_scalar(fm, 'source_type')
    captured      = extract_scalar(fm, 'captured')
    tags          = extract_list(fm, 'tags')

    if not source_title:
        # Derive from filename: strip leading "0001-" style prefix
        stem = re.sub(r'^\d+-', '', input_path.stem)
        source_title = stem.replace('-', ' ').title()
        print(f"⚠️  No source_title found, derived from filename: {source_title}")

    slug = slugify(source_title)
    if captured and re.match(r'^\d{4}-\d{2}-\d{2}$', captured):
        date = captured
    else:
        if captured:
            print(f"⚠️  Invalid captured date '{captured}', defaulting to today")
        date = datetime.now().strftime('%Y-%m-%d')
    description = extract_description_from_body(body)

    # Build Hugo frontmatter
    fm_lines = [
        f'title: "{yaml_str(source_title)}"',
        f'date: {date}',
        'draft: false',
    ]
    if description:
        fm_lines.append(f'description: "{yaml_str(description)}"')
    if tags:
        fm_lines.append('tags:')
        for tag in tags:
            fm_lines.append(f'  - {tag}')
    embed_type = detect_social_platform(source_url)
    if embed_type and not source_type:
        source_type = {'x': 'X Post', 'bluesky': 'Bluesky Post', 'mastodon': 'Mastodon Post'}[embed_type]

    embed_html = None
    if embed_type in ('x', 'bluesky'):
        print(f"🔗 Fetching {embed_type} oEmbed...")
        embed_html = fetch_oembed_html(embed_type, source_url)
        if embed_html:
            print(f"   ✓ Got embed HTML ({len(embed_html)} chars)")
        else:
            print(f"   ⚠️  Falling back to client-side embed")

    if source_url:
        fm_lines.append(f'source_url: "{yaml_str(source_url)}"')
    if source_title:
        fm_lines.append(f'source_title: "{yaml_str(source_title)}"')
    if source_author:
        fm_lines.append(f'source_author: "{yaml_str(source_author)}"')
    if source_type:
        fm_lines.append(f'source_type: "{yaml_str(source_type)}"')
    if embed_type:
        fm_lines.append(f'embed_type: "{embed_type}"')
    if embed_html:
        # Store as YAML literal block scalar so indentation is preserved
        fm_lines.append('embed_html: |')
        for line in embed_html.splitlines():
            fm_lines.append(f'  {line}')

    fm_out = '\n'.join(fm_lines)
    final_content = f"---\n{fm_out}\n---\n\n{body.lstrip()}"

    # Write output as a Hugo page bundle
    base_dir = Path(__file__).parent.parent
    find_dir = base_dir / "content" / "finds" / slug
    find_dir.mkdir(parents=True, exist_ok=True)
    (find_dir / "index.md").write_text(final_content, encoding='utf-8')

    print(f"✅  Written: content/finds/{slug}/index.md")
    print(f"    Title:  {source_title}")
    print(f"    Date:   {date}")
    print(f"    Tags:   {', '.join(tags) if tags else '(none)'}")
    print(f"\n🎉 Done!")


if __name__ == "__main__":
    main()
