#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 10: Hoof It

Part 1:
- For each trailhead (cells with height 0), count how many distinct height-9 cells
  are reachable via paths that strictly increase by 1 at each step (orthogonal moves).

Part 2:
- For each trailhead, compute its rating as the number of distinct increasing
  paths from that trailhead to any height-9 cell. Memoization is used to sum
  path counts from overlapping subproblems.
"""

import os
from collections import deque
from functools import lru_cache


def parse_grid(text: str) -> list[list[int]]:
    """
    Parse the input text into a 2D grid of integers.
    Args:
        text: Map string containing rows of digits
    Returns:
        Matrix of ints representing heights
    """
    lines = [line.strip() for line in text.splitlines() if line.strip() != ""]
    return [[int(ch) for ch in line] for line in lines]


def neighbors(r: int, c: int, rows: int, cols: int):
    """
    Yield orthogonal neighbor coordinates within bounds.
    Args:
        r, c: Current row and column
        rows, cols: Grid dimensions
    Yields:
        (nr, nc) neighbor positions
    """
    if r > 0:
        yield r - 1, c
    if r + 1 < rows:
        yield r + 1, c
    if c > 0:
        yield r, c - 1
    if c + 1 < cols:
        yield r, c + 1


def trailhead_score(grid: list[list[int]], start_r: int, start_c: int) -> int:
    """
    Compute the Part 1 score for a single trailhead.
    A BFS follows only edges that increase height by exactly +1,
    collecting all unique height-9 endpoints reachable.
    Args:
        grid: Height map
        start_r, start_c: Trailhead coordinates (must be height 0)
    Returns:
        Count of distinct height-9 positions reachable
    """
    rows, cols = len(grid), len(grid[0])
    q = deque()
    q.append((start_r, start_c))
    visited = set()
    visited.add((start_r, start_c))
    found9 = set()
    while q:
        r, c = q.popleft()
        h = grid[r][c]
        if h == 9:
            # Stop exploring past 9; just record endpoint
            found9.add((r, c))
            continue
        nh = h + 1
        for nr, nc in neighbors(r, c, rows, cols):
            if (nr, nc) not in visited and grid[nr][nc] == nh:
                visited.add((nr, nc))
                q.append((nr, nc))
    return len(found9)


def sum_trailhead_scores(grid: list[list[int]]) -> int:
    """
    Sum Part 1 scores across all trailheads (height 0 cells).
    Args:
        grid: Height map
    Returns:
        Total score across trailheads
    """
    total = 0
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total += trailhead_score(grid, r, c)
    return total


def trailhead_rating(grid: list[list[int]], start_r: int, start_c: int) -> int:
    """
    Compute the Part 2 rating (number of distinct trails) for a trailhead.
    Uses memoized DFS that counts all paths that increase by +1 up to height 9.
    Args:
        grid: Height map
        start_r, start_c: Trailhead coordinates (must be height 0)
    Returns:
        Number of distinct increasing paths ending at any height-9 cell
    """
    rows, cols = len(grid), len(grid[0])

    @lru_cache(maxsize=None)
    def count_paths(r: int, c: int) -> int:
        """
        Recursively count paths from (r, c) to any cell of height 9,
        stepping only to neighbors with height +1. Memoized by (r, c).
        """
        h = grid[r][c]
        if h == 9:
            return 1
        nh = h + 1
        total = 0
        if r > 0 and grid[r - 1][c] == nh:
            total += count_paths(r - 1, c)
        if r + 1 < rows and grid[r + 1][c] == nh:
            total += count_paths(r + 1, c)
        if c > 0 and grid[r][c - 1] == nh:
            total += count_paths(r, c - 1)
        if c + 1 < cols and grid[r][c + 1] == nh:
            total += count_paths(r, c + 1)
        return total

    return count_paths(start_r, start_c)


def sum_trailhead_ratings(grid: list[list[int]]) -> int:
    """
    Sum Part 2 ratings across all trailheads (height 0 cells).
    Args:
        grid: Height map
    Returns:
        Total rating across trailheads
    """
    total = 0
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total += trailhead_rating(grid, r, c)
    return total


def verify_examples() -> None:
    """
    Verify example map results for both parts:
    - Part 1 expected sum of scores: 36
    - Part 2 expected sum of ratings: 81
    Prints verification status.
    """
    example_large = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    grid = parse_grid(example_large)
    result_p1 = sum_trailhead_scores(grid)
    result_p2 = sum_trailhead_ratings(grid)
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 10 - Parts 1 & 2)")
    print("=" * 70)
    print(
        f"Part 1: Sum of trailhead scores: {result_p1} (expected 36) -> Match: {result_p1 == 36}"
    )
    print(
        f"Part 2: Sum of trailhead ratings: {result_p2} (expected 81) -> Match: {result_p2 == 81}"
    )
    print("=" * 70)


def main() -> None:
    """
    Load input map and compute:
    - Part 1: sum of trailhead scores
    - Part 2: sum of trailhead ratings
    Prints both results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day10.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    grid = parse_grid(content)
    result_p1 = sum_trailhead_scores(grid)
    result_p2 = sum_trailhead_ratings(grid)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 10: Hoof It")
    print("=" * 70)
    print(f"Map size: {len(grid)} rows x {len(grid[0]) if grid else 0} cols")
    print(f"Part 1 - Sum of trailhead scores: {result_p1}")
    print(f"Part 2 - Sum of trailhead ratings: {result_p2}")
    print("=" * 70)


if __name__ == "__main__":
    verify_examples()
    main()
