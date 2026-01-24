---
title: Group JUnit Tests with @Nested
summary: Use the @Nested annotation to group JUnit tests similar to a describe block in jest
author:
  - Jamal Hansen
date: 2025-02-14
lastmod: 2026-01-11
tags:
  - java
  - junit
categories:
  - Automated testing
draft: false
toc: false
series:
canonical_url: https://jamalhansen.com/blog/group-junit-tests-with-nested
slug: group-junit-tests-with-nested
layout: post

---

I really like the way that I can nest my JavaScript tests using describe blocks. This keeps my tests nicely organized and grouped together in functional blocks which can be super useful when you get a whole lot of tests created.

```javascript
describe("my component", () => {
    describe("validation", () => {
        it("ensures that user name is provided", () => {
            // test here
        })
        
        it("ensures that password is valid", () => {
            // test here
        })
    })
    
    describe("when saved", () => {
        it("displays an indication that mutation is in progress", () => {
            // test here
        })
        
        it("provides feedback of success", () => {
            // test here
        })
        
        it("provides an error message on failure", () => {
            // test here
        })
    })
})
```

I was not aware that you can do something like this in Java with JUnit. Reading through [Pragmatic Unit Testing in Java with JUnit](https://pragprog.com/titles/utj3/pragmatic-unit-testing-in-java-with-junit-third-edition/) I found that this functionality is available by making an inner class and using the `@Nested` annotation.

Note that `@Nested` is a JUnit 5 feature, so you'll need to import it:

```java
import org.junit.jupiter.api.Nested;
```

Here is an example of how the code above might be organized using JUnit and Java:

```java
class MyComponentTest {

    @Nested
    class Validation {

        @Test
        void ensuresThatUserNameIsProvided() {
            // test here
        }

        @Test
        void ensuresThatPasswordIsValid() {
            // test here
        }
    }

    @Nested
    class WhenSaved {

        @Test
        void displaysIndicationThatMutationIsInProgress() {
            // test here
        }

        @Test
        void providesFeedbackOfSuccess() {
            // test here
        }

        @Test
        void providesErrorMessageOnFailure() {
            // test here
        }
    }
}
```

One nice bonus: each `@Nested` class can have its own `@BeforeEach` setup method, so you can share setup logic within a group without affecting other groups.

I enjoy finding ways to make my testing better and easier to use. Do you have a favorite tip that you use to make your tests better organized?
