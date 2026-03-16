---
title: "(All) Databases Are Just Files. Postgres Too."
date: 2026-03-12
draft: false
description: "DuckDB's file-native design is a first-class feature, not a limitation. File-native is good design. This article makes that clearer by pulling back the curtain..."
tags:
  - duckdb
  - databases
source_url: "https://tselai.com/all-databases-are-just-files"
source_title: "(All) Databases Are Just Files. Postgres Too."
source_author: "Florents Tselai"
source_type: "blog post"
---

## Why This Caught My Eye

DuckDB's file-native design is a first-class feature, not a limitation. File-native is good design. This article makes that clearer by pulling back the curtain on Postgres -- a great database, but ultimately a complex program that stores data in a filesystem.

Note: the article contains a long quote used here for context. Trim to under 15 words before publishing.

> At its core, `postgres` is simply a program that turns SQL queries into filesystem operations. A `CREATE TABLE` becomes a mkdir. An `UPDATE` eventually becomes: open a file, write to it, close it. It’s a complex and powerful system—but fundamentally, it’s just an executable that manipulates files.
