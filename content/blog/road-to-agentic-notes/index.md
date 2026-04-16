---
slug: road-to-agentic-notes
title: The Road to Agentic Notes
description: Why Karpathy's LLM-based knowledge bases are so powerful and how you can start building one.
author:
  - Jamal Hansen
lastmod: 2026-04-05
tags:
  - knowledge-management
  - llm
  - obsidian
  - foam
  - notes
  - junior-developer
categories:
  - AI Tools
  - Developer Productivity
date: 2026-04-05
cover:
  image: road-to-bright-sky.jpg
  alt: ""
  caption: ""
draft: false
---


Karpathy published his LLM-powered personal knowledge system. The post went viral, and for good reason.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">LLM Knowledge Bases<br><br>Something I&#39;m finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, and more into manipulating…</p>&mdash; Andrej Karpathy (@karpathy) <a href="https://twitter.com/karpathy/status/2039805659525644595?ref_src=twsrc%5Etfw">April 2, 2026</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

The basic idea is that an LLM builds and maintains a wiki for you. You drop in source material. The LLM reads it, extracts what matters, and integrates it into an existing network of markdown files. It updates pages when new information contradicts old claims. It cross-references concepts across everything you have ever added. 

What makes it interesting goes beyond note-taking. That network of markdown files lives on your local device. An LLM you chat with in Claude Code (or any tool with filesystem access) can use it as context.

Every source you add makes the whole thing richer. Every question compounds.

It is a lot of concepts at once, so you probably should not start here.

## Why most developer knowledge disappears

You finish a tutorial. You build the thing. Two weeks later, you are back on Stack Overflow (or in your favorite LLM), looking up the same syntax or solving the same issue.

This is not a memory problem. It is a storage problem. You understood the concept. You did not put it anywhere that survives.

Most people keep notes the way that they keep leftover Whataburger ketchup and the extra three birthday candles from the pack: dropped in a drawer, never looked at again. Quietly gone in the next laptop migration. These are not notes. They are evidence that learning happened.

The difference between that and what Karpathy built is not intelligence. It is structure. Notes that reference each other, grow over time, and feed back into your questions are a different category of thing entirely.

## What Karpathy built

Most AI tools for documents work the same way. NotebookLM, ChatGPT file uploads, most RAG systems: they retrieve from raw documents at query time. The LLM reads your files, answers your question, and forgets. Ask the same question six months later and it starts from scratch. Nothing accumulates.

Karpathy's wiki is different. The LLM does not retrieve. It compiles. When you add a source, the LLM integrates it into the existing wiki, updating entity pages, revising concept summaries, noting where new information contradicts old claims. The synthesis is already there by the time you need it. The cross-references are already made.

When you ask a question, the answer does not disappear into chat history. It gets filed back into the wiki as a new page. Your explorations compound the same way your sources do.

His description of the division of labor is worth keeping: "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."

That is the destination. The starting line is simpler than it looks.

## Where you can start

You do not start with a system. You start with a habit.

Before an LLM can maintain your wiki, you need two things: a collection of notes worth maintaining, and the practice of adding to it. Neither of those comes from installing a tool. They come from writing things down consistently until it becomes automatic.

The files in Karpathy's system are standard markdown text. The notes you create today are the same files an LLM will maintain later. When you start out writing your first note, you are building the foundation.

## Start today

### Step 1

Install [Foam](https://foambubble.github.io/foam/) in VS Code. It takes about two minutes. You probably already have VS Code open. You do not have to learn a new application or leave your editor.

That is it. You have a wiki.

_Note: if you already use Obsidian, it's a perfect alternative._

### Step 2

Make a dedicated folder for your notes. Call it `notes/` or `wiki/` or whatever you will actually use. That folder is your wiki.

### Step 3

Learn the one piece of syntax that makes this work: `[[double brackets]]`. Write `[[merge conflicts]]` in any note and Foam treats it as a link to another note. That linked note needs to live as `merge conflicts.md` in your folder. It does not have to exist yet. Write the link first. Create the file when you get there.

## What a note looks like

<!-- test:skip -->
```markdown
# git pull runs a fetch and a merge under the hood

When you run git pull, it downloads the latest changes (like [[git fetch]])
and merges them into your current branch automatically.
That is why you can still get [[merge conflicts]] from a simple pull.
```

Four rules, nothing else:

**One concept, one note.** Not one topic, not one tutorial. One thing you understood today. If you are writing about two things, you have two notes.

**Title as a claim.** "git pull runs a fetch and a merge" not "git pull." The title should be something you could agree or disagree with. A topic is not a claim. A claim is something you learned.

**Write it in your own words.** After you understand it, not while you are figuring it out. If you cannot explain it without looking at the source, you do not understand it yet. Come back when you do.

**Add a link when two things connect.** `[[merge conflicts]]` does not have to exist yet. Write it anyway. You will fill it in when you get there. The link is the thing that makes this a wiki and not a folder of text files.

That is the whole practice. One concept per note. Title as claim. Your words. One link when you see one.

Now, go write something.

## What comes next

Do this for a month. You will have somewhere between thirty and a hundred notes, depending on what you are working on.

At that point, you will hit the first real problem: you cannot find the note you know you wrote. You remember writing something about what happens when a git pull fails mid-merge, but you cannot remember what you called it.

That is the signal that your notes need to be queryable. Tags, dates, status fields, and structured metadata that let you filter and search by something other than the title. That is the next post.

After that, the notes you have been building are the raw material Karpathy's system needs. Same files. Same links. The LLM picks up maintenance from where you left off. Your month of notes becomes the foundation of the compounding system you wanted at the start.

---

**Go deeper:**

- [Karpathy's knowledge system gist](https://gist.github.com/karpathy/442a6c3be336f01adb80): the full idea, worth reading carefully
- [Foam for VS Code](https://foambubble.github.io/foam/): the starting tool
- [Markdown Syntax](https://www.markdownguide.org/basic-syntax/): markdown offers more than just wikilinks, it can format your notes too
- [Obsidian](https://obsidian.md): when you are ready to graduate from VS Code
- [Andy Matuschak's working notes](https://notes.andymatuschak.org): the philosophy behind note-as-claim, shown in practice
