#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 12: Garden Groups

Part 1:
- Identify contiguous regions (4-directional) of same-letter plots
- For each region, compute:
  - area = number of plots
  - perimeter = number of region edges exposed to outside/different letter
- Total price = sum(area * perimeter)

Part 2:
- Compute number of "sides" instead of simple perimeter
- A continuous straight boundary run counts as one side, even if it spans multiple unit edges
- Total price (Part 2) = sum(area * sides)
"""

import os
from collections import deque
from typing import List, Tuple, Set


def parse_map(text: str) -> List[List[str]]:
    """
    Parse the garden map into a 2D grid of letters.
    Args:
        text: Lines of equal length containing letters
    Returns:
        Matrix of single-character strings
    """
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() != ""]
    return [list(line) for line in lines]


def neighbors4(r: int, c: int, rows: int, cols: int):
    """
    Yield 4-directional neighbor positions within bounds.
    Args:
        r, c: Current coordinates
        rows, cols: Grid dimensions
    Yields:
        (nr, nc) positions for up/down/left/right
    """
    if r > 0:
        yield r - 1, c
    if r + 1 < rows:
        yield r + 1, c
    if c > 0:
        yield r, c - 1
    if c + 1 < cols:
        yield r, c + 1


def find_regions(grid: List[List[str]]) -> List[Tuple[str, Set[Tuple[int, int]]]]:
    """
    Flood-fill regions of same letter using 4-connectivity.
    Args:
        grid: Letter matrix
    Returns:
        List of tuples (letter, set_of_cells_in_region)
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    regions: List[Tuple[str, Set[Tuple[int, int]]]] = []

    for r in range(rows):
        for c in range(cols):
            if visited[r][c]:
                continue
            letter = grid[r][c]
            q = deque([(r, c)])
            visited[r][c] = True
            region_cells: Set[Tuple[int, int]] = {(r, c)}

            while q:
                cr, cc = q.popleft()
                for nr, nc in neighbors4(cr, cc, rows, cols):
                    if not visited[nr][nc] and grid[nr][nc] == letter:
                        visited[nr][nc] = True
                        q.append((nr, nc))
                        region_cells.add((nr, nc))

            regions.append((letter, region_cells))

    return regions


def compute_area_and_perimeter(
    grid: List[List[str]], region: Set[Tuple[int, int]]
) -> Tuple[int, int]:
    """
    Compute area and standard perimeter for a region.
    Perimeter counts all unit edges exposed to outside or different letter.
    Args:
        grid: Letter matrix
        region: Set of (r, c) in the region
    Returns:
        (area, perimeter)
    """
    rows, cols = len(grid), len(grid[0])
    area = len(region)
    perimeter = 0
    region_set = region

    for r, c in region_set:
        # up
        if r == 0 or (r - 1, c) not in region_set:
            perimeter += 1
        # down
        if r == rows - 1 or (r + 1, c) not in region_set:
            perimeter += 1
        # left
        if c == 0 or (r, c - 1) not in region_set:
            perimeter += 1
        # right
        if c == cols - 1 or (r, c + 1) not in region_set:
            perimeter += 1

    return area, perimeter


def compute_sides(grid: List[List[str]], region: Set[Tuple[int, int]]) -> int:
    """
    Compute the number of "sides" of a region as continuous straight boundary runs.
    Strategy:
    - Build exposure masks for N/S/E/W edges of region cells
    - Count runs horizontally for N/S, vertically for W/E
    Args:
        grid: Letter matrix
        region: Set of (r, c) in the region
    Returns:
        Number of sides
    """
    rows, cols = len(grid), len(grid[0])
    region_set = region

    # Exposure masks
    expN = [[False] * cols for _ in range(rows)]
    expS = [[False] * cols for _ in range(rows)]
    expW = [[False] * cols for _ in range(rows)]
    expE = [[False] * cols for _ in range(rows)]

    for r, c in region_set:
        # north exposure
        if r == 0 or (r - 1, c) not in region_set:
            expN[r][c] = True
        # south exposure
        if r == rows - 1 or (r + 1, c) not in region_set:
            expS[r][c] = True
        # west exposure
        if c == 0 or (r, c - 1) not in region_set:
            expW[r][c] = True
        # east exposure
        if c == cols - 1 or (r, c + 1) not in region_set:
            expE[r][c] = True

    sides = 0

    # Horizontal runs (north and south)
    for r in range(rows):
        # north runs
        run = False
        for c in range(cols):
            if expN[r][c]:
                if not run:
                    sides += 1
                    run = True
            else:
                run = False
        # south runs
        run = False
        for c in range(cols):
            if expS[r][c]:
                if not run:
                    sides += 1
                    run = True
            else:
                run = False

    # Vertical runs (west and east)
    for c in range(cols):
        # west runs
        run = False
        for r in range(rows):
            if expW[r][c]:
                if not run:
                    sides += 1
                    run = True
            else:
                run = False
        # east runs
        run = False
        for r in range(rows):
            if expE[r][c]:
                if not run:
                    sides += 1
                    run = True
            else:
                run = False

    return sides


def total_price_part1(grid: List[List[str]]) -> int:
    """
    Compute total price for Part 1: sum(area * perimeter) across all regions.
    Args:
        grid: Letter matrix
    Returns:
        Total price
    """
    regions = find_regions(grid)
    total = 0
    for letter, cells in regions:
        area, perimeter = compute_area_and_perimeter(grid, cells)
        total += area * perimeter
    return total


def total_price_part2(grid: List[List[str]]) -> int:
    """
    Compute total price for Part 2: sum(area * sides) across all regions.
    Args:
        grid: Letter matrix
    Returns:
        Total price using side-based fencing
    """
    regions = find_regions(grid)
    total = 0
    for letter, cells in regions:
        area, _ = compute_area_and_perimeter(grid, cells)
        sides = compute_sides(grid, cells)
        total += area * sides
    return total


def verify_examples() -> None:
    """
    Verify sample maps for Part 1 totals from the description.
    Prints verification results.
    """
    ex1 = """\
AAAA
BBCD
BBCC
EEEC"""
    ex2 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    ex_large = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    g1 = parse_map(ex1)
    g2 = parse_map(ex2)
    gl = parse_map(ex_large)

    p1_1 = total_price_part1(g1)
    p1_2 = total_price_part1(g2)
    p1_l = total_price_part1(gl)

    print("=" * 70)
    print("VERIFYING EXAMPLES (Day 12 - Part 1)")
    print("=" * 70)
    print(f"Example 1 total price: {p1_1} (expected 140) -> Match: {p1_1 == 140}")
    print(f"Example 2 total price: {p1_2} (expected 772) -> Match: {p1_2 == 772}")
    print(
        f"Larger example total price: {p1_l} (expected 1930) -> Match: {p1_l == 1930}"
    )
    print("=" * 70)


def main() -> None:
    """
    Load input map and compute:
    - Part 1: total price using perimeter
    - Part 2: total price using number of sides
    Prints both results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day12.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    grid = parse_map(content)

    total_p1 = total_price_part1(grid)
    total_p2 = total_price_part2(grid)

    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 12: Garden Groups")
    print("=" * 70)
    print(f"Part 1 - Total price (area * perimeter): {total_p1}")
    print(f"Part 2 - Total price (area * sides): {total_p2}")
    print("=" * 70)


if __name__ == "__main__":
    verify_examples()
    main()
