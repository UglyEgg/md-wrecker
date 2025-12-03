# SPDX-License-Identifier: GPL-3.0-or-later
"""
Unit tests for the core module.

Copyright (C) 2025 NinjaTech AI

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import io
import unittest
from mdformat.core import MarkdownProcessor, BlockType


class TestMarkdownProcessor(unittest.TestCase):
    """Test cases for the MarkdownProcessor class."""
    
    def setUp(self):
        """Set up the test case."""
        self.processor = MarkdownProcessor()
    
    def test_identify_block_type(self):
        """Test the _identify_block_type method."""
        # Test paragraph
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "This is a paragraph", False, False, False
        )
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test code block
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "```python", False, False, False
        )
        self.assertEqual(block_type, BlockType.CODE_BLOCK)
        self.assertTrue(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test task list
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "- [ ] Task item", False, False, False
        )
        self.assertEqual(block_type, BlockType.TASK_LIST)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test completed task list
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "- [x] Completed task", False, False, False
        )
        self.assertEqual(block_type, BlockType.TASK_LIST)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test numbered task list
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "1. [x] Numbered task", False, False, False
        )
        self.assertEqual(block_type, BlockType.TASK_LIST)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test HTML block
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "<div>", False, False, False
        )
        self.assertEqual(block_type, BlockType.HTML_BLOCK)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test HTML self-closing tag
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "<img src='test.jpg' />", False, False, False
        )
        self.assertEqual(block_type, BlockType.HTML_BLOCK)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test HTML comment
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "<!-- This is a comment -->", False, False, False
        )
        self.assertEqual(block_type, BlockType.HTML_BLOCK)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test regular list (not task list)
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "- Regular item", False, False, False
        )
        self.assertEqual(block_type, BlockType.LIST)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
        
        # Test empty line
        block_type, in_code_block, in_frontmatter, in_json_frontmatter = self.processor._identify_block_type(
            "", False, False, False
        )
        self.assertEqual(block_type, BlockType.EMPTY)
        self.assertFalse(in_code_block)
        self.assertFalse(in_frontmatter)
        self.assertFalse(in_json_frontmatter)
    
    def test_html_block_state(self):
        """Test HTML block state tracking."""
        # Test opening HTML block
        self.processor._update_html_block_state("<div>")
        self.assertTrue(self.processor.in_html_block)
        self.assertEqual(self.processor.html_block_tag, "div")
        
        # Test content inside HTML block
        self.processor._update_html_block_state("    <p>Content</p>")
        self.assertTrue(self.processor.in_html_block)
        self.assertEqual(self.processor.html_block_tag, "div")
        
        # Test closing HTML block
        self.processor._update_html_block_state("</div>")
        self.assertFalse(self.processor.in_html_block)
        self.assertIsNone(self.processor.html_block_tag)
        
        # Test self-closing tag
        self.processor._update_html_block_state("<img src='test.jpg' />")
        self.assertFalse(self.processor.in_html_block)
        self.assertIsNone(self.processor.html_block_tag)
    
    def test_preserve_inline_elements(self):
        """Test the _preserve_inline_elements method."""
        # Test with strikethrough
        text = "This has ~~strikethrough~~ text."
        processed_text, preserved = self.processor._preserve_inline_elements(text)
        
        self.assertNotIn("~~strikethrough~~", processed_text)
        self.assertIn("__STRIKETHROUGH_", processed_text)
        self.assertEqual(len(preserved), 1)
        
        restored_text = self.processor._restore_inline_elements(processed_text, preserved)
        self.assertEqual(restored_text, text)
        
        # Test with emoji shortcodes
        text = "This has :smile: emoji."
        processed_text, preserved = self.processor._preserve_inline_elements(text)
        
        self.assertNotIn(":smile:", processed_text)
        self.assertIn("__EMOJI_", processed_text)
        self.assertEqual(len(preserved), 1)
        
        restored_text = self.processor._restore_inline_elements(processed_text, preserved)
        self.assertEqual(restored_text, text)
        
        # Test with autolinks
        text = "This has https://example.com autolink."
        processed_text, preserved = self.processor._preserve_inline_elements(text)
        
        self.assertNotIn("https://example.com", processed_text)
        self.assertIn("__AUTOLINK_", processed_text)
        self.assertEqual(len(preserved), 1)
        
        restored_text = self.processor._restore_inline_elements(processed_text, preserved)
        self.assertEqual(restored_text, text)
        
        # Test with multiple elements
        text = "This has ~~strikethrough~~, :smile: emoji, and https://example.com."
        processed_text, preserved = self.processor._preserve_inline_elements(text)
        
        self.assertNotIn("~~strikethrough~~", processed_text)
        self.assertNotIn(":smile:", processed_text)
        self.assertNotIn("https://example.com", processed_text)
        self.assertIn("__STRIKETHROUGH_", processed_text)
        self.assertIn("__EMOJI_", processed_text)
        self.assertIn("__AUTOLINK_", processed_text)
        self.assertEqual(len(preserved), 3)
        
        restored_text = self.processor._restore_inline_elements(processed_text, preserved)
        self.assertEqual(restored_text, text)
    
    def test_process_paragraph_soft_wrap(self):
        """Test the _process_paragraph method with soft-wrapping."""
        lines = [
            "This is a paragraph",
            "with multiple lines",
            "that will be joined",
            "into a single line."
        ]
        
        result = self.processor._process_paragraph(lines, line_width=None)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0],
            "This is a paragraph with multiple lines that will be joined into a single line."
        )
        self.assertEqual(self.processor.stats.wraps_removed, 3)
        self.assertEqual(self.processor.stats.paragraphs_formatted, 1)
    
    def test_process_paragraph_with_inline_elements(self):
        """Test processing paragraphs with inline elements."""
        # Test with strikethrough
        lines = [
            "This paragraph has ~~strikethrough~~",
            "text that should be preserved",
            "when formatting."
        ]
        
        result = self.processor._process_paragraph(lines, line_width=None)
        
        self.assertEqual(len(result), 1)
        self.assertIn("~~strikethrough~~", result[0])
        self.assertEqual(self.processor.stats.wraps_removed, 2)
        
        # Test with emoji
        lines = [
            "This has :smile: emoji",
            "and :heart: more emoji",
            "in the paragraph."
        ]
        
        result = self.processor._process_paragraph(lines, line_width=None)
        
        self.assertEqual(len(result), 1)
        self.assertIn(":smile:", result[0])
        self.assertIn(":heart:", result[0])
        
        # Test with autolinks
        lines = [
            "This has https://example.com",
            "and https://github.com autolinks",
            "in the paragraph."
        ]
        
        result = self.processor._process_paragraph(lines, line_width=None)
        
        self.assertEqual(len(result), 1)
        self.assertIn("https://example.com", result[0])
        self.assertIn("https://github.com", result[0])
    
    def test_task_list_preservation(self):
        """Test that task lists are preserved during processing."""
        input_text = """
