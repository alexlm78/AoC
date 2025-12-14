#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 25: Code Chronicle

Part 1:
- Parse lock and key schematics from ASCII art
- Locks: pins extend down from top, Keys: notches extend up from bottom
- Check which lock/key pairs fit (no column overlaps)
- For each column: lock_height + key_height must be ≤ 5
"""


def parse_schematic(lines):
    """
    Parse a schematic and determine if it's a lock or key.
    Return type ('lock' or 'key') and column heights.

    Locks: top row filled (#####), bottom row empty (.....)
    Keys: top row empty (.....), bottom row filled (#####)
    """
    # Check if it's a lock or key
    if lines[0] == "#####":
        schematic_type = "lock"
    else:
        schematic_type = "key"

    # Calculate heights for each column
    num_cols = len(lines[0])
    heights = []

    for col in range(num_cols):
        if schematic_type == "lock":
            # For locks, count # symbols from top (excluding the top row of all #'s)
            height = 0
            for row in range(1, len(lines)):
                if lines[row][col] == "#":
                    height += 1
                else:
                    break
            heights.append(height)
        else:
            # For keys, count # symbols from bottom (excluding the bottom row of all #'s)
            height = 0
            for row in range(len(lines) - 2, -1, -1):
                if lines[row][col] == "#":
                    height += 1
                else:
                    break
            heights.append(height)

    return schematic_type, heights


def fits_together(lock_heights, key_heights, max_height):
    """
    Check if a lock and key fit together.
    They fit if no column has lock_height + key_height > max_height.
    """
    for lock_h, key_h in zip(lock_heights, key_heights):
        if lock_h + key_h > max_height:
            return False
    return True


def solve_locks_and_keys(input_text):
    """
    Parse all schematics and count fitting lock/key pairs.
    """
    lines = input_text.strip().split("\n")

    schematics = []
    current_schematic = []

    # Parse all schematics
    for line in lines:
        if line.strip() == "":
            if current_schematic:
                schematics.append(current_schematic)
                current_schematic = []
        else:
            current_schematic.append(line.strip())

    # Don't forget the last schematic
    if current_schematic:
        schematics.append(current_schematic)

    # Separate locks and keys
    locks = []
    keys = []

    for schematic in schematics:
        schematic_type, heights = parse_schematic(schematic)
        if schematic_type == "lock":
            locks.append(heights)
        else:
            keys.append(heights)

    print(f"Found {len(locks)} locks and {len(keys)} keys")

    # The available height is the schematic height minus 2 (top and bottom rows)
    max_height = len(schematics[0]) - 2
    print(f"Available space per column: {max_height}")

    # Count fitting pairs
    fitting_pairs = 0
    for lock in locks:
        for key in keys:
            if fits_together(lock, key, max_height):
                fitting_pairs += 1

    return fitting_pairs, locks, keys


def verify_with_example():
    """Verify with the example from the problem."""
    print("=" * 70)
    print("VERIFYING WITH EXAMPLE")
    print("=" * 70)

    example = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

    fitting_pairs, locks, keys = solve_locks_and_keys(example)

    print("\nLocks:")
    for i, lock in enumerate(locks):
        print(f"  Lock {i}: {lock}")

    print("\nKeys:")
    for i, key in enumerate(keys):
        print(f"  Key {i}: {key}")

    print(f"\n{'=' * 70}")
    print(f"Fitting lock/key pairs: {fitting_pairs}")
    print("Expected: 3")
    print(f"Match: {fitting_pairs == 3}")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    # Verify with example
    verify_with_example()

    # Read actual input
    with open("day25.txt", "r") as f:
        input_text = f.read()

    # Solve actual puzzle
    print("\n" + "=" * 70)
    print("SOLVING ACTUAL PUZZLE")
    print("=" * 70 + "\n")

    fitting_pairs, locks, keys = solve_locks_and_keys(input_text)

    print(f"\n{'=' * 70}")
    print(f"ANSWER: {fitting_pairs} unique lock/key pairs fit together")
    print(f"{'=' * 70}")
