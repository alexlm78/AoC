#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 10: Factory - Part 2
Solve the voltage configuration using integer linear programming
"""

import re
from typing import List, Tuple
import pulp


def parse_machine_part2(line: str) -> Tuple[List[int], List[List[int]]]:
    """
    Parse an input line to extract target voltages and buttons.

    Args:
        line: Input line in the format [pattern] (button1) (button2) ... {voltages}

    Returns:
        Tuple of (target_voltages, buttons_list)
    """
    # Extract target voltages between curly braces
    voltages_match = re.search(r"\{([0-9,]+)\}", line)
    if not voltages_match:
        raise ValueError(f"No voltages were found on the line: {line}")

    voltages_str = voltages_match.group(1)
    target_voltages = [int(x) for x in voltages_str.split(",")]

    # Extract buttons between parentheses
    button_matches = re.findall(r"\(([0-9,]+)\)", line)
    buttons = []

    for button_str in button_matches:
        button_indices = [int(x) for x in button_str.split(",")]
        buttons.append(button_indices)

    return target_voltages, buttons


def solve_voltage_system(target_voltages: List[int], buttons: List[List[int]]) -> int:
    """
    Solve the voltage system using integer linear programming.

    Args:
        target_voltages: Target voltages for each counter
        buttons: List of buttons, each with the indices of counters it affects

    Returns:
        Minimal number of presses, or -1 if no solution exists
    """
    num_counters = len(target_voltages)
    num_buttons = len(buttons)

    # Create the linear programming problem
    prob = pulp.LpProblem("VoltageConfiguration", pulp.LpMinimize)

    # Variables: number of times each button is pressed
    button_presses = []
    for i in range(num_buttons):
        var = pulp.LpVariable(f"button_{i}", lowBound=0, cat="Integer")
        button_presses.append(var)

    # Objective function: minimize total presses
    prob += pulp.lpSum(button_presses)

    # Constraints: each counter must reach its target voltage
    for counter_idx in range(num_counters):
        # Sum contributions of all buttons that affect this counter
        counter_sum = 0
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                counter_sum += button_presses[button_idx]

        # The counter must equal the target voltage exactly
        prob += counter_sum == target_voltages[counter_idx]

    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # Check if a solution was found
    if prob.status == pulp.LpStatusOptimal:
        total_presses = sum(var.varValue for var in button_presses)
        return int(total_presses)
    else:
        return -1


def solve_machine_part2(target_voltages: List[int], buttons: List[List[int]]) -> int:
    """
    Solve a single machine for part 2.

    Args:
        target_voltages: Target voltages
        buttons: List of available buttons

    Returns:
        Minimal number of presses, or -1 if no solution exists
    """
    return solve_voltage_system(target_voltages, buttons)


def test_examples_part2():
    """Test the examples for part 2"""

    # Example 1: {3,5,4,7} with buttons (3) (1,3) (2) (2,3) (0,2) (0,1)
    # Expected answer: 10 presses
    example1 = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
    target1, buttons1 = parse_machine_part2(example1)
    result1 = solve_machine_part2(target1, buttons1)
    print(f"Example 1: {result1} presses (expected: 10)")

    # Example 2: {7,5,12,7,2} with buttons (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4)
    # Expected answer: 12 presses
    example2 = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
    target2, buttons2 = parse_machine_part2(example2)
    result2 = solve_machine_part2(target2, buttons2)
    print(f"Example 2: {result2} presses (expected: 12)")

    # Example 3: {10,11,11,5,10,5} with buttons (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2)
    # Expected answer: 11 presses
    example3 = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    target3, buttons3 = parse_machine_part2(example3)
    result3 = solve_machine_part2(target3, buttons3)
    print(f"Example 3: {result3} presses (expected: 11)")

    total_expected = 10 + 12 + 11
    total_actual = result1 + result2 + result3
    print(f"\nExamples total: {total_actual} presses (expected: {total_expected})")

    return total_actual == total_expected


def main():
    """Main function that solves the full puzzle for part 2."""

    # First, test the examples
    print("Testing part 2 examples...")
    if not test_examples_part2():
        print("❌ Examples do not match. Check the algorithm.")
        return
    print("✅ Examples correct! Solving the full puzzle...\n")

    total_presses = 0

    with open("input_10.txt", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        try:
            target_voltages, buttons = parse_machine_part2(line)
            min_presses = solve_machine_part2(target_voltages, buttons)

            if min_presses == -1:
                print(f"Machine {i + 1}: No solution")
                return
            else:
                print(f"Machine {i + 1}: {min_presses} minimum presses")
                total_presses += min_presses

        except Exception as e:
            print(f"Error processing machine {i + 1}: {e}")
            return

    print(f"\nTotal minimum presses required (Part 2): {total_presses}")


if __name__ == "__main__":
    main()
