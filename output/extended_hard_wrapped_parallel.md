# Test Extended Markdown Elements

This is a paragraph with multiple lines that will be joined into a single line.

This is another paragraph that will also be joined.

## JSON Frontmatter

;;;
{
  "title": "Test Document",
  "author": "NinjaTech AI",
  "date": "2025-09-08"
}
;;;

This is a paragraph after the JSON frontmatter that should be joined into a
single line.

## Footnotes

Here is a sentence with a footnote[^1].

And another sentence with a footnote[^note].

[^1]: This is the first footnote.
It can span multiple lines.

[^note]: This is the second footnote.
It can also span multiple lines.

## Links

This is a [link to example.com](https://example.com) in a paragraph that should be preserved when formatting.

This is a paragraph with [multiple](https://example.com) [links](https://example.org) that should all be preserved.

## Inline Math

This paragraph contains inline math $E = mc^2$ that should be preserved when
formatting.

This paragraph contains multiple inline math elements $a^2 + b^2 = c^2$ and $F = G\frac{m_1 m_2}{r^2}$
that should all be preserved.

## Definition Lists

Term 1
: Definition 1
: Definition 2

Term 2
: Definition 3
This definition spans multiple lines.

## Horizontal Rules

Above this is a paragraph.

---

Below this is a paragraph.

***

Another paragraph.

_____

Final paragraph.

## Combined Elements

This paragraph has [links](https://example.com) and inline math $E = mc^2$
that should be preserved when formatting[^combined].

[^combined]: This is a footnote for the combined elements section.
