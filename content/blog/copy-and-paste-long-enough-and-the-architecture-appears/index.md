---
Created: 2026-03-10
series:
  - "I vibe coded and lived to tell"
published:
target_date: 2026-03-27
title: Copy and Paste Long Enough and the Architecture Appears
description: You can't design your way to a good abstraction. You have to earn it through repetition. Vibe coding made that repetition happen faster, not slower.
author:
  - Jamal Hansen
date: 2026-03-27
lastmod: 2026-03-26
tags:
  - vibe-coding
  - architecture
  - python
newsletter_url: ""
cover:
  image: "bernard-hermant-ItAyhwNUCHY-unsplash.jpg"
  alt: "A geometric black and white pattern"
  caption: ""
  relative: true
  credit:
    name: "Bernard Hermant"
    username: "bernardhermant"
    photo_id: "a-black-and-white-photo-of-a-pattern-ItAyhwNUCHY"
---

Ever find yourself writing the same code in a different repo? I have. What did you do about it?

Maybe your first reaction is to reach for an existing library to do the work for you? Or perhaps you start thinking about the DRY principle and how you need to start optimizing and combining your code.

I'm up to 16 different repositories, each containing a tool that I've vibe-coded with some help from Claude Code and/or Gemini. Things like:
- A 100% local baby journal with auto-tagging
- An opinionated voice transcription summarizer
- A [content discovery agent](https://jamalhansen.com/blog/the-content-curator/)
- A blog post draft feedback tool

These tools are built so that they can use a local LLM from Ollama, and easily switch it out for another one, or a frontier cloud model for comparison and experimentation. As I've mentioned, [I'm looking for that sweet spot where local models are a better choice](https://jamalhansen.com/blog/why-i-run-ai-locally-and-you-might-want-to/) than a cloud model.

As you can imagine, each tool rewrites a lot of the same code. Just like human developers, when AI reimplements the same requirement, it comes out a little different each time. Maybe the needs of the tool are a bit different. It could just be that it decided to take a slightly different approach.

By the time I reached three repositories, the Don't Repeat Yourself (DRY) alarm was already ringing in my head, and I was considering consolidating code bases. But I didn't.

I waited until I got to about six repositories. That's lots of repetition. Each time it was slightly (or occasionally wildly) different. You might call it reckless or a waste of tokens.

That patience paid off. It took time and repetition before the real abstraction emerged. If you'd asked me after the first project to design the shared version, I would have gotten it wrong. I know this because I would have designed for the shape of that one project, not the shape of the actual problem.

## The Conventional Wisdom Is Backwards

Everyone assumes that vibe coding with AI makes premature abstraction more tempting. And on paper, that makes sense. It's trivially easy to ask an LLM to scaffold a shared library on day one. You could have your abstract base class, your plugin registry, your configuration schema. All before writing a single line of real business logic.

But that's not what happened. The actual experience was the opposite.

AI made the copy-paste period faster. I could spin up a new tool in an afternoon instead of a week. That meant I hit "enough repetition to see the real pattern" sooner, not later. Vibe coding didn't eliminate the need to earn the abstraction. It compressed the timeline for earning it.

## DRY Is Discovery, Not Discipline

The conventional framing of DRY is moral. Don't Repeat Yourself. It sounds like a rule you follow out of professionalism, like washing your hands or writing unit tests.

The real value of DRY is epistemic. Repetition teaches you what's actually repeated. You can't skip the repetition and still get the learning.

Think of it this way. If you write a function once, you know what that function does. If you write a similar function three times across three projects, you start to see which parts are truly shared and which parts only looked shared because the first project was the only context you had.

The repetition is the research. Skipping it means guessing.

## Build Three Things, Then Extract

If you design a shared library before building the tools that use it, you're guessing at the interface. You might get close. You might even get lucky. But you're still working from theory.

If you build three tools and then extract the shared parts, the interface is revealed by use. The real API is the one that three different callers independently needed. Not the one you imagined on a whiteboard.

This is what happened with my projects. I built a promo generator, a blog reviewer, a content discovery tool, a transcription summarizer, a daily note summarizer, and a baby journal app. Each one talked to LLMs. Each one had some kind of provider abstraction. Each one handled CLI arguments.

The overlaps were real, but they weren't where I expected them to be.

## What Moved and What Didn't

Here's the part that surprised me. When I finally sat down to extract a shared library, some things moved cleanly and some didn't move at all.

The `BaseProvider` pattern (an abstract class for talking to LLMs) appeared in six projects with many slightly different shapes.

blog-reviewer and content-discovery were nearly identical. daily-note-summarizer added Pydantic schema support for structured responses. transcription-summarizer was simpler. The drift between them told me exactly where the boundaries were.

The CLI frameworks told their own story. Typer, argparse, and Click were all used. In some cases, you can see why a particular library was chosen based on what the tool needed when it was built. That inconsistency isn't a mistake. It's evidence of real decisions made in real contexts.

One tool, the baby journal, was a bit different from the others. It valued privacy above all. It read and wrote markdown like other tools, but the markdown it produced *was* the journal itself, not notes about something stored elsewhere. Because of this, the utilities in the codebase looked like overlap with the other tools at first glance. Markdown discovery, note serialization, file handling. But when I tried to extract them, they didn't move. The vault discovery used TOML config. The note serialization was tied to a typed `JournalEntry` model. The LLM-based tagging and photo handling were completely unique.

That's not a failure. That's the abstraction having a real boundary. If everything had moved, I would have been extracting noise. The things that didn't move prove the things that did were signal.

## The 26-Tool Constraint

The same thing happened at the project level.

At some point I had to decide: monorepo or separate repos? I had 26 tool ideas on a list. Too many to consolidate into one repository. That constraint forced each tool into its own repo, with shared code installed as a dependency.

Turns out that's a better architecture for this use case than a monorepo would have been. Each tool stays independent. Shared code evolves through explicit versioning. Nothing is coupled that doesn't need to be.

I never would have made that call on project one. It took building enough tools to have 26 ideas before the right structure became obvious.

## Earning It

The lesson is simple, even if it feels counterintuitive. You can't design your way to a good abstraction. You have to build enough things that the abstraction reveals itself.

AI didn't change that. It just made the building faster. Sixteen tools in a few months instead of sixteen tools in a few years. The copy-paste happened at higher speed, and the architecture appeared on a shorter timeline.

If you're vibe coding and your projects feel repetitive, that's not a problem to solve. That's the process working. Keep building. The patterns will show up when they're ready.

Next time, I'll show you the technical details of what the shared library actually looks like and how I extracted it. The code behind the argument.

Have you ever built the same thing three times before you understood what it really was? I'd love to hear about it.
