---
slug: i-extracted-a-shared-library-and-got-400-tests-i-didnt-ask-for
post: 6
arc: Architecture Arc
title: I Extracted a Shared Library and Got 400 Tests I Didn't Ask For
description: Six Python projects, four duplicated files, one shared library. Here's the code behind the extraction, what moved, what didn't, and the surprise that made it worth it.
series:
  - "I vibe coded and lived to tell"
author:
  - Jamal Hansen
lastmod: 2026-03-31
tags:
  - vibe-coding
  - architecture
  - python
cover:
  image: "trnava-university-BEEyeib-am8-unsplash.jpg"
  alt: "A bookshelf in a library"
  caption: ""
  relative: true
  credit:
    name: "Trnava University"
    username: "trnavskauni"
    photo_id: "brown-wooden-book-shelf-with-books-BEEyeib-am8"
date: 2026-04-10
---

[Last time](https://jamalhansen.com/blog/copy-and-paste-long-enough-and-the-architecture-appears) I argued that you can't design your way to a good abstraction. You have to earn it through repetition. Here's what that actually looked like.

I had six Python projects, each containing its own version of the same four files:
- A provider abstraction for talking to LLMs
- CLI argument helpers
- Obsidian utilities for reading and writing notes
- A testing module for stubbing out model calls

I knew that I wasn't sharing code between the tools and that each would have similar needs. But it wasn't my priority to fix, so I let it happen. And the code accumulated, one project at a time, each one re-creating a variation on the same logic. Like a lazy developer, copy-pasting code from another repository and tweaking it to fit.

Here's how I extracted the shared logic into a shared library called `local-first-common`: what moved, what didn't, and the side effect that made the whole thing worth it.

## Four Files, Six Times

Every tool in my workflow talks to LLMs. That means every tool needs:

**`providers/`** - An abstract `BaseProvider` class with a `complete()` method, plus concrete implementations for Ollama, Anthropic, Groq, and DeepSeek. Local models are the priority, but some aren't capable enough on their own, so cloud providers matter for comparison. Each provider knows its default model, its list of known models, and where to find the full catalog online.

**`cli.py`** - Shared argument definitions for `--provider`, `--model`, `--verbose`, and `--dry-run`. A `resolve_provider()` function that takes the provider name and optional model override, instantiates the right class, and hands it back ready to use.

**`obsidian.py`** - Most of my tools read from or write to an Obsidian vault. This handles vault path discovery, frontmatter reading and writing, and note updates.

**`testing.py`** - A `MockProvider` that returns canned responses without hitting any API. This one turned out to matter more than I expected.

Six projects. Four duplicated modules. All slightly different. That's the starting point.

## Three Ways to Share Code (One That Fits)

Once I decided to extract a shared library, the question was how to distribute it. I had three options.

**Monorepo.** Put everything in one repository. It probably would have been easier if I had chosen this route, especially at the beginning. I had 26 tool ideas in the backlog, and the list was growing. As I write this, the list is up to 42 tools, and I am questioning my sanity. Cramming all of this into one repo would mean every tool shares a commit history, a CI pipeline, and a release cycle with every other tool. I wasn't willing to do that.

**Publish to PyPI.** Clearly, this is the "real" way to share a Python package. But publishing to a registry means maintaining version numbers, writing a release workflow, and dealing with authentication. For a library that has exactly one consumer (me), that's way too much overhead.

**Git URL dependency.** Point each tool's `pyproject.toml` at the shared library's GitHub repo. No registry. No release pipeline. Just a URL.

Here's what that looks like in the `pyproject.toml`:

```toml
[tool.uv.sources]
local-first-common = { git = "https://github.com/jamalhansen/local-first-common.git", rev = "main" }
```

Run `uv sync`, and the library installs directly from the repo. When I push a change to `local-first-common`, each tool picks it up on its next sync.

This is the middle path. Less overhead than PyPI, less coupling than a monorepo. For personal tooling, it is the right trade-off.

### Local Development Override

There's one big problem with this solution. When you're actively working on the shared library, you don't want to push a commit and re-sync every time you change a line. The fix is a `pyproject.toml` file that swaps the git reference for a local editable path.

```toml
[tool.uv.sources]
local-first-common = {path = "../local-first-common", editable = true}
```

## What Moved (and What Didn't)

The migration itself was straightforward, especially with the help of Claude Code: 
1. Create the `local-first-common` repo
2. Move the four modules in
3. Update `pyproject.toml` in each tool
4. Delete the local copies
5. Run the tests
6. Fix anything that broke

One interesting part was what didn't migrate.

One of the tools is a privacy-minded baby journal. It seemed to be a strong candidate for using this shared code. It reads and writes markdown. It discovers files in a directory. It serializes structured data into notes. All of that sounds like overlap with `obsidian.py`.

But none of it moved. The baby journal's file discovery uses TOML config to find its data directory, not Obsidian vault detection. Its note serialization is tied to a typed `JournalEntry` model with fields like `mood`, `milestones`, and `photo_paths`. Its LLM-based auto-tagging and photo handling have no equivalent in any other tool, and its privacy-first stance didn't benefit from gaining access to cloud models.

The utilities looked similar from a distance. Up close, they were solving different problems. If I'd forced them into the shared library up front, I would have been extracting noise, not signal, and adding unneeded complexity to the shared code.

That false negative made the abstraction boundary real. The things that didn't move validate the things that did.

## The Before and After: Promo Generator

The promo-generator is the clearest example of what the migration looked like in practice. Before the migration, it hardcoded the `ollama` Python package with a fixed model. It looked something like this:

<!-- test:setup -->
```python
provider_name = "ollama"
model = "llama3.2"
```
```python
import ollama

def generate_promo(content: str, platform: str) -> str:
    response = ollama.generate(
        model="llama3.2",
        prompt=f"Write a {platform} promo for this blog post:\n\n{content}",
    )
    return response["response"]
```

After the migration, it uses the shared provider abstraction:

```python
from local_first_common.cli import resolve_provider
from local_first_common.providers import PROVIDERS

def generate_platform(platform_key, platform, provider, url, context, config, verbose, dry_run):
    system = build_system_prompt()
    prompt = build_platform_prompt(platform, url, context, config)
    result = provider.complete(system, prompt)
    return result

# In the CLI
provider = resolve_provider(PROVIDERS, provider_name, model)
```

The function no longer knows or cares which LLM it's talking to. Ollama, Anthropic, Groq, DeepSeek, they all work. The provider is chosen at the command line with `--provider` and `--model`, same as other tools.

That's an improvement, but it's not the best part.

## The Thing I Didn't Ask For

The best part was testability.

Before the migration, promo-generator had zero tests. Every function that did anything interesting called an LLM. Patching out a third-party SDK call is tedious and fragile, even with a coding agent at your disposal.

`local-first-common` now includes `MockProvider`, a provider that returns canned responses without hitting any API or model. After the migration, testing an LLM-powered function looks like this:

```python
from local_first_common.testing import MockProvider

def test_generate_platform():
    url = "https://jamalhansen.com/blog/my-post"
    provider = MockProvider(response=f"Check out this post.\n{url}")
    result = generate_platform(
        "twitter", SAMPLE_PLATFORM, provider,
        url, "HOOK: Something", {}, verbose=False, dry_run=False,
    )
    assert isinstance(result, str)
    assert url in result
    assert len(provider.calls) == 1
```

No HTTP mocking. No patching. No fixtures. You pass in a `MockProvider` and get a predictable response.

Promo-generator went from 0 tests to 33 after the migration. Not because the logic changed. The logic was already there. The migration made it testable.

Across all seven repos, I ended up with over 400 passing tests. That's a nice number, but the number isn't the point. Good architecture and good testability are the same thing. When your functions take their dependencies as arguments instead of reaching out to global state, testing becomes trivial. The shared library made that pattern the default.

## What's in the Box

`local-first-common` has four modules:

- **`providers/`** - `BaseProvider` abstract class, plus `OllamaProvider`, `AnthropicProvider`, `GroqProvider`, `DeepSeekProvider`, and `GeminiProvider`. A `PROVIDERS` dict mapping names to classes, and `resolve_provider()` for instantiating the right one from CLI flags.
- **`obsidian.py`** - Vault path discovery, frontmatter reading and writing, note creation helpers.
- **`cli.py`** - Shared argument definitions for `--provider`, `--model`, `--verbose`, and `--dry-run`. Works with argparse, Typer, or Click.
- **`testing.py`** - `MockProvider` for stubbing LLM calls in tests without patching anything.

Four modules at the time of extraction. The library has grown since, and it now has utilities for tracking, social posting, HTTP helpers, and more. Those came later, one tool at a time, the same way the original four did.

## The Takeaway

Don't extract early. The pattern has to repeat enough times that you actually know what the pattern is. If I'd pulled a shared library out after two tools, I would have extracted the wrong thing.

Git URL dependencies are the right middle ground for personal tooling. No registry. No release pipeline. No version numbers to maintain. Push to the repo, run `uv sync`, move on.

Pay attention to what doesn't migrate. If everything moves, you didn't find a real abstraction. The baby journal not moving validated everything that did.

The testability wasn't something I planned. It was a consequence of the architecture. When functions take their dependencies as arguments instead of reaching out to global state, tests become straightforward to write. The shared library made that the default pattern across all the tools.

Next time, BartBot takes the keyboard. The topic is institutional memory, skill files, and the mild strangeness of an AI writing instructions for itself.
