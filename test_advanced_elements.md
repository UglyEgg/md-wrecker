# Test Advanced Markdown Elements

This is a paragraph
with multiple lines
that will be joined
into a single line.

## Task Lists

- [ ] Uncompleted task item
- [x] Completed task item
- [ ] Another uncompleted task
- [x] Another completed task

1. [ ] Uncompleted numbered task
2. [x] Completed numbered task

* [ ] Uncompleted star task
* [x] Completed star task

+ [ ] Uncompleted plus task
+ [x] Completed plus task

## HTML Blocks

### Simple HTML Block

<div class="container">
    <p>This is HTML content</p>
    <span>With multiple tags</span>
</div>

### Self-closing HTML Tag

<img src="image.jpg" alt="Description" />

### HTML Comment

<!-- This is an HTML comment that should be preserved -->

### Complex HTML Block

<table>
    <tr>
        <th>Header 1</th>
        <th>Header 2</th>
    </tr>
    <tr>
        <td>Cell 1</td>
        <td>Cell 2</td>
    </tr>
</table>

## Strikethrough Text

This paragraph contains ~~strikethrough text~~ that should be preserved.

Multiple ~~strikethrough~~ elements in a ~~single paragraph~~ should all be preserved.

## Emoji Shortcodes

This paragraph contains emoji shortcodes like :smile: and :heart: that should be preserved.

Multiple emoji :wink: :tada: :rocket: in a single paragraph should all be preserved.

Mixed text with emoji :thumbs_up: and regular text.

## Autolinks

This paragraph contains an autolink https://example.com that should be preserved.

Multiple autolinks https://google.com and https://github.com in a paragraph.

Mixed with regular links: [explicit link](https://example.com) and autolink https://example.org.

## Extended Tables

### Standard Table

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

### Aligned Table

| Left | Center | Right |
|:-----|:------:|------:|
| Text | Center | Right |
| Left | Middle | Align |
| Data | Center | Value |

### Multi-line Content Table

| Header | Description |
|--------|-------------|
| Item 1 | This is a longer description that wraps |
        | across multiple lines in the source |
| Item 2 | Another description with
        | multiple lines |

## Combined Elements

This paragraph has [links](https://example.com), ~~strikethrough~~, emoji :smile:, and autolinks https://github.com all in one.

Task lists in paragraphs: - [x] completed and - [ ] pending items.

Mixed HTML <span>inline</span> with other elements.

## Nested Elements

> This blockquote contains [links](https://example.com), ~~strikethrough~~, and emoji :smile:.
>
> Multiple lines with - [ ] task lists and autolinks https://example.com.

### Code blocks with inline elements

This paragraph has `inline code` and ~~strikethrough~~ text.

## Complex Example

Here's a complex example with all elements:

- [ ] Task item with [link](https://example.com)
- [x] Completed item with ~~strikethrough~~
- [ ] Item with emoji :rocket:
- [x] Item with autolink https://github.com

<div class="example">
    <p>HTML block with <strong>bold</strong> and ~~strikethrough~~ text</p>
    <a href="https://example.com">HTML link</a>
</div>

Final paragraph with :smile: emoji, [links](https://example.com), ~~strikethrough~~, and autolinks https://github.com.