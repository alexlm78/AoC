#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 17: Chronospatial Computer

Part 1:
- Simulate the 3-bit CPU with registers A, B, C, and 8 opcodes (0..7)
- Execute and concatenate the outputs of opcode 5 (out)

Part 2:
- Find the smallest positive A that causes the program to print its own listing
- Construct A in base 8, validating output suffixes against the target
"""

import os
from typing import List, Tuple


def parse_input(text: str) -> Tuple[int, int, int, List[int]]:
    """
    Parse debugger input for registers and program.
    Args:
        text: Lines with 'Register A:', 'Register B:', 'Register C:' and 'Program:'
    Returns:
        (A, B, C, program_list)
    """
    lines = [line.rstrip("\n") for line in text.splitlines()]
    a = b = c = None
    program: List[int] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("Register A:"):
            a = int(s.split(":")[1].strip())
        elif s.startswith("Register B:"):
            b = int(s.split(":")[1].strip())
        elif s.startswith("Register C:"):
            c = int(s.split(":")[1].strip())
        elif s.startswith("Program:"):
            prog_str = s.split(":")[1].strip()
            program = [int(x) for x in prog_str.split(",") if x.strip() != ""]
    if a is None or b is None or c is None or not program:
        raise ValueError("Invalid input")
    return a, b, c, program


def exec_program(program: List[int], a: int, b: int, c: int) -> List[int]:
    """
    Execute the 3-bit computer program and collect outputs.
    Args:
        program: List of 3-bit numbers (opcodes and operands alternating)
        a,b,c: Initial register values
    Returns:
        List of output values emitted by opcode 5
    """
    out: List[int] = []
    ip = 0

    def combo_value(x: int) -> int:
        if 0 <= x <= 3:
            return x
        if x == 4:
            return a
        if x == 5:
            return b
        if x == 6:
            return c
        raise ValueError("Invalid combo operand")

    while 0 <= ip < len(program):
        opcode = program[ip]
        if ip + 1 >= len(program):
            break
        operand = program[ip + 1]

        if opcode == 0:
            denom = 1 << combo_value(operand)
            a = a // denom
            ip += 2
        elif opcode == 1:
            b = b ^ operand
            ip += 2
        elif opcode == 2:
            b = combo_value(operand) % 8
            ip += 2
        elif opcode == 3:
            if a != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:
            b = b ^ c
            ip += 2
        elif opcode == 5:
            out.append(combo_value(operand) % 8)
            ip += 2
        elif opcode == 6:
            denom = 1 << combo_value(operand)
            b = a // denom
            ip += 2
        elif opcode == 7:
            denom = 1 << combo_value(operand)
            c = a // denom
            ip += 2
        else:
            break
    return out


def find_min_a(program: List[int], b0: int, c0: int) -> int:
    """
    Find the lowest positive A that makes program output exactly itself.
    Builds A in base-8 from most significant digit, matching suffix outputs.
    Args:
        program: Target output sequence
        b0,c0: Initial B and C (unchanged)
    Returns:
        Smallest positive A achieving exact output match
    """
    target = program[:]
    n = len(target)
    candidates = {0}
    for i in range(n):
        base = 8 ** (n - 1 - i)
        next_candidates = set()
        for a in candidates:
            for d in range(8):
                a2 = a + d * base
                out = exec_program(program, a2, b0, c0)
                if len(out) >= i + 1 and out[-(i + 1) :] == target[-(i + 1) :]:
                    next_candidates.add(a2)
        if not next_candidates:
            return 0
        candidates = next_candidates
    res = min(x for x in candidates if x > 0)
    return res


def main():
    """
    Read input, run program for Part 1 outputs and compute Part 2 minimal A.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day17.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    a, b, c, program = parse_input(content)
    outputs = exec_program(program, a, b, c)
    joined = ",".join(str(x) for x in outputs)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 17: Chronospatial Computer")
    print("=" * 70)
    print(f"Part 1 - Output: {joined}")
    a2 = find_min_a(program, b, c)
    print(f"Part 2 - Lowest A: {a2}")
    print("=" * 70)


if __name__ == "__main__":
    main()
