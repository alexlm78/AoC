#!/usr/bin/env python3

def parse_input(input_text):
    """
    Parse the input into fresh ranges and available IDs.
    """
    lines = input_text.strip().split('\n')
    
    # Find the blank line separating ranges from IDs
    blank_line_idx = lines.index('')
    
    # Parse fresh ranges
    fresh_ranges = []
    for line in lines[:blank_line_idx]:
        parts = line.split('-')
        start = int(parts[0])
        end = int(parts[1])
        fresh_ranges.append((start, end))
    
    # Parse available IDs
    available_ids = []
    for line in lines[blank_line_idx + 1:]:
        if line.strip():
            available_ids.append(int(line))
    
    return fresh_ranges, available_ids

def is_fresh(ingredient_id, fresh_ranges):
    """
    Check if an ingredient ID is fresh (falls within any range).
    """
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False

def count_fresh_ingredients(fresh_ranges, available_ids):
    """
    Count how many available ingredient IDs are fresh.
    """
    fresh_count = 0
    fresh_ids = []
    spoiled_ids = []
    
    for ingredient_id in available_ids:
        if is_fresh(ingredient_id, fresh_ranges):
            fresh_count += 1
            fresh_ids.append(ingredient_id)
        else:
            spoiled_ids.append(ingredient_id)
    
    return fresh_count, fresh_ids, spoiled_ids

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE")
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
    
    fresh_ranges, available_ids = parse_input(example)
    
    print("\nFresh ID ranges:")
    for start, end in fresh_ranges:
        print(f"  {start}-{end}")
    
    print(f"\nAvailable ingredient IDs: {available_ids}")
    
    print("\nChecking each ingredient:")
    for ingredient_id in available_ids:
        fresh = is_fresh(ingredient_id, fresh_ranges)
        status = "fresh" if fresh else "spoiled"
        
        # Find which range(s) it falls into
        ranges = []
        for start, end in fresh_ranges:
            if start <= ingredient_id <= end:
                ranges.append(f"{start}-{end}")
        
        if ranges:
            print(f"  ID {ingredient_id}: {status} (in ranges: {', '.join(ranges)})")
        else:
            print(f"  ID {ingredient_id}: {status}")
    
    fresh_count, fresh_ids, spoiled_ids = count_fresh_ingredients(fresh_ranges, available_ids)
    
    print(f"\n{'='*70}")
    print(f"Fresh ingredients: {fresh_count}")
    print(f"Expected: 3")
    print(f"Match: {fresh_count == 3}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_05.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    fresh_ranges, available_ids = parse_input(input_text)
    
    print(f"Number of fresh ID ranges: {len(fresh_ranges)}")
    print(f"Number of available ingredient IDs: {len(available_ids)}")
    
    # Show a few examples of ranges
    print(f"\nFirst 5 fresh ranges:")
    for i, (start, end) in enumerate(fresh_ranges[:5], 1):
        size = end - start + 1
        print(f"  {i}. {start}-{end} (size: {size:,})")
    
    print(f"\nFirst 10 available IDs:")
    for i, ingredient_id in enumerate(available_ids[:10], 1):
        fresh = is_fresh(ingredient_id, fresh_ranges)
        status = "✓ fresh" if fresh else "✗ spoiled"
        print(f"  {i}. {ingredient_id}: {status}")
    
    # Count fresh ingredients
    fresh_count, fresh_ids, spoiled_ids = count_fresh_ingredients(fresh_ranges, available_ids)
    
    print(f"\n{'='*70}")
    print(f"ANSWER: {fresh_count} ingredient IDs are fresh")
    print(f"Spoiled: {len(spoiled_ids)}")
    print(f"Total: {len(available_ids)}")
    print(f"Fresh percentage: {100 * fresh_count / len(available_ids):.1f}%")
    print(f"{'='*70}")
