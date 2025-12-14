#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 12: Christmas Tree Farm - Optimized Version
Solve the 2D packing problem with aggressive optimizations
"""

from typing import List, Tuple


class FastShape:
    """Optimized version of Shape with fewer variants"""

    def __init__(self, pattern: List[str]):
        self.coords = self._pattern_to_coords(pattern)
        self.variants = self._generate_minimal_variants()
        self.area = len(self.coords)

    def _pattern_to_coords(self, pattern: List[str]) -> List[Tuple[int, int]]:
        """Convert pattern to normalized coordinates"""
        coords = []
        for y, row in enumerate(pattern):
            for x, cell in enumerate(row):
                if cell == "#":
                    coords.append((x, y))
        return self._normalize(coords)

    def _normalize(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Normalize coordinates to the origin"""
        if not coords:
            return []
        min_x = min(x for x, y in coords)
        min_y = min(y for x, y in coords)
        return sorted([(x - min_x, y - min_y) for x, y in coords])

    def _generate_minimal_variants(self) -> List[List[Tuple[int, int]]]:
        """Generate only the essential unique variants"""
        variants = set()

        # Original
        current = self.coords
        variants.add(tuple(current))

        # 3 rotaciones más
        for _ in range(3):
            current = self._rotate_90(current)
            variants.add(tuple(self._normalize(current)))

        # Horizontal reflection + rotations
        current = self._flip_horizontal(self.coords)
        variants.add(tuple(self._normalize(current)))
        for _ in range(3):
            current = self._rotate_90(current)
            variants.add(tuple(self._normalize(current)))

        return [list(v) for v in variants]

    def _rotate_90(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return [(-y, x) for x, y in coords]

    def _flip_horizontal(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return [(-x, y) for x, y in coords]


class FastRegion:
    """Optimized version of Region"""

    def __init__(self, width: int, height: int, requirements: List[int]):
        self.width = width
        self.height = height
        self.requirements = requirements
        self.area = width * height
        self.grid = 0  # Usar bitset para el grid

    def _coord_to_bit(self, x: int, y: int) -> int:
        """Convert coordinate to bit position"""
        return y * self.width + x

    def is_occupied(self, x: int, y: int) -> bool:
        """Check if a position is occupied"""
        return bool(self.grid & (1 << self._coord_to_bit(x, y)))

    def can_place_shape(
        self, shape_coords: List[Tuple[int, int]], start_x: int, start_y: int
    ) -> bool:
        """Check if a shape can be placed"""
        for dx, dy in shape_coords:
            x, y = start_x + dx, start_y + dy
            if (
                x < 0
                or x >= self.width
                or y < 0
                or y >= self.height
                or self.is_occupied(x, y)
            ):
                return False
        return True

    def place_shape(
        self, shape_coords: List[Tuple[int, int]], start_x: int, start_y: int
    ):
        """Place a shape"""
        for dx, dy in shape_coords:
            x, y = start_x + dx, start_y + dy
            self.grid |= 1 << self._coord_to_bit(x, y)

    def remove_shape(
        self, shape_coords: List[Tuple[int, int]], start_x: int, start_y: int
    ):
        """Remove a shape"""
        for dx, dy in shape_coords:
            x, y = start_x + dx, start_y + dy
            self.grid &= ~(1 << self._coord_to_bit(x, y))


def parse_input_fast(filename: str) -> Tuple[List[FastShape], List[FastRegion]]:
    """Parse the input file in an optimized way"""
    shapes = []
    regions = []

    with open(filename, "r") as f:
        content = f.read().strip()

    lines = content.split("\n")
    i = 0

    # Parse shapes
    while i < len(lines):
        line = lines[i].strip()
        if ":" in line and "x" not in line:
            # It's a shape
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and ":" not in lines[i]:
                shape_lines.append(lines[i].rstrip())
                i += 1
            if shape_lines:
                shapes.append(FastShape(shape_lines))
        else:
            # It's a region
            if "x" in line and ":" in line:
                parts = line.split(": ")
                if len(parts) == 2:
                    size_part = parts[0]
                    requirements_part = parts[1]

                    width, height = map(int, size_part.split("x"))
                    requirements = list(map(int, requirements_part.split()))

                    regions.append(FastRegion(width, height, requirements))
            i += 1

    return shapes, regions


def quick_feasibility_check(region: FastRegion, shapes: List[FastShape]) -> bool:
    """Quick feasibility check before full backtracking"""

    # Check total area
    total_required_area = sum(
        count * shapes[i].area for i, count in enumerate(region.requirements)
    )

    if total_required_area > region.area:
        return False

    # Verify each individual shape can fit
    for shape_idx, count in enumerate(region.requirements):
        if count == 0:
            continue

        shape = shapes[shape_idx]
        can_fit_any_variant = False

        for variant in shape.variants:
            if not variant:
                continue

            max_x = max(x for x, y in variant)
            max_y = max(y for x, y in variant)

            if max_x < region.width and max_y < region.height:
                can_fit_any_variant = True
                break

        if not can_fit_any_variant:
            return False

    return True


def solve_ultra_fast(region: FastRegion, shapes: List[FastShape]) -> bool:
    """Ultra-fast version with time limits and aggressive heuristics"""

    # Quick feasibility check
    if not quick_feasibility_check(region, shapes):
        return False

    # Create gift list ordered by area (largest first)
    presents = []
    for shape_idx, count in enumerate(region.requirements):
        for _ in range(count):
            presents.append(shape_idx)

    if not presents:
        return True

    # Sort by area descending
    presents.sort(key=lambda idx: shapes[idx].area, reverse=True)

    # Iteration limit to avoid timeouts
    max_iterations = 500000
    iterations = 0

    def backtrack(present_idx: int) -> bool:
        nonlocal iterations
        iterations += 1

        if iterations > max_iterations:
            return False

        if present_idx >= len(presents):
            return True

        shape_idx = presents[present_idx]
        shape = shapes[shape_idx]

        # Try all variants
        for variant in shape.variants:
            if not variant:
                continue

            max_x = max(x for x, y in variant)
            max_y = max(y for x, y in variant)

            # Try all valid positions
            for start_y in range(region.height - max_y + 1):
                for start_x in range(region.width - max_x + 1):
                    if region.can_place_shape(variant, start_x, start_y):
                        region.place_shape(variant, start_x, start_y)

                        if backtrack(present_idx + 1):
                            return True

                        region.remove_shape(variant, start_x, start_y)

        return False

    return backtrack(0)


def main():
    """Optimized main function"""

    print("Loading data...")
    shapes, regions = parse_input_fast("Day12/input_12.txt")

    print(f"Shapes: {len(shapes)}, Regions: {len(regions)}")

    successful_count = 0

    for i, region in enumerate(regions):
        if i % 50 == 0:
            print(f"Progress: {i}/{len(regions)}")

        try:
            can_fit = solve_ultra_fast(region, shapes)
            if can_fit:
                successful_count += 1
        except:  # noqa: E722
            pass

    print(f"\n🎯 Successful regions: {successful_count}")


if __name__ == "__main__":
    main()
