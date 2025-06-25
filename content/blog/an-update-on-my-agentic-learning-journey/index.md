---
title: An update on my agentic learning journey
summary: An update after a few weeks about learning agentic AI, it's been a fun journey and I've found some great resources
author:
  - Jamal Hansen
date: 2025-06-24
lastmod: ""
tags:
  - agentic
categories: 
featureimage: agentic-update-landscape.jpg
cardimage: agentic-update-card.jpg
draft: false
toc: false
series: 
canonical_url: https://jamalhansen.com/blog/an-update-on-my-agentic-learning-journey
slug: an-update-on-my-agentic-learning-journey
layout: post
---

A few weeks back I started on an agentic journey with the Udemy offering The Complete Agentic AI Engineering Course. This has been a great hands-on offering. I've completed 4 of the 6 weeks covering OpenAI Agents SDK, CrewAI, and LangGraph as well as some foundational theory. Throughout the course, the instructor [Ed Donner](https://www.linkedin.com/in/eddonner) has done a great job teaching enthusiastically and providing real world code that demonstrates the concepts of each framework. 

I found out that Ed also runs live events on the OReilly platform and so I signed up for today's live session called Hands-On LLM Engineering. I persuaded some of my colleagues to check it out with me as well. During the live event Ed provided the same high quality of hands-on learning materials that makes his recorded trainings great. It was a great session and I look forward to reviewing the concepts covered in greater depth and incorporating them in my studies. 

If you are interested in learning more about what it means for AI to be 'agentic', I highly recommend this training. 

I've also been dabbling in using Model Context Protocol (MCP). I've written an MCP server that serves up small slices of my obsidian notes in a controlled way. This allows me to reference it from Claude without worrying about excessive access to files that I don't want viewed, or accidentally having write access. 

So far I've exposed my obsidian notes about my high level 2025 goals and a set of trainings that I wrote. It is interesting to see the insights that Claude has, or asking it what I can do right now to advance my yearly goals. 

Note: I just asked that and it told me that I want to write more in 2025 and so I should probably stop talking to it and start writing :)

I don't fully understand the purpose of resources and prompts in the MCP spec. I initially exposed my notes in three tools. The first returns as list of note sets which are the slices of notes that I'm exposing. The second gives the files available in the slice with a brief description. The third returns the content of a specific note. 

After consideration, I thought that it would make sense to expose these as resources rather than tools, so I updated my mcp server. Once I changed, them Claude could no longer access them or see them. I'm most likely doing something wrong but for now I switched them back to tools. 

So all in all it's going well, I want to apply what I'm learning and will probably be trying out some new agent ideas here soon. 
### Links 

- [Hands-On LLM Engineering Live Event (O'Reilly)](https://learning.oreilly.com/live-events/hands-on-llm-engineering/0642572011365/0642572178284/)
- [The Complete Agentic AI Engineering Course (Udemy)](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course)