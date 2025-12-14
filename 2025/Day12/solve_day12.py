#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 12: Christmas Tree Farm
Solve the 2D packing problem for gifts with specific shapes
"""

from typing import List, Tuple


class Shape:
    """Represents a gift shape with its possible rotations and reflections"""

    def __init__(self, pattern: List[str]):
        self.original = pattern
        self.variants = self._generate_variants(pattern)

    def _generate_variants(self, pattern: List[str]) -> List[List[Tuple[int, int]]]:
        """Generate all possible rotations and reflections of the shape"""
        variants = []

        # Convert pattern to coordinates
        coords = []
        for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell == "#":
                    coords.append((x, y))

        # Generate 4 rotations
        current = coords
        for _ in range(4):
            variants.append(self._normalize_coords(current))
            current = self._rotate_90(current)

        # Generate horizontal reflections of the 4 rotations
        current = self._flip_horizontal(coords)
        for _ in range(4):
            variants.append(self._normalize_coords(current))
            current = self._rotate_90(current)

        # Remove duplicates
        unique_variants = []
        for variant in variants:
            if variant not in unique_variants:
                unique_variants.append(variant)

        return unique_variants

    def _rotate_90(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Rotate coordinates 90 degrees clockwise"""
        return [(-y, x) for x, y in coords]

    def _flip_horizontal(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Reflect coordinates horizontally"""
        return [(-x, y) for x, y in coords]

    def _normalize_coords(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Normalize coordinates to start at (0,0)"""
        if not coords:
            return []

        min_x = min(x for x, y in coords)
        min_y = min(y for x, y in coords)

        normalized = [(x - min_x, y - min_y) for x, y in coords]
        return sorted(normalized)


class Region:
    """Represents a region where gifts must be placed"""

    def __init__(self, width: int, height: int, requirements: List[int]):
        self.width = width
        self.height = height
        self.requirements = requirements
        self.grid = [[False] * width for _ in range(height)]

    def can_place_shape(
        self, shape_coords: List[Tuple[int, int]], start_x: int, start_y: int
    ) -> bool:
        """Check if a shape can be placed at the given position"""
        for dx, dy in shape_coords:
            x, y = start_x + dx, start_y + dy
            if x < 0 or x >= self.width or y < 0 or y >= self.height or self.grid[y][x]:
                return False
        return True

    def place_shape(
        self, shape_coords: List[Tuple[int, int]], start_x: int, start_y: int
    ):
        """Place a shape in the region"""
        for dx, dy in shape_coords:
            x, y = start_x + dx, start_y + dy
            self.grid[y][x] = True

    def remove_shape(
        self, shape_coords: List[Tuple[int, int]], start_x: int, start_y: int
    ):
        """Remove a shape from the region"""
        for dx, dy in shape_coords:
            x, y = start_x + dx, start_y + dy
            self.grid[y][x] = False

    def copy(self):
        """Create a copy of the region"""
        new_region = Region(self.width, self.height, self.requirements.copy())
        new_region.grid = [row.copy() for row in self.grid]
        return new_region


def parse_input(filename: str) -> Tuple[List[Shape], List[Region]]:
    """Parse the input file"""
    shapes = []
    regions = []

    with open(filename, "r") as f:
        lines = [line.rstrip() for line in f.readlines()]

    i = 0
    # Parse shapes
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if ":" in line and "x" not in line:
            # It's a shape
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and ":" not in lines[i]:
                shape_lines.append(lines[i].rstrip())
                i += 1
            if shape_lines:
                shapes.append(Shape(shape_lines))
        else:
            # It's a region
            if "x" in line:
                parts = line.split(": ")
                if len(parts) == 2:
                    size_part = parts[0]
                    requirements_part = parts[1]

                    width, height = map(int, size_part.split("x"))
                    requirements = list(map(int, requirements_part.split()))

                    regions.append(Region(width, height, requirements))
            i += 1

    return shapes, regions


def can_fit_all_presents(region: Region, shapes: List[Shape]) -> bool:
    """
    Check if all required gifts can fit in the region using backtracking
    """
    # Create the list of gifts to place
    presents_to_place = []
    for shape_idx, count in enumerate(region.requirements):
        for _ in range(count):
            presents_to_place.append(shape_idx)

    if not presents_to_place:
        return True

    def backtrack(present_idx: int, current_region: Region) -> bool:
        if present_idx >= len(presents_to_place):
            return True

        shape_idx = presents_to_place[present_idx]
        shape = shapes[shape_idx]

        # Try all shape variants
        for variant in shape.variants:
            # Try all possible positions
            for start_y in range(current_region.height):
                for start_x in range(current_region.width):
                    if current_region.can_place_shape(variant, start_x, start_y):
                        # Place the shape
                        current_region.place_shape(variant, start_x, start_y)

                        # Recursion
                        if backtrack(present_idx + 1, current_region):
                            return True

                        # Backtrack: remove the shape
                        current_region.remove_shape(variant, start_x, start_y)

        return False

    return backtrack(0, region.copy())


def solve_optimized(region: Region, shapes: List[Shape]) -> bool:
    """
    Optimized version that uses heuristics to reduce the search space
    """
    # Create the list of gifts to place, ordered by size (largest first)
    presents_to_place = []
    for shape_idx, count in enumerate(region.requirements):
        for _ in range(count):
            presents_to_place.append(shape_idx)

    if not presents_to_place:
        return True

    # Sort by shape size (heuristic: place larger shapes first)
    presents_to_place.sort(key=lambda idx: len(shapes[idx].variants[0]), reverse=True)

    def backtrack_optimized(present_idx: int, current_region: Region) -> bool:
        if present_idx >= len(presents_to_place):
            return True

        shape_idx = presents_to_place[present_idx]
        shape = shapes[shape_idx]

        # Try variants ordered by occupied area
        for variant in shape.variants:
            # Compute the variant bounding box
            if not variant:
                continue

            max_x = max(x for x, y in variant)
            max_y = max(y for x, y in variant)

            # Only try positions where the shape can fully fit
            for start_y in range(current_region.height - max_y):
                for start_x in range(current_region.width - max_x):
                    if current_region.can_place_shape(variant, start_x, start_y):
                        # Place the shape
                        current_region.place_shape(variant, start_x, start_y)

                        # Recursion
                        if backtrack_optimized(present_idx + 1, current_region):
                            return True

                        # Backtrack: remove the shape
                        current_region.remove_shape(variant, start_x, start_y)

        return False

    return backtrack_optimized(0, region.copy())


def test_example():
    """Test with the example from the statement"""

    # Create example shapes
    shapes = [
        Shape(["###", "##.", "##."]),  # 0
        Shape(["###", "##.", ".##"]),  # 1
        Shape([".##", "###", "##."]),  # 2
        Shape(["##.", "###", "##."]),  # 3
        Shape(["###", "#..", "###"]),  # 4
        Shape(["###", ".#.", "###"]),  # 5
    ]

    # Create example regions
    regions = [
        Region(4, 4, [0, 0, 0, 0, 2, 0]),  # 4x4: 0 0 0 0 2 0
        Region(12, 5, [1, 0, 1, 0, 2, 2]),  # 12x5: 1 0 1 0 2 2
        Region(12, 5, [1, 0, 1, 0, 3, 2]),  # 12x5: 1 0 1 0 3 2
    ]

    results = []
    for i, region in enumerate(regions):
        can_fit = solve_optimized(region, shapes)
        results.append(can_fit)
        print(f"Region {i + 1}: {'✓' if can_fit else '✗'}")

    successful_regions = sum(results)
    print(f"\nSuccessful regions: {successful_regions} (expected: 2)")

    return successful_regions == 2


def main():
    """Main function"""

    print("Testing with the example...")
    if not test_example():
        print("❌ The example does not match. Verify the algorithm.")
        return

    print("✅ Example correct! Solving the full puzzle...\n")

    # Load data from file
    shapes, regions = parse_input("Day12/input_12.txt")

    print(f"Shapes loaded: {len(shapes)}")
    print(f"Regions to verify: {len(regions)}")

    successful_count = 0

    for i, region in enumerate(regions):
        print(f"Processing region {i + 1}/{len(regions)}... ", end="", flush=True)

        can_fit = solve_optimized(region, shapes)
        if can_fit:
            successful_count += 1
            print("✓")
        else:
            print("✗")

    print(f"\n🎯 Total regions that can accommodate all gifts: {successful_count}")


if __name__ == "__main__":
    main()
