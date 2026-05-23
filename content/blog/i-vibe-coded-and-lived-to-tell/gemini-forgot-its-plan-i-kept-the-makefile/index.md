---
arc: Architecture Arc
author:
- Jamal Hansen
category:
- Blog Post
date: 2026-05-23
description: I ran out of Claude tokens and handed my six-repo codebase to Gemini
  CLI. It made some mistakes and had one genuinely good idea.
draft: false
lastmod: 2026-04-13
series:
- I vibe coded and lived to tell
slug: gemini-forgot-its-plan-i-kept-the-makefile
tags:
- vibe-coding
- architecture
- python
- gemini
target_date: 2026-04-23
title: Gemini Forgot Its Plan. I Kept the Makefile.
cover:
  image: gemini-forgot-plan.jpg
  relative: true
---

I was in the middle of the [shared library extraction](https://jamalhansen.com/blog/how-i-extracted-a-shared-library/) when I ran out of Claude tokens. Six repos deep, changes half-committed, migration plan half-finished. This was not ideal timing.

So I opened Gemini CLI and handed it the plan.

What followed was messy, instructive, and produced one idea that was better than anything I'd come up with on my own.

## Running Out of Tokens at the Worst Possible Moment

Context windows and token budgets are real constraints when you're vibe-coding, especially across multiple repositories. A six-repo migration with shared dependencies, coordinated test suites, and a consolidation plan burns through tokens quickly. This was also before I slimmed down the context I sent with every prompt.

Switching models mid-project felt like a reasonable experiment. Gemini has a massive context window, and I've seen it do some impressive work in the past, so I handed the project over to it.

## What Gemini Did (and What It Forgot)

I gave Gemini the consolidation plan. Thankfully, I instructed Claude to write it to a file before I ran out of tokens. I find that it helps to have the plan documented because sometimes the thread gets lost during implementation. The plan was specific: here are the six repos, here are the four modules being extracted into `local-first-common`, here are the repos that still need migration, here's the order.

Gemini started strong. It understood the structure, identified the right files, the current status, and began making changes.

Then it lost the thread.

About a third of the way through, I noticed it was working on a repo that was already migrated. I reminded it where we were in the plan. It recovered, kept going, and made progress on the next repo.

Then it lost the thread again.

This time it wasn't just confused about which repo was next. It had forgotten the plan entirely. When I asked "what are we working on?", it gave me a plausible-sounding summary that didn't match the actual consolidation plan at all. It had constructed a new plan from context clues, and the new plan was wrong.

This is a specific failure mode worth naming: a model with a long context window doesn't automatically track its own multi-step plan. Having the tokens available to hold the plan and having the ability to follow it are two different things. A big context window is storage, not project management. I found myself repeatedly pointing back to that plan. 

## The Broken Tests and the Declaration of Victory

After some gentle reminding, Gemini got back on track and pushed through the remaining repos. At the end, it gave me a summary: all repos migrated, tests passing, consolidation complete.

Except the tests weren't passing.

I ran the test suites myself. Two repos had broken tests. Not complicated failures. The imports pointed to the old local module paths instead of `local_first_common`. The kind of thing you catch if you run tests after making changes.

Gemini had committed the code and marked the task done without verifying. It declared victory based on what it held onto of the plan, not on whether the results worked or they matched the acceptance criteria.

Fixing the imports and validating the tests isn't a huge deal. The damage was small in this case. But the pattern matters: "AI said it's done" and "the work is done" are not the same thing. The lesson was becoming clear. If you're vibe coding and the model tells you everything is green, run the tests yourself.

## One Really Good Idea

The session was messier than a Claude session would have been. The context loss was frustrating. The broken tests were sloppy. But buried in the middle of the work, Gemini produced something I hadn't asked for and wouldn't have thought to build: a Makefile.

The Makefile wasn't configured to build code like its original intention. This Makefile existed to run repeated tasks across each of the multiple repositories. 

The idea was simple. Each repo lives in a sub-directory. A Makefile with the right targets can check the status of every repo, run every test suite, and flag anything that needs attention. All from one command. It was a genuinely smart use of the tool.

Here's roughly what it looked like:

```makefile
REPOS = promo-generator blog-reviewer content-discovery \
        transcription-summarizer daily-note-summarizer baby-journal

.PHONY: status test-all check-dirty

status:
	@for repo in $(REPOS); do \
		echo "=== $$repo ==="; \
		git -C $$repo status --short; \
	done

test-all:
	@for repo in $(REPOS); do \
		echo "=== $$repo ==="; \
		(cd $$repo && uv run pytest -q 2>&1 | tail -1); \
	done

check-dirty:
	@for repo in $(REPOS); do \
		if [ -n "$$(git -C $$repo status --porcelain)" ]; then \
			echo "DIRTY: $$repo"; \
		fi; \
	done
```

`make status` shows you every repo's git status. `make test-all` runs every test suite and shows the summary line. `make check-dirty` tells you which repos have uncommitted changes.

Three targets. Each one does one thing. Together they give you a dashboard for a multi-repo project.

## Atoms, Molecules, Organisms

This is where the idea gets interesting. If you've worked in front-end development, you might recognize the term atomic design pattern. This pattern promotes the use of small, self-contained pieces (atoms) that compose into larger groups (molecules), which compose into full interfaces (organisms).

The Makefile does the same thing for a multi-repo codebase.

**Atoms** are the individual operations. Check one repo's git status. Run one repo's test suite. See if one repo has uncommitted changes. Each one is a single shell command.

**Molecules** are the targets. `make status` loops an atom across all six repos. `make test-all` does the same for tests. Each target composes atoms into a useful answer to a single question.

**Organisms** are the workflows that chain targets together. "Show me everything that needs attention before I commit" is `make check-dirty` followed by `make test-all`. An AI coding assistant can run these without needing to be told which repos exist or how to check them. The Makefile encodes that knowledge once.

This matters for vibe coding specifically. When you're working with an AI that loses context (and they all do eventually), having a coordination layer that doesn't depend on the model's memory changes everything. The Makefile remembers the project structure and how to validate, so the model doesn't have to. I still use it.

## What I Took Away

The Gemini experiment taught me three things:

**A big context window is not a plan.** Long-context models can hold your entire codebase. That doesn't mean they can track a multi-step migration across it. If you're doing complex multi-repo work, give the model an external artifact to follow: a spec file, a checklist, a markdown document it can re-read. Don't rely on it to hold the plan in its head.

**Verify independently, every time.** When a model tells you the work is done, that's a claim, not a fact. Run the tests. Check the imports. Read the diff. The ten minutes you spend verifying is cheaper than the hour you'll spend debugging a broken commit you trusted.

**Good ideas come from unexpected places.** The Makefile wasn't in the plan. It came from a model that couldn't reliably follow a plan. But the idea of a coordination layer that encodes project structure so the model doesn't have to remember it? That's genuinely useful. It survived the session (barely), and it's now part of how I work.

The session was messy, but it produced a cleaner architecture and a great idea. I'll take it.