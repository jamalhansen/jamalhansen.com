# Obsidian to Hugo Conversion Scripts

Tools for converting Obsidian notes to Hugo page bundles.

## Scripts

| Script | Purpose |
|---|---|
| `./scripts/new-post` | Shell wrapper — converts a blog draft to `content/blog/` |
| `./scripts/new-find` | Shell wrapper — converts a find to `content/finds/` |
| `./scripts/obsidian-to-hugo.py` | Blog post converter (called by `new-post`) |
| `./scripts/finds-to-hugo.py` | Finds converter (called by `new-find`) |
| `./scripts/check-setup` | Verify environment and script permissions |

---

## Blog Posts

### One-time setup

```bash
# Add to ~/.zshrc or ~/.bashrc
export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"
source ~/.zshrc
```

### Converting a post

```bash
./scripts/new-post path/to/obsidian-note.md [slug] [vault-path]
```

The slug is derived from the filename if not provided. Examples:

```bash
# With explicit slug
./scripts/new-post jamalhansen.com/_drafts/my-post.md my-post-slug

# Slug derived from filename
./scripts/new-post jamalhansen.com/_drafts/my-post.md

# Relative path resolved against $OBSIDIAN_VAULT_PATH
./scripts/new-post my-note.md my-post-slug
```

### What `obsidian-to-hugo.py` does

**Syntax conversion (body):**
- `![[image.jpg]]` → `![Image](image.jpg)`
- `![[image.jpg|alt text]]` → `![alt text](image.jpg)`
- `> [!info] Title` → `> **info**: Title` (Obsidian callouts → blockquotes)

**Frontmatter normalization:**
- `summary:` → `description:`
- `toc: true` → `ShowToc: true` + `TocOpen: false`
- `image: file.jpg` → full PaperMod `cover:` block
- `unsplash_name/user/id` → `cover.credit` block
- `series: "slug"` → `series:\n  - slug` (scalar to array)
- Strips Obsidian-only fields: `status`, `created`, `published_date`, `Category`, `promo_file`, `series_position`, `slug`, `canonical_url`, `layout`
- Strips `weight:` if empty; keeps it if set
- Keeps `lastmod` for Hugo SEO

**Image handling:**
1. Copies images from the source note's directory into the Hugo page bundle
2. If a vault path is provided, searches the vault for any referenced images not found locally

**Output:** `content/blog/{slug}/index.md`

### Obsidian frontmatter → Hugo frontmatter

| Obsidian field | Hugo output | Notes |
|---|---|---|
| `title` | `title` | Pass-through |
| `description` | `description` | Pass-through |
| `date` | `date` | Pass-through |
| `lastmod` | `lastmod` | Pass-through (kept for SEO) |
| `tags` | `tags` | Hash prefixes and empty entries stripped |
| `draft` | `draft` | Pass-through |
| `author` | `author` | Pass-through |
| `image` | `cover:` block | Expanded to PaperMod cover format |
| `unsplash_*` | `cover.credit` | Merged into cover block |
| `series` (string) | `series` (array) | Converted to list format |
| `newsletter_url` | `newsletter_url` | Pass-through |
| `summary` | `description` | Renamed |
| `toc` | `ShowToc`/`TocOpen` | Renamed to PaperMod fields |
| `status`, `created`, `published_date`, `Category`, `promo_file`, `series_position`, `slug`, `canonical_url`, `layout`, `weight` (empty) | *(stripped)* | Obsidian-only or redundant fields |

---

## Finds

Finds are short posts linking to something worth reading, with your commentary. They live in `content/finds/` and have a separate RSS feed at `/finds/index.xml` (excluded from the main blog feed).

### Converting a find

```bash
python3 scripts/finds-to-hugo.py path/to/_finds/note.md
```

Example:

```bash
python3 scripts/finds-to-hugo.py "_finds/0001-Use any Python AI agent framework.md"
```

The slug is derived from `source_title` in the frontmatter.

### What `finds-to-hugo.py` does

- Extracts `source_title`, `source_url`, `source_author`, `source_type`, `captured`, `tags`
- Uses `captured` as the Hugo `date` (validated as `YYYY-MM-DD`; falls back to today)
- Auto-generates a `description` from the first paragraph of your commentary
- Strips all Obsidian-only fields: `status`, `created`, `published_date`, `canonical_url`, `category`, `related`
- Writes to `content/finds/{slug}/index.md`

### Obsidian finds frontmatter

```yaml
status: idea
created: "2026-03-05"
published_date: ""
canonical_url: ""
tags:
  - python
source_url: "https://example.com/article"
source_title: "The Article Title"
source_author: "Author Name"
source_type: "blog post"
captured: "2026-03-05"
category: "[[Find]]"
related:
  - "[[0000-finds-inbox]]"
```

### Hugo output fields

| Obsidian field | Hugo output |
|---|---|
| `source_title` | `title` + `source_title` |
| `captured` | `date` |
| `tags` | `tags` |
| `source_url` | `source_url` |
| `source_author` | `source_author` |
| `source_type` | `source_type` |
| Commentary body | `description` (auto-extracted) |

---

## Verify setup

```bash
./scripts/check-setup
```

Checks `OBSIDIAN_VAULT_PATH`, vault directory, Python availability, and script permissions.

## Troubleshooting

**File not found**
- Use absolute paths or paths relative to `$OBSIDIAN_VAULT_PATH`
- Run `./scripts/check-setup` to confirm paths

**Permission denied**
```bash
chmod +x scripts/new-post scripts/check-setup
```

**Frontmatter field not stripped/converted**
- Fields are matched at line start — ensure no leading whitespace on the field name
- `weight:` is only stripped if the value is empty; `weight: 5` is kept
