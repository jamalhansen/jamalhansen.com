---
title: Add External Dependencies to Python Scripts with uv
description: No virtual environment needed — declare dependencies directly in your script
date: 2025-04-19
lastmod: 2026-01-10
tags: ["python", "uv"]
categories: ["Python"]
draft: false
ShowToc: false
TocOpen: false
series:
---

Ever wanted to share a Python script that uses external packages without making the recipient set up a virtual environment? With `uv`, you can embed dependencies directly in the script.

## The Command

```bash
uv add --script example.py 'requests<3' 'rich'
```

This adds inline metadata to your script:

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