- [ ] Uncompleted task
- [x] Completed task
- [ ] Another uncompleted

1. [x] Completed numbered
2. [ ] Uncompleted numbered

This is a paragraph
that should be formatted.
"""
        
        input_stream = io.StringIO(input_text)
        output_stream = io.StringIO()
        
        stats = self.processor.process_markdown(
            input_stream,
            output_stream,
            line_width=None,
            add_lint_comment=True,
            remove_lint_comment=False
        )
        
        output_text = output_stream.getvalue()
        
        # Check that task lists are preserved
        self.assertIn("- [ ] Uncompleted task", output_text)
        self.assertIn("- [x] Completed task", output_text)
        self.assertIn("1. [x] Completed numbered", output_text)
        self.assertIn("2. [ ] Uncompleted numbered", output_text)
        
        # Check that paragraph is formatted
        self.assertIn("This is a paragraph that should be formatted.", output_text)
        
        self.assertEqual(stats.paragraphs_formatted, 1)
        self.assertGreaterEqual(stats.blocks_ignored, 2)  # Task lists
    
    def test_html_block_preservation(self):
        """Test that HTML blocks are preserved during processing."""
        input_text = """
<div class="container">
    <p>This is HTML content</p>
    <span>With multiple tags</span>
</div>

This is a paragraph
that should be formatted.

<img src="image.jpg" alt="Description" />

<!-- HTML comment -->

Final paragraph
to be formatted.
"""
        
        input_stream = io.StringIO(input_text)
        output_stream = io.StringIO()
        
        stats = self.processor.process_markdown(
            input_stream,
            output_stream,
            line_width=None,
            add_lint_comment=True,
            remove_lint_comment=False
        )
        
        output_text = output_stream.getvalue()
        
        # Check that HTML blocks are preserved
        self.assertIn('<div class="container">', output_text)
        self.assertIn("<p>This is HTML content</p>", output_text)
        self.assertIn("<span>With multiple tags</span>", output_text)
        self.assertIn("</div>", output_text)
        self.assertIn('<img src="image.jpg" alt="Description" />', output_text)
        self.assertIn("<!-- HTML comment -->", output_text)
        
        # Check that paragraphs are formatted
        self.assertIn("This is a paragraph that should be formatted.", output_text)
        self.assertIn("Final paragraph to be formatted.", output_text)
        
        self.assertEqual(stats.paragraphs_formatted, 2)
        self.assertGreaterEqual(stats.blocks_ignored, 3)  # HTML blocks
    
    def test_strikethrough_preservation(self):
        """Test that strikethrough text is preserved during processing."""
        input_text = """
This paragraph has ~~strikethrough text~~ that should be preserved.

Another paragraph with ~~multiple~~ strikethrough ~~elements~~.
"""
        
        input_stream = io.StringIO(input_text)
        output_stream = io.StringIO()
        
        stats = self.processor.process_markdown(
            input_stream,
            output_stream,
            line_width=None,
            add_lint_comment=True,
            remove_lint_comment=False
        )
        
        output_text = output_stream.getvalue()
        
        # Check that strikethrough is preserved
        self.assertIn("~~strikethrough text~~", output_text)
        self.assertIn("~~multiple~~", output_text)
        self.assertIn("~~elements~~", output_text)
        
        self.assertEqual(stats.paragraphs_formatted, 2)
    
    def test_emoji_shortcode_preservation(self):
        """Test that emoji shortcodes are preserved during processing."""
        input_text = """
