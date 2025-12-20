def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return

    grid = [list(line) for line in lines]
    height = len(grid)
    width = len(grid[0])

    def get_neighbors(x, y, current_grid):
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    neighbors.append(current_grid[ny][nx])
        return neighbors

    def step(current_grid):
        new_grid = [["" for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                cell = current_grid[y][x]
                neighbors = get_neighbors(x, y, current_grid)

                trees = neighbors.count("|")
                lumberyards = neighbors.count("#")

                if cell == ".":
                    if trees >= 3:
                        new_grid[y][x] = "|"
                    else:
                        new_grid[y][x] = "."
                elif cell == "|":
                    if lumberyards >= 3:
                        new_grid[y][x] = "#"
                    else:
                        new_grid[y][x] = "|"
                elif cell == "#":
                    if lumberyards >= 1 and trees >= 1:
                        new_grid[y][x] = "#"
                    else:
                        new_grid[y][x] = "."
        return new_grid

    # Part 1: 10 minutes
    # Part 2: 1000000000 minutes

    current_grid = [row[:] for row in grid]
    seen_states = {}
    history = []

    total_minutes = 1000000000

    for minute in range(1, total_minutes + 1):
        current_grid = step(current_grid)

        # Serialize grid for state tracking
        state = "\n".join("".join(row) for row in current_grid)

        if minute == 10:
            tree_count = sum(row.count("|") for row in current_grid)
            lumberyard_count = sum(row.count("#") for row in current_grid)
            print(f"Part 1 Result: {tree_count * lumberyard_count}")

        if state in seen_states:
            prev_minute = seen_states[state]
            period = minute - prev_minute
            remaining = total_minutes - minute
            offset = remaining % period

            # The result is at prev_minute + offset
            target_minute = prev_minute + offset

            # We can retrieve the grid from history (0-indexed, so index is minute-1)
            final_state_str = history[target_minute - 1]

            # Count resources from the final state string
            final_tree_count = final_state_str.count("|")
            final_lumberyard_count = final_state_str.count("#")

            print(f"Part 2 Result: {final_tree_count * final_lumberyard_count}")
            return

        seen_states[state] = minute
        history.append(state)

    # Fallback if loop finishes without cycle (unlikely for 1B)
    tree_count = sum(row.count("|") for row in current_grid)
    lumberyard_count = sum(row.count("#") for row in current_grid)

    print(f"Final Result: {tree_count * lumberyard_count}")


if __name__ == "__main__":
    solve()
