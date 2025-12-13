#!/usr/bin/env python3

def is_repeated_pattern(num_str):
    """
    Check if a number string is a pattern repeated exactly twice.
    Examples: '55' (5 twice), '6464' (64 twice), '123123' (123 twice)
    
    The number must have even length and first half == second half.
    No leading zeros allowed.
    """
    # Must have even length to be repeated twice
    if len(num_str) % 2 != 0:
        return False
    
    # Check for leading zeros (invalid)
    if num_str[0] == '0':
        return False
    
    # Split in half and check if they're equal
    mid = len(num_str) // 2
    first_half = num_str[:mid]
    second_half = num_str[mid:]
    
    return first_half == second_half

def find_invalid_ids_in_range(start, end):
    """
    Find all invalid IDs (repeated patterns) in the range [start, end].
    Returns a list of invalid IDs.
    """
    invalid_ids = []
    
    for num in range(start, end + 1):
        num_str = str(num)
        if is_repeated_pattern(num_str):
            invalid_ids.append(num)
    
    return invalid_ids

def solve_puzzle(input_text):
    """
    Parse the input ranges and find all invalid IDs.
    """
    # Parse the ranges
    ranges_str = input_text.strip()
    range_parts = ranges_str.split(',')
    
    all_invalid_ids = []
    
    print(f"Processing {len(range_parts)} ranges...\n")
    
    for i, range_part in enumerate(range_parts, 1):
        range_part = range_part.strip()
        start_str, end_str = range_part.split('-')
        start = int(start_str)
        end = int(end_str)
        
        invalid_ids = find_invalid_ids_in_range(start, end)
        
        if invalid_ids:
            print(f"Range {i}: {start}-{end} has {len(invalid_ids)} invalid ID(s): {invalid_ids}")
        else:
            print(f"Range {i}: {start}-{end} has no invalid IDs")
        
        all_invalid_ids.extend(invalid_ids)
    
    return all_invalid_ids

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE")
    print("="*70)
    
    example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
    
    # Test the pattern checker first
    print("\nTesting pattern checker:")
    test_cases = [
        ('55', True),
        ('6464', True),
        ('123123', True),
        ('11', True),
        ('22', True),
        ('99', True),
        ('1010', True),
        ('1188511885', True),
        ('222222', True),
        ('446446', True),
        ('38593859', True),
        ('123', False),
        ('1234', False),
        ('0101', False),  # Leading zero
    ]
    
    for test, expected in test_cases:
        result = is_repeated_pattern(test)
        status = "✓" if result == expected else "✗"
        print(f"  {status} is_repeated_pattern('{test}') = {result} (expected {expected})")
    
    print("\nProcessing example ranges:")
    invalid_ids = solve_puzzle(example)
    
    total = sum(invalid_ids)
    print(f"\nTotal invalid IDs found: {len(invalid_ids)}")
    print(f"Sum of all invalid IDs: {total}")
    print(f"Expected: 1227775554")
    print(f"Match: {total == 1227775554}")
    print("="*70 + "\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_day02.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    invalid_ids = solve_puzzle(input_text)
    
    total = sum(invalid_ids)
    print(f"\n{'='*70}")
    print(f"ANSWER: Sum of all invalid IDs = {total}")
    print(f"Total invalid IDs found: {len(invalid_ids)}")
    print(f"{'='*70}")
