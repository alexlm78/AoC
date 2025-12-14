#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 21: Keypad Conundrum

Part 1:
- Compute the minimal number of button presses on your directional keypad
  that make the bottom robot type each code on the numeric keypad
- Sum complexity: for each code, (minimal presses) * (numeric value of the code)

Approach:
- Model both keypads as grids with a single gap None
- Precompute all shortest valid move sequences (ending with 'A') between any pair of keys
- Recursively expand sequences across two directional layers with memoization

Part 2:
- Compute the minimal number of button presses on your directional keypad
  that make the bottom robot type each code on the numeric keypad
- Sum complexity: for each code, (minimal presses) * (numeric value of the code)

Approach:
- Model both keypads as grids with a single gap None
- Precompute all shortest valid move sequences (ending with 'A') between any pair of keys
- Recursively expand sequences across two directional layers with memoization
"""

import os
from typing import Dict, List, Tuple


def load_codes(text: str) -> List[str]:
    """
    Load code lines from input text.
    - Each non-empty line is a numeric keypad code that ends with 'A'.
    - Empty lines are ignored.
    """
    return [line.strip() for line in text.splitlines() if line.strip()]


def numeric_value(code: str) -> int:
    """
    Return the numeric part of the code, ignoring the trailing 'A'.
    Example: '029A' -> 29
    """
    return int(code[:-1])


DIR_KEYS = ["^", "A", "<", "v", ">"]
NUM_KEYS = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "0", "A"]

# Directional keypad layout
DIR_GRID = [
    [None, "^", "A"],
    ["<", "v", ">"],
]
DIR_POS: Dict[str, Tuple[int, int]] = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

# Numeric keypad layout
NUM_GRID = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]
NUM_POS: Dict[str, Tuple[int, int]] = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}


def arrow_for_delta(dr: int, dc: int) -> List[str]:
    """
    Build a sequence of arrows to move dr rows and dc columns.
    Note: helper function; final computation uses BFS and precomputed tables.
    """
    seq = []
    if dr < 0:
        seq.extend("^" for _ in range(-dr))
    if dr > 0:
        seq.extend("v" for _ in range(dr))
    if dc < 0:
        seq.extend("<" for _ in range(-dc))
    if dc > 0:
        seq.extend(">" for _ in range(dc))
    return seq


def simulate_path(
    grid: List[List[str]], start: Tuple[int, int], moves: List[str]
) -> bool:
    """
    Simulate an arrow sequence on a keypad grid.
    Returns False if at any step the pointer lands on the gap (None) or outside the grid.
    """
    r, c = start
    for m in moves:
        if m == "^":
            r -= 1
        elif m == "v":
            r += 1
        elif m == "<":
            c -= 1
        elif m == ">":
            c += 1
        if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] is None:
            return False
    return True


def shortest_sequences(
    grid: List[List[str]], pos: Dict[str, Tuple[int, int]]
) -> Dict[Tuple[str, str], List[str]]:
    """
    Enumerate all shortest valid arrow sequences between keys (a -> b),
    avoiding the keypad gap. Appends 'A' to the end of every sequence.
    - Uses BFS to compute minimal distance and multiple parents to reconstruct all shortest paths.
    """
    result: Dict[Tuple[str, str], List[str]] = {}
    keys = [k for k in pos.keys()]
    for a in keys:
        for b in keys:
            ar, ac = pos[a]
            br, bc = pos[b]
            # BFS to enumerate all shortest arrow sequences from (ar,ac) to (br,bc)
            from collections import deque

            q = deque()
            q.append((ar, ac))
            dist = {(ar, ac): 0}
            parents: Dict[Tuple[int, int], List[Tuple[Tuple[int, int], str]]] = {
                (ar, ac): []
            }
            directions = [(-1, 0, "^"), (1, 0, "v"), (0, -1, "<"), (0, 1, ">")]
            rows, cols = len(grid), len(grid[0])
            while q:
                r, c = q.popleft()
                for dr, dc, ch in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] is not None:
                        nd = dist[(r, c)] + 1
                        if (nr, nc) not in dist:
                            dist[(nr, nc)] = nd
                            parents[(nr, nc)] = [((r, c), ch)]
                            q.append((nr, nc))
                        else:
                            if nd == dist[(nr, nc)]:
                                parents[(nr, nc)].append(((r, c), ch))
            if (br, bc) not in dist:
                result[(a, b)] = [] if a != b else ["A"]
                continue
            # Reconstruct all shortest arrow strings by DFS from end to start
            dist[(br, bc)]
            memo_paths: Dict[Tuple[int, int], List[str]] = {}

            def collect(node: Tuple[int, int]) -> List[str]:
                if node == (ar, ac):
                    return [""]
                if node in memo_paths:
                    return memo_paths[node]
                res: List[str] = []
                for (pr, pc), ch in parents.get(node, []):
                    for p in collect((pr, pc)):
                        res.append(p + ch)
                memo_paths[node] = res
                return res

            arrows = collect((br, bc))
            uniq = sorted(set(arrows))
            result[(a, b)] = (
                [s + "A" for s in uniq] if uniq else (["A"] if a == b else [])
            )
    return result


DIR_SHORTEST = shortest_sequences(DIR_GRID, DIR_POS)
NUM_SHORTEST = shortest_sequences(NUM_GRID, NUM_POS)


def build_preferred_table(
    grid: List[List[str]], pos: Dict[str, Tuple[int, int]], gap: Tuple[int, int]
) -> Dict[Tuple[str, str], List[str]]:
    def crosses_gap_horiz(row: int, c1: int, c2: int) -> bool:
        gr, gc = gap
        if row != gr:
            return False
        lo, hi = (c1, c2) if c1 <= c2 else (c2, c1)
        return lo <= gc <= hi

    out: Dict[Tuple[str, str], List[str]] = {}
    keys = list(pos.keys())
    for a in keys:
        for b in keys:
            if a == b:
                out[(a, b)] = ["A"]
                continue
            ar, ac = pos[a]
            br, bc = pos[b]
            horiz = ["<"] * (ac - bc) if ac > bc else [">"] * (bc - ac)
            vert = ["^"] * (ar - br) if ar > br else ["v"] * (br - ar)
            first = None
            if not crosses_gap_horiz(ar, ac, bc):
                first = horiz + vert
            elif not crosses_gap_horiz(br, ac, bc):
                first = vert + horiz
            else:
                first = vert + horiz
            out[(a, b)] = ["".join(first + ["A"])]
    return out


DIR_SHORTEST = shortest_sequences(DIR_GRID, DIR_POS)
NUM_SHORTEST = shortest_sequences(NUM_GRID, NUM_POS)


def ensure_sequences(
    grid: List[List[str]],
    pos: Dict[str, Tuple[int, int]],
    table: Dict[Tuple[str, str], List[str]],
) -> Dict[Tuple[str, str], List[str]]:
    """
    Ensure at least one sequence exists for trivial pairs (a == b -> 'A').
    If a pair is missing, try to construct horizontal/vertical routes that avoid the gap.
    Makes the tables robust for edge cases.
    """
    out: Dict[Tuple[str, str], List[str]] = {}
    keys = list(pos.keys())
    for a in keys:
        for b in keys:
            seqs = table.get((a, b), [])
            if seqs or a == b:
                out[(a, b)] = seqs if seqs else ["A"]
                continue
            ar, ac = pos[a]
            br, bc = pos[b]
            dr = br - ar
            dc = bc - ac
            horiz = ["<"] * (-dc) if dc < 0 else [">"] * dc
            vert = ["^"] * (-dr) if dr < 0 else ["v"] * dr
            candidates: List[List[str]] = []
            if simulate_path(grid, (ar, ac), horiz + vert):
                candidates.append(horiz + vert + ["A"])
            if simulate_path(grid, (ar, ac), vert + horiz):
                candidates.append(vert + horiz + ["A"])
            if candidates:
                uniq = sorted(set("".join(m) for m in candidates))
                out[(a, b)] = uniq
            else:
                out[(a, b)] = []
    return out


DIR_SHORTEST = ensure_sequences(DIR_GRID, DIR_POS, DIR_SHORTEST)
NUM_SHORTEST = ensure_sequences(NUM_GRID, NUM_POS, NUM_SHORTEST)


def build_dir_costs(max_depth: int) -> Dict[int, Dict[Tuple[str, str], int]]:
    """
    Depth DP for directional keypad transitions.
    - depth = 0: cost equals the length of the minimal sequence (including the final 'A').
    - depth > 0: cost is obtained by expanding each arrow via the costs of the previous layer.
    - Uses a large INF to prevent real values from colliding with the sentinel.
    """
    costs: Dict[int, Dict[Tuple[str, str], int]] = {}
    base: Dict[Tuple[str, str], int] = {}
    for pair, seqs in DIR_SHORTEST.items():
        base[pair] = min((len(s) for s in seqs), default=10**9)
    costs[0] = base
    for d in range(1, max_depth + 1):
        layer: Dict[Tuple[str, str], int] = {}
        for pair, seqs in DIR_SHORTEST.items():
            if not seqs:
                layer[pair] = 10**9
                continue
            best = 10**30
            for s in seqs:
                cur = "A"
                total = 0
                for ch in s:
                    total += costs[d - 1][(cur, ch)]
                    cur = ch
                if total < best:
                    best = total
            layer[pair] = best
        costs[d] = layer
    return costs


def build_num_costs(
    depth: int, dir_costs: Dict[int, Dict[Tuple[str, str], int]]
) -> Dict[Tuple[str, str], int]:
    """
    Compute numeric keypad transition costs (a -> b) using directional sequences
    at the given depth. Starts at 'A'.
    """
    out: Dict[Tuple[str, str], int] = {}
    for pair, seqs in NUM_SHORTEST.items():
        if not seqs:
            out[pair] = 10**9
            continue
        best = 10**30
        for s in seqs:
            cur = "A"
            total = 0
            for ch in s:
                total += dir_costs[depth][(cur, ch)]
                cur = ch
            if total < best:
                best = total
        out[pair] = best
    return out


def minimal_presses_for_code(code: str, depth: int) -> int:
    """
    Compute the minimal button presses to produce 'code' with a chain of 'depth'
    directional keypads above the numeric keypad.
    - Maintains the current pointer on the top directional keypad (cur_dir),
      chooses the sequence that minimizes cost for each numeric transition,
      and updates the final pointer position (no reset between characters).
    """
    dir_costs = build_dir_costs(depth)
    cur_num = "A"
    cur_dir = "A"
    total = 0
    for ch in code:
        seqs = NUM_SHORTEST[(cur_num, ch)]
        best = 10**30
        best_end_dir = cur_dir
        for s in seqs:
            p = cur_dir
            cost = 0
            for dch in s:
                cost += dir_costs[depth][(p, dch)]
                p = dch
            if cost < best:
                best = cost
                best_end_dir = p
        total += best
        cur_dir = best_end_dir
        cur_num = ch
    return total


def main():
    """
    I/O:
    - Read 'day21.txt' and compute:
      Part 1: depth = 1 (one directional keypad)
      Part 2: depth = 24 (24 directional keypads between your keypad and the numeric)
    - Print the required sum of complexities for both parts.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day21.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    codes = load_codes(content)
    # Quick sanity on tables
    empty_dir = [k for k, v in DIR_SHORTEST.items() if not v]
    empty_num = [k for k, v in NUM_SHORTEST.items() if not v]
    if empty_dir or empty_num:
        print("WARN: empty sequences found")
        print(f"DIR empty: {len(empty_dir)} examples: {empty_dir[:5]}")
        print(f"NUM empty: {len(empty_num)} examples: {empty_num[:5]}")
    part1 = sum(
        minimal_presses_for_code(code, 1) * numeric_value(code) for code in codes
    )
    part2 = sum(
        minimal_presses_for_code(code, 24) * numeric_value(code) for code in codes
    )
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 21: Keypad Conundrum")
    print("=" * 70)
    print(f"Part 1 - Sum of complexities: {part1}")
    print(f"Part 2 - Sum of complexities: {part2}")
    print("=" * 70)


if __name__ == "__main__":
    main()
