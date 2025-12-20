def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        coordinates = []
        for line in lines:
            x, y = map(int, line.strip().split(", "))
            coordinates.append((x, y))

        # Determine the grid boundaries
        min_x = min(c[0] for c in coordinates)
        max_x = max(c[0] for c in coordinates)
        min_y = min(c[1] for c in coordinates)
        max_y = max(c[1] for c in coordinates)

        # Mapping from coordinate index to area size
        area_sizes = {i: 0 for i in range(len(coordinates))}
        infinite_areas = set()

        # Iterate over the grid
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                min_dist = float("inf")
                closest_coord = -1

                for i, (cx, cy) in enumerate(coordinates):
                    dist = manhattan_distance((x, y), (cx, cy))
                    if dist < min_dist:
                        min_dist = dist
                        closest_coord = i
                    elif dist == min_dist:
                        closest_coord = -1  # Tie

                if closest_coord != -1:
                    area_sizes[closest_coord] += 1

                    # If a point is on the boundary, its area is considered infinite
                    if x == min_x or x == max_x or y == min_y or y == max_y:
                        infinite_areas.add(closest_coord)

        # Filter out infinite areas and find the max size
        max_area = 0
        for i, size in area_sizes.items():
            if i not in infinite_areas:
                if size > max_area:
                    max_area = size

        print(f"Largest finite area: {max_area}")

        # Part 2
        limit = 10000
        region_size = 0
        # Calculate a safe margin to expand the search grid
        # If we are outside the bounding box by 'k' units, the total distance increases by at least k * len(coordinates)
        # So k < limit / len(coordinates)
        margin = limit // len(coordinates) + 1

        for x in range(min_x - margin, max_x + margin + 1):
            for y in range(min_y - margin, max_y + margin + 1):
                total_dist = 0
                for cx, cy in coordinates:
                    total_dist += abs(x - cx) + abs(y - cy)
                    if total_dist >= limit:
                        break

                if total_dist < limit:
                    region_size += 1

        print(f"Region size: {region_size}")

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
