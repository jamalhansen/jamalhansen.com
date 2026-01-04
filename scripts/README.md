# Obsidian to Hugo Conversion Scripts

Automated tools for converting Obsidian markdown posts to Hugo blog posts with smart image handling and environment variable integration.

## 🚀 Quick Start

### Step 1: One-time Setup
```bash
# Add to your shell profile (~/.zshrc, ~/.bashrc, etc.)
export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"

# Reload your shell
source ~/.zshrc  # or ~/.bashrc
```

### Step 2: Use Simple Commands
```bash
# From your vault's jamalhansen.com/_drafts/ folder
./scripts/new-post jamalhansen.com/_drafts/my-post.md awesome-post-slug

# From anywhere in your vault
./scripts/new-post my-note.md post-slug
```

### Step 3: Verify Setup
```bash
./scripts/check-setup
```

## What It Does

1. **Converts Obsidian syntax** to Hugo-compatible markdown:
   - `![[image.jpg]]` → `![Image](image.jpg)`
   - `![[image.jpg|alt text]]` → `![alt text](image.jpg)`

2. **Smart Image Organization**:
   - **Feature/Card Images** → `/assets/post-slug/` (for homepage cards, social sharing)
   - **Content Images** → `/content/blog/post-slug/` (for inline post content)
   - **Interactive categorization** during conversion process

3. **Creates complete Hugo post structure**:
   ```
   assets/my-post/
   ├── hero-image.jpg        # Feature/card images
   └── social-card.png
   
   content/blog/my-post/
   ├── index.md              # Converted markdown with frontmatter
   ├── screenshot1.jpg       # Content images
   └── diagram.png
   ```

4. **Generates Hugo frontmatter** with:
   - Title (extracted from first `#` heading)
   - Current date
   - Author info
   - Proper URL slug
   - Draft status (set to `true` initially)

5. **Interactive image categorization** prompts you to specify which images are for features/cards vs content

## 🛠️ Setup & Configuration

### Environment Variable Approach (Recommended)

1. **Set your Obsidian vault path**:
   ```bash
   # Add this line to your shell profile:
   # ~/.zshrc (for Zsh) or ~/.bashrc (for Bash)
   export OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"
   ```

2. **Reload your shell**:
   ```bash
   source ~/.zshrc  # or ~/.bashrc
   ```

3. **Verify setup**:
   ```bash
   ./scripts/check-setup
   ```

### Your Obsidian Vault Structure
```
YourObsidianVault/
├── jamalhansen.com/
│   └── _drafts/              # Your blog drafts folder
│       ├── aws-tutorial.md   # Post with content
│       ├── screenshot.png    # Images
│       └── diagram.jpg
├── other-notes.md            # Other vault content
└── projects/
    └── side-project.md
```

### Alternative Setup
If you don't set `OBSIDIAN_VAULT_PATH`, the script falls back to `~/Documents/ObsidianVault`

## Usage Examples

With `OBSIDIAN_VAULT_PATH` set, you can use simple relative paths:

```bash
# From your vault's jamalhansen.com/_drafts/ folder
./scripts/new-post jamalhansen.com/_drafts/my-aws-post.md aws-data-pipeline-tutorial

# Any note in your vault
./scripts/new-post my-ai-experiments.md agentic-ai-exploration

# Still works with absolute paths
./scripts/new-post ~/full/path/to/note.md awesome-tutorial

# Override vault path if needed
./scripts/new-post my-note.md post-slug /different/vault/path
```

### 📝 Your Complete Workflow

```bash
# 1. Write post in Obsidian with ![[image.jpg]] syntax
#    Location: YourVault/jamalhansen.com/_drafts/cool-post.md

# 2. Convert to Hugo with one command:
./scripts/new-post jamalhansen.com/_drafts/cool-post.md cool-post-slug

# 3. Script will:
#    - Show found images for categorization
#    - Copy feature/card images → /assets/cool-post-slug/
#    - Copy content images → /content/blog/cool-post-slug/
#    - Create Hugo post with proper frontmatter

# 4. Edit frontmatter, set draft: false, publish!
```

### 🔧 Available Scripts

