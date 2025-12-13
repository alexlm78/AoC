#!/usr/bin/env python3

def find_max_joltage(bank):
    """
    Find the maximum joltage possible from a bank by selecting
    exactly two batteries (digits) that form the largest two-digit number.
    
    The key insight: we want the largest digit in the leftmost position,
    and the second-largest digit (that comes after it) in the rightmost position.
    """
    # Try all pairs of positions i and j where i < j
    max_joltage = 0
    
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form a two-digit number from positions i and j
            joltage = int(bank[i] + bank[j])
            max_joltage = max(max_joltage, joltage)
    
    return max_joltage

def solve_puzzle(input_text):
    """
    Find the maximum joltage from each bank and sum them up.
    """
    banks = input_text.strip().split('\n')
    
    total_joltage = 0
    results = []
    
    for i, bank in enumerate(banks, 1):
        max_joltage = find_max_joltage(bank)
        total_joltage += max_joltage
        results.append((i, bank, max_joltage))
    
    return total_joltage, results

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE")
    print("="*70)
    
    example = """
    987654321111111
    811111111111119
    234234234234278
    818181911112111
    """
    
    # Test each bank
    test_cases = [
        ('987654321111111', 98, "first two batteries: 9 and 8"),
        ('811111111111119', 89, "batteries 8 and 9"),
        ('234234234234278', 78, "last two batteries: 7 and 8"),
        ('818181911112111', 92, "positions with 9 and 2"),
    ]
    
    print("\nTesting individual banks:")
    for bank, expected, explanation in test_cases:
        result = find_max_joltage(bank)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {bank[:20]}... -> {result} ({explanation})")
    
    # Test full example
    total, results = solve_puzzle(example)
    
    print(f"\nFull example:")
    for i, bank, joltage in results:
        print(f"  Bank {i}: {joltage} jolts")
    
    print(f"\nTotal output joltage: {total}")
    print(f"Expected: 357")
    print(f"Match: {total == 357}")
    print("="*70 + "\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('input_03.txt', 'r') as f:
        input_text = f.read()
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    total_joltage, results = solve_puzzle(input_text)
    
    # Show first few and last few banks
    print("First 10 banks:")
    for i, bank, joltage in results[:10]:
        preview = bank[:30] + "..." if len(bank) > 30 else bank
        print(f"  Bank {i:3d}: {preview:35s} -> {joltage} jolts")
    
    print("\n...")
    
    print("\nLast 10 banks:")
    for i, bank, joltage in results[-10:]:
        preview = bank[:30] + "..." if len(bank) > 30 else bank
        print(f"  Bank {i:3d}: {preview:35s} -> {joltage} jolts")
    
    print(f"\n{'='*70}")
    print(f"ANSWER: Total output joltage = {total_joltage}")
    print(f"Number of banks: {len(results)}")
    print(f"{'='*70}")
