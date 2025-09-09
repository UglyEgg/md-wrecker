# Markdown Paragraph Formatting Tools

A set of command-line tools for formatting paragraphs in Markdown documents:
- `soft-wrap-document`: Converts hard-wrapped text to soft-wrapped text
- `hard-wrap-document`: Converts soft-wrapped text to hard-wrapped text with a specified line width

## Features

- Preserves special Markdown elements:
  - Code blocks (```...)
  - Lists (-, *, +, or numbered)
  - Tables (starting with | and containing |---)
  - Blockquotes (starting with >)
  - Headings (starting with #)
  - YAML/TOML frontmatter (between --- or +++ delimiters)
  - JSON frontmatter (between ;;; delimiters)
  - Footnotes ([^1]: ...)
  - Definition lists (Term\n: Definition)
  - Horizontal rules (---, ***, _____)
  - Links ([text](url))
  - Inline math ($formula$)
- Processes only regular paragraph text
- Supports both soft-wrapping (removing line breaks within paragraphs) and hard-wrapping (adding line breaks at a specified width)
- Tracks statistics about the processing (wraps removed/added, paragraphs formatted, blocks ignored)
- Handles markdownlint-disable comments
- Supports parallel processing for large files

## Installation

```bash
# Install from source
pip install .
```

## Usage

### Soft-wrap Tool

The soft-wrap tool removes line breaks within paragraphs while preserving paragraph breaks.

```bash
# Basic usage
soft-wrap-document input.md output.md

# Use stdin/stdout
cat input.md | soft-wrap-document - > output.md

# Don't add markdownlint-disable comment
soft-wrap-document input.md output.md --no-lint-comment

# Create a backup of the original file
soft-wrap-document input.md output.md --backup

# Print output to stdout without saving
soft-wrap-document input.md --dry-run

# Use parallel processing for large files
soft-wrap-document input.md output.md --parallel

# Specify chunk size for parallel processing
soft-wrap-document input.md output.md --parallel --chunk-size 2000
```

### Hard-wrap Tool

The hard-wrap tool adds line breaks within paragraphs at a specified width.

```bash
# Basic usage
hard-wrap-document input.md output.md

# Specify line width
hard-wrap-document input.md output.md --width 100

# Use stdin/stdout
cat input.md | hard-wrap-document - > output.md

# Create a backup of the original file
hard-wrap-document input.md output.md --backup

# Print output to stdout without saving
hard-wrap-document input.md --dry-run

# Use parallel processing for large files
hard-wrap-document input.md output.md --parallel

# Specify chunk size for parallel processing
hard-wrap-document input.md output.md --parallel --chunk-size 2000
```

## Examples

### Soft-wrap Example

Input:
```markdown
This is a paragraph
with multiple lines
that will be joined
into a single line.

This is another paragraph
that will also be joined.

```

Output:
```markdown
<!-- markdownlint-disable -->
This is a paragraph with multiple lines that will be joined into a single line.

This is another paragraph that will also be joined.
```

### Hard-wrap Example

Input:
```markdown
This is a paragraph with multiple lines that will be wrapped at 40 characters.

This is another paragraph that will also be wrapped at 40 characters.
```

Output (with `--width 40`):
```markdown
This is a paragraph with multiple lines
that will be wrapped at 40 characters.

This is another paragraph that will also
be wrapped at 40 characters.
```

### Extended Markdown Elements Example

The tools preserve various Markdown elements:

```markdown
# Heading

This is a paragraph with [a link](https://example.com) and inline math $E = mc^2$.

;;;
{
  "title": "JSON Frontmatter"
}
;;;

Term
: Definition

[^1]: This is a footnote.

---

```

## Requirements

- Python 3.11+

## License

GPL-3.0-or-later