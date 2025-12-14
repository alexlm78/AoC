#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 19: Linen Layout

Part 1:
- Check for each design whether it is possible to compose it by concatenating patterns
- DP with index memoization, filtering by the first character of the pattern

Part 2:
- Count the total number of different arrangements for each design
- Add the quantities for the total answer
"""

import os
from functools import lru_cache
from typing import List, Tuple


def parse_input(text: str) -> Tuple[List[str], List[str]]:
    """
    Parse available towel patterns and desired designs.
    Args:
        text: Input containing first line of comma-separated patterns, blank line, then designs
    Returns:
        (patterns, designs) lists of strings
    """
    parts = text.strip("\n").split("\n\n")
    patterns = [p.strip() for p in parts[0].split(",")]
    designs = [line.strip() for line in parts[1].splitlines() if line.strip()]
    return patterns, designs


def can_make(design: str, patterns: List[str]) -> bool:
    """
    Check if a design can be formed by concatenating available patterns.
    Args:
        design: Target stripe sequence
        patterns: Available towel patterns (unlimited supply)
    Returns:
        True if design is buildable, False otherwise
    """
    by_first = {}
    for p in patterns:
        if not p:
            continue
        by_first.setdefault(p[0], []).append(p)

    @lru_cache(None)
    def dfs(i: int) -> bool:
        if i == len(design):
            return True
        lst = by_first.get(design[i], [])
        for p in lst:
            L = len(p)
            if design.startswith(p, i) and dfs(i + L):
                return True
        return False

    return dfs(0)


def count_ways(design: str, patterns: List[str]) -> int:
    """
    Count distinct ways to form the design by concatenating patterns.
    Args:
        design: Target stripe sequence
        patterns: Available towel patterns (unlimited supply)
    Returns:
        Number of different compositions (order matters)
    """
    by_first = {}
    for p in patterns:
        if not p:
            continue
        by_first.setdefault(p[0], []).append(p)

    @lru_cache(None)
    def dfs(i: int) -> int:
        if i == len(design):
            return 1
        total = 0
        for p in by_first.get(design[i], []):
            L = len(p)
            if design.startswith(p, i):
                total += dfs(i + L)
        return total

    return dfs(0)


def main():
    input_path = os.path.join(os.path.dirname(__file__), "day19.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    patterns, designs = parse_input(content)
    count = 0
    total_ways = 0
    for d in designs:
        if can_make(d, patterns):
            count += 1
        total_ways += count_ways(d, patterns)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 19: Linen Layout")
    print("=" * 70)
    print(f"Part 1 - Possible designs: {count}")
    print(f"Part 2 - Total arrangements: {total_ways}")
    print("=" * 70)


if __name__ == "__main__":
    main()
