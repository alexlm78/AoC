#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 13: Claw Contraption

Part 1:
- For each machine, find non-negative integers (a, b) such that:
    ax*a + bx*b = px
    ay*a + by*b = py
  with a, b <= 100
- Cost = 3*a + 1*b; choose minimal cost per solvable machine
- Sum costs across all solvable machines

Part 2:
- Prize coordinates are corrected by adding OFFSET = 10000000000000 to both X and Y
- No press limit; solve linear system exactly for integer (a, b) if possible
- Cost = 3*a + 1*b; sum across solvable machines
"""

import os
import re
from typing import List, Tuple, Optional


def parse_input(text: str) -> List[Tuple[int, int, int, int, int, int]]:
    """
    Parse machines from the input text.
    Args:
        text: Blocks with Button A/B and Prize lines
    Returns:
        List of tuples (ax, ay, bx, by, px, py)
    """
    blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    machines: List[Tuple[int, int, int, int, int, int]] = []
    for b in blocks:
        lines = b.splitlines()
        # Example line formats:
        # Button A: X+94, Y+34
        # Button B: X+22, Y+67
        # Prize: X=8400, Y=5400
        a_match = re.search(r"Button A:\s*X\+(\d+),\s*Y\+(\d+)", lines[0])
        b_match = re.search(r"Button B:\s*X\+(\d+),\s*Y\+(\d+)", lines[1])
        p_match = re.search(r"Prize:\s*X=(\d+),\s*Y=(\d+)", lines[2])
        if not (a_match and b_match and p_match):
            raise ValueError(f"Invalid machine block:\n{b}")
        ax, ay = int(a_match.group(1)), int(a_match.group(2))
        bx, by = int(b_match.group(1)), int(b_match.group(2))
        px, py = int(p_match.group(1)), int(p_match.group(2))
        machines.append((ax, ay, bx, by, px, py))
    return machines


def solve_min_cost_part1(machine: Tuple[int, int, int, int, int, int]) -> Optional[int]:
    """
    Brute-force within press limit (<= 100) to find minimal cost solution if any.
    Args:
        machine: (ax, ay, bx, by, px, py)
    Returns:
        Minimal token cost or None if unsolvable
    """
    ax, ay, bx, by, px, py = machine
    best = None
    for a in range(0, 101):
        # Compute b from X equation; must match Y equation too
        rem_x = px - ax * a
        if rem_x < 0:
            continue
        if rem_x % bx != 0:
            continue
        b = rem_x // bx
        if b < 0 or b > 100:
            continue
        if ay * a + by * b != py:
            continue
        cost = 3 * a + b
        if best is None or cost < best:
            best = cost
    return best


def solve_min_cost_part2(machine: Tuple[int, int, int, int, int, int]) -> Optional[int]:
    """
    Exact linear solve with prize offset; integers only; no press limit.
    Args:
        machine: (ax, ay, bx, by, px, py)
    Returns:
        Minimal token cost or None if unsolvable
    """
    OFFSET = 10_000_000_000_000
    ax, ay, bx, by, px, py = machine
    px += OFFSET
    py += OFFSET
    # Solve:
    # [ax bx] [a] = [px]
    # [ay by] [b]   [py]
    D = ax * by - ay * bx
    if D == 0:
        # Collinear moves; skip for simplicity
        return None
    num_a = px * by - py * bx
    num_b = ax * py - ay * px
    if num_a % D != 0 or num_b % D != 0:
        return None
    a = num_a // D
    b = num_b // D
    if a < 0 or b < 0:
        return None
    return 3 * a + b


def verify_example() -> None:
    """
    Verify the sample from the problem statement for Part 1.
    Expected: total minimal tokens = 480 across solvable machines.
    """
    example = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    machines = parse_input(example)
    total = 0
    wins = 0
    for m in machines:
        cost = solve_min_cost_part1(m)
        if cost is not None:
            total += cost
            wins += 1
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 13 - Part 1)")
    print("=" * 70)
    print(f"Solvable machines: {wins} (expected 2) -> Match: {wins == 2}")
    print(f"Total minimal tokens: {total} (expected 480) -> Match: {total == 480}")
    print("=" * 70)


def main() -> None:
    """
    Load input machines and compute:
    - Part 1: minimal tokens across solvable machines with press limit 100
    - Part 2: minimal tokens across solvable machines with prize offset 1e13
    Prints both results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day13.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    machines = parse_input(content)

    total_p1 = 0
    wins_p1 = 0
    for m in machines:
        cost = solve_min_cost_part1(m)
        if cost is not None:
            total_p1 += cost
            wins_p1 += 1

    total_p2 = 0
    wins_p2 = 0
    for m in machines:
        cost = solve_min_cost_part2(m)
        if cost is not None:
            total_p2 += cost
            wins_p2 += 1

    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 13: Claw Contraption")
    print("=" * 70)
    print(f"Part 1 - Solvable machines: {wins_p1}, Minimal tokens: {total_p1}")
    print(f"Part 2 - Solvable machines: {wins_p2}, Minimal tokens (offset): {total_p2}")
    print("=" * 70)


if __name__ == "__main__":
    verify_example()
    main()
