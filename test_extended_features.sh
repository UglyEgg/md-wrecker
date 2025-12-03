#!/bin/bash

# Create output directory
mkdir -p tests/output

# Run soft-wrap tool on the extended elements test document
echo -e "\nRunning soft-wrap tool on extended elements..."
python src/soft_wrap_document.py tests/test_extended_elements.md tests/output/extended_soft_wrapped.md
echo "Soft-wrapped output saved to tests/output/extended_soft_wrapped.md"

# Run hard-wrap tool on the soft-wrapped output with different widths
echo -e "\nRunning hard-wrap tool with width=80 on extended elements..."
python src/hard_wrap_document.py tests/output/extended_soft_wrapped.md tests/output/extended_hard_wrapped_80.md --width 80
echo "Hard-wrapped output (width=80) saved to tests/output/extended_hard_wrapped_80.md"

echo -e "\nRunning hard-wrap tool with width=40 on extended elements..."
python src/hard_wrap_document.py tests/output/extended_soft_wrapped.md tests/output/extended_hard_wrapped_40.md --width 40
echo "Hard-wrapped output (width=40) saved to tests/output/extended_hard_wrapped_40.md"

# Test parallel processing
echo -e "\nRunning soft-wrap tool with parallel processing..."
python src/soft_wrap_document.py tests/test_extended_elements.md tests/output/extended_soft_wrapped_parallel.md --parallel
echo "Soft-wrapped output (parallel) saved to tests/output/extended_soft_wrapped_parallel.md"

echo -e "\nRunning hard-wrap tool with parallel processing..."
python src/hard_wrap_document.py tests/output/extended_soft_wrapped.md tests/output/extended_hard_wrapped_parallel.md --width 80 --parallel
echo "Hard-wrapped output (parallel) saved to tests/output/extended_hard_wrapped_parallel.md"

# Compare the parallel and sequential outputs
echo -e "\nComparing parallel and sequential outputs..."
diff tests/output/extended_soft_wrapped.md tests/output/extended_soft_wrapped_parallel.md
if [ $? -eq 0 ]; then
    echo "Soft-wrap parallel and sequential outputs match."
else
    echo "Soft-wrap parallel and sequential outputs differ."
fi

diff tests/output/extended_hard_wrapped_80.md tests/output/extended_hard_wrapped_parallel.md
if [ $? -eq 0 ]; then
    echo "Hard-wrap parallel and sequential outputs match."
else
    echo "Hard-wrap parallel and sequential outputs differ."
fi

# Display file contents
echo -e "\nOriginal document:"
cat tests/test_extended_elements.md

echo -e "\nSoft-wrapped document:"
cat tests/output/extended_soft_wrapped.md

echo -e "\nHard-wrapped document with width=40:"
cat tests/output/extended_hard_wrapped_40.md

echo -e "\nTests completed."