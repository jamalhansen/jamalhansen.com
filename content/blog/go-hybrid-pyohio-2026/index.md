---
alt: 'Title slide reading Go Hybrid: Find the Results LIKE Can''t, PyOhio 2026, Jamal Hansen.'
author:
- Jamal Hansen
categories:
- Python
- SQL
- AI
category:
- Blog Post
cover:
  alt: 'Title slide: Go Hybrid, Find the Results LIKE Can''t'
  caption: ''
  image: go-hybrid-cover.png
  relative: true
date: 2026-07-24
description: Companion page for my PyOhio 2026 talk. Slides, code, and the dog-spa
  dataset for searching free text beyond LIKE with BM25, vectors, and hybrid.
draft: false
lastmod: 2026-07-24
slug: go-hybrid-pyohio-2026
tags:
- python
- sql
- duckdb
- search
- bm25
- vector-search
- pyohio
- conferences
target_date: 2026-07-24
title: 'Go Hybrid: Find the Results LIKE Can''t'
---

This is the companion page for my [PyOhio 2026](https://www.pyohio.org/) talk. Everything I demoed is here to take home: the slides, the notebooks, and the dataset.

`LIKE` is the tool most of us reach for first when we search free text. You end up chaining `OR` and `NOT LIKE` clauses to patch each miss, and you are still reading every record by hand.

The talk works through what to reach for instead, using 448 free-text notes from a fictional dog spa.

## Take it home

- **[Code and notebooks on GitHub](https://github.com/jamalhansen/go-hybrid)** -- start with `search_toolkit.ipynb`. Each method is a few lines you can lift straight into your own DuckDB project. `go_hybrid.ipynb` is the full walkthrough that follows the talk.
- **[Download the slides (PDF)](go-hybrid-slides.pdf)**

## Run the code

```bash
git clone https://github.com/jamalhansen/go-hybrid
cd go-hybrid
uv sync
uv run jupyter lab search_toolkit.ipynb
```

The first run downloads the embedding model (`all-MiniLM-L6-v2`, about 90 MB). After that it is fully offline.

The dataset is synthetic and curated so each method fails visibly. Bring a note of your own, drop it in, and see which tools find it.

If you saw the talk, thank you for coming. If you have questions, [reach out](/about/).
