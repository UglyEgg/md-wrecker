#!/bin/bash

# Run unit tests
echo "Running unit tests..."
python -m unittest discover tests

# Create output directory
mkdir -p tests/output

# Run soft-wrap tool on test document
echo -e "\nRunning soft-wrap tool..."
python src/soft_wrap_document.py tests/test_document.md tests/output/soft_wrapped.md
echo "Soft-wrapped output saved to tests/output/soft_wrapped.md"

# Run hard-wrap tool on the soft-wrapped output with different widths
echo -e "\nRunning hard-wrap tool with width=80..."
python src/hard_wrap_document.py tests/output/soft_wrapped.md tests/output/hard_wrapped_80.md --width 80
echo "Hard-wrapped output (width=80) saved to tests/output/hard_wrapped_80.md"

echo -e "\nRunning hard-wrap tool with width=40..."
python src/hard_wrap_document.py tests/output/soft_wrapped.md tests/output/hard_wrapped_40.md --width 40
echo "Hard-wrapped output (width=40) saved to tests/output/hard_wrapped_40.md"

# Display file sizes
echo -e "\nFile sizes:"
ls -l tests/test_document.md tests/output/soft_wrapped.md tests/output/hard_wrapped_*.md

# Display file contents
echo -e "\nOriginal document (first 10 lines):"
head -n 10 tests/test_document.md

echo -e "\nSoft-wrapped document (first 10 lines):"
head -n 10 tests/output/soft_wrapped.md

echo -e "\nHard-wrapped document with width=80 (first 10 lines):"
head -n 10 tests/output/hard_wrapped_80.md

echo -e "\nHard-wrapped document with width=40 (first 10 lines):"
head -n 10 tests/output/hard_wrapped_40.md

echo -e "\nTests completed."