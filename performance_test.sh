#!/bin/bash

# Create output directory
mkdir -p tests/performance

# Generate test files of different sizes
echo "Generating test files..."
python tests/generate_large_file.py 0.1 tests/performance/test_0.1mb.md
python tests/generate_large_file.py 0.5 tests/performance/test_0.5mb.md
python tests/generate_large_file.py 1 tests/performance/test_1mb.md
python tests/generate_large_file.py 2 tests/performance/test_2mb.md
python tests/generate_large_file.py 5 tests/performance/test_5mb.md

# Function to run performance test
run_performance_test() {
    size=$1
    echo -e "\n=== Testing with ${size}MB file ==="
    
    # Soft-wrap test
    echo "Soft-wrap test:"
    time python src/soft_wrap_document.py tests/performance/test_${size}mb.md tests/performance/test_${size}mb_soft.md > /dev/null 2>&1
    
    # Hard-wrap test
    echo "Hard-wrap test:"
    time python src/hard_wrap_document.py tests/performance/test_${size}mb_soft.md tests/performance/test_${size}mb_hard.md --width 80 > /dev/null 2>&1
    
    # File sizes
    echo "File sizes:"
    ls -lh tests/performance/test_${size}mb.md tests/performance/test_${size}mb_soft.md tests/performance/test_${size}mb_hard.md
}

# Run tests
run_performance_test 0.1
run_performance_test 0.5
run_performance_test 1
run_performance_test 2
run_performance_test 5

echo -e "\nPerformance tests completed."