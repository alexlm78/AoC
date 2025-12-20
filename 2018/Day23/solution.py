import re


def solve():
    bots = []
    pattern = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")

    with open("input.txt", "r") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                x, y, z, r = map(int, match.groups())
                bots.append(((x, y, z), r))

    # Part 1
    strongest = max(bots, key=lambda b: b[1])
    sx, sy, sz = strongest[0]
    sr = strongest[1]

    count = 0
    for (bx, by, bz), br in bots:
        dist = abs(sx - bx) + abs(sy - by) + abs(sz - bz)
        if dist <= sr:
            count += 1

    print(f"Part 1 Result: {count}")

    # Part 2
    # Coordinate range estimation
    xs = [b[0][0] for b in bots]
    ys = [b[0][1] for b in bots]
    zs = [b[0][2] for b in bots]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    # We need a cube that covers everything.
    max_range = max(max_x - min_x, max_y - min_y, max_z - min_z)
    size = 1
    while size <= max_range:
        size *= 2

    import heapq

    # Priority Queue: (-num_bots, distance_to_origin, size, x, y, z)
    # We want to maximize num_bots, then minimize distance, then minimize size (optional)
    # Since heapq is min-heap, we store -num_bots.

    # Initial box covering the bounds
    # Center it somewhat or just start from min
    pq = []

    # Let's create an initial box that definitely covers the potential solution space.
    # The solution is likely within the bounding box of bot centers.
    # Actually, the optimal point is within the intersection of ranges.
    # If ranges intersect, they must overlap in coordinate space.
    # So covering [min_x, max_x] x [min_y, max_y] x [min_z, max_z] is sufficient?
    # Actually, a point could be slightly outside if radii are huge?
    # No, if a point is optimal, it must be "pulled" towards the dense cluster.
    # The geometric median property suggests it's within the hull of centers.
    # But let's be safe and cover a bit more if needed, but min/max of centers is a good start.
    # However, to use a perfect power-of-2 cube, we might overshoot.

    # Let's just use the min corner and a size.
    # Adjust min_x, min_y, min_z to be the corner.

    heapq.heappush(
        pq, (0, 0, size, min_x, min_y, min_z)
    )  # Dummy count for start, will be recalculated?
    # Actually, calculate count for initial box properly.

    def count_intersects(bx, by, bz, bsize):
        c = 0
        for (x, y, z), r in bots:
            # Distance from box to point
            dist = 0
            # X
            if x < bx:
                dist += bx - x
            elif x > bx + bsize - 1:
                dist += x - (bx + bsize - 1)
            # Y
            if y < by:
                dist += by - y
            elif y > by + bsize - 1:
                dist += y - (by + bsize - 1)
            # Z
            if z < bz:
                dist += bz - z
            elif z > bz + bsize - 1:
                dist += z - (bz + bsize - 1)

            if dist <= r:
                c += 1
        return c

    # Re-initialize PQ with correct count
    initial_count = count_intersects(min_x, min_y, min_z, size)

    # Distance to origin for the box
    # Dist is 0 if origin is inside, else dist to nearest face
    def dist_to_origin(bx, by, bz, bsize):
        d = 0
        if 0 < bx:
            d += bx
        elif 0 > bx + bsize - 1:
            d += -(bx + bsize - 1)  # i.e. origin is right of box
        # Actually standard logic:
        # if origin is in [bx, bx+size-1], dist is 0 along that axis.
        # if origin < bx, dist is bx - 0 = bx
        # if origin > bx+size-1, dist is 0 - (bx+size-1) ... wait, dist is origin - max = -bx-size+1
        # Let's use generic dist(box, point) function where point is (0,0,0)

        dx = 0
        if 0 < bx:
            dx = bx
        elif 0 > bx + bsize - 1:
            dx = 0 - (bx + bsize - 1)

        dy = 0
        if 0 < by:
            dy = by
        elif 0 > by + bsize - 1:
            dy = 0 - (by + bsize - 1)

        dz = 0
        if 0 < bz:
            dz = bz
        elif 0 > bz + bsize - 1:
            dz = 0 - (bz + bsize - 1)

        return dx + dy + dz

    pq = []
    heapq.heappush(
        pq,
        (
            -initial_count,
            dist_to_origin(min_x, min_y, min_z, size),
            size,
            min_x,
            min_y,
            min_z,
        ),
    )

    while pq:
        neg_count, dist, sz, x, y, z = heapq.heappop(pq)

        if sz == 1:
            print(f"Part 2 Result: {dist}")
            break

        half = sz // 2
        for dx in [0, half]:
            for dy in [0, half]:
                for dz in [0, half]:
                    nx, ny, nz = x + dx, y + dy, z + dz

                    # Optimization: check if this sub-box is within bounds?
                    # Not strictly necessary if we rely on intersection counts,
                    # empty space will have 0 intersections eventually (or just far away bots).
                    # But if our initial box is huge, many sub-boxes might be empty.

                    cnt = count_intersects(nx, ny, nz, half)
                    d = dist_to_origin(nx, ny, nz, half)
                    heapq.heappush(pq, (-cnt, d, half, nx, ny, nz))


if __name__ == "__main__":
    solve()
