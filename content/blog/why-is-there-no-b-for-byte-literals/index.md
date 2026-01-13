---
title: You don't need a 'B' suffix for byte literals in Java
summary: Unlike long, the Java byte literal doesn't require a suffix. Diving into a rabbit hole to find out why
author:
  - Jamal Hansen
date: 2025-02-07
lastmod: 2026-01-11
tags:
  - java
  - byte
categories: Java
featureimage:
cardimage:
draft: false
toc: false
series:
canonical_url: https://jamalhansen.com/blog/why-is-there-no-b-for-byte-literals
slug: why-is-there-no-b-for-byte-literals
layout: post

---

Today I was coding in Java and I came across a part of the code where I was using a byte literal. I've been using Java for a while, so I knew that you have to suffix `long` literals with an 'L' otherwise Java complains.

```java
long myLong = 3000000000L;     // Java is happy
long myOtherLong = 3000000000; // Java is sad (too big for int)
```

So when I went to create my byte literal I figured I would need to put a suffix on the number, like I do with long literals. But when I tried it, it turns out I didn't need to.

```java
byte myByte = 12;  // Java is happy
byte myByte = 12B; // Java is sad
```

## Long Needs an L Suffix

So I looked into it and found out that Java integer literals are always created as `int` by default. This makes sense because I knew that when I forgot the 'L' when assigning a value to a `long`, the message was about trying to assign an `int` to a `long` variable. So, to tell Java that you are in fact trying to assign a `long` literal to a `long` variable, you include the 'L'. If you don't provide the 'L', Java gets confused.

## Java Doesn't Have a B Suffix for byte

Java automatically converts integer values to `byte` if they are within the valid range for a byte type (-128 to 127). This is called a narrowing primitive conversion, and Java allows it for compile-time constants that fit in the target range. So Java will automatically convert a value, say 1, to a byte and assign it. You can also explicitly cast it if you prefer.

```java
byte b = (byte) 1;  // Java is happy
byte b = 1;         // Java is happy
```

This is good to know but seems counterintuitive. I would think that an automatic type conversion would be allowed when putting a type with a smaller range into one of a larger range because there is no risk of overflow. Why does it work in the opposite way?

The answer is that Java *does* allow widening conversions (small to large) implicitly — you can assign a `byte` to an `int` without casting. But for narrowing conversions (large to small), Java normally requires an explicit cast because data could be lost. The exception is compile-time constants: if Java can verify at compile time that the value fits, it allows the assignment without a cast. That's why `byte b = 12;` works but `byte b = someIntVariable;` would not.
