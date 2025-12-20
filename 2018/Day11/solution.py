def get_power_level(x, y, serial_number):
    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    power = (power // 100) % 10
    power -= 5
    return power


def solve():
    try:
        with open("input.txt", "r") as f:
            content = f.read().strip()
            if not content:
                print("Error: input.txt is empty. Please provide a serial number.")
                serial_number = 18
                print(f"Running with EXAMPLE serial number: {serial_number}")
            else:
                serial_number = int(content)
                print(f"Running with serial number: {serial_number}")
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    grid_size = 300
    # Grid for individual power levels (1-based indexing for convenience, 0-row/col unused)
    grid = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]

    # Calculate power levels
    for y in range(1, grid_size + 1):
        for x in range(1, grid_size + 1):
            grid[y][x] = get_power_level(x, y, serial_number)

    # Build Summed-Area Table (SAT)
    # sat[y][x] contains sum of all cells in rectangle defined by (1,1) to (x,y) inclusive
    sat = [[0] * (grid_size + 1) for _ in range(grid_size + 1)]

    for y in range(1, grid_size + 1):
        for x in range(1, grid_size + 1):
            sat[y][x] = grid[y][x] + sat[y - 1][x] + sat[y][x - 1] - sat[y - 1][x - 1]

    def get_square_power(x, y, size):
        x0, y0 = x - 1, y - 1
        x1, y1 = x + size - 1, y + size - 1
        return sat[y1][x1] - sat[y0][x1] - sat[y1][x0] + sat[y0][x0]

    # Part 1: Fixed size 3
    max_power_p1 = -float("inf")
    best_coord_p1 = (0, 0)

    for y in range(1, grid_size - 2):
        for x in range(1, grid_size - 2):
            total_power = get_square_power(x, y, 3)
            if total_power > max_power_p1:
                max_power_p1 = total_power
                best_coord_p1 = (x, y)

    print(
        f"Part 1 Best 3x3: {best_coord_p1[0]},{best_coord_p1[1]} (Power: {max_power_p1})"
    )

    # Part 2: Any size
    max_power_p2 = -float("inf")
    best_identifier_p2 = (0, 0, 0)

    # We can iterate size.
    # Optimization: If max power for a size starts dropping significantly or is negative for too long, maybe break?
    # But with SAT, brute force over all sizes is acceptable (300^3 ~ 27M ops).

    for size in range(1, grid_size + 1):
        for y in range(1, grid_size - size + 2):
            for x in range(1, grid_size - size + 2):
                total_power = get_square_power(x, y, size)

                if total_power > max_power_p2:
                    max_power_p2 = total_power
                    best_identifier_p2 = (x, y, size)

    print(
        f"Part 2 Best Square: {best_identifier_p2[0]},{best_identifier_p2[1]},{best_identifier_p2[2]} (Power: {max_power_p2})"
    )


if __name__ == "__main__":
    solve()
