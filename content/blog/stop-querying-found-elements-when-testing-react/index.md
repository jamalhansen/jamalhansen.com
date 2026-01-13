---
title: Stop querying found elements when testing react
summary: Use Testing Library's within() to query nested elements in one readable line and avoid repeating yourself
author:
  - Jamal Hansen
date: 2025-02-15
lastmod: 2026-01-10
tags:
  - JavaScript
  - jest
  - vite
  - testing-library
categories:
  - Automated testing
  - Today I learned
featureimage:
cardimage:
draft: false
toc: false
series:
canonical_url: https://jamalhansen.com/blog/stop-querying-found-elements-when-testing-react
slug: stop-querying-found-elements-when-testing-react
layout: post

---

I've been working through Stephen Grider's [React Testing Library and Jest](http://udemy.com/course/react-testing-library-and-jest) course and stumbled on something that will clean up my tests: the `within()` function.

There are many times when I find myself drilling into a part of a component to test something nested inside another element. I might take two or three hops to get there:

```jsx
import { within, screen } from '@testing-library/react'

const table = screen.getByRole("table")
const rows = within(table).getAllByRole("row")
```

This takes two lines and, more importantly:
- It isn't immediately clear what I am doing
- I declare the `table` constant when it isn't relevant to anything

With `within()`, you can shorten this to a single readable line:

```jsx
const rows = within(screen.getByRole("table")).getAllByRole("row")
```

I like this because it reads like a sentence and clearly expresses the intention. It also doesn't create a meaningless intermediate constant.

## When to Use `within()`

- Testing a specific row in a table
- Checking content inside a modal or card
- Any time you need to scope queries to a container

## A Note on Async Queries

If you're using `findBy*` queries (which are async), remember to `await`:

```jsx
const rows = within(await screen.findByRole("table")).getAllByRole("row")
```

Or if both queries are async:

```jsx
const button = await within(await screen.findByTestId("modal")).findByRole("button")
```

When possible, prefer `getBy*` (synchronous) for cleaner one-liners.

Do you have any testing tips you've learned recently?