1. **`./scripts/new-post`** - Main conversion script (use this one!)
2. **`./scripts/check-setup`** - Verify environment and settings
3. **`./scripts/obsidian-to-hugo.py`** - Direct Python script (advanced usage)

## The Conversion Process

When you run the script, you'll see:

```bash
📸 Found 3 images. Let's categorize them:
  1. hero-screenshot.png
  2. step-by-step.jpg  
  3. final-result.png

💡 Image types:
   Feature/Card: Used for homepage cards, social sharing, post headers
   Content: Inline images within the post content

🎯 Enter numbers of FEATURE/CARD images (comma-separated, or 'none'): 1,3

📁 Categorization result:
   Feature/Card (2): hero-screenshot.png, final-result.png
   Content (1): step-by-step.jpg

📸 Copying feature/card images to /assets/my-post/:
   ✓ hero-screenshot.png
   ✓ final-result.png

📝 Copying content images to post directory:
   ✓ step-by-step.jpg
```

## After Running the Script

1. ✅ Your post is created in `content/blog/your-slug/`
2. ✅ Images are automatically copied to appropriate locations
3. ✅ Markdown is converted to Hugo format
4. ✅ Image categorization optimizes for Hugo's resource system

**Next steps:**
1. Edit the frontmatter in `index.md`
2. Set `featureimage` and/or `cardimage` to your feature/card images
3. Add tags, categories, and summary
4. Set `draft: false` when ready to publish
5. Commit and deploy!

## Supported Obsidian Features

- ✅ `![[image.jpg]]` - Basic image embedding
- ✅ `![[image.jpg|alt text]]` - Image with alt text
- ✅ Automatic image file copying from vault
- ✅ Title extraction from first heading
- ❌ `[[Wiki Links]]` - Commented out (enable in script if needed)
- ❌ Obsidian callouts - Not converted (yet)

## 🔧 Setup Validation

### Check Your Configuration
```bash
# Run this to verify everything is working
./scripts/check-setup
```

**This will check:**
- ✅ `OBSIDIAN_VAULT_PATH` environment variable
- ✅ Vault directory exists
- ✅ `jamalhansen.com/_drafts/` folder (if present)
- ✅ Script permissions
- ✅ Python availability
- 📝 Sample posts in your _drafts folder

### Sample Output
```bash
🔍 Checking Obsidian-to-Hugo setup...

✅ OBSIDIAN_VAULT_PATH: /Users/you/Documents/MyVault
✅ Vault directory exists
✅ _drafts folder found: /Users/you/Documents/MyVault/jamalhansen.com/_drafts
📝 Sample posts found:
  - /Users/you/Documents/MyVault/jamalhansen.com/_drafts/aws-post.md
✅ Python 3 available: Python 3.11.5
✅ new-post script is executable
✅ obsidian-to-hugo.py is executable

🎯 Ready to use! Try:
   ./scripts/new-post jamalhansen.com/_drafts/my-post.md my-post-slug
```

## 🚨 Troubleshooting

### Environment Issues
**`OBSIDIAN_VAULT_PATH not set`**
```bash
# Add to your shell profile and reload
echo 'export OBSIDIAN_VAULT_PATH="/path/to/vault"' >> ~/.zshrc
source ~/.zshrc
```

**`File not found` errors**
- Use relative paths from vault root: `jamalhansen.com/_drafts/post.md`
- Or use absolute paths: `~/full/path/to/post.md`
- Run `./scripts/check-setup` to verify paths

### Image Issues
**Images not copying?**
- Verify images exist in your Obsidian vault
- Check that `OBSIDIAN_VAULT_PATH` is correct
- Ensure images are referenced with `![[image.jpg]]` syntax

### Script Issues  
**Permission denied**
```bash
# Make scripts executable
chmod +x scripts/new-post scripts/check-setup scripts/obsidian-to-hugo.py
```

**Python errors**
- Ensure Python 3.6+ is installed: `python3 --version`
- All required modules are built-in (no pip install needed)

### Path Issues
**Script not found**
- Always run from Hugo project root: `./scripts/new-post`
- Or use full path: `/path/to/project/scripts/new-post`