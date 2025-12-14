#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 20: Race Condition

Part 1 (two-step cheat):
- Compute the optimal track-only time from S to E with BFS
- Enumerate all possible single cheat activations of up to 2 steps (ignoring walls)
- For each cheat from track cell U to track cell V (Manhattan distance <= 2),
  compute cheated time: distS[U] + cheat_length + distE[V]
- Count cheats with savings >= 100 relative to the baseline time

Part 2 (twenty-step cheat):
- Same idea, except cheats can last up to 20 steps
- Enumerate all V such that Manhattan distance(U,V) in [1..20] and V is track
- Count how many achieve savings >= 100 picoseconds
"""

import os
from collections import deque
from typing import List, Tuple


def parse_grid(text: str) -> Tuple[List[str], Tuple[int, int], Tuple[int, int]]:
    """
    Parse racetrack map and locate start/end positions.
    Args:
        text: Lines containing '.', '#', 'S', 'E'
    Returns:
        (lines, start_rc, end_rc)
    """
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() != ""]
    rows, cols = len(lines), len(lines[0])
    s = e = None
    for r in range(rows):
        for c in range(cols):
            ch = lines[r][c]
            if ch == "S":
                s = (r, c)
            elif ch == "E":
                e = (r, c)
    return lines, s, e


def is_track(ch: str) -> bool:
    return ch in (".", "S", "E")


def bfs_dist(lines: List[str], start: Tuple[int, int]) -> List[List[int]]:
    """
    BFS to compute shortest track-only distances from a start cell.
    Args:
        lines: Map lines
        start: (r,c) start on track
    Returns:
        2D array of distances (or -1 for unreachable)
    """
    rows, cols = len(lines), len(lines[0])
    dist = [[-1] * cols for _ in range(rows)]
    sr, sc = start
    q = deque([(sr, sc)])
    dist[sr][sc] = 0
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                if is_track(lines[nr][nc]):
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))
    return dist


def count_cheats(
    lines: List[str],
    s: Tuple[int, int],
    e: Tuple[int, int],
    min_saving: int,
    cheat_limit: int,
) -> int:
    """
    Count cheats that save at least min_saving picoseconds.
    Cheat: exactly once, move up to 2 steps ignoring walls, from track U to track V.
    Args:
        lines: Map
        s: Start cell
        e: End cell
        min_saving: Threshold for savings
    Returns:
        Number of (U,V) cheats with savings >= min_saving
    """
    distS = bfs_dist(lines, s)
    distE = bfs_dist(lines, e)
    base = distS[e[0]][e[1]]
    rows, cols = len(lines), len(lines[0])
    total = 0
    for r in range(rows):
        for c in range(cols):
            if distS[r][c] == -1:
                continue
            # Begin cheat at U=(r,c)
            for dr in range(-cheat_limit, cheat_limit + 1):
                # Manhattan diamond enumeration
                rem = cheat_limit - abs(dr)
                for dc in range(-rem, rem + 1):
                    cheat_len = abs(dr) + abs(dc)
                    if cheat_len == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and is_track(lines[nr][nc]):
                        if distE[nr][nc] == -1:
                            continue
                        cheated_time = distS[r][c] + cheat_len + distE[nr][nc]
                        saving = base - cheated_time
                        if saving >= min_saving:
                            total += 1
    return total


def main():
    input_path = os.path.join(os.path.dirname(__file__), "day20.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines, s, e = parse_grid(content)
    n100_part1 = count_cheats(lines, s, e, min_saving=100, cheat_limit=2)
    n100_part2 = count_cheats(lines, s, e, min_saving=100, cheat_limit=20)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 20: Race Condition")
    print("=" * 70)
    print(f"Part 1 - Cheats saving at least 100 ps: {n100_part1}")
    print(f"Part 2 - Cheats saving at least 100 ps: {n100_part2}")
    print("=" * 70)


if __name__ == "__main__":
    main()
