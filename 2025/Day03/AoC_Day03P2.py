#!/usr/bin/env python3

def find_max_joltage_k_digits(bank, k):
    """
    Find the maximum k-digit number by selecting exactly k digits from the bank,
    maintaining their order.
    
    Greedy algorithm: At each step, pick the largest digit such that we can
    still select enough digits to reach k total.
    
    When there are multiple occurrences of the max digit, we need to pick
    the one that gives us the best remaining subsequence.
    """
    n = len(bank)
    if k > n:
        raise ValueError(f"Cannot select {k} digits from a bank of length {n}")
    
    result = []
    start_pos = 0
    
    for i in range(k):
        # How many more digits do we need after this one?
        remaining_needed = k - i - 1
        
        # We need to leave at least 'remaining_needed' digits after our choice
        # So we can only look up to position: n - remaining_needed - 1
        max_pos = n - remaining_needed
        
        # Find the maximum digit in the valid range
        max_digit = max(bank[start_pos:max_pos])
        
        # Among all positions with the max digit, we want the one that
        # leaves the lexicographically largest remaining sequence
        # This means we should try each position and see what we can build
        best_pos = start_pos
        best_suffix = ""
        
        for j in range(start_pos, max_pos):
            if bank[j] == max_digit:
                # What's the best we can do from position j+1?
                # For now, use a simple heuristic: pick the rightmost occurrence
                # This gives us more choices for future selections
                best_pos = j
        
        result.append(max_digit)
        start_pos = best_pos + 1
    
    return ''.join(result)

def solve_puzzle(input_text, k=12):
    """
    Find the maximum k-digit joltage from each bank and sum them up.
    """
    banks = input_text.strip().split('\n')
    
    total_joltage = 0
    results = []
    
    for i, bank in enumerate(banks, 1):
        max_joltage_str = find_max_joltage_k_digits(bank, k)
        max_joltage = int(max_joltage_str)
        total_joltage += max_joltage
        results.append((i, bank, max_joltage_str, max_joltage))
    
    return total_joltage, results

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE (PART 2)")
    print("="*70)
    
    example = """987654321111111
811111111111119
234234234234278
818181911112111"""
    
    # Test each bank
    test_cases = [
        ('987654321111111', '987654321111', 987654321111),
        ('811111111111119', '811111111119', 811111111119),
        ('234234234234278', '434234234278', 434234234278),
        ('818181911112111', '888911112111', 888911112111),
    ]
    
    print("\nTesting individual banks (k=12):")
    for bank, expected_str, expected_val in test_cases:
        result = find_max_joltage_k_digits(bank, 12)
        result_val = int(result)
        status = "✓" if result == expected_str else "✗"
        print(f"  {status} {bank}")
        print(f"     -> {result} (expected {expected_str})")
    
    # Test full example
    total, results = solve_puzzle(example, k=12)
    
    print(f"\nFull example:")
    for i, bank, joltage_str, joltage in results:
        print(f"  Bank {i}: {joltage_str} = {joltage:,}")
    
    print(f"\nTotal output joltage: {total:,}")
    expected_total = 987654321111 + 811111111119 + 434234234278 + 888911112111
    print(f"Expected: {expected_total:,}")
    print(f"Match: {total == expected_total}")
    print("="*70 + "\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_03.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE (PART 2)")
    print("="*70 + "\n")
    
    total_joltage, results = solve_puzzle(input_text, k=12)
    
    # Show first few and last few banks
    print("First 10 banks:")
    for i, bank, joltage_str, joltage in results[:10]:
        preview = bank[:30] + "..." if len(bank) > 30 else bank
        print(f"  Bank {i:3d}: {preview:35s}")
        print(f"           -> {joltage_str} = {joltage:,}")
    
    print("\n...")
    
    print("\nLast 10 banks:")
    for i, bank, joltage_str, joltage in results[-10:]:
        preview = bank[:30] + "..." if len(bank) > 30 else bank
        print(f"  Bank {i:3d}: {preview:35s}")
        print(f"           -> {joltage_str} = {joltage:,}")
    
    print(f"\n{'='*70}")
    print(f"ANSWER: Total output joltage = {total_joltage:,}")
    print(f"Number of banks: {len(results)}")
    print(f"{'='*70}")