This paragraph has :smile: emoji that should be preserved.

Multiple emoji :wink: :tada: :rocket: in a single paragraph.

Mixed text with emoji :thumbs_up: and regular text.
"""
        
        input_stream = io.StringIO(input_text)
        output_stream = io.StringIO()
        
        stats = self.processor.process_markdown(
            input_stream,
            output_stream,
            line_width=None,
            add_lint_comment=True,
            remove_lint_comment=False
        )
        
        output_text = output_stream.getvalue()
        
        # Check that emoji shortcodes are preserved
        self.assertIn(":smile:", output_text)
        self.assertIn(":wink:", output_text)
        self.assertIn(":tada:", output_text)
        self.assertIn(":rocket:", output_text)
        self.assertIn(":thumbs_up:", output_text)
        
        self.assertEqual(stats.paragraphs_formatted, 3)
    
    def test_autolink_preservation(self):
        """Test that autolinks are preserved during processing."""
        input_text = """
This paragraph contains https://example.com autolink.

Multiple autolinks https://google.com and https://github.com in a paragraph.

Mixed with regular links: [explicit link](https://example.com) and autolink https://example.org.
"""
        
        input_stream = io.StringIO(input_text)
        output_stream = io.StringIO()
        
        stats = self.processor.process_markdown(
            input_stream,
            output_stream,
            line_width=None,
            add_lint_comment=True,
            remove_lint_comment=False
        )
        
        output_text = output_stream.getvalue()
        
        # Check that autolinks are preserved
        self.assertIn("https://example.com", output_text)
        self.assertIn("https://google.com", output_text)
        self.assertIn("https://github.com", output_text)
        self.assertIn("https://example.org", output_text)
        
        # Check that regular links are also preserved
        self.assertIn("[explicit link](https://example.com)", output_text)
        
        self.assertEqual(stats.paragraphs_formatted, 3)
    
    def test_combined_elements_preservation(self):
        """Test that all new elements work together correctly."""
        input_text = """
This paragraph has [links](https://example.com), ~~strikethrough~~, emoji :smile:, and autolinks https://github.com all in one.

<div class="example">
    <p>HTML block with <strong>bold</strong> and ~~strikethrough~~ text</p>
    <a href="https://example.com">HTML link</a>
</div>

- [x] Completed task with [link](https://example.com)
- [ ] Uncompleted task with ~~strikethrough~~
- [ ] Task with emoji :rocket:
- [x] Task with autolink https://github.com

Final paragraph with all elements combined.
"""
        
        input_stream = io.StringIO(input_text)
        output_stream = io.StringIO()
        
        stats = self.processor.process_markdown(
            input_stream,
            output_stream,
            line_width=None,
            add_lint_comment=True,
            remove_lint_comment=False
        )
        
        output_text = output_stream.getvalue()
        
        # Check that all elements are preserved
        self.assertIn("[links](https://example.com)", output_text)
        self.assertIn("~~strikethrough~~", output_text)
        self.assertIn(":smile:", output_text)
        self.assertIn("https://github.com", output_text)
        
        self.assertIn('<div class="example">', output_text)
        self.assertIn("<p>HTML block with", output_text)
        self.assertIn("</div>", output_text)
        
        self.assertIn("- [x] Completed task", output_text)
        self.assertIn("- [ ] Uncompleted task", output_text)
        
        self.assertEqual(stats.paragraphs_formatted, 2)
        self.assertGreaterEqual(stats.blocks_ignored, 2)  # HTML block and task list
    
    def test_hard_wrap_with_inline_elements(self):
        """Test hard wrapping with inline elements."""
        input_text = """
This is a very long paragraph with ~~strikethrough~~ text, emoji :smile: emoji, and autolinks https://example.com that should be wrapped at 40 characters.
"""
        
        input_stream = io.StringIO(input_text)
        output_stream = io.StringIO()
        
        stats = self.processor.process_markdown(
            input_stream,
            output_stream,
            line_width=40,
            add_lint_comment=False,
            remove_lint_comment=True
        )
        
        output_text = output_stream.getvalue()
        
        lines = output_text.strip().split('\n')
        
        # Check that lines are approximately wrapped at 40 characters
        # (allowing some flexibility for preserved inline elements)
        for line in lines:
            if line and not line.startswith('#'):  # Skip headers
                # Allow some extra length due to preserved elements
                self.assertLessEqual(len(line), 50)
        
        # Check that inline elements are preserved
        joined_text = '\n'.join(lines)
        self.assertIn("~~strikethrough~~", joined_text)
        self.assertIn(":smile:", joined_text)
        self.assertIn("https://example.com", joined_text)
        
        self.assertEqual(stats.paragraphs_formatted, 1)
        self.assertGreater(stats.wraps_added, 0)


if __name__ == "__main__":
    unittest.main()