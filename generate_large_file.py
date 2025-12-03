#!/usr/bin/env python3
"""
Generate a large Markdown file for testing.
"""

import random
import sys

# Define some sample paragraphs
PARAGRAPHS = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    "Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris.",
    "Integer in mauris eu nibh euismod gravida. Duis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor.",
    "Pellentesque malesuada nulla a mi. Duis sapien sem, aliquet nec, commodo eget, consequat quis, neque. Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing sapien, sed malesuada diam lacus eget erat.",
    "Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat."
]

# Define some Markdown elements
CODE_BLOCKS = [
    "```python\ndef hello_world():\n    print(&quot;Hello, World!&quot;)\n```",
    "```javascript\nfunction helloWorld() {\n    console.log(&quot;Hello, World!&quot;);\n}\n```",
    "```bash\necho &quot;Hello, World!&quot;\n```"
]

LISTS = [
    "- Item 1\n- Item 2\n- Item 3",
    "1. First item\n2. Second item\n3. Third item",
    "* Point A\n* Point B\n* Point C"
]

TABLES = [
    "| Header 1 | Header 2 | Header 3 |\n|----------|----------|----------|\n| Cell 1   | Cell 2   | Cell 3   |\n| Cell 4   | Cell 5   | Cell 6   |",
    "| Name | Age | Location |\n|------|-----|----------|\n| John | 30  | New York  |\n| Jane | 25  | London    |"
]

BLOCKQUOTES = [
    "> This is a blockquote\n> that spans multiple lines\n> and should be preserved.",
    "> Another blockquote\n> with multiple lines."
]

HEADINGS = [
    "# Heading 1",
    "## Heading 2",
    "### Heading 3",
    "#### Heading 4"
]


def generate_hard_wrapped_paragraph(paragraph, width=80):
    """Generate a hard-wrapped paragraph."""
    words = paragraph.split()
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + (1 if current_line else 0) > width:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            if current_line:
                current_length += 1 + len(word)
            else:
                current_length = len(word)
            current_line.append(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return "\n".join(lines)


def generate_large_file(file_path, size_mb=1, hard_wrapped=True):
    """Generate a large Markdown file."""
    with open(file_path, "w") as f:
        f.write("# Large Test File\n\n")
        
        # Calculate approximate number of paragraphs needed
        # Assuming average paragraph is about 500 bytes
        num_paragraphs = int((size_mb * 1024 * 1024) / 500)
        
        for i in range(num_paragraphs):
            # Add a heading every 10 paragraphs
            if i % 10 == 0:
                f.write(f"\n{random.choice(HEADINGS)}\n\n")
            
            # Add a special element every 5 paragraphs
            if i % 5 == 0:
                element_type = random.choice(["code", "list", "table", "blockquote"])
                if element_type == "code":
                    f.write(f"\n{random.choice(CODE_BLOCKS)}\n\n")
                elif element_type == "list":
                    f.write(f"\n{random.choice(LISTS)}\n\n")
                elif element_type == "table":
                    f.write(f"\n{random.choice(TABLES)}\n\n")
                elif element_type == "blockquote":
                    f.write(f"\n{random.choice(BLOCKQUOTES)}\n\n")
            
            # Add a paragraph
            paragraph = random.choice(PARAGRAPHS)
            if hard_wrapped:
                paragraph = generate_hard_wrapped_paragraph(paragraph, width=random.randint(60, 100))
            
            f.write(f"{paragraph}\n\n")


if __name__ == "__main__":
    size_mb = 1  # Default size: 1 MB
    output_file = "tests/large_test_file.md"
    hard_wrapped = True
    
    if len(sys.argv) > 1:
        size_mb = float(sys.argv[1])
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    if len(sys.argv) > 3:
        hard_wrapped = sys.argv[3].lower() in ("true", "yes", "1")
    
    generate_large_file(output_file, size_mb, hard_wrapped)
    print(f"Generated {size_mb} MB Markdown file at {output_file}")