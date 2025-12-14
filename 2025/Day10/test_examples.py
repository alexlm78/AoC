#!/usr/bin/env python3
"""
Verify the examples given in the problem statement
"""

from solve_day10 import parse_machine, solve_machine


def test_examples():
    """Test the examples from the statement"""

    # Example 1: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    # Expected answer: 2 presses
    example1 = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    target1, buttons1 = parse_machine(example1)
    result1 = solve_machine(target1, buttons1)
    print(f"Example 1: {result1} presses (expected: 2)")

    # Example 2: [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    # Expected answer: 3 presses
    example2 = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
    target2, buttons2 = parse_machine(example2)
    result2 = solve_machine(target2, buttons2)
    print(f"Example 2: {result2} presses (expected: 3)")

    # Example 3: [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
    # Expected answer: 2 presses
    example3 = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    target3, buttons3 = parse_machine(example3)
    result3 = solve_machine(target3, buttons3)
    print(f"Example 3: {result3} presses (expected: 2)")

    total_expected = 2 + 3 + 2
    total_actual = result1 + result2 + result3
    print(f"\nExamples total: {total_actual} presses (expected: {total_expected})")

    # Verify they match
    if total_actual == total_expected:
        print("✅ All examples are correct!")
    else:
        print("❌ Differences found in the examples")


if __name__ == "__main__":
    test_examples()
