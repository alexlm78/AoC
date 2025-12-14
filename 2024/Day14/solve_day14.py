#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 14: Restroom Redoubt

Part 1:
- Simulate robot positions after T seconds (wrapping on a WxH grid)
- Count robots in the four quadrants (exclude middle row/column)
- Safety factor = product of quadrant counts

Part 2:
- Find the second t in [0, lcm(W, H)) where robots form the most "compact" picture
- Heuristic: minimize bounding box area of robot positions
- Print the time and a visualization of the grid at that time
"""

import os
from typing import List, Tuple
from math import gcd


def parse_input(text: str) -> List[Tuple[int, int, int, int]]:
    """
    Parse robot positions and velocities from lines 'p=x,y v=dx,dy'.
    Args:
        text: Input lines
    Returns:
        List of tuples (x, y, dx, dy) for each robot
    """
    robots: List[Tuple[int, int, int, int]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Format: p=0,4 v=3,-3
        left, right = line.split()
        px, py = left.split("=")[1].split(",")
        vx, vy = right.split("=")[1].split(",")
        robots.append((int(px), int(py), int(vx), int(vy)))
    return robots


def step_position(
    x: int, y: int, dx: int, dy: int, t: int, width: int, height: int
) -> Tuple[int, int]:
    """
    Compute position after t seconds with wrap-around on a width x height grid.
    Args:
        x, y: Initial position
        dx, dy: Velocity per second
        t: Seconds to advance
        width, height: Grid dimensions
    Returns:
        (x', y') wrapped position
    """
    nx = (x + dx * t) % width
    ny = (y + dy * t) % height
    return nx, ny


def safety_factor_after_t(
    robots: List[Tuple[int, int, int, int]], t: int, width: int, height: int
) -> int:
    """
    Compute safety factor after t seconds:
    - Exclude robots on middle row/column
    - Count in the four quadrants
    - Return product of counts
    """
    mid_x = width // 2
    mid_y = height // 2
    q1 = q2 = q3 = q4 = 0
    for x, y, dx, dy in robots:
        nx, ny = step_position(x, y, dx, dy, t, width, height)
        if nx == mid_x or ny == mid_y:
            continue
        if nx < mid_x and ny < mid_y:
            q1 += 1
        elif nx > mid_x and ny < mid_y:
            q2 += 1
        elif nx < mid_x and ny > mid_y:
            q3 += 1
        elif nx > mid_x and ny > mid_y:
            q4 += 1
    return q1 * q2 * q3 * q4


def lcm(a: int, b: int) -> int:
    """Least common multiple"""
    return a // gcd(a, b) * b


def bounding_box_area(positions: List[Tuple[int, int]]) -> int:
    """
    Compute area of the minimal axis-aligned bounding box covering positions.
    Args:
        positions: List of (x, y)
    Returns:
        Area as (max_x - min_x + 1) * (max_y - min_y + 1)
    """
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)


def render_grid(positions: List[Tuple[int, int]], width: int, height: int) -> str:
    """
    Render robots on a WxH grid, '.' for empty and '#' for robot.
    Args:
        positions: List of (x, y)
        width, height: Grid dimensions
    Returns:
        String representation of the grid
    """
    grid = [["." for _ in range(width)] for _ in range(height)]
    for x, y in positions:
        grid[y][x] = "#"
    return "\n".join("".join(row) for row in grid)


def find_most_compact_time(
    robots: List[Tuple[int, int, int, int]], width: int, height: int
) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Search t in [0, lcm(width,height)) for time with minimal bounding box area.
    Args:
        robots: Robot definitions
        width, height: Grid dimensions
    Returns:
        (best_t, positions_at_best_t)
    """
    period = lcm(width, height)
    best_t = 0
    best_area = None
    best_positions: List[Tuple[int, int]] = []
    for t in range(period):
        positions = [
            step_position(x, y, dx, dy, t, width, height) for x, y, dx, dy in robots
        ]
        area = bounding_box_area(positions)
        if best_area is None or area < best_area:
            best_area = area
            best_t = t
            best_positions = positions
    return best_t, best_positions


def largest_component_size(positions: List[Tuple[int, int]]) -> int:
    """
    Compute the size of the largest connected component (4-neighborhood).
    """
    pos_set = set(positions)
    visited = set()
    best = 0
    for p in pos_set:
        if p in visited:
            continue
        stack = [p]
        visited.add(p)
        size = 0
        while stack:
            x, y = stack.pop()
            size += 1
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if (nx, ny) in pos_set and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny))
        if size > best:
            best = size
    return best


def find_most_tree_like_time(
    robots: List[Tuple[int, int, int, int]], width: int, height: int
) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Search t in [0, lcm(width,height)) for time with maximal largest connected component.
    Ties broken by choosing the smallest bounding box area, then smallest t.
    """
    period = lcm(width, height)
    best_t = 0
    best_comp = -1
    best_area = None
    best_positions: List[Tuple[int, int]] = []
    for t in range(period):
        positions = [
            step_position(x, y, dx, dy, t, width, height) for x, y, dx, dy in robots
        ]
        comp = largest_component_size(positions)
        area = bounding_box_area(positions)
        if (
            comp > best_comp
            or (comp == best_comp and (best_area is None or area < best_area))
            or (comp == best_comp and area == best_area and t < best_t)
        ):
            best_comp = comp
            best_area = area
            best_t = t
            best_positions = positions
    return best_t, best_positions


def verify_example() -> None:
    """
    Verify the small example safety factor after 100 seconds.
    Example space: width=11, height=7; expected safety factor = 12.
    """
    example = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    robots = parse_input(example)
    sf = safety_factor_after_t(robots, 100, width=11, height=7)
    print("=" * 70)
    print("VERIFYING EXAMPLE (Day 14 - Part 1)")
    print("=" * 70)
    print(f"Safety factor after 100s: {sf} (expected 12) -> Match: {sf == 12}")
    print("=" * 70)


def main() -> None:
    """
    Load input robots and compute:
    - Part 1: safety factor after 100 seconds on 101x103 grid
    - Part 2: time with most compact bounding box and render the grid
    Prints results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day14.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    robots = parse_input(content)

    width, height = 101, 103
    sf = safety_factor_after_t(robots, 100, width, height)

    compact_t, compact_positions = find_most_compact_time(robots, width, height)
    tree_t, tree_positions = find_most_tree_like_time(robots, width, height)
    picture = render_grid(tree_positions, width, height)

    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 14: Restroom Redoubt")
    print("=" * 70)
    print(f"Part 1 - Safety factor after 100s: {sf}")
    print(f"Part 2 - Most compact time (bbox): t = {compact_t}")
    print(f"Part 2 - Most tree-like time (largest cluster): t = {tree_t}")
    print("Part 2 - Grid at tree-like t:")
    print(picture)
    print("=" * 70)


if __name__ == "__main__":
    verify_example()
    main()
