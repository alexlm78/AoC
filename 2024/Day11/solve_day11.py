#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 11: Plutonian Pebbles

Rules per blink:
- 0 becomes 1
- Even number of digits splits the number into its left and right halves
- Otherwise multiply by 2024

Approach:
- Use memoization (value, steps) -> count of resulting stones after 'steps' blinks
- Sum counts across initial stones for required step counts (25, 75)
"""

import os
from functools import lru_cache


def parse_numbers(text: str) -> list[int]:
    """
    Parse space-separated integers from input text.
    Args:
        text: A string containing numbers separated by spaces
    Returns:
        List of integers
    """
    return [int(x) for x in text.strip().split()]


@lru_cache(maxsize=None)
def count_after_steps(value: int, steps: int) -> int:
    """
    Count how many stones a single starting value produces after 'steps' blinks.
    Applies transformation rules and sums results recursively, memoized.
    Args:
        value: Starting stone value
        steps: Number of blinks to simulate
    Returns:
        Total stones produced by this value after the given steps
    """
    if steps == 0:
        return 1
    if value == 0:
        # Rule: 0 -> 1
        return count_after_steps(1, steps - 1)
    s = str(value)
    if len(s) % 2 == 0:
        # Rule: even digits -> split in halves
        mid = len(s) // 2
        left = int(s[:mid])
        right = int(s[mid:])
        return count_after_steps(left, steps - 1) + count_after_steps(right, steps - 1)
    # Rule: otherwise multiply by 2024
    return count_after_steps(value * 2024, steps - 1)


def verify_example() -> None:
    """
    Verify example '125 17' for:
    - After 6 blinks: should be 22 stones
    - After 25 blinks: should be 55312 stones
    Prints verification status.
    """
    example = "125 17"
    stones = parse_numbers(example)

    total_6 = sum(count_after_steps(v, 6) for v in stones)
    total_25 = sum(count_after_steps(v, 25) for v in stones)

    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 11 - Part 1)")
    print("=" * 70)
    print(f"After 6 blinks: {total_6} (expected 22) -> Match: {total_6 == 22}")
    print(f"After 25 blinks: {total_25} (expected 55312) -> Match: {total_25 == 55312}")
    print("=" * 70)


def main() -> None:
    """
    Load input stones and compute:
    - Part 1: total stones after 25 blinks
    - Part 2: total stones after 75 blinks
    Prints both results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day11.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    stones = parse_numbers(content)

    total_25 = sum(count_after_steps(v, 25) for v in stones)
    total_75 = sum(count_after_steps(v, 75) for v in stones)

    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 11: Plutonian Pebbles")
    print("=" * 70)
    print(f"Part 1 - Stones after 25 blinks: {total_25}")
    print(f"Part 2 - Stones after 75 blinks: {total_75}")
    print("=" * 70)


if __name__ == "__main__":
    verify_example()
    main()
