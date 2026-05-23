---
arc: Architecture Arc
author:
- Jamal Hansen
category:
- Blog Post
date: 2026-05-26
description: After extracting a shared library, starting a new tool went from a day
  of boilerplate to two imports. The queue got longer, not shorter. Here's what's
  next.
draft: false
lastmod: 2026-03-25
post: 9
series:
- I vibe coded and lived to tell
slug: the-queue-is-full
tags:
- vibe-coding
- architecture
- python
target_date: 2026-05-14
title: 'The Queue Is Full: What I''m Building Next with Local-First AI'
cover:
  image: queue-is-full.jpg
  relative: true
---

I have a text file with 26 tool ideas on it. That number keeps growing. And for the first time, that feels like a good thing.

For most of this series, I've been writing about what happens when you vibe code a bunch of tools and let the architecture emerge. The [copy-paste period](https://jamalhansen.com/blog/copy-and-paste-long-enough-and-the-architecture-appears/). The [shared library extraction](https://jamalhansen.com/blog/how-i-extracted-a-shared-library/). The [Makefile that almost didn't survive](https://jamalhansen.com/blog/gemini-forgot-its-plan-i-kept-the-makefile/).

This post is about what comes after. The infrastructure is in place. Starting a new tool is cheap now. So the question changes from "can I build this?" to "what's worth building next?"

## What Starting a Tool Used to Cost

Before the shared library, every new tool started the same way. Copy the provider abstraction from the last project. Copy the CLI helpers. Copy the Obsidian utilities. Copy the testing module. Wire them all together. Fix the imports. Make sure the tests pass.

That was 60-70% of the work before writing a single line of actual tool logic. The interesting part of each project, the thing that made it different from the last one, was buried under a pile of boilerplate I'd already written six times.

It wasn't hard work. But it was slow work, and it created a real barrier. Every time I had an idea for a new tool, the mental cost of "copy four files, wire them up, fix the imports" made me hesitate. Some ideas never got past that hesitation.

## What It Costs Now

After extracting `local-first-common`, starting a new tool looks like this:

<!-- test:skip -->
```bash
uv init my-new-tool
uv add "local-first-common @ git+https://github.com/jamalhansen/local-first-common.git@main"
```

And then, in the code:

<!-- test:skip -->
```python
from local_first_common.providers import PROVIDERS, resolve_provider
from local_first_common.cli import add_provider_args
```

That's it. Two commands, two imports. The provider abstraction, CLI helpers, Obsidian utilities, and `MockProvider` for testing are all available. The only code left to write is the code that makes this tool different from every other tool.

The shift is significant. The cost of starting a new project dropped from "an afternoon of boilerplate" to "five minutes of setup." When the startup cost is that low, ideas that used to stall in the "maybe someday" pile actually get built.

Which brings me to the queue.

## The Read-Later Queue

My Obsidian vault has a read-later system. Articles get tagged, scored by my [content discovery tool](https://jamalhansen.com/blog/the-content-curator/), and queued for review. The problem is that "review" currently means me opening each article, reading it, deciding if it's worth keeping, and writing a note about why.

That's fine for five articles a week. It's not fine for thirty.

The tool I want to build is a genuine multi-step agent. Not a single LLM call that summarizes an article. A workflow that makes decisions:

1. Fetch the article and read it
2. Summarize the key ideas
3. Cross-reference against what's already in my vault (do I already have notes on this topic?)
4. Annotate the article with connections to existing notes
5. Decide: keep, archive, or discard, with a reason

Steps 1 and 2 are straightforward. Steps 3 through 5 are where it gets interesting, because they require the tool to know what's in the vault, make a judgment call, and explain that judgment in a way I can review.

This is different in kind from the tools I've built so far. The promo generator takes input and produces output. The transcription summarizer does the same. They're single-shot: content in, content out. The read-later agent needs to hold state, query external sources, and make decisions that depend on context it has to go find.

I don't know exactly what this looks like yet, and I'm not going to over-specify it here. The details will change when I actually build it. But the shared library means I can focus entirely on the agentic workflow without spending a day on provider abstraction and CLI setup first.

## The Weekly Digest

The other project I'm thinking about is a cross-project weekly digest. I have three tools that produce content on three different schedules:

**Voice memos** happen whenever I think of something. Could be twice a day, could be nothing for a week. The transcription summarizer cleans them up and writes them to my vault, but there's no rhythm to when they arrive.

**Daily notes** happen daily (obviously). They capture what I worked on, what I'm thinking about, and what's coming up. They're structured and predictable.

**Content scoring** happens on a schedule. The content discovery tool runs periodically, scores articles, and surfaces the ones worth reading. The cadence is regular but doesn't align with the other two.

The digest problem is: take these three streams, which don't line up in time or structure, and produce one coherent weekly narrative. What did I think about this week? What did I read that mattered? What themes keep showing up across voice memos, daily notes, and content scores?

This is a coordination problem, not just a summarization problem. A tool that concatenates three outputs and asks an LLM to summarize them would produce mush. The interesting work is in figuring out which pieces from each source actually connect, and presenting them in a way that tells me something I didn't already know.

## The Queue Is Long

I'm not going to list all 26 tool ideas. A list that long is immediately out of date, and half of them won't survive contact with reality. What matters is that the list exists and keeps growing.

Before the shared library, a long ideas list felt like debt. Every item was a project that would take a day of boilerplate before I could start on the interesting part. Now that the startup cost is five minutes, a long list feels like momentum. The infrastructure is in place. The ideas just need time.

Some of them will turn into posts in this series. Some will get built and quietly used without anyone hearing about them. Some will turn out to be bad ideas that die in the first hour. That's fine. The cost of finding out is low enough now that it's worth trying.

## What This Arc Was About

This is the last post in the Architecture Arc. Looking back, the through-line is:

1. [Copy-paste long enough and the real abstraction appears](https://jamalhansen.com/blog/copy-and-paste-long-enough-and-the-architecture-appears/)
2. [Extract the shared parts into a library](https://jamalhansen.com/blog/how-i-extracted-a-shared-library/)
3. [Even messy sessions produce useful architecture](https://jamalhansen.com/blog/gemini-forgot-its-plan-i-kept-the-makefile/)
4. The architecture pays for itself by making the next thing cheaper to build

Vibe coding didn't replace the engineering work. It accelerated the part where you figure out what engineering work is worth doing. The repetition wasn't waste. The messy sessions weren't failure. The growing queue isn't debt. They're all evidence that the system is working.