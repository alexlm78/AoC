#!/usr/bin/env python3

def parse_ranges(input_text):
    """
    Parse the input to extract just the fresh ranges.
    """
    lines = input_text.strip().split('\n')
    
    # Find the blank line
    blank_line_idx = lines.index('')
    
    # Parse fresh ranges
    fresh_ranges = []
    for line in lines[:blank_line_idx]:
        parts = line.split('-')
        start = int(parts[0])
        end = int(parts[1])
        fresh_ranges.append((start, end))
    
    return fresh_ranges

def merge_ranges(ranges):
    """
    Merge overlapping ranges to get non-overlapping ranges.
    This helps us count the total number of unique IDs covered.
    """
    if not ranges:
        return []
    
    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    
    # Merge overlapping ranges
    merged = [sorted_ranges[0]]
    
    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        # Check if current range overlaps with or is adjacent to the last merged range
        if current_start <= last_end + 1:
            # Merge by extending the end of the last range
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as new range
            merged.append((current_start, current_end))
    
    return merged

def count_ids_in_ranges(ranges):
    """
    Count the total number of IDs covered by a list of ranges.
    Assumes ranges are already merged (non-overlapping).
    """
    total = 0
    for start, end in ranges:
        total += (end - start + 1)
    return total

def solve_part2(fresh_ranges):
    """
    Count all unique ingredient IDs considered fresh.
    """
    # Merge overlapping ranges
    merged_ranges = merge_ranges(fresh_ranges)
    
    # Count total IDs
    total_ids = count_ids_in_ranges(merged_ranges)
    
    return total_ids, merged_ranges

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE (PART 2)")
    print("="*70)
    
    example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    
    fresh_ranges = parse_ranges(example)
    
    print("\nOriginal fresh ID ranges:")
    for start, end in fresh_ranges:
        print(f"  {start}-{end}")
    
    total_ids, merged_ranges = solve_part2(fresh_ranges)
    
    print("\nMerged ranges (non-overlapping):")
    for start, end in merged_ranges:
        size = end - start + 1
        ids = list(range(start, end + 1)) if size <= 20 else None
        if ids:
            print(f"  {start}-{end}: {ids}")
        else:
            print(f"  {start}-{end} (size: {size})")
    
    print(f"\n{'='*70}")
    print(f"Total fresh ingredient IDs: {total_ids}")
    print(f"Expected: 14")
    print(f"Match: {total_ids == 14}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_05.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE (PART 2)")
    print("="*70 + "\n")
    
    fresh_ranges = parse_ranges(input_text)
    
    print(f"Number of original fresh ID ranges: {len(fresh_ranges)}")
    
    # Show some statistics about original ranges
    total_before_merge = sum(end - start + 1 for start, end in fresh_ranges)
    print(f"Total IDs if ranges didn't overlap: {total_before_merge:,}")
    
    total_ids, merged_ranges = solve_part2(fresh_ranges)
    
    print(f"\nNumber of merged ranges: {len(merged_ranges)}")
    print(f"Reduction: {len(fresh_ranges)} → {len(merged_ranges)} ranges")
    
    # Show first few merged ranges
    print(f"\nFirst 10 merged ranges:")
    for i, (start, end) in enumerate(merged_ranges[:10], 1):
        size = end - start + 1
        print(f"  {i}. {start:,} - {end:,} (size: {size:,})")
    
    if len(merged_ranges) > 10:
        print("\n  ...")
        print(f"\nLast 3 merged ranges:")
        for i, (start, end) in enumerate(merged_ranges[-3:], len(merged_ranges) - 2):
            size = end - start + 1
            print(f"  {i}. {start:,} - {end:,} (size: {size:,})")
    
    print(f"\n{'='*70}")
    print(f"ANSWER: {total_ids:,} ingredient IDs are considered fresh")
    print(f"Overlap reduction: {total_before_merge - total_ids:,} duplicate IDs removed")
    print(f"{'='*70}")
