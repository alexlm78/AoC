import sys
import re


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return

    clay = set()
    for line in lines:
        # x=495, y=2..7 or y=7, x=495..501
        if line.startswith("x="):
            # x=V, y=S..E
            m = re.match(r"x=(\d+), y=(\d+)\.\.(\d+)", line)
            x = int(m.group(1))
            y_start = int(m.group(2))
            y_end = int(m.group(3))
            for y in range(y_start, y_end + 1):
                clay.add((x, y))
        else:
            # y=V, x=S..E
            m = re.match(r"y=(\d+), x=(\d+)\.\.(\d+)", line)
            y = int(m.group(1))
            x_start = int(m.group(2))
            x_end = int(m.group(3))
            for x in range(x_start, x_end + 1):
                clay.add((x, y))

    if not clay:
        print("No clay found")
        return

    min_y = min(c[1] for c in clay)
    max_y = max(c[1] for c in clay)
    min_x = min(c[0] for c in clay)
    max_x = max(c[0] for c in clay)

    # We need a grid. Let's make it wide enough.
    # Water starts at 500.
    # We should handle x dynamically or just make a large enough array.
    # To be safe, let's use a dictionary or a large array with offset.
    # Dictionary might be slower but easier for sparse.
    # Actually, 2D list is faster for frequent access.
    # x range: min_x can be around 0? Input usually centered around 500.
    # Let's check min_x and max_x from input to be sure.

    padding = 200  # Allow flow to spread
    offset_x = min_x - padding
    width = max_x - min_x + 2 * padding
    height = max_y + 2

    # Grid codes: .: 0, #: 1, |: 2, ~: 3
    # Using chars is easier for debugging
    grid = [["." for _ in range(width)] for _ in range(height)]

    for cx, cy in clay:
        grid[cy][cx - offset_x] = "#"

    sys.setrecursionlimit(10000)

    def get(x, y):
        if 0 <= x < width and 0 <= y < height:
            return grid[y][x]
        return "."  # Treat out of bounds as sand/void

    def set_cell(x, y, val):
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = val

    def fall(x, y):
        # Mark visited/flowing
        set_cell(x, y, "|")

        if y >= max_y:
            return

        below = get(x, y + 1)

        if below == ".":
            fall(x, y + 1)
            below = get(x, y + 1)  # Re-check after return

        if below == "#" or below == "~":
            # Hit solid ground, try to spread
            l = x  # noqa: E741
            r = x

            # Scan left
            while True:
                curr = get(l, y)
                down = get(l, y + 1)
                if curr == "#":  # Hit wall to the left
                    break
                if down not in ["#", "~"]:  # Found a drop
                    break
                l -= 1  # noqa: E741

            # Scan right
            while True:
                curr = get(r, y)
                down = get(r, y + 1)
                if curr == "#":  # Hit wall to the right
                    break
                if down not in ["#", "~"]:  # Found a drop
                    break
                r += 1

            # Identify boundaries
            # If loop broke because curr == '#', then we are bounded.
            # But wait, the loop variable l decrements.
            # If get(l, y) == '#', then the wall is at l. The water goes up to l+1.
            # So the range of water is l+1 .. r-1.

            left_wall = get(l, y) == "#"
            right_wall = get(r, y) == "#"

            if left_wall and right_wall:
                # Settle
                for k in range(l + 1, r):
                    set_cell(k, y, "~")
            else:
                # Flow
                for k in range(
                    l if not left_wall else l + 1, r if not right_wall else r
                ):
                    set_cell(k, y, "|")

                # Recurse down at edges
                if not left_wall:
                    fall(l, y)  # Start fall from the drop point
                if not right_wall:
                    fall(r, y)

    # Re-checking the scan logic:
    # `l` loop:
    # Start l=x.
    # Check `grid[l][y]`? No, we are moving in `y` row.
    # We walk left as long as we are NOT in a wall and we HAVE support.
    # Actually, we mark '|' as we go?
    # The `fall` function marks `x, y`.
    # When spreading, we should mark '|' unless we settle.

    # Revised logic:
    # 1. Find boundaries first without modifying grid (except maybe temp).
    # 2. If bounded, fill '~'.
    # 3. If not bounded, fill '|' and recurse.

    # Correct scan loop:
    # Start l = x
    # While grid[y][l-1] != '#' and (grid[y+1][l] in '#~'):
    #    l -= 1
    # Check left condition:
    # if grid[y+1][l] not in '#~': we found a drop at l.
    # else: we hit a wall at l-1.

    # Let's write the `fall` function carefully.

    def fall_recursive(x, y):
        set_cell(x, y, "|")
        if y >= max_y:
            return

        if get(x, y + 1) == ".":
            fall_recursive(x, y + 1)

        # After return, or if it was already solid
        if get(x, y + 1) in ["#", "~"]:
            # Spread
            l = x  # noqa: E741
            while get(l - 1, y) != "#" and get(l, y + 1) in ["#", "~"]:
                l -= 1  # noqa: E741

            r = x
            while get(r + 1, y) != "#" and get(r, y + 1) in ["#", "~"]:
                r += 1

            get(l - 1, y) == "#"
            get(r + 1, y) == "#"

            get(l, y + 1) in ["#", "~"]
            get(r, y + 1) in ["#", "~"]

            # If we stopped going left because of support loss, left_supported is False (at l).
            # Wait, the loop condition `get(l, y+1) in ['#', '~']` ensures that for the current l, we ARE supported.
            # So if the loop terminates, it's either because:
            # 1. `get(l-1, y) == '#'` -> Wall to the left. We are at l. Supported at l.
            # 2. `get(l, y+1)` NOT in ['#', '~'] -> Wait, loop runs while supported.
            # So if we exit the loop, it means EITHER `get(l-1, y) == '#'` OR `get(l, y+1)` is NOT supported?
            # No, if `get(l, y+1)` is NOT supported, the loop wouldn't have entered for this `l`?
            # Actually, we start at `x`. `x` is supported (checked before).
            # So we move left.

            # Correct Loop:
            # l = x
            # while get(l-1, y) != '#' and get(l, y+1) in ['#', '~']:
            #    l -= 1
            #
            # Case 1: Stopped because `get(l-1, y) == '#'`.
            #    We are at `l`. `l` is supported. `l-1` is wall. -> Bounded left.
            # Case 2: Stopped because `get(l, y+1)` NOT in ['#', '~'].
            #    Wait, loop checks `get(l, y+1)`. If it is false, we don't decrement.
            #    So we are at `l`. `l` is NOT supported?
            #    If `l=x`, and `x` is supported, loop runs?
            #    If `x` is supported, `get(x, y+1)` is true.
            #    Then we check `get(x-1, y)`. If not wall, we decrement l to x-1.
            #    Then we check `get(l, y+1)` i.e. `get(x-1, y+1)`.
            #    If that is NOT supported, we stop.
            #    So `l` is `x-1`. It is NOT supported.
            #    So we spill at `l`.

            # Wait, my loop structure:
            # while get(l-1, y) != '#' and get(l-1, y+1) in ['#', '~']:
            #    l -= 1
            # That checks if the NEXT step is valid.

            l = x  # noqa: E741
            while get(l - 1, y) != "#" and get(l, y + 1) in ["#", "~"]:
                l -= 1  # noqa: E741
            # If we stopped, check why.
            # If get(l, y+1) not supported -> Spill at l.
            # Else (supported), then get(l-1, y) == '#' -> Wall.

            # Actually, if `get(l, y+1)` is not supported, it means we reached an edge at `l`.
            # So `l` is the spill point.

            # Let's trace carefully.
            # Start x. Supported.
            # Check x-1. If wall, stop. l=x.
            # If not wall, check support at x. (Already checked).
            # Wait, we need to check support at x-1 to move there?
            # If x-1 has floor, we move there.
            # If x-1 has NO floor, we move there AND STOP, because it's a spill point.

            # Loop:
            # l = x
            # while get(l-1, y) != '#':
            #     l -= 1
            #     if get(l, y+1) not in ['#', '~']:
            #         break

            # After loop:
            # If get(l, y+1) not in ['#', '~']: Spill at l.
            # Else: Wall at l-1.

            l = x  # noqa: E741
            while get(l - 1, y) != "#":
                # Try moving left
                if get(l, y + 1) not in ["#", "~"]:
                    break  # Current l is a spill point
                l -= 1  # noqa: E741
                if get(l, y + 1) not in ["#", "~"]:
                    break  # Moved to l, found it's a spill point

            # Wait, the first check `if get(l, y+1)` inside loop is redundant if we check before decrement?
            # Let's simplify:

            # Scan Left
            l = x  # noqa: E741
            while get(l - 1, y) != "#" and get(l, y + 1) in ["#", "~"]:
                l -= 1  # noqa: E741
            # Now we are at l.
            # If get(l, y+1) is not supported, we spilled at l.
            # Else, we are supported at l, so we must have hit a wall at l-1.

            left_open = get(l, y + 1) not in ["#", "~"]

            # Scan Right
            r = x
            while get(r + 1, y) != "#" and get(r, y + 1) in ["#", "~"]:
                r += 1
            right_open = get(r, y + 1) not in ["#", "~"]

            if not left_open and not right_open:
                # Bounded
                for k in range(l, r + 1):
                    set_cell(k, y, "~")
            else:
                # Flow
                for k in range(l, r + 1):
                    set_cell(k, y, "|")
                if left_open:
                    fall_recursive(l, y)  # Will fall down from l immediately
                if right_open:
                    fall_recursive(r, y)

    # Start simulation
    fall_recursive(500 - offset_x, 0)

    # Count
    # "How many tiles can the water reach within the range of y values in your scan?"
    # Range is min_y to max_y (inclusive).

    count = 0
    count_rest = 0
    for y in range(min_y, max_y + 1):
        for x in range(width):
            if grid[y][x] in ["|", "~"]:
                count += 1
            if grid[y][x] == "~":
                count_rest += 1

    print(f"Part 1 Result: {count}")
    print(f"Part 2 Result: {count_rest}")

    # Check if grid dump is needed for debugging
    # with open('debug_grid.txt', 'w') as f:
    #     for row in grid:
    #         f.write("".join(row) + "\n")


if __name__ == "__main__":
    solve()
