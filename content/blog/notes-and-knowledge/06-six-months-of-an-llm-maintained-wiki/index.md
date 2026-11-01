---
title: Six Months of an LLM-Maintained Wiki
slug: six-months-of-an-llm-maintained-wiki
description: I ran a Karpathy-style LLM-maintained wiki for six months. What compounded, what didn't, and the 614 notes I archived.
author:
- Jamal Hansen
tags:
- obsidian
- ai
- learning
series:
- Notes and Knowledge
cover:
  image: cover.jpg
  alt: A green seedling growing up through dried leaves and wood mulch
  caption: ''
  relative: true
draft: false
date: 2026-11-01
---

*In April I wrote about [Karpathy's method](/blog/road-to-agentic-notes/) as a starting point. I'd been running my own version since March. Here's what six months looks like.*

## The vault

I started with the [arscontexta Claude Code plugin](https://github.com/agenticnotetaking/arscontexta) and an Obsidian vault. I added interesting articles, my thoughts, and what I've learned while building and breaking vibe-coded tooling. Claude Code reads these source files and compiles them into claim-titled notes. I was excited to try something new and recommended that was still relatively unexplored. Plus, it solves real problems, and it is at a crossroads of my interests.

So, yeah, I went in curious to see how it would turn out. My first input file was processed on 2026-03-21. This is a matter of putting the file into the inbox and running a */reduce* command to extract the information from it, format it, and archive the input.

## Rinse and Repeat

Now, with 950+ extracted live notes and nearly 340 sources processed, I have a significant vault. One that I use often to filter my work and my questions through. The vault provides both basic and specific context to Claude when responding to me. It is like the built-in memory feature, but more robust and transparent.

A simple example of this: it knows my preferences and my projects. I don't have to explain myself to it every time; it is there for it to explore. More specifically, when it starts building a script from a prompt, it will know my preference for using `uv`, and it will know that I have some basic custom libraries and harnesses for reviewing the code. This context is very helpful.

## What surprised me

I was super into my vault project, and it was helping me to explore other ideas. Each of these ideas filtered through the vault. These were both high-level concepts and learnings and details of obscure topics that I would never visit again. It didn't take too long before I started accumulating so much text; it was kinda like digital hoarding.

### I kind of always knew that would happen

I think I kind of always knew that would happen, because I was just throwing everything at it. As I've been working in knowledge management and even AI context, I find that it's better to be able to curate the data and have it focused on the things that you want. But I also was very interested in how this would work and if it would scale, and what it was that I actually wanted to store. I didn't really have answers to those questions, so I just threw everything at it.

A lot of the logic used was pre-established for me, which was great because I didn't need to understand it all initially. I was using a plugin. I didn't write those rules. Someone smarter than me did and was nice enough to share them. When you're trying something out that's new and you don't really know how it's going to turn out, which is most of AI and LLMs right now, you're experimenting. Often it's best to experiment with things that you're interested in and with live data, even though sometimes that can turn out badly.

### Time to do some spring cleaning

But text was accumulating, and a good chunk of it wasn't something I needed. It was starting to take longer and longer to add new information, just because there's more and more stuff for it to sift through and link to. And going along with that, it was using additional tokens. It was time to do some spring cleaning.

I found that there were projects that I had been looking into that ended up being dead ends and never completed, which is so easy to do when working with LLMs. There were ideas that I picked up and dropped. And a lot of the implementation details that I put in there to begin with really weren't what I was interested in pursuing. Really, it was more about the ideas, the thinking, and that side of things. That was what I trimmed back to.

By the time I was done, I had archived 614 notes, almost 40% of everything the vault had written. They're still there if I need them; they just aren't part of the live vault anymore.

It felt great. It felt like cleaning the house or washing the car, or doing something else that I'd felt needed being done for quite a while.

### I was only doing the first step

There was another issue that I ran into: I was adding content to my vault and extracting claims, but those claims weren't being woven into the existing claims or being checked for validity.

As I've said, I didn't necessarily understand exactly how it worked internally, and I just wanted to make sure I was capturing my notes. Extracting claims is only the first step. After that, the new claims are supposed to be connected to the existing notes, the older notes get updated to point back at them, and the result gets verified. A lot of the time I would capture my notes and turn them from the raw note into a claim, but then I wouldn't integrate it into the vault. I thought it was chugging along just fine, but then I did some diagnostics and found a backlog of claims that had never been linked or checked. So I ran that backlog through the rest of the steps, which added about 200 links. I had to play a little catch-up there, because I was only doing the first step.

### What actually compounded

Honestly, the notes since the fix feel about the same for the most part. I'm not going in and checking out individual notes or individual claims. I'm letting the system use them, reference them, summarize them, and use them as context. That's the part that compounded: the context I described earlier, where it knows my projects and my preferences and I don't have to explain myself every time. Looking at individual notes might be something I do from time to time, but it's not the point of the entire project.

## What I'd tell someone starting today

### Standing on the shoulders of lots of other people

I'm just standing on the shoulders of lots of other people who are interested in this space. It's nothing that I came up with. Starting with someone else's system and adding things, addressing issues as they come up, building iteratively: I think that's really what all software development is about. And I think a lot of life is forming the habits that are important, and then iterating and figuring out what you did wrong and fixing it.

### Throw a bunch of stuff out and see what sticks

I'd recommend that you do it the same way I did. Just throw a bunch of stuff out and see what sticks, and then go back and trim and clean, and get a little bit more focused once you've tried some stuff out. Chances are, if you say, I'm going to do this thing, and that's all you do, and then you realize three months in that you're really not interested in that, that's not going to work out so well.

### Give it a shot

If you are just using an LLM by itself, and you are getting tired of having it ask you the same questions and having to do the same things: I know there are features like Claude Projects and ChatGPT's memory that do something similar, but I really enjoy this method, with the vault and the LLM together. So give it a shot.

## What's next

### Is it still worth it?

If it can help me to think and come up with strategies for projects that I'm working on, and ideas, and continue to generate interesting thoughts without me having to tell it the background, the context, what I'm thinking, what I'm interested in: as long as it's continuing to do that, I think it's worthwhile.

### Contradictory, but still valid

You don't necessarily know, especially when you're learning, what's right and what's wrong. And right and wrong maybe aren't even the right words here: what's relevant and what's not relevant. You can get one opinion, two opinions, and maybe they're different. It's good to capture both, so that when you learn more later, you can look back at them, see what the tension is, see what's important. Maybe they're contradictory, but still valid.

That's what the next post is about: the part of the system that keeps both sides of an argument instead of overwriting one, and what it taught me about `temperature=0`.
<!-- TODO: link "the next post" to /blog/contradictions-are-a-feature/ once post 7 is live -->
