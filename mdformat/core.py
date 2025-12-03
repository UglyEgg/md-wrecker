# SPDX-License-Identifier: GPL-3.0-or-later
"""
Core functionality for Markdown paragraph formatting.

This module provides the core functionality for parsing and processing Markdown content,
including identifying and preserving special Markdown elements, and formatting paragraphs.

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

import re
import multiprocessing
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generator, Iterator, List, Optional, TextIO, Tuple, Dict, Any


class BlockType(Enum):
    """Enum representing different types of Markdown blocks."""
    PARAGRAPH = auto()
    CODE_BLOCK = auto()
    LIST = auto()
    TABLE = auto()
    BLOCKQUOTE = auto()
    HEADING = auto()
    FRONTMATTER = auto()
    JSON_FRONTMATTER = auto()
    DEFINITION_LIST = auto()
    HORIZONTAL_RULE = auto()
    FOOTNOTE = auto()
    HTML_BLOCK = auto()
    TASK_LIST = auto()
    EMPTY = auto()


@dataclass
class Statistics:
    """Statistics about the processing of a Markdown document."""
    wraps_removed: int = 0
    wraps_added: int = 0
    paragraphs_formatted: int = 0
    blocks_ignored: int = 0


class MarkdownProcessor:
    """
    Core class for processing Markdown content.
    
    This class handles the parsing and processing of Markdown content,
    including identifying and preserving special Markdown elements,
    and formatting paragraphs.
    """
    
    # Regular expressions for identifying special Markdown elements
    CODE_BLOCK_PATTERN = re.compile(r'^```')
    LIST_PATTERN = re.compile(r'^(\s*)([-*+]|\d+\.)\s')
    TABLE_PATTERN = re.compile(r'^\|.*\|$')
    TABLE_DELIMITER_PATTERN = re.compile(r'^\|(\s*:?-+:?\s*\|)+$')
    BLOCKQUOTE_PATTERN = re.compile(r'^\s*>')
    HEADING_PATTERN = re.compile(r'^#{1,6}\s')
    FRONTMATTER_PATTERN = re.compile(r'^(---|\+\+\+)$')
    JSON_FRONTMATTER_PATTERN = re.compile(r'^;;;$')
    DEFINITION_LIST_PATTERN = re.compile(r'^:\s')
    HORIZONTAL_RULE_PATTERN = re.compile(r'^(\*\*\*|---|\*\*\*\*\*|_____|---)$')
    FOOTNOTE_PATTERN = re.compile(r'^\[\^[a-zA-Z0-9_-]+\]:')
    MARKDOWNLINT_DISABLE_PATTERN = re.compile(r'^<!--\s*markdownlint-disable\s*-->')
    
    # New patterns for enhanced elements
    TASK_LIST_PATTERN = re.compile(r'^(\s*)(-|\*|\+|\d+\.)\s+\[([ x])\]\s+')
    HTML_BLOCK_START_PATTERN = re.compile(r'^<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(\/?)>')
    HTML_BLOCK_END_PATTERN = re.compile(r'^<\/([a-zA-Z][a-zA-Z0-9]*)\s*>')
    HTML_COMMENT_PATTERN = re.compile(r'^<!--.*-->$')
    
    # Regular expressions for inline elements that should be preserved
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    AUTOLINK_PATTERN = re.compile(r'(?<!\[)(https?:\/\/[^\s<>"{}|\\^`\[\]]+)')
    INLINE_MATH_PATTERN = re.compile(r'\$([^$]+)\$')
    STRIKETHROUGH_PATTERN = re.compile(r'~~(.+?)~~')
    EMOJI_SHORTCODE_PATTERN = re.compile(r':([a-zA-Z0-9_+-]+):')
    
    def __init__(self):
        """Initialize the MarkdownProcessor."""
        self.stats = Statistics()
        self.in_html_block = False
        self.html_block_tag = None
    
    def _identify_block_type(self, line: str, in_code_block: bool, in_frontmatter: bool, in_json_frontmatter: bool) -> Tuple[BlockType, bool, bool, bool]:
        """
        Identify the type of Markdown block for a given line.
        
        Args:
            line: The line to identify.
            in_code_block: Whether we're currently in a code block.
            in_frontmatter: Whether we're currently in frontmatter.
            in_json_frontmatter: Whether we're currently in JSON frontmatter.
            
        Returns:
            A tuple containing the block type, whether we're in a code block,
            whether we're in frontmatter, and whether we're in JSON frontmatter.
        """
        # Check if we're in a code block
        if self.CODE_BLOCK_PATTERN.match(line):
            return BlockType.CODE_BLOCK, not in_code_block, in_frontmatter, in_json_frontmatter
        
        if in_code_block:
            return BlockType.CODE_BLOCK, in_code_block, in_frontmatter, in_json_frontmatter
        
        # Check if we're in frontmatter
        if self.FRONTMATTER_PATTERN.match(line):
            return BlockType.FRONTMATTER, in_code_block, not in_frontmatter, in_json_frontmatter
        
        if in_frontmatter:
            return BlockType.FRONTMATTER, in_code_block, in_frontmatter, in_json_frontmatter
        
        # Check if we're in JSON frontmatter
        if self.JSON_FRONTMATTER_PATTERN.match(line):
            return BlockType.JSON_FRONTMATTER, in_code_block, in_frontmatter, not in_json_frontmatter
        
        if in_json_frontmatter:
            return BlockType.JSON_FRONTMATTER, in_code_block, in_frontmatter, in_json_frontmatter
        
        # Check for HTML blocks
        if self.HTML_BLOCK_START_PATTERN.match(line) or self.HTML_BLOCK_END_PATTERN.match(line) or self.HTML_COMMENT_PATTERN.match(line):
            self._update_html_block_state(line)
            return BlockType.HTML_BLOCK, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.in_html_block:
            return BlockType.HTML_BLOCK, in_code_block, in_frontmatter, in_json_frontmatter
        
        # Check for other block types
        if not line.strip():
            return BlockType.EMPTY, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.HEADING_PATTERN.match(line):
            return BlockType.HEADING, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.TASK_LIST_PATTERN.match(line):
            return BlockType.TASK_LIST, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.LIST_PATTERN.match(line):
            return BlockType.LIST, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.TABLE_PATTERN.match(line) or self.TABLE_DELIMITER_PATTERN.match(line):
            return BlockType.TABLE, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.BLOCKQUOTE_PATTERN.match(line):
            return BlockType.BLOCKQUOTE, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.DEFINITION_LIST_PATTERN.match(line):
            return BlockType.DEFINITION_LIST, in_code_block, in_frontmatter, in_json_frontmatter
        
        # Check for horizontal rule (not at the beginning of the document where it might be confused with frontmatter)
        if self.HORIZONTAL_RULE_PATTERN.match(line) and not self.FRONTMATTER_PATTERN.match(line):
            return BlockType.HORIZONTAL_RULE, in_code_block, in_frontmatter, in_json_frontmatter
        
        if self.FOOTNOTE_PATTERN.match(line):
            return BlockType.FOOTNOTE, in_code_block, in_frontmatter, in_json_frontmatter
        
        # Default to paragraph
        return BlockType.PARAGRAPH, in_code_block, in_frontmatter, in_json_frontmatter
    
    def _update_html_block_state(self, line: str) -> None:
        """Update the HTML block state based on the current line."""
        # Check for self-closing tag
        if self.HTML_BLOCK_START_PATTERN.match(line):
            match = self.HTML_BLOCK_START_PATTERN.match(line)
            if match and match.group(2) == '/':  # Self-closing tag
                self.in_html_block = False
                self.html_block_tag = None
                return
        
        # Check for opening tag
        if self.HTML_BLOCK_START_PATTERN.match(line):
            match = self.HTML_BLOCK_START_PATTERN.match(line)
            if match and not match.group(2):  # Not self-closing
                tag = match.group(1).lower()
                # Check if this is a block-level tag
                block_tags = {'address', 'article', 'aside', 'base', 'basefont', 'blockquote', 
                            'body', 'caption', 'center', 'col', 'colgroup', 'dd', 'details',
                            'dialog', 'dir', 'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure',
                            'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5',
                            'h6', 'head', 'header', 'hr', 'html', 'iframe', 'legend', 'li',
                            'link', 'main', 'menu', 'menuitem', 'meta', 'nav', 'noframes',
                            'ol', 'optgroup', 'option', 'p', 'param', 'section', 'source',
                            'summary', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead',
                            'title', 'tr', 'track', 'ul'}
                if tag in block_tags:
                    self.in_html_block = True
                    self.html_block_tag = tag
                    return
        
        # Check for closing tag
        if self.HTML_BLOCK_END_PATTERN.match(line):
            match = self.HTML_BLOCK_END_PATTERN.match(line)
            if match:
                tag = match.group(1).lower()
                if tag == self.html_block_tag:
                    self.in_html_block = False
                    self.html_block_tag = None
    
    def _group_lines_by_block(self, lines: Iterator[str]) -> Generator[Tuple[BlockType, List[str]], None, None]:
        """
        Group lines by their block type.
        
        Args:
            lines: An iterator of lines from the Markdown document.
            
        Yields:
            Tuples containing the block type and a list of lines in that block.
        """
        current_block_type = None
        current_block_lines = []
        in_code_block = False
        in_frontmatter = False
        in_json_frontmatter = False
        
        for line in lines:
            line = line.rstrip('\n')
            block_type, in_code_block, in_frontmatter, in_json_frontmatter = self._identify_block_type(
                line, in_code_block, in_frontmatter, in_json_frontmatter
            )
            
            # If we're starting a new block type, yield the current block and start a new one
            if current_block_type is not None and block_type != current_block_type:
                yield current_block_type, current_block_lines
                current_block_lines = []
            
            current_block_type = block_type
            current_block_lines.append(line)
        
        # Yield the last block
        if current_block_lines:
            yield current_block_type, current_block_lines
    
    def _preserve_inline_elements(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Preserve inline elements like links, math, and other special elements by replacing them with placeholders.
        
        Args:
            text: The text to process.
            
        Returns:
            A tuple containing the processed text and a dictionary mapping placeholders to original content.
        """
        preserved = {}
        
        # Preserve strikethrough text
        def replace_strikethrough(match):
            placeholder = f"__STRIKETHROUGH_{len(preserved)}__"
            preserved[placeholder] = match.group(0)
            return placeholder
        
        text = self.STRIKETHROUGH_PATTERN.sub(replace_strikethrough, text)
        
        # Preserve emoji shortcodes
        def replace_emoji(match):
            placeholder = f"__EMOJI_{len(preserved)}__"
            preserved[placeholder] = match.group(0)
            return placeholder
        
        text = self.EMOJI_SHORTCODE_PATTERN.sub(replace_emoji, text)
        
        # Preserve explicit links first (to avoid conflicts with autolinks)
        def replace_link(match):
            placeholder = f"__LINK_{len(preserved)}__"
            preserved[placeholder] = match.group(0)
            return placeholder
        
        text = self.LINK_PATTERN.sub(replace_link, text)
        
        # Preserve autolinks
        def replace_autolink(match):
            placeholder = f"__AUTOLINK_{len(preserved)}__"
            preserved[placeholder] = match.group(0)
            return placeholder
        
        text = self.AUTOLINK_PATTERN.sub(replace_autolink, text)
        
        # Preserve inline math
        def replace_math(match):
            placeholder = f"__MATH_{len(preserved)}__"
            preserved[placeholder] = match.group(0)
            return placeholder
        
        text = self.INLINE_MATH_PATTERN.sub(replace_math, text)
        
        return text, preserved
    
    def _restore_inline_elements(self, text: str, preserved: Dict[str, str]) -> str:
        """
        Restore inline elements from their placeholders.
        
        Args:
            text: The text with placeholders.
            preserved: A dictionary mapping placeholders to original content.
            
        Returns:
            The text with original content restored.
        """
        for placeholder, original in preserved.items():
            text = text.replace(placeholder, original)
        
        return text
    
    def _process_paragraph(self, lines: List[str], line_width: Optional[int] = None) -> List[str]:
        """
        Process a paragraph block.
        
        Args:
            lines: The lines in the paragraph block.
            line_width: The maximum line width for hard-wrapping, or None for soft-wrapping.
            
        Returns:
            The processed lines.
        """
        # For soft-wrapping, join all lines into a single line
        if line_width is None:
            # Count the number of wraps removed
            self.stats.wraps_removed += len(lines) - 1
            self.stats.paragraphs_formatted += 1
            
            # Join lines, preserving inline elements
            text = ' '.join(line.strip() for line in lines)
            text, preserved = self._preserve_inline_elements(text)
            text = self._restore_inline_elements(text, preserved)
            
            return [text]
        
        # For hard-wrapping, split the paragraph into lines of the specified width
        text = ' '.join(line.strip() for line in lines)
        
        # Preserve inline elements before wrapping
        text, preserved = self._preserve_inline_elements(text)
        
        words = text.split()
        result_lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            # If adding this word would exceed the line width, start a new line
            if current_length + len(word) + (1 if current_line else 0) > line_width and current_line:
                result_lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                # Add the word to the current line
                if current_line:
                    current_length += 1 + len(word)
                else:
                    current_length = len(word)
                current_line.append(word)
        
        # Add the last line
        if current_line:
            result_lines.append(' '.join(current_line))
        
        # Restore inline elements after wrapping
        result_lines = [self._restore_inline_elements(line, preserved) for line in result_lines]
        
        # Count the number of wraps added
        self.stats.wraps_added += len(result_lines) - 1
        self.stats.paragraphs_formatted += 1
        
        return result_lines
    
    def process_markdown(self, input_stream: TextIO, output_stream: TextIO, line_width: Optional[int] = None,
                         add_lint_comment: bool = False, remove_lint_comment: bool = False,
                         use_parallel: bool = False, chunk_size: int = 1000) -> Statistics:
        """
        Process a Markdown document.
        
        Args:
            input_stream: The input stream to read from.
            output_stream: The output stream to write to.
            line_width: The maximum line width for hard-wrapping, or None for soft-wrapping.
            add_lint_comment: Whether to add a markdownlint-disable comment at the top of the file.
            remove_lint_comment: Whether to remove any existing markdownlint-disable comment from the top of the file.
            use_parallel: Whether to use parallel processing for large files.
            chunk_size: The number of lines to process in each chunk when using parallel processing.
            
        Returns:
            Statistics about the processing.
        """
        # Reset statistics
        self.stats = Statistics()
        
        # Read all lines from the input stream
        lines = input_stream.readlines()
        
        # Check for markdownlint-disable comment at the top of the file
        if lines and remove_lint_comment and self.MARKDOWNLINT_DISABLE_PATTERN.match(lines[0].strip()):
            # Skip the line if we're removing the lint comment
            lines = lines[1:]
        
        # Add markdownlint-disable comment if requested
        if add_lint_comment:
            output_stream.write("<!-- markdownlint-disable -->\n")
        
        # Reset HTML block state
        self.in_html_block = False
        self.html_block_tag = None
        
        if use_parallel and len(lines) > chunk_size:
            # Process in parallel
            return self._process_markdown_parallel(lines, output_stream, line_width, chunk_size)
        else:
            # Process sequentially
            return self._process_markdown_sequential(lines, output_stream, line_width)
    
    def _process_markdown_sequential(self, lines: List[str], output_stream: TextIO, line_width: Optional[int] = None) -> Statistics:
        """
        Process a Markdown document sequentially.
        
        Args:
            lines: The lines from the Markdown document.
            output_stream: The output stream to write to.
            line_width: The maximum line width for hard-wrapping, or None for soft-wrapping.
            
        Returns:
            Statistics about the processing.
        """
        # Process the document by blocks
        for block_type, block_lines in self._group_lines_by_block(iter(lines)):
            if block_type == BlockType.PARAGRAPH:
                # Process paragraphs
                processed_lines = self._process_paragraph(block_lines, line_width)
                output_stream.write('\n'.join(processed_lines) + '\n')
            else:
                # Preserve other block types
                if block_type != BlockType.EMPTY:
                    self.stats.blocks_ignored += 1
                output_stream.write('\n'.join(block_lines) + '\n')
        
        return self.stats
    
    def _process_markdown_parallel(self, lines: List[str], output_stream: TextIO, line_width: Optional[int] = None,
                                  chunk_size: int = 1000) -> Statistics:
        """
        Process a Markdown document in parallel.
        
        Args:
            lines: The lines from the Markdown document.
            output_stream: The output stream to write to.
            line_width: The maximum line width for hard-wrapping, or None for soft-wrapping.
            chunk_size: The number of lines to process in each chunk.
            
        Returns:
            Statistics about the processing.
        """
        # This is a simplified parallel implementation that doesn't actually process in parallel
        # because proper parallel processing would require more complex block boundary handling
        # For now, we'll just use the sequential implementation
        stats = self._process_markdown_sequential(lines, output_stream, line_width)
        
        # In a real implementation, we would:
        # 1. Split the document into chunks
        # 2. Process each chunk in parallel
        # 3. Combine the results
        # But this requires careful handling of block boundaries
        
        return stats