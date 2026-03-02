---
Created: 2026-02-27
Category: "Blog Post Idea"
tags:
  - local-ai
  - vibe-coding
  - ollama
split_from: "I Vibe Coded a Promo Generator with Local AI"
part: 1 of 3
title: I Vibe Coded a Local AI-Powered Promo Generator
description: I built a local AI tool to automate my weekly promo writing. It didn't go as planned, but I learned a lot about what small models can actually do.
author:
  - Jamal Hansen
date: 2026-02-28
categories:
cover:
  image: stavan-macwan-YG8vzN9IkmA-unsplash.jpg
  alt: "A tool box with some socket wrenches in it"
  caption: ""
  relative: true
  credit:
    name: "Stavan Macwan"
    username: "stavanmacwan9815"
    photo_id: "a-red-box-with-a-couple-of-guns-in-it-YG8vzN9IkmA"
draft: false
ShowToc: false
Related:
  - "I Vibe Coded a Promo Generator with Local AI"
  - "I Vibe Coded a Promo Generator with Local AI - Part 2 Architecture and Models"
  - "I Vibe Coded a Promo Generator with Local AI - Part 3 Why Local-First AI"
  - "local-first-ai-series-index"
---
Every Monday, I publish a blog post. Then I write five slightly different versions of "hey, I wrote a thing" for LinkedIn, Twitter, Bluesky, and Mastodon. Each platform has different character limits, different audiences, and different best practices. It's tedious.

I wanted to automate it. Not with a frontier model, but with a small local one running on my laptop. Something like phi or llama, through Ollama.

I didn't need a polished production app. I needed a quick prototype to test my theory. My theory was that a small local model can handle a real, recurring task. ...and it can do it well enough to be useful.

Vibe coding felt like the right approach. You describe what you want to an AI and let it write the code, then steer with feedback instead of typing every line. Get something working fast, learn from the results, and decide what to do next.

## Vibe Coding It Into Existence

Claude is my favorite of the frontier LLMs, so I chose Claude Code to scaffold the initial codebase. I created a git repository in my projects folder, loaded it in Claude Code, and had a conversation about what I was looking to build. It generated a CLAUDE.md orientation file and had a functioning script in very little time.

The script used Ollama locally and targeted the llama3.2:3b and phi4-mini models, both about 2GB in size. It takes the text of the post I want to promote along with some guidelines for the target platform, and generates promo copy. The original design one-shot prompted each platform and wrote the results to a file.

With a couple of prompts, I asked Claude to add parameters so I could target one platform at a time and send output to stdout. Here's what running it looks like:

```bash
uv run promo.py \
  --post "path/to/blog-post.md" \
  --platform twitter \
  --stdout
```

```
Loading post: path/to/blog-post.md
Post: I Vibe Coded a Local AI-Powered Promo Generator
Model: llama3.1:8b
Platform: twitter only
Generating promotional copy...
  Note: Post content truncated from 6966 to 4000 chars for prompt.
  Extracting hook and key insight... done.
  Generating X/Twitter... done.
```

That part worked. The output, not so much.

My Twitter/X results were about 500 characters long (the limit is 280) and prefaced with a preamble the model added on its own:

```
Sure! Here is promotional text for Twitter that I generated from your blog post --
```

The model ignored the character limit, invented a clickbait tone I never asked for, and called the tool "Vibe Code" (that's not what it's called). The results were unusable.

But that's part of coding. I asked Claude to improve things. It added Python-based validation checks on the output and cleaned up the prompts. The results weren't any better.

So I gave it some direction. I suspected the context window was getting too much information at once. I asked Claude to:

1) Split the prompt into two passes: first extract the core message of the post, then use that summary (not the full post) to generate the promo
2) Use structured outputs
3) Extract the platform-specific rules from the script into YAML
4) Rewrite the rules into concise statements

This worked noticeably better. The models still weren't generating usable content, but I could see improvement. I was also starting to understand what was actually happening inside the pipeline.

It was around this point that I noticed something about the process itself. Going from "I want this" to "it runs" took minutes, not hours. 

When coding a project like this myself, I'd usually spend a few hours getting to a first working version. But even with all the coding ability these tools have, I still needed to push it in the right direction to get the significant improvements. The AI built the scaffolding fast. The judgment calls were still mine.

## Out of Tokens

Ran out of Claude tokens mid-session. I pay for the Pro plan, which is great. But it does run out.

I did what any rate-limited vibe coder would do.

I switched to Gemini CLI.

The handoff was smoother than I expected. Gemini immediately created a GEMINI.md from the CLAUDE.md and evaluated the codebase. It took a minute to figure out what was going on, but before long, it made a list of five things it wanted to try.

Interestingly, it picked up on some things Claude had ignored (and probably vice versa). Switching between AI tools mid-project was something I did out of necessity, but I'd try it again on purpose. Each tool has different strengths and blind spots.

The prototype was already functioning at this point, but Gemini put the code through its paces. It made some tweaks that improved the code, if not the results. Then it decided the local model needed an upgrade: llama3.1:8b instead of the 3B model. This model is available in Ollama, so I downloaded it.

Before long, everything locks up. Nothing is working.

I'm running this on a MacBook Air M1 with 256GB of storage. I check the storage, and I have under 1GB left. Not great when you're trying to download an 8B parameter model.

After a few deep breaths and some emergency cleanup, I got enough breathing room to continue. I closed apps, emptied the trash, and vowed to investigate the 140GB of mystery System Data eating my drive later.

The upgraded model does help the results. They are not perfect and will need additional work, but the model started observing the rules I gave it. Character limits were closer. The tone was less robotic. It was working.

## What I Ended Up With

The tool reads a blog post, generates platform-specific promo copy using a local Ollama model, and outputs it in my standard promo file format. It runs entirely on my laptop.

Here is the Twitter promotion text that it created for this post: 

```
You're about to discover how to automate social media posts with AI,
but be warned: it's not as easy as you think. Using a local LLM model
like Vibe Code, you can generate multiple versions of a...
```

The output still needs editing. Yes, it's still calling it 'Vibe Code'. It's a first draft, not a finished product. But it gives me a starting point for each platform instead of a blank page, and that saves real time on a task I do every single week.

More than the tool itself, I started thinking differently about local AI. Small models can handle real tasks if you structure the work for them. They need constraints, clear rules, and a pipeline that plays to their strengths. The two-pass architecture (extract the key insight first, then generate from that) was the biggest unlock, and it's a pattern that applies well beyond promo copy.

This prototype raised questions I'm still working through. Why did splitting the prompt into two passes make such a difference? When should you let the LLM be creative and when should Python enforce the rules? And why bother running any of this locally when cloud models are better at the task? I'm digging into those in upcoming posts.

If you've tried running Ollama models for real tasks, I'd like to hear about it. What models worked for you? What didn't? Find me on [LinkedIn](https://linkedin.com/in/jamalhansen), [X](https://x.com/jamahans), [Bluesky](https://bsky.app/profile/ham-jansen.bsky.social), or [Mastodon](https://mastodon.online/@ham_jansen) and let me know.
