#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 16: Reindeer Maze

Part 1:
- Dijkstra in state (r,c,dir) with cost: move forward=1, turn=1000
- Start facing east from ‘S’ and minimize the cost to ‘E’

Part 2:
- Construct optimal edges (dist[u] + w == dist[v])
- Forward range from S and reverse range from E to count tiles
"""

import os
import heapq


def parse_grid(text: str):
    """
    Parse maze into lines and locate start/end positions.
    Args:
        text: Maze string containing 'S' (start) and 'E' (end), '#' walls
    Returns:
        (lines, start_rc, end_rc)
    """
    lines = [line.rstrip("\n") for line in text.splitlines() if line.strip() != ""]
    rows, cols = len(lines), len(lines[0])
    start = end = None
    for r in range(rows):
        for c in range(cols):
            ch = lines[r][c]
            if ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)
    return lines, start, end


def dijkstra(lines, start, end):
    """
    Compute minimal score to reach end with moves and rotations.
    Movement cost: 1 forward, rotation cost: 1000.
    Args:
        lines: Maze grid as list of strings
        start: (r,c) start cell, initial facing East
        end: (r,c) destination cell
    Returns:
        (dist_matrix[r][c][dir], best_cost_to_end)
    """
    rows, cols = len(lines), len(lines[0])
    # dirs: 0=E,1=S,2=W,3=N
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    INF = 10**18
    dist = [[[INF] * 4 for _ in range(cols)] for __ in range(rows)]
    pq = []
    sr, sc = start
    # start facing East (0)
    dist[sr][sc][0] = 0
    heapq.heappush(pq, (0, sr, sc, 0))
    while pq:
        d, r, c, dir = heapq.heappop(pq)
        if d != dist[r][c][dir]:
            continue
        # forward
        nr, nc = r + dr[dir], c + dc[dir]
        if 0 <= nr < rows and 0 <= nc < cols and lines[nr][nc] != "#":
            nd = d + 1
            if nd < dist[nr][nc][dir]:
                dist[nr][nc][dir] = nd
                heapq.heappush(pq, (nd, nr, nc, dir))
        # rotate left
        ndir = (dir + 3) % 4
        nd = d + 1000
        if nd < dist[r][c][ndir]:
            dist[r][c][ndir] = nd
            heapq.heappush(pq, (nd, r, c, ndir))
        # rotate right
        ndir = (dir + 1) % 4
        nd = d + 1000
        if nd < dist[r][c][ndir]:
            dist[r][c][ndir] = nd
            heapq.heappush(pq, (nd, r, c, ndir))
    best = min(dist[end[0]][end[1]])
    return dist, best


def best_tiles_count(lines, start, end, dist, best_cost):
    """
    Count tiles that belong to any optimal path.
    Uses forward reach from start and reverse reach from end over optimal edges.
    Args:
        lines: Maze grid
        start: start cell
        end: end cell
        dist: distance states from dijkstra
        best_cost: minimal cost to any end orientation
    Returns:
        Number of tiles on at least one optimal route
    """
    rows, cols = len(lines), len(lines[0])
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    # Build good edges: dist[u]+w == dist[v]
    good_fwd = [[[False] * 4 for _ in range(cols)] for __ in range(rows)]
    good_rev = [[[False] * 4 for _ in range(cols)] for __ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if lines[r][c] == "#":
                continue
            for dir in range(4):
                d = dist[r][c][dir]
                if d >= 10**18:
                    continue
                # forward
                nr, nc = r + dr[dir], c + dc[dir]
                if 0 <= nr < rows and 0 <= nc < cols and lines[nr][nc] != "#":
                    nd = d + 1
                    if nd == dist[nr][nc][dir]:
                        good_fwd[r][c][dir] = True
                        good_rev[nr][nc][dir] = True
                # rotate left
                ndir = (dir + 3) % 4
                nd = d + 1000
                if nd == dist[r][c][ndir]:
                    good_fwd[r][c][dir] = True  # mark state has outgoing good edge
                    good_rev[r][c][ndir] = True
                # rotate right
                ndir = (dir + 1) % 4
                nd = d + 1000
                if nd == dist[r][c][ndir]:
                    good_fwd[r][c][dir] = True
                    good_rev[r][c][ndir] = True
    # forward reach from start via good edges
    fvis = [[[False] * 4 for _ in range(cols)] for __ in range(rows)]
    stack = [(start[0], start[1], 0)]
    fvis[start[0]][start[1]][0] = True
    while stack:
        r, c, dir = stack.pop()
        d = dist[r][c][dir]
        # forward
        nr, nc = r + dr[dir], c + dc[dir]
        if 0 <= nr < rows and 0 <= nc < cols and lines[nr][nc] != "#":
            nd = d + 1
            if nd == dist[nr][nc][dir] and not fvis[nr][nc][dir]:
                fvis[nr][nc][dir] = True
                stack.append((nr, nc, dir))
        # left
        ndir = (dir + 3) % 4
        nd = d + 1000
        if nd == dist[r][c][ndir] and not fvis[r][c][ndir]:
            fvis[r][c][ndir] = True
            stack.append((r, c, ndir))
        # right
        ndir = (dir + 1) % 4
        nd = d + 1000
        if nd == dist[r][c][ndir] and not fvis[r][c][ndir]:
            fvis[r][c][ndir] = True
            stack.append((r, c, ndir))
    # reverse reach from any end dir via good reverse edges
    rvis = [[[False] * 4 for _ in range(cols)] for __ in range(rows)]
    stack = []
    er, ec = end
    for dir in range(4):
        if dist[er][ec][dir] == best_cost:
            rvis[er][ec][dir] = True
            stack.append((er, ec, dir))
    while stack:
        r, c, dir = stack.pop()
        # reverse of forward from predecessor states
        # predecessors could be:
        # forward from (r-dr[dir], c-dc[dir], dir) with +1
        pr, pc = r - dr[dir], c - dc[dir]
        if 0 <= pr < rows and 0 <= pc < cols and lines[pr][pc] != "#":
            if dist[pr][pc][dir] + 1 == dist[r][c][dir] and not rvis[pr][pc][dir]:
                rvis[pr][pc][dir] = True
                stack.append((pr, pc, dir))
        # rotations from same cell
        # left rotation predecessor: prev_dir = (dir+1)%4
        pdir = (dir + 1) % 4
        if dist[r][c][pdir] + 1000 == dist[r][c][dir] and not rvis[r][c][pdir]:
            rvis[r][c][pdir] = True
            stack.append((r, c, pdir))
        # right rotation predecessor: prev_dir = (dir+3)%4
        pdir = (dir + 3) % 4
        if dist[r][c][pdir] + 1000 == dist[r][c][dir] and not rvis[r][c][pdir]:
            rvis[r][c][pdir] = True
            stack.append((r, c, pdir))
    tiles = set()
    for r in range(rows):
        for c in range(cols):
            if lines[r][c] == "#":
                continue
            for dir in range(4):
                if fvis[r][c][dir] and rvis[r][c][dir]:
                    tiles.add((r, c))
                    break
    return len(tiles)


def verify_examples():
    """
    Print verification results for AoC examples (Part 1 expected scores).
    """
    ex1 = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    lines, s, e = parse_grid(ex1)
    dist, best = dijkstra(lines, s, e)
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 16 - Part 1)")
    print("=" * 70)
    print(f"Best score: {best} (expected 7036) -> Match: {best == 7036}")
    ex2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    lines, s, e = parse_grid(ex2)
    dist, best = dijkstra(lines, s, e)
    print(f"Best score: {best} (expected 11048) -> Match: {best == 11048}")
    print("=" * 70)


def main():
    """
    Read input, compute Part 1 (lowest score) and Part 2 (tiles on best paths),
    then print results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day16.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines, start, end = parse_grid(content)
    dist, best = dijkstra(lines, start, end)
    tiles = best_tiles_count(lines, start, end, dist, best)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 16: Reindeer Maze")
    print("=" * 70)
    print(f"Part 1 - Lowest score: {best}")
    print(f"Part 2 - Tiles on any best path: {tiles}")
    print("=" * 70)


if __name__ == "__main__":
    verify_examples()
    main()
