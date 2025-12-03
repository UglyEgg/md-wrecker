# Test Markdown Document

This is a paragraph with multiple lines
that will be joined into a single line.

This is another paragraph that will also
be joined.

## Code Block

```python
def hello_world():
    print("Hello, World!")
    # This should be preserved as-is
    # with all line breaks intact
```

## Lists

- Item 1
- Item 2
  - Nested item 1
  - Nested item 2
- Item 3

1. Numbered item 1
2. Numbered item 2
3. Numbered item 3

## Table

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Blockquote

> This is a blockquote
> that spans multiple lines
> and should be preserved.

## YAML Frontmatter

---
title: Test Document
author: NinjaTech AI
date: 2025-09-07
---

This is a paragraph after the
frontmatter that should be joined into a
single line.

This is a very long paragraph that
should be hard-wrapped at the specified
width. Lorem ipsum dolor sit amet,
consectetur adipiscing elit. Sed do
eiusmod tempor incididunt ut labore et
dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor
in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia
deserunt mollit anim id est laborum.
