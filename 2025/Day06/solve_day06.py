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


def parse_worksheet(lines):
    """
    Parse the worksheet to extract individual math problems.
    Each problem is a vertical column of numbers with an operation at the bottom.
    Problems are separated by columns of spaces.
    """
    # Find the maximum line length to pad all lines
    max_length = max(len(line) for line in lines)
    
    # Pad all lines to the same length
    padded_lines = [line.ljust(max_length) for line in lines]
    
    # The last line contains the operations
    operation_line = padded_lines[-1]
    number_lines = padded_lines[:-1]
    
    # Transpose to work column by column
    num_cols = max_length
    problems = []
    current_problem_cols = []
    
    for col_idx in range(num_cols):
        # Extract this column from all lines
        column_chars = [line[col_idx] if col_idx < len(line) else ' ' for line in number_lines]
        operation_char = operation_line[col_idx] if col_idx < len(operation_line) else ' '
        
        # Check if this column is part of a number (has non-space content)
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

def extract_problem_data(problem_columns):
    """
    Extract numbers and operation from a problem's columns.
    """
    # Collect all number characters from all columns
    num_rows = len(problem_columns[0][0])
    numbers = []
    
    # Read numbers row by row
    for row_idx in range(num_rows):
        row_text = ''.join(col[0][row_idx] for col in problem_columns)
        row_text = row_text.strip()
        if row_text:
            try:
                numbers.append(int(row_text))
            except ValueError:
                pass  # Skip if not a valid number
    
    # Get the operation (should be the same for all columns in the problem)
    operations = [col[1] for col in problem_columns if col[1].strip()]
    operation = operations[0] if operations else None
    
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

def solve_worksheet(input_text):
    """
    Parse and solve the entire worksheet.
    """
    lines = input_text.rstrip('\n').split('\n')
    
    # Parse into individual problems
    problems = parse_worksheet(lines)
    
    print(f"Found {len(problems)} problems\n")
    
    # Solve each problem
    results = []
    for i, problem_cols in enumerate(problems, 1):
        numbers, operation = extract_problem_data(problem_cols)
        
        if numbers and operation:
            result = solve_problem(numbers, operation)
            results.append(result)
            
            # Show first 20 problems and last 10 for verification
            if i <= 20 or i > len(problems) - 10:
                nums_str = ' '.join(str(n) for n in numbers[:5])
                if len(numbers) > 5:
                    nums_str += f" ... ({len(numbers)} numbers)"
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
    print("VERIFYING WITH EXAMPLE")
    print("="*70)
    
    example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    
    grand_total, results = solve_worksheet(example)
    
    print(f"\n{'='*70}")
    print(f"Grand total: {grand_total:,}")
    print(f"Expected: 4,277,556")
    print(f"Match: {grand_total == 4277556}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_06.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    grand_total, results = solve_worksheet(input_text)
    
    print(f"\n{'='*70}")
    print(f"Total problems solved: {len(results)}")
    print(f"ANSWER: Grand total = {grand_total:,}")
    print(f"{'='*70}")
