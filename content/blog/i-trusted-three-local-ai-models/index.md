---
Created: 2026-03-04
tags:
  - local-ai
  - ollama
  - python
  - 
series:
  - "I vibe coded and lived to tell"
Related:
  - "I Vibe Coded a Local AI-Powered Promo Generator"
title: I trusted three local AI models, and Python had to clean up their mess
description: Small local models bring creativity. They don't bring discipline. Here's what I learned testing llama3.2, phi4-mini, and llama3.1:8b so you don't have to.
author:
  - Jamal Hansen
date: 2026-03-13
lastmod: 2026-03-10
newsletter_url: ""
cover:
  image: "ricardo-viana--tYsPFKMm7g-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Ricardo Viana"
    username: "ricardoviana"
    photo_id: "assorted-color-bottles-on-white-surface-with-paint-scribbles--tYsPFKMm7g"
draft: false
---


Previously, I reported that I vibe-coded [a tool that reads a blog post I've written and generates platform-specific promo copy using a local Ollama model](https://jamalhansen.com/blog/i-vibe-coded-a-local-ai-powered-promo-generator/). I chose local models because I'm curious about them. They seem to be the future of AI, at least for use cases like this... and it works... sort of.

Now, the continued story of how I trusted three local AI models and Python had to clean up after them. The truth is that I was asking too much of them, and they returned occasionally insightful and often malformed and hallucinatory results. 

The LLM brings a lot of things:
- Creative results
- Predictions (and oddly unpredictability)
- Natural language inputs and outputs

These are very significant and they make all of the hype around AI totally understandable. It's not about chatbots or a new way to search the internet. It is a fundamentally new way to use computers. 

It is in a way similar to blockchain. People get excited about it as a store of value or an immutable ledger, and it is those things. What I think is most interesting about it isn't those things. It is that blockchain is a new tool in computing. It is a way to make a digital asset unique. Before blockchain, you could always make a copy of a digital asset, and it would be exactly the same as the original. With blockchain, you can copy something, but it is no longer the same as the original 

I think of Large Language Models (LLMs) in a similar way. They have many benefits that we are already finding out about. But perhaps the most interesting is that they can introduce non-linear creativity. This should be used sparingly, or else chaos ensues. 

Thankfully for our sanity, only part of the power of agents comes from the LLM. The LLM brings the creativity you can't script, and Python brings discipline the model doesn't have. You need both to be successful.

## The Two-Pass Breakthrough

After the initially disappointing results, I suspected that the smaller model was struggling with a request that had too many instructions. The model was dealing with too many words in the prompt (the post, the instructions, the format, the promo output). It got overwhelmed and just started spewing out results for better or worse. 

My first instinct was to limit the context by splitting the actions. Two main things were happening in the prompt. It was understanding the post text that it received, and then it was outputting a promo teaser for the post on the target platform based on. The size, style, and tone of the promo post vary slightly from target platform to target platform. 

I split the single prompt into two. The first would read the post and extract the main point. Then the second would generate the promo text from that smaller summary of the post. This might lose some of the nuance of the post, but it significantly reduced the size of each prompt. It also focused both prompts on the task they were meant to do. 

This is a key takeaway that I will use going forward, especially with smaller models. Focus the request on a single task rather than a multi-step process. 

## The Architecture That Makes It Work

Of course, there is more to tuning an agent than simply shrinking the context and request. There is the ever-popular prompt engineering. This isn't a term I'm especially excited about. In this case, I didn't think that there was a magical incantation I had to discover. 

That wasn't going to stop me from trying out different details to see how the results changed. When I need to change things quickly in my programs, I like to extract those variables from the code and into configuration files. 

My next step was to create configuration files that stored the instructions for each platform's output, the brand voice, and other data points needed to tweak the prompts and evaluate the results. 

This made the flow:
1. Find the topic of the blog post
2. Load configuration for the target platform and task
3. Combine the gathered information into a new prompt
4. Output the results of the prompt.

I felt pretty good about the code at this point and anticipated that I would find success.

## Three Models, Three Lessons

I did not find success.

The changes did improve the results, but there were still some glaring issues. Here is a comparison table of the three models I tried.

| Model       | Structured extraction | Twitter char limit | Hashtag rules | Voice quality |
| ----------- | --------------------- | ------------------ | ------------- | ------------- |
| llama3.2:3b | Poor                  | Fails              | Fails         | Poor          |
| phi4-mini   | Good (with schema)    | Fails              | Mostly fails  | Mediocre      |
| llama3.1:8b | Good (with schema)    | Over by ~60 chars  | Passes        | Good          |

I started with llama3.2:3b, hopeful that a small model could handle things. That would mean that I might even be able to delegate the work to a raspberry pi and offload the work from my laptop. It did not perform well. The structured extraction fell apart, and constraints like the character limit were ignored entirely.

After consulting Claude on what would be a good model to attempt next, I pulled in results from phi4-mini. This model did a better job, but it still struggled. The output was structured in the way that I wanted it via Pydantic, but still couldn't hold character limits or follow platform rules consistently. 

After switching to Gemini CLI, I gave llama3.1:8b a shot. The jump from 3 billion to 8 billion parameters was apparent, and things started working. Structured output was reliable. The quality of the tone was noticeably better. Sadly, it wasn't perfect. Even with the additional parameters, it still overshot the character limits by about 60 chars.

I learned that at least with these models, and llama3.1:8b filling 4GB of hard drive space, none of the models I tested can do this task unsupervised. I was disappointed, but I learned about the models and the importance of guardrails. 

## Python Guardrails

So I told the small models to be structured and constrained, and it failed to do what I asked exactly the way that I asked for it. I probably should have expected that. After all, the LLM is bringing the chaos and the creativity to the project. 

I needed to use Python to enforce the structure so that, together, the final product works. 

### Character limit enforcement

The model overshoots every time, so Python truncates intelligently. Even when Llama 3.1 was told it had a "hard limit" of 280 characters, it would consistently return ~320. I implemented a post-processing guardrail that trims the body while preserving the URL and, importantly, avoiding mid-code-block truncation.

```python
def _enforce_char_limit(text: str, url: str, limit: int) -> str:
    """Trim text body so that text + newline + url fits within limit."""
    url_block = f"\n{url}"
    budget = limit - len(url_block)
    if len(text) <= budget:
        return f"{text}{url_block}"

    code_block_match = re.search(r"\n```", text)
    if code_block_match and code_block_match.start() < budget:
        trimmed = text[:code_block_match.start()].rstrip()
    else:
        trimmed = text[:budget - 3].rsplit(None, 1)[0] + "..."

    return f"{trimmed}{url_block}"
```

### Preamble stripping

"Sure, here's your tweet..." gets stripped. Just give me the output. Small models love to narrate their actions or offer "excited" greetings. A set of regex patterns aggressively scrub the "AI chatter" and leading quotes before the post is saved.

```python
def _strip_preamble(text: str) -> str:
    """Remove 'Here is the X post:' style narration the model sometimes prepends."""
    patterns = [
        r"^(?:here (?:is|are) the \w[\w /]*:?\s*)+",
        r"^(?:here's the \w[\w /]*:?\s*)+",
        r"^(?:sure, here (?:is|are) the \w[\w /]*:?\s*)+",
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE).strip()
    return text.strip(' "')
```

The `\w[\w /]*` pattern catches multi-word platform names like "Twitter post" or "Mastodon toot". The `*` is load-bearing. Without it, only single-character names match and nearly every real preamble slips through.

### "NO-GO ZONE" prompt constraints

No hashtags on Twitter, no emoji, no em dashes. These go in the prompt, not the code. I found that creating a dedicated "NO-GO ZONE" section in the system prompt, using high-contrast language, was far more effective than just listing style rules buried in a paragraph.

```python
PLATFORM_PROMPT_TEMPLATE = """Write the {label} post for this blog post using the provided context.

## NO-GO ZONE (Violations will cause failure)
- NO hashtags (except for Mastodon)
- NO emoji
- NO em dashes (--)
- NO announcement filler ("I'm excited to share", "New post", "Check out")
- NO hype words ("revolutionary", "game-changing", "amazing")

## Platform rules
{instructions}
{char_limit_line}
{hashtag_line}
{emoji_line}

## Fixed values
Post URL: {url}
{cta_line}
{subscribe_line}

## Context (extracted from the post)
{context}

## Output format
{output_format}"""
```

Each platform's format variables (`{instructions}`, `{char_limit_line}`, etc.) are filled from a `platforms.yaml` config file, so adding a new platform is a YAML edit, not a code change.

### Regex-based JSON fallback

When structured output comes back messy, catch it instead of crashing. Small models often wrap their JSON in Markdown backticks or add conversational text around it, causing standard JSON parsers to fail. The `_parse_json_response` method in the shared `local-first-common` library handles this with a two-stage fallback:

```python
def _parse_json_response(self, content: str, response_model: Any) -> Dict[str, Any]:
    try:
        result = json.loads(content)
        return self._clean_json(result, response_model)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            result = json.loads(match.group())
            return self._clean_json(result, response_model)
        raise
```

First, try a clean `json.loads`. If that fails, use `re.DOTALL` to hunt for the first `{...}` block in whatever the model returned (backticks, preamble, and all). If even that fails, it raises rather than silently returning bad data. No phantom defaults, no silent swallowing of errors. The caller decides what to do with a genuinely unparseable response.

## Lessons Learned

Smaller models may yet have a place in my toolbox, but they aren't as polished as the frontier models. Using the strengths of each of my tools is key to making the project work. 

To be honest, this "generate then validate" pattern isn't unique to local models. Cloud APIs need guardrails too. Small local models just make the pattern impossible to ignore because the gaps are bigger and far more noticeable.

I'm glad that I got to work with models that aren't polished. Working closely with them taught me things about LLM behavior I wouldn't learn from a cloud model. It's a bit like driving a car with a standard transmission vs an automatic. You can feel the "road" of the constraints (model size, memory, speed) in a way that's invisible behind a cloud endpoint.

Ultimately, the tool needs more work, but it does do most of what I ask it to. It's not perfect. But it saves real time on a weekly task, and the architecture is solid enough to improve over time.

So, the architecture works, the guardrails work, but why should I run any of this locally when cloud models handle it better? Part 3 makes the case for local-first.

Do you have experience with smaller models or local-first AI? I'd like to know more about it. Please reach out and let me know if your experience was similar to mine. 
