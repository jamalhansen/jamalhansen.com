---
slug: why-i-run-ai-locally-and-you-might-want-to
Created: 2026-02-27
tags:
  - local-ai
  - philosophy
  - ollama
  - 
series: 
  - "I vibe coded and lived to tell"
title: Why I Run AI Locally (and You Might Want to)
description: A practical framework for when local wins. Privacy, cost, independence, and learning, grounded in real tool-building.
author:
  - Jamal Hansen
date: 2026-03-22
lastmod: 2026-03-21
draft: false
newsletter_url: ""
cover:
  image: "markus-spiske-bk11wZwb9F4-unsplash.jpg"
  alt: "A home garden growing happily"
  caption: ""
  relative: true
  credit:
    name: "Markus Spiske"
    username: "markusspiske"
    photo_id: "green-plants-on-black-metal-train-rail-during-daytime-bk11wZwb9F4"
---

As I admitted before in posts [1](https://jamalhansen.com/blog/i-vibe-coded-a-local-ai-powered-promo-generator/) and [2](https://jamalhansen.com/blog/i-trusted-three-local-ai-models) I vibe-coded and lived to tell. This post answers the question I kept avoiding. _Why run any of this locally when cloud models are flatly better at the task?_

The answer isn't that _cloud AI is bad_. It is more complicated than that. It turns out that it is the wrong question, and there is a place for both tools. 
## Frontier cloud models are impressive

Cloud models are better than anything I can run locally for complex reasoning. They handle more context, have larger parameter counts, and represent the current state of the art. For plenty of tasks, they are a frankly amazing tool.

I won't argue with you.

I also won't tell you that you must use one today.

That's not the question I'm asking.

I am interested in a different question: *when and why does running AI locally make sense?*
## The Case for Local-First AI

The answer, as far as I can tell, is in four parts: privacy, cost, control, and personal growth.
### Privacy
My blog content and whatever data that I send to the LLM stay on my machine. I'm not training someone else's model, and they aren't collecting my data for marketing. If I'm working on something family-related or personal, like my thoughts and notes, this matters. I may decide to send the data to the cloud, but I have a choice. 
### Control
I pick the model. I can test three and compare. I have more control over the process. It means the tool's behavior is fully mine to understand and change, and that may be important for some use cases.
### Cost
Zero dollars is an appealing price. I can run it a hundred times while iterating, and it's still free. When I'm testing output quality across three models and tweaking prompts, cloud costs add up fast. Cloud API costs aren't much, but they are something. 

### Personal Growth
Now you might be calling me out a bit on that last one. I feel it too. It's like growing your own vegetable garden. Sure, you can pick and eat your vegetables for free, but with all the time and supplies, it's not cheaper. That's a fair argument.

Running Ollama and testing models locally teaches you things about model behavior you'd never learn from an API. You feel the constraints in a way that's invisible behind a cloud endpoint. It's the standard transmission vs. automatic analogy from [my last post](https://jamalhansen.com/blog/i-trusted-three-local-ai-models/#lessons-learned). Getting your hands dirty is a legitimate reason on its own.

## The Philosophy

Unix has a philosophy that each tool should [do one thing well](http://www.catb.org/esr/writings/taoup/html/ch01s06.html) and compose tools together. I like this idea and would like to explore how it relates to AI tooling as well. Doing one thing well is useful, but it also keeps ideas small and shrinks context windows. Both things that are beneficial to smaller models. 

What's new here isn't the automation, it's the primitive. Local AI brings reasoning and non-determinism into otherwise deterministic code. That's not "AI" in the chatbot sense. It's a new thing you can reach for when building a tool. Something that is worth exploring because it hasn't existed before. 

Today, local-first AI tooling is rough, limited, and requires tinkering. It's a wide-open field, and that's exactly why it's interesting to be here now.
## When Local, When Cloud?

So, when should local AI be used and when should a cloud or frontier model be used? It's a good question, and one that I don't have a great answer for at this point. But I do have some basic thoughts to make a decision framework. 

| Situation | Lean local | Lean cloud |
|---|---|---|
| Data sensitivity | Private notes, personal writing | Not relevant |
| Iteration cost | Testing many variations | Production, one-shot |
| Task complexity | Focused single-step tasks | Multi-step reasoning |
| Context size | Short inputs | Large documents |
| Quality bar | Good enough, editable first draft | Best available, unedited |

That leaves a place where most people probably land; local for drafts and iteration, cloud for final polish. It is what I'm doing with the promo generator today, at least until I can get to a point where I learn enough to choose differently. 

## Closing

So far this has been the story of one tool. What I built, what surprised me, how I chose to do it this way, and why it was worth doing at all.

The promo generator is small by design. One input, one output, a model that runs on my laptop. Building it taught me something I couldn't have gotten from an API call: what it feels like when the constraints are real and the cost is zero.

Local AI right now is not polished. It's barely convenient. But the learning curve is steep in the best way, and the floor on what you can build is lower than it's ever been.

[Subscribers of my newsletter](https://jamalhansen.beehiiv.com) have watched this unfold in real time, and I appreciate that. There's more coming. The promo generator is the first tool in what's turning into a collection. And when you build enough tools, the patterns start showing up. You find yourself copy-pasting the same scaffolding, making the same tradeoffs.

This is where the next arc picks up. My next posts will explore what happens when the tools multiply and you start thinking in systems instead of scripts.
