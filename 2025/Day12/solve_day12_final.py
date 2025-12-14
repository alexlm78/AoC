#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 12: Christmas Tree Farm - Final Version
"""

from solve_day12_fast import FastShape, FastRegion, solve_ultra_fast, parse_input_fast


def test_example():
    """Verify with the example from the statement"""

    # Create example shapes
    shapes = [
        FastShape(["###", "##.", "##."]),  # 0
        FastShape(["###", "##.", ".##"]),  # 1
        FastShape([".##", "###", "##."]),  # 2
        FastShape(["##.", "###", "##."]),  # 3
        FastShape(["###", "#..", "###"]),  # 4
        FastShape(["###", ".#.", "###"]),  # 5
    ]

    # Create example regions
    regions = [
        FastRegion(4, 4, [0, 0, 0, 0, 2, 0]),  # 4x4: 0 0 0 0 2 0
        FastRegion(12, 5, [1, 0, 1, 0, 2, 2]),  # 12x5: 1 0 1 0 2 2
        FastRegion(12, 5, [1, 0, 1, 0, 3, 2]),  # 12x5: 1 0 1 0 3 2
    ]

    results = []
    for i, region in enumerate(regions):
        can_fit = solve_ultra_fast(region, shapes)
        results.append(can_fit)
        print(f"Example region {i + 1}: {'✓ Fits' if can_fit else '✗ Does not fit'}")

    successful = sum(results)
    print(f"Successful example regions: {successful}/3 (expected: 2)")

    return successful == 2


def main():
    """Main function with verification"""

    print("=== ADVENT OF CODE 2025 - DAY 12 ===")
    print("Christmas Tree Farm - 2D Packing\n")

    # Verify example
    print("🧪 Verifying example...")
    if test_example():
        print("✅ Example correct!\n")
    else:
        print("❌ Example incorrect. Review algorithm.\n")

    # Solve full puzzle
    print("🎯 Solving full puzzle...")
    shapes, regions = parse_input_fast("Day12/input_12.txt")

    print("📊 Loaded data:")
    print(f"   • Gift shapes: {len(shapes)}")
    print(f"   • Regions to verify: {len(regions)}")

    # Show shape information
    print("\n📦 Shape information:")
    for i, shape in enumerate(shapes):
        print(f"   Shape {i}: {shape.area} cells, {len(shape.variants)} variants")

    successful_count = 0

    print("\n🔄 Processing regions...")
    for i, region in enumerate(regions):
        if i % 100 == 0:
            print(f"   Progress: {i}/{len(regions)} ({i / len(regions) * 100:.1f}%)")

        try:
            can_fit = solve_ultra_fast(region, shapes)
            if can_fit:
                successful_count += 1
        except Exception:
            # In case of error, assume it does not fit
            pass

    print("\n🎯 FINAL RESULT:")
    print(f"   Regions that can accommodate all gifts: {successful_count}")
    print(f"   Success rate: {successful_count / len(regions) * 100:.1f}%")


if __name__ == "__main__":
    main()
