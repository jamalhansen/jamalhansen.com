---
title: Add External Dependencies to Python Scripts with uv
slug: add-dependencies-to-python-scripts-with-uv
date: 2025-04-19
lastmod: 2026-01-10
description: No virtual environment needed. Declare dependencies directly in your script.
author:
- Jamal Hansen
tags:
- python
- tools
categories:
- Python
draft: false
ShowToc: false
TocOpen: false
cover:
  image: cover.jpg
  alt: "A single sheet of paper on a clipboard beside a small potted fern"
  relative: true
---

Ever wanted to share a Python script that uses external packages without making the recipient set up a virtual environment? With `uv`, you can embed dependencies directly in the script.

## The Command

<!-- test:skip -->
```bash
uv add --script example.py 'requests<3' 'rich'
```

This adds inline metadata to your script:

<!-- test:skip -->
```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
```

## Running It

Anyone with `uv` installed can now run the script directly:

<!-- test:skip -->
```bash
uv run example.py
```

`uv` reads the embedded metadata, installs dependencies in an isolated environment, and executes the script. No `requirements.txt`, no `venv`, no friction.

## Why This Matters

This is perfect for:
- Sharing utility scripts with teammates
- Quick prototypes that need packages
- Scripts you want to version-control as single files

## Reference
- [uv: Running scripts with dependencies](https://docs.astral.sh/uv/guides/scripts/#running-a-script-with-dependencies)
