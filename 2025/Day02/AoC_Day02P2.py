#!/usr/bin/env python3

def is_repeated_pattern_part2(num_str):
    """
    Check if a number string is a pattern repeated at least twice.
    Examples: 
    - '111' = "1" three times
    - '12341234' = "1234" two times
    - '123123123' = "123" three times
    - '1212121212' = "12" five times
    
    The pattern can be of any length that divides the total length evenly,
    and must repeat at least twice (so pattern length < total length).
    No leading zeros allowed.
    """
    # Check for leading zeros (invalid)
    if num_str[0] == '0':
        return False
    
    length = len(num_str)
    
    # Try all possible pattern lengths from 1 to length//2
    # (pattern must repeat at least twice, so max length is half)
    for pattern_len in range(1, length // 2 + 1):
        # Pattern length must divide the total length evenly
        if length % pattern_len == 0:
            pattern = num_str[:pattern_len]
            repetitions = length // pattern_len
            
            # Check if the whole string is this pattern repeated
            if pattern * repetitions == num_str:
                return True
    
    return False

def find_invalid_ids_in_range(start, end):
    """
    Find all invalid IDs (repeated patterns) in the range [start, end].
    Returns a list of invalid IDs.
    """
    invalid_ids = []
    
    for num in range(start, end + 1):
        num_str = str(num)
        if is_repeated_pattern_part2(num_str):
            invalid_ids.append(num)
    
    return invalid_ids

def solve_puzzle(input_text, show_details=True):
    """
    Parse the input ranges and find all invalid IDs.
    """
    # Parse the ranges
    ranges_str = input_text.strip()
    range_parts = ranges_str.split(',')
    
    all_invalid_ids = []
    
    if show_details:
        print(f"Processing {len(range_parts)} ranges...\n")
    
    for i, range_part in enumerate(range_parts, 1):
        range_part = range_part.strip()
        start_str, end_str = range_part.split('-')
        start = int(start_str)
        end = int(end_str)
        
        invalid_ids = find_invalid_ids_in_range(start, end)
        
        if show_details:
            if invalid_ids:
                if len(invalid_ids) <= 10:
                    print(f"Range {i}: {start}-{end} has {len(invalid_ids)} invalid ID(s): {invalid_ids}")
                else:
                    print(f"Range {i}: {start}-{end} has {len(invalid_ids)} invalid ID(s): {invalid_ids[:5]}...{invalid_ids[-5:]}")
            else:
                print(f"Range {i}: {start}-{end} has no invalid IDs")
        
        all_invalid_ids.extend(invalid_ids)
    
    return all_invalid_ids

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE (PART 2)")
    print("="*70)
    
    example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
    
    # Test the pattern checker first
    print("\nTesting pattern checker:")
    test_cases = [
        ('11', True, "1 twice"),
        ('99', True, "9 twice"),
        ('111', True, "1 three times"),
        ('999', True, "9 three times"),
        ('1010', True, "10 twice"),
        ('12341234', True, "1234 twice"),
        ('123123123', True, "123 three times"),
        ('1212121212', True, "12 five times"),
        ('1111111', True, "1 seven times"),
        ('1188511885', True, "11885 twice"),
        ('222222', True, "22 three times or 222 twice"),
        ('446446', True, "446 twice"),
        ('38593859', True, "3859 twice"),
        ('565656', True, "56 three times"),
        ('824824824', True, "824 three times"),
        ('2121212121', True, "21 five times"),
        ('123', False, "no repetition"),
        ('1234', False, "no repetition"),
        ('0101', False, "leading zero"),
    ]
    
    for test, expected, description in test_cases:
        result = is_repeated_pattern_part2(test)
        status = "✓" if result == expected else "✗"
        print(f"  {status} is_repeated_pattern('{test}') = {result} ({description})")
    
    print("\nProcessing example ranges:")
    invalid_ids = solve_puzzle(example)
    
    total = sum(invalid_ids)
    print(f"\nTotal invalid IDs found: {len(invalid_ids)}")
    print(f"Sum of all invalid IDs: {total}")
    print(f"Expected: 4174379265")
    print(f"Match: {total == 4174379265}")
    print("="*70 + "\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_day02.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE (PART 2)")
    print("="*70 + "\n")
    
    invalid_ids = solve_puzzle(input_text, show_details=False)
    
    # Show summary by range
    ranges_str = input_text.strip()
    range_parts = ranges_str.split(',')
    
    print("Summary by range (showing ranges with invalid IDs):")
    for i, range_part in enumerate(range_parts, 1):
        range_part = range_part.strip()
        start_str, end_str = range_part.split('-')
        start = int(start_str)
        end = int(end_str)
        
        # Count how many invalid IDs are in this range
        range_invalid = [id for id in invalid_ids if start <= id <= end]
        
        if range_invalid:
            range_sum = sum(range_invalid)
            if len(range_invalid) <= 5:
                print(f"Range {i:2d}: {start}-{end} -> {len(range_invalid)} invalid IDs: {range_invalid} (sum: {range_sum})")
            else:
                print(f"Range {i:2d}: {start}-{end} -> {len(range_invalid)} invalid IDs (sum: {range_sum})")
    
    total = sum(invalid_ids)
    print(f"\n{'='*70}")
    print(f"ANSWER: Sum of all invalid IDs = {total}")
    print(f"Total invalid IDs found: {len(invalid_ids)}")
    print(f"{'='*70}")
