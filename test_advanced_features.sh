#!/bin/bash

# Create output directory
mkdir -p tests/output

echo "======================================"
echo "Testing Advanced Markdown Elements"
echo "======================================"

# Run soft-wrap tool on the advanced elements test document
echo -e "\n1. Running soft-wrap tool on advanced elements..."
python src/soft_wrap_document.py tests/test_advanced_elements.md tests/output/advanced_soft_wrapped.md
echo "Soft-wrapped output saved to tests/output/advanced_soft_wrapped.md"

# Run hard-wrap tool on the soft-wrapped output with different widths
echo -e "\n2. Running hard-wrap tool with width=80 on advanced elements..."
python src/hard_wrap_document.py tests/output/advanced_soft_wrapped.md tests/output/advanced_hard_wrapped_80.md --width 80
echo "Hard-wrapped output (width=80) saved to tests/output/advanced_hard_wrapped_80.md"

echo -e "\n3. Running hard-wrap tool with width=40 on advanced elements..."
python src/hard_wrap_document.py tests/output/advanced_soft_wrapped.md tests/output/advanced_hard_wrapped_40.md --width 40
echo "Hard-wrapped output (width=40) saved to tests/output/advanced_hard_wrapped_40.md"

# Test parallel processing
echo -e "\n4. Running soft-wrap tool with parallel processing..."
python src/soft_wrap_document.py tests/test_advanced_elements.md tests/output/advanced_soft_wrapped_parallel.md --parallel
echo "Soft-wrapped output (parallel) saved to tests/output/advanced_soft_wrapped_parallel.md"

echo -e "\n5. Running hard-wrap tool with parallel processing..."
python src/hard_wrap_document.py tests/output/advanced_soft_wrapped.md tests/output/advanced_hard_wrapped_parallel.md --width 80 --parallel
echo "Hard-wrapped output (parallel) saved to tests/output/advanced_hard_wrapped_parallel.md"

# Compare the parallel and sequential outputs
echo -e "\n6. Comparing parallel and sequential outputs..."
diff tests/output/advanced_soft_wrapped.md tests/output/advanced_soft_wrapped_parallel.md
if [ $? -eq 0 ]; then
    echo "✓ Soft-wrap parallel and sequential outputs match."
else
    echo "✗ Soft-wrap parallel and sequential outputs differ."
fi

diff tests/output/advanced_hard_wrapped_80.md tests/output/advanced_hard_wrapped_parallel.md
if [ $? -eq 0 ]; then
    echo "✓ Hard-wrap parallel and sequential outputs match."
else
    echo "✗ Hard-wrap parallel and sequential outputs differ."
fi

# Verify specific elements are preserved
echo -e "\n7. Verifying element preservation..."

echo "Checking task lists:"
if grep -q "\- \[ \]" tests/output/advanced_soft_wrapped.md && grep -q "\- \[x\]" tests/output/advanced_soft_wrapped.md; then
    echo "✓ Task lists preserved"
else
    echo "✗ Task lists not preserved"
fi

echo "Checking HTML blocks:"
if grep -q "<div class=&quot;container&quot;>" tests/output/advanced_soft_wrapped.md; then
    echo "✓ HTML blocks preserved"
else
    echo "✗ HTML blocks not preserved"
fi

echo "Checking strikethrough:"
if grep -q "~~" tests/output/advanced_soft_wrapped.md; then
    echo "✓ Strikethrough preserved"
else
    echo "✗ Strikethrough not preserved"
fi

echo "Checking emoji shortcodes:"
if grep -q ":smile:" tests/output/advanced_soft_wrapped.md; then
    echo "✓ Emoji shortcodes preserved"
else
    echo "✗ Emoji shortcodes not preserved"
fi

echo "Checking autolinks:"
if grep -q "https://example.com" tests/output/advanced_soft_wrapped.md; then
    echo "✓ Autolinks preserved"
else
    echo "✗ Autolinks not preserved"
fi

echo -e "\n8. Displaying file sizes:"
ls -lh tests/test_advanced_elements.md tests/output/advanced_*.md

# Display statistics
echo -e "\n9. Processing statistics:"
echo "Soft-wrap statistics:"
echo "  Paragraphs formatted: $(grep -o 'Paragraphs formatted: [0-9]*' tests/output/advanced_soft_wrapped.md.debug 2>/dev/null || echo 'N/A')"
echo "  Blocks ignored: $(grep -o 'Blocks ignored: [0-9]*' tests/output/advanced_soft_wrapped.md.debug 2>/dev/null || echo 'N/A')"

echo -e "\n10. Sample output display:"
echo "Original document (first 20 lines):"
head -n 20 tests/test_advanced_elements.md

echo -e "\nSoft-wrapped document (first 20 lines):"
head -n 20 tests/output/advanced_soft_wrapped.md

echo -e "\nHard-wrapped document with width=40 (first 20 lines):"
head -n 20 tests/output/advanced_hard_wrapped_40.md

echo -e "\n======================================"
echo "Advanced Features Tests Completed"
echo "======================================"