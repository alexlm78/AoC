import re
from collections import defaultdict


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        # Grid to store claim counts for each square inch
        grid = defaultdict(int)
        claims = []

        # Parse and populate grid
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Parse line like #1 @ 1,3: 4x4
            match = re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
            if match:
                claim_id = int(match.group(1))
                left = int(match.group(2))
                top = int(match.group(3))
                width = int(match.group(4))
                height = int(match.group(5))

                claims.append(
                    {
                        "id": claim_id,
                        "left": left,
                        "top": top,
                        "width": width,
                        "height": height,
                    }
                )

                for x in range(left, left + width):
                    for y in range(top, top + height):
                        grid[(x, y)] += 1

        # Part 1: Count square inches with 2 or more claims
        overlap_count = 0
        for count in grid.values():
            if count >= 2:
                overlap_count += 1

        print(f"Part 1 - Square inches within two or more claims: {overlap_count}")

        # Part 2: Find non-overlapping claim
        for claim in claims:
            is_overlap = False
            for x in range(claim["left"], claim["left"] + claim["width"]):
                for y in range(claim["top"], claim["top"] + claim["height"]):
                    if grid[(x, y)] > 1:
                        is_overlap = True
                        break
                if is_overlap:
                    break

            if not is_overlap:
                print(
                    f"Part 2 - ID of the only claim that doesn't overlap: {claim['id']}"
                )
                return

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
