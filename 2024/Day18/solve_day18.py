#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 18: RAM Run

Part 1:
- Mark the first 1024 coordinates as corrupt in a 71x71 grid
- Calculate the minimum path from (0,0) to (70,70) with BFS avoiding corrupt cells

Part 2:
- Scan the byte sequence and detect the first one that completely blocks the output
- Use BFS after each insertion to verify reachability
"""

import os
from collections import deque
from typing import List, Tuple, Set


def parse_points(text: str) -> List[Tuple[int, int]]:
    """
    Parse list of incoming byte positions as (x,y) pairs.
    Args:
        text: Lines of 'X,Y'
    Returns:
        List of integer coordinate tuples
    """
    pts = []
    for line in text.strip().splitlines():
        s = line.strip()
        if not s:
            continue
        x_str, y_str = s.split(",")
        pts.append((int(x_str), int(y_str)))
    return pts


def bfs_min_steps(n: int, blocked: Set[Tuple[int, int]]) -> int:
    """
    BFS shortest path on n x n grid avoiding blocked cells.
    Args:
        n: Grid size where coordinates range 0..n-1
        blocked: Set of corrupted coordinates
    Returns:
        Minimum steps from (0,0) to (n-1,n-1), or -1 if unreachable
    """
    start = (0, 0)
    end = (n - 1, n - 1)
    if start in blocked or end in blocked:
        return -1
    q = deque([start])
    dist = {start: 0}
    while q:
        x, y = q.popleft()
        if (x, y) == end:
            return dist[(x, y)]
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < n
                and 0 <= ny < n
                and (nx, ny) not in blocked
                and (nx, ny) not in dist
            ):
                dist[(nx, ny)] = dist[(x, y)] + 1
                q.append((nx, ny))
    return -1


def first_blocking_byte(pts: List[Tuple[int, int]], n: int) -> Tuple[int, int]:
    """
    Find first incoming byte that makes the exit unreachable.
    Args:
        pts: Sequence of bytes (coordinates) in falling order
        n: Grid size
    Returns:
        The coordinate (x,y) of first blocking byte, or (-1,-1) if none
    """
    blocked: Set[Tuple[int, int]] = set()
    for p in pts:
        blocked.add(p)
        if bfs_min_steps(n, blocked) == -1:
            return p
    return (-1, -1)


def main():
    """
    Read input, simulate first 1024 bytes for Part 1 steps,
    and scan for the first byte that blocks the path (Part 2).
    """
    input_path = os.path.join(os.path.dirname(__file__), "day18.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    pts = parse_points(content)
    n = 71
    k = 1024
    blocked = set(pts[:k])
    steps = bfs_min_steps(n, blocked)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 18: RAM Run")
    print("=" * 70)
    print(f"Part 1 - Minimum steps after {k} bytes: {steps}")
    bx, by = first_blocking_byte(pts, n)
    print(f"Part 2 - First blocking byte: {bx},{by}")
    print("=" * 70)


if __name__ == "__main__":
    main()
