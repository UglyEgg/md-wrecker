# SPDX-License-Identifier: GPL-3.0-or-later
"""
Command-line tool for soft-wrapping Markdown documents.

This tool removes line breaks within paragraphs while preserving paragraph breaks
and special Markdown elements.

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

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Optional, TextIO

from mdformat.core import MarkdownProcessor


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Soft-wrap Markdown documents by removing line breaks within paragraphs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="Input file path (use '-' or omit for stdin)"
    )
    
    parser.add_argument(
        "output",
        nargs="?",
        default="-",
        help="Output file path (use '-' or omit for stdout)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print output to stdout without saving"
    )
    
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create a backup of the original file"
    )
    
    parser.add_argument(
        "--no-lint-comment",
        action="store_true",
        help="Don't add markdownlint-disable comment at the top of the file"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Use parallel processing for large files"
    )
    
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Number of lines to process in each chunk when using parallel processing"
    )
    
    return parser.parse_args()


def get_input_stream(input_path: str) -> TextIO:
    """
    Get the input stream based on the input path.
    
    Args:
        input_path: The input path, or '-' for stdin.
        
    Returns:
        The input stream.
    """
    if input_path == "-":
        return sys.stdin
    else:
        return open(input_path, "r", encoding="utf-8")


def get_output_stream(output_path: str, dry_run: bool) -> TextIO:
    """
    Get the output stream based on the output path and dry-run flag.
    
    Args:
        output_path: The output path, or '-' for stdout.
        dry_run: Whether to print output to stdout without saving.
        
    Returns:
        The output stream.
    """
    if dry_run or output_path == "-":
        return sys.stdout
    else:
        return open(output_path, "w", encoding="utf-8")


def create_backup(file_path: str) -> None:
    """
    Create a backup of a file.
    
    Args:
        file_path: The path to the file to back up.
    """
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Backup created at {backup_path}", file=sys.stderr)


def main() -> None:
    """Main entry point for the soft-wrap tool."""
    args = parse_args()
    
    # Create a backup if requested and the input is a file
    if args.backup and args.input != "-" and os.path.isfile(args.input):
        create_backup(args.input)
    
    # Get input and output streams
    input_stream: Optional[TextIO] = None
    output_stream: Optional[TextIO] = None
    
    try:
        input_stream = get_input_stream(args.input)
        output_stream = get_output_stream(args.output, args.dry_run)
        
        # Process the Markdown document
        processor = MarkdownProcessor()
        stats = processor.process_markdown(
            input_stream,
            output_stream,
            line_width=None,  # Soft-wrapping
            add_lint_comment=not args.no_lint_comment,
            remove_lint_comment=False,
            use_parallel=args.parallel,
            chunk_size=args.chunk_size
        )
        
        # Print statistics to stderr
        print(f"Soft-wrap complete:", file=sys.stderr)
        print(f"  Wraps removed: {stats.wraps_removed}", file=sys.stderr)
        print(f"  Paragraphs formatted: {stats.paragraphs_formatted}", file=sys.stderr)
        print(f"  Blocks ignored: {stats.blocks_ignored}", file=sys.stderr)
        if args.parallel:
            print(f"  Parallel processing: enabled (chunk size: {args.chunk_size})", file=sys.stderr)
        
    finally:
        # Close the streams if they're not stdin/stdout
        if input_stream and input_stream is not sys.stdin:
            input_stream.close()
        
        if output_stream and output_stream is not sys.stdout:
            output_stream.close()


if __name__ == "__main__":
    main()