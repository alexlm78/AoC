#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 6: Trash Compactor

Problem Description:
-------------------
Solve cephalopod math problems arranged in a unique vertical format. Numbers
are stacked vertically in columns with operations at the bottom. Part 2 reveals
that cephalopod math is read right-to-left, with each column representing one
complete number.

Key Concepts:
------------
- 2D grid parsing (transpose columns to rows)
- Reading direction matters (left-to-right vs right-to-left)
- Column-based number representation
- Each column = one digit position (Part 1) vs one complete number (Part 2)

Input Format:
------------
Multiple rows of numbers and operations:
  123 328  51 64 
   45 64  387 23 
    6 98  215 314
  *   +   *   +  

Approach:
---------
Part 1: Read numbers row-by-row, apply operations
Part 2: Read each column as a complete number (top-to-bottom digits),
        process columns right-to-left

Complexity:
----------
- Time: O(rows × cols) for parsing
- Space: O(problems) to store results

Result: Part 1: 4.7 trillion, Part 2: 11.6 trillion (2.48× larger!)
"""


def parse_worksheet_rtl(lines):
    """
    Parse the worksheet reading right-to-left.
    Each digit occupies its own column.
    Numbers are formed by reading columns right-to-left,
    with digits reading top-to-bottom within each column.
    """
    # Find the maximum line length to pad all lines
    max_length = max(len(line) for line in lines)
    
    # Pad all lines to the same length
    padded_lines = [line.ljust(max_length) for line in lines]
    
    # The last line contains the operations
    operation_line = padded_lines[-1]
    number_lines = padded_lines[:-1]
    
    # Work through columns to identify problems
    num_cols = max_length
    problems = []
    current_problem_cols = []
    
    for col_idx in range(num_cols):
        # Extract this column from all lines
        column_chars = [line[col_idx] if col_idx < len(line) else ' ' for line in number_lines]
        operation_char = operation_line[col_idx] if col_idx < len(operation_line) else ' '
        
        # Check if this column is part of a problem (has non-space content)
        has_content = any(char.strip() for char in column_chars) or operation_char.strip()
        
        if has_content:
            current_problem_cols.append((column_chars, operation_char))
        else:
            # This is a separator column (all spaces)
            if current_problem_cols:
                # We've finished collecting a problem
                problems.append(current_problem_cols)
                current_problem_cols = []
    
    # Don't forget the last problem if there is one
    if current_problem_cols:
        problems.append(current_problem_cols)
    
    return problems

def extract_problem_data_rtl(problem_columns):
    """
    Extract numbers and operation reading RIGHT-TO-LEFT.
    Each column represents ONE COMPLETE NUMBER.
    Within each column, digits are read top-to-bottom.
    """
    # Get the operation (should be consistent across the problem)
    operations = [col[1] for col in problem_columns if col[1].strip()]
    operation = operations[0] if operations else None
    
    # Read numbers right-to-left
    # Each column is ONE number, with digits stacked vertically
    numbers = []
    
    # Process columns from RIGHT to LEFT
    for col_idx in range(len(problem_columns) - 1, -1, -1):
        column_chars = problem_columns[col_idx][0]
        
        # Read digits from top to bottom in this column to form one number
        digit_str = ''.join(char if char.strip() and char.isdigit() else '' for char in column_chars)
        
        if digit_str:
            # This column represents one complete number
            numbers.append(int(digit_str))
    
    return numbers, operation

def solve_problem(numbers, operation):
    """
    Solve a single math problem by applying the operation to all numbers.
    """
    if not numbers or not operation:
        return 0
    
    result = numbers[0]
    for num in numbers[1:]:
        if operation == '+':
            result += num
        elif operation == '*':
            result *= num
    
    return result

def solve_worksheet_rtl(input_text):
    """
    Parse and solve the entire worksheet using right-to-left reading.
    """
    lines = input_text.rstrip('\n').split('\n')
    
    # Parse into individual problems
    problems = parse_worksheet_rtl(lines)
    
    print(f"Found {len(problems)} problems\n")
    
    # Solve each problem
    results = []
    for i, problem_cols in enumerate(problems, 1):
        numbers, operation = extract_problem_data_rtl(problem_cols)
        
        if numbers and operation:
            result = solve_problem(numbers, operation)
            results.append(result)
            
            # Show first 20 problems and last 10 for verification
            if i <= 20 or i > len(problems) - 10:
                nums_str = ' '.join(str(n) for n in numbers)
                if len(nums_str) > 50:
                    nums_str = nums_str[:50] + "..."
                print(f"Problem {i:3d}: {nums_str} [{operation}] = {result:,}")
    
    if len(problems) > 30:
        print(f"\n... (showing first 20 and last 10 problems) ...\n")
    
    # Calculate grand total
    grand_total = sum(results)
    
    return grand_total, results

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE (PART 2 - RIGHT-TO-LEFT)")
    print("="*70)
    
    example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    
    print("\nOriginal worksheet:")
    print(example)
    
    print("\nExpected problems (reading right-to-left):")
    print("  Problem 1 (rightmost): 4 + 431 + 623 = 1058")
    print("  Problem 2: 175 * 581 * 32 = 3,253,600")
    print("  Problem 3: 8 + 248 + 369 = 625")
    print("  Problem 4 (leftmost): 356 * 24 * 1 = 8,544")
    print("  Expected grand total: 3,263,827")
    
    grand_total, results = solve_worksheet_rtl(example)
    
    print(f"\n{'='*70}")
    print(f"Grand total: {grand_total:,}")
    print(f"Expected: 3,263,827")
    print(f"Match: {grand_total == 3263827}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_06.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE (PART 2 - RIGHT-TO-LEFT)")
    print("="*70 + "\n")
    
    grand_total, results = solve_worksheet_rtl(input_text)
    
    print(f"\n{'='*70}")
    print(f"Total problems solved: {len(results)}")
    print(f"ANSWER: Grand total = {grand_total:,}")
    print(f"{'='*70}")
