#!/usr/bin/env python3
import os
from collections import defaultdict
from math import gcd


def parse_map(text: str) -> list[str]:
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() != ""]
    if not lines:
        return []
    width = len(lines[0])
    for i, line in enumerate(lines):
        if len(line) != width:
            raise ValueError(
                f"Inconsistent row width at line {i}: expected {width}, got {len(line)}"
            )
    return lines


def find_antennas(grid: list[str]) -> dict[str, list[tuple[int, int]]]:
    by_freq: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch != ".":
                by_freq[ch].append((r, c))
    return by_freq


def antinodes_for_pair(
    a: tuple[int, int], b: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    dr = b[0] - a[0]
    dc = b[1] - a[1]
    # Two antinodes: one beyond each antenna along the line
    p1 = (a[0] - dr, a[1] - dc)  # 2a - b
    p2 = (b[0] + dr, b[1] + dc)  # 2b - a
    return p1, p2


def count_unique_antinodes(grid: list[str]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    antennas = find_antennas(grid)
    antinode_set: set[tuple[int, int]] = set()

    for freq, points in antennas.items():
        n = len(points)
        if n < 2:
            continue
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = antinodes_for_pair(points[i], points[j])
                if 0 <= p1[0] < rows and 0 <= p1[1] < cols:
                    antinode_set.add(p1)
                if 0 <= p2[0] < rows and 0 <= p2[1] < cols:
                    antinode_set.add(p2)

    return len(antinode_set)


def count_unique_antinodes_part2(grid: list[str]) -> int:
    """
    Harmonics model (Part 2):
    Any grid position exactly in line with at least two antennas of the same frequency
    becomes an antinode, regardless of distance. This includes antenna positions themselves
    (unless there's only a single antenna of that frequency).
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    antennas = find_antennas(grid)
    antinode_set: set[tuple[int, int]] = set()

    for freq, points in antennas.items():
        if len(points) < 2:
            continue
        # For each pair, mark the entire line within the grid, stepping by the reduced vector
        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                a = points[i]
                b = points[j]
                dr = b[0] - a[0]
                dc = b[1] - a[1]
                g = gcd(abs(dr), abs(dc))
                step_r = dr // g
                step_c = dc // g

                # Walk backwards from 'a' until leaving the grid
                r, c = a
                while 0 <= r < rows and 0 <= c < cols:
                    antinode_set.add((r, c))
                    r -= step_r
                    c -= step_c

                # Walk forwards from 'a' until leaving the grid
                r, c = a[0] + step_r, a[1] + step_c
                while 0 <= r < rows and 0 <= c < cols:
                    antinode_set.add((r, c))
                    r += step_r
                    c += step_c

    return len(antinode_set)


def verify_with_example() -> None:
    example = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    grid = parse_map(example)
    result_p1 = count_unique_antinodes(grid)
    result_p2 = count_unique_antinodes_part2(grid)
    print("=" * 70)
    print("VERIFYING WITH EXAMPLE (Day 8 - Parts 1 & 2)")
    print("=" * 70)
    print(f"Rows: {len(grid)}, Cols: {len(grid[0]) if grid else 0}")
    print(
        f"Part 1 example antinodes: {result_p1} (expected 14) -> Match: {result_p1 == 14}"
    )
    print(
        f"Part 2 example antinodes: {result_p2} (expected 34) -> Match: {result_p2 == 34}"
    )
    print("=" * 70)


def main() -> None:
    input_path = os.path.join(os.path.dirname(__file__), "day08.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    grid = parse_map(content)
    result_p1 = count_unique_antinodes(grid)
    result_p2 = count_unique_antinodes_part2(grid)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 8: Resonant Collinearity")
    print("=" * 70)
    print(f"Grid size: {len(grid)} rows x {len(grid[0]) if grid else 0} cols")
    print(f"Part 1 - Unique antinode locations: {result_p1}")
    print(f"Part 2 - Unique antinode locations (harmonics): {result_p2}")
    print("=" * 70)


if __name__ == "__main__":
    verify_with_example()
    main()
