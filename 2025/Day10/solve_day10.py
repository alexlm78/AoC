#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 10: Factory
Solve the indicator lights configuration using linear algebra over GF(2)

The problem can be modeled as a system of linear equations over GF(2):
- Each light is a binary variable (on/off)
- Each button represents an equation that XORs certain lights
- We need to find the minimal combination of button presses
"""

import re
from typing import List, Tuple
import numpy as np


def parse_machine(line: str) -> Tuple[List[int], List[List[int]]]:
    """
    Parse an input line to extract the target pattern and buttons.

    Args:
        line: Input line in the format [pattern] (button1) (button2) ... {voltages}

    Returns:
        Tuple of (target_pattern, buttons_list)
    """
    # Extract target pattern between brackets
    pattern_match = re.search(r"\[([.#]+)\]", line)
    if not pattern_match:
        raise ValueError(f"No se encontró patrón en la línea: {line}")

    pattern_str = pattern_match.group(1)
    target_pattern = [1 if c == "#" else 0 for c in pattern_str]

    # Extract buttons between parentheses
    button_matches = re.findall(r"\(([0-9,]+)\)", line)
    buttons = []

    for button_str in button_matches:
        button_indices = [int(x) for x in button_str.split(",")]
        buttons.append(button_indices)

    return target_pattern, buttons


def create_system_matrix(
    target_pattern: List[int], buttons: List[List[int]]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create the matrix for the system of linear equations over GF(2).

    Args:
        target_pattern: Target light pattern (0s and 1s)
        buttons: List of buttons, each with indices of lights it affects

    Returns:
        Tuple of (matrix_A, vector_b) where Ax = b over GF(2)
    """
    num_lights = len(target_pattern)
    num_buttons = len(buttons)

    # Create matrix A where A[i][j] = 1 if button j affects light i
    A = np.zeros((num_lights, num_buttons), dtype=int)

    for j, button in enumerate(buttons):
        for light_idx in button:
            if light_idx < num_lights:  # Validate index range
                A[light_idx][j] = 1

    # Target vector b
    b = np.array(target_pattern, dtype=int)

    return A, b


def solve_gf2_system(A: np.ndarray, b: np.ndarray) -> Tuple[bool, List[int]]:
    """
    Solve Ax = b over GF(2) using Gaussian elimination.
    Search for the solution with the minimum number of 1s (minimal presses).

    Args:
        A: System matrix
        b: Target vector

    Returns:
        Tuple of (has_solution, minimal_solution)
    """
    m, n = A.shape

    # Create augmented matrix [A|b]
    augmented = np.hstack([A.copy(), b.reshape(-1, 1)])

    # Gaussian elimination over GF(2)
    pivot_row = 0
    pivot_cols = []

    for col in range(n):
        # Find pivot in the current column
        found_pivot = False
        for row in range(pivot_row, m):
            if augmented[row, col] == 1:
                # Swap rows if needed
                if row != pivot_row:
                    augmented[[pivot_row, row]] = augmented[[row, pivot_row]]
                found_pivot = True
                break

        if not found_pivot:
            continue

        pivot_cols.append(col)

        # Eliminate other 1s in this column
        for row in range(m):
            if row != pivot_row and augmented[row, col] == 1:
                # Row XOR over GF(2)
                augmented[row] = (augmented[row] + augmented[pivot_row]) % 2

        pivot_row += 1

    # Check consistency
    for row in range(pivot_row, m):
        if augmented[row, -1] == 1:  # Inconsistent row
            return False, []

    # System is consistent, search for minimal solution
    # Free variables can be 0 or 1
    free_vars = [i for i in range(n) if i not in pivot_cols]

    min_solution = None
    min_cost = float("inf")

    # Try all combinations of free variables
    for mask in range(1 << len(free_vars)):
        solution = [0] * n

        # Assign values to free variables
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1

        # Compute basic variables
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            row = i

            # solution[col] = (b[row] - sum(A[row][j] * solution[j] for j != col)) % 2
            val = augmented[row, -1]
            for j in range(n):
                if j != col:
                    val = (val - augmented[row, j] * solution[j]) % 2
            solution[col] = val % 2

        # Verify that the solution is valid
        result = np.dot(A, solution) % 2
        if np.array_equal(result, b):
            cost = sum(solution)
            if cost < min_cost:
                min_cost = cost
                min_solution = solution

    return min_solution is not None, min_solution if min_solution else []


def solve_machine(target_pattern: List[int], buttons: List[List[int]]) -> int:
    """
    Solve a single machine and return the minimal number of presses.

    Args:
        target_pattern: Target light pattern
        buttons: List of available buttons

    Returns:
        Minimal number of presses, or -1 if no solution exists
    """
    A, b = create_system_matrix(target_pattern, buttons)
    has_solution, solution = solve_gf2_system(A, b)

    if has_solution:
        return sum(solution)
    else:
        return -1


def main():
    """Main function that solves the full puzzle."""
    total_presses = 0

    with open("input_10.txt", "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        try:
            target_pattern, buttons = parse_machine(line)
            min_presses = solve_machine(target_pattern, buttons)

            if min_presses == -1:
                print(f"Machine {i + 1}: No solution")
                return
            else:
                print(f"Machine {i + 1}: {min_presses} minimum presses")
                total_presses += min_presses

        except Exception as e:
            print(f"Error processing machine {i + 1}: {e}")
            return

    print(f"\nTotal minimum presses required: {total_presses}")


if __name__ == "__main__":
    main()
