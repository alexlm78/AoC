#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 15: Warehouse Woes

Part 1:
- Simulate robot pushes on a grid with walls '#', boxes 'O', empty '.', and robot '@'
- When moving into a box, push contiguous boxes if possible; blocked by walls
- After all moves, sum GPS coordinates for all boxes: 100*y + x (0-indexed from top-left)

Part 2:
- Expand the map: each 'O' becomes '[]' (two cells), each '#' becomes '##'
- Robot '@' remains a single-cell
- Vertical pushes must move entire 2-cell boxes; use dependency accumulation to check if move is possible
- GPS sum uses positions of the left bracket '[' only
"""

import os
from typing import List, Tuple


def parse_input(text: str) -> Tuple[List[str], str]:
    """
    Parse the warehouse map and move sequence.
    Args:
        text: Input containing map lines, blank line, then moves broken across lines
    Returns:
        (map_lines, moves_string_without_newlines)
    """
    parts = text.strip("\n").split("\n\n")
    grid_lines = [line.rstrip("\n") for line in parts[0].splitlines()]
    moves = "".join(parts[1].splitlines())
    return grid_lines, moves


def find_robot(grid: List[List[str]]) -> Tuple[int, int]:
    """
    Find robot coordinates '@'.
    Returns:
        (row, col)
    """
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "@":
                return r, c
    raise ValueError("Robot '@' not found")


def simulate_part1(grid_lines: List[str], moves: str) -> List[List[str]]:
    """
    Simulate Part 1 movement and pushing.
    Args:
        grid_lines: Original map lines
        moves: Sequence of moves '^', 'v', '<', '>'
    Returns:
        Final grid as list of lists of chars
    """
    grid = [list(row) for row in grid_lines]
    R, C = len(grid), len(grid[0])
    r, c = find_robot(grid)
    dirs = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    for mv in moves:
        dr, dc = dirs[mv]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < R and 0 <= nc < C):
            continue
        if grid[nr][nc] == "#":
            continue
        if grid[nr][nc] == ".":
            grid[r][c] = "."
            grid[nr][nc] = "@"
            r, c = nr, nc
            continue
        if grid[nr][nc] == "O":
            # push contiguous O's in direction until '.' or wall
            chain = []
            cr, cc = nr, nc
            while 0 <= cr < R and 0 <= cc < C and grid[cr][cc] == "O":
                chain.append((cr, cc))
                cr += dr
                cc += dc
            if not (0 <= cr < R and 0 <= cc < C):
                continue
            if grid[cr][cc] != ".":
                continue
            # move boxes: last to '.'; shift chain forward
            grid[cr][cc] = "O"
            for i in reversed(range(len(chain))):
                pr, pc = chain[i]
                nr2, nc2 = pr + dr, pc + dc
                grid[nr2][nc2] = "O"
                grid[pr][pc] = "."
            # move robot
            grid[r][c] = "."
            grid[nr][nc] = "@"
            r, c = nr, nc
    return grid


def gps_sum_part1(grid: List[List[str]]) -> int:
    """
    Sum GPS coordinates of all 'O' boxes: 100*y + x.
    """
    total = 0
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "O":
                total += 100 * y + x
    return total


def expand_map_part2(grid_lines: List[str]) -> List[List[str]]:
    """
    Expand the map for Part 2:
    - '#' -> '##'
    - 'O' -> '[]'
    - '@' -> '@.'
    - '.' -> '..'
    """
    expanded: List[List[str]] = []
    for line in grid_lines:
        row: List[str] = []
        for ch in line:
            if ch == "#":
                row.extend(["#", "#"])
            elif ch == "O":
                row.extend(["[", "]"])
            elif ch == "@":
                row.extend(["@", "."])
            elif ch == ".":
                row.extend([".", "."])
            else:
                raise ValueError(f"Unknown char '{ch}'")
        expanded.append(row)
    return expanded


def simulate_part2(grid_lines: List[str], moves: str) -> List[List[str]]:
    """
    Simulate Part 2 with wide boxes.
    Rules:
    - Horizontal move into '[' or ']' pushes contiguous bracket pairs along direction if space exists
    - Vertical move must move entire 2-wide boxes; recursively collect all brackets that would be affected
      by moving up/down, ensure destination cells are free of walls '#'
    """
    grid = expand_map_part2(grid_lines)
    R, C = len(grid), len(grid[0])
    r, c = find_robot(grid)
    dirs = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

    def is_box_cell(ch: str) -> bool:
        return ch in "[]"

    for mv in moves:
        dr, dc = dirs[mv]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < R and 0 <= nc < C):
            continue
        target = grid[nr][nc]
        if target == "#":
            continue
        if target == ".":
            grid[r][c] = "."
            grid[nr][nc] = "@"
            r, c = nr, nc
            continue
        if is_box_cell(target):
            if dc != 0:
                # horizontal push: treat as 1D chain of bracket cells
                chain = []
                cr, cc = nr, nc
                while 0 <= cr < R and 0 <= cc < C and is_box_cell(grid[cr][cc]):
                    chain.append((cr, cc))
                    cc += dc
                if not (0 <= cr < R and 0 <= cc < C):
                    continue
                if grid[cr][cc] != ".":
                    continue
                # push brackets horizontally
                grid[cr][cc] = (
                    grid[cr - dr][cc - dc] if False else "]" if dc < 0 else "["
                )  # placeholder fixed below
                # shift chain forward
                # We need to move pairs; simpler: shift all cells by one
                for i in reversed(range(len(chain))):
                    pr, pc = chain[i]
                    nr2, nc2 = pr + dr, pc + dc
                    grid[nr2][nc2] = grid[pr][pc]
                    grid[pr][pc] = "."
                # move robot
                grid[r][c] = "."
                grid[nr][nc] = "@"
                r, c = nr, nc
            else:
                # vertical push: accumulate affected bracket positions
                to_move = set()
                frontier = {(nr, nc)}
                blocked = False
                while frontier and not blocked:
                    new_frontier = set()
                    for pr, pc in frontier:
                        if (pr, pc) in to_move:
                            continue
                        to_move.add((pr, pc))
                        # include pair mate horizontally
                        if grid[pr][pc] == "[":
                            mate = (pr, pc + 1)
                        else:  # ']'
                            mate = (pr, pc - 1)
                        to_move.add(mate)
                        # check destination cells
                        for qr, qc in (
                            (pr + dr, pc + dc),
                            (mate[0] + dr, mate[1] + dc),
                        ):
                            if not (0 <= qr < R and 0 <= qc < C):
                                blocked = True
                                break
                            dest = grid[qr][qc]
                            if dest == "#":
                                blocked = True
                                break
                            if is_box_cell(dest):
                                new_frontier.add((qr, qc))
                        if blocked:
                            break
                    frontier = new_frontier
                if blocked:
                    continue
                # perform move: clear originals, write brackets at new positions
                # Must preserve bracket orientation.
                sorted(to_move)  # order not critical; we'll clear then write
                # compute destinations
                dests = {(pr + dr, pc + dc): grid[pr][pc] for (pr, pc) in to_move}
                for pr, pc in to_move:
                    grid[pr][pc] = "."
                for (qr, qc), ch in dests.items():
                    grid[qr][qc] = ch
                # move robot
                grid[r][c] = "."
                grid[nr][nc] = "@"
                r, c = nr, nc
    return grid


def gps_sum_part2(grid: List[List[str]]) -> int:
    """
    Sum GPS coordinates of all wide boxes using left bracket '[' positions: 100*y + x.
    """
    total = 0
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "[":
                total += 100 * y + x
    return total


def verify_examples() -> None:
    """
    Verify with the provided small example and large example totals for Part 1.
    """
    # Small example
    small_map = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########"""
    small_moves = "<^^>>>vv<v>>v<<"
    grid_lines = small_map.splitlines()
    grid_final = simulate_part1(grid_lines, small_moves)
    s1 = gps_sum_part1(grid_final)
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 15 - Part 1, small)")
    print("=" * 70)
    print(f"GPS sum: {s1} (expected 2028) -> Match: {s1 == 2028}")
    print("=" * 70)

    # Larger example
    large_map = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########"""
    large_moves = (
        "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^"
        "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v"
        "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<"
        "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^"
        "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><"
        "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^"
        ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^"
        "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>"
        "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>"
        "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"
    )
    grid_lines2 = large_map.splitlines()
    grid_final2 = simulate_part1(grid_lines2, large_moves)
    s2 = gps_sum_part1(grid_final2)
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 15 - Part 1, large)")
    print("=" * 70)
    print(f"GPS sum: {s2} (expected 10092) -> Match: {s2 == 10092}")
    print("=" * 70)


def main() -> None:
    """
    Load the input and compute:
    - Part 1: GPS sum after all moves
    - Part 2: GPS sum after all moves on expanded map
    Prints both results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day15.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    grid_lines, moves = parse_input(content)

    final_p1 = simulate_part1(grid_lines, moves)
    ans_p1 = gps_sum_part1(final_p1)

    final_p2 = simulate_part2(grid_lines, moves)
    ans_p2 = gps_sum_part2(final_p2)

    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 15: Warehouse Woes")
    print("=" * 70)
    print(f"Part 1 - GPS sum: {ans_p1}")
    print(f"Part 2 - GPS sum (expanded boxes): {ans_p2}")
    print("=" * 70)


if __name__ == "__main__":
    verify_examples()
    main()
