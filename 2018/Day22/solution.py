import sys
import heapq

# Set recursion limit higher just in case
sys.setrecursionlimit(20000)


def solve():
    depth = 11394
    target_x, target_y = 7, 701

    # Memoization for erosion levels
    erosion_cache = {}

    def get_erosion_level(x, y):
        if (x, y) in erosion_cache:
            return erosion_cache[(x, y)]

        geo_index = 0
        if (x, y) == (0, 0):
            geo_index = 0
        elif (x, y) == (target_x, target_y):
            geo_index = 0
        elif y == 0:
            geo_index = x * 16807
        elif x == 0:
            geo_index = y * 48271
        else:
            geo_index = get_erosion_level(x - 1, y) * get_erosion_level(x, y - 1)

        erosion_level = (geo_index + depth) % 20183
        erosion_cache[(x, y)] = erosion_level
        return erosion_level

    # Part 1
    total_risk = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            el = get_erosion_level(x, y)
            risk = el % 3
            total_risk += risk

    print(f"Part 1 Result: {total_risk}")

    # Part 2
    # Tools: 0=Neither, 1=Torch, 2=Climbing Gear
    # Regions: 0=Rocky, 1=Wet, 2=Narrow
    # Valid tools for region type T: {0, 1, 2} - {T}
    # Target is Rocky (0), so valid tools are {1, 2}. Start with Torch (1). End with Torch (1).

    # Dijkstra
    # State: (time, x, y, tool)
    queue = [(0, 0, 0, 1)]
    best_time = {}  # (x, y, tool) -> time
    best_time[(0, 0, 1)] = 0

    while queue:
        time, x, y, tool = heapq.heappop(queue)

        # Pruning: if we found a faster way to this state already
        if time > best_time.get((x, y, tool), float("inf")):
            continue

        if (x, y) == (target_x, target_y) and tool == 1:
            print(f"Part 2 Result: {time}")
            break

        # Current region type
        current_type = get_erosion_level(x, y) % 3

        # 1. Switch Tool
        for next_tool in range(3):
            if next_tool != tool and next_tool != current_type:
                # Can switch to next_tool
                new_time = time + 7
                if new_time < best_time.get((x, y, next_tool), float("inf")):
                    best_time[(x, y, next_tool)] = new_time
                    heapq.heappush(queue, (new_time, x, y, next_tool))

        # 2. Move
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue

            # Heuristic pruning to avoid exploring too far
            # Increased buffer to 100
            if nx > target_x + 100 or ny > target_y + 100:
                continue

            # Check if valid tool for new region
            next_type = get_erosion_level(nx, ny) % 3
            if tool != next_type:
                new_time = time + 1
                if new_time < best_time.get((nx, ny, tool), float("inf")):
                    best_time[(nx, ny, tool)] = new_time
                    heapq.heappush(queue, (new_time, nx, ny, tool))


if __name__ == "__main__":
    solve()
