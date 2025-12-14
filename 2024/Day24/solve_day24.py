#!/usr/bin/env python3
import os

"""
Advent of Code 2024 - Día 24: Crossed Wires

Description:
- A combinational circuit with AND/OR/XOR gates on binary inputs `xNN` and `yNN` is simulated.
- The outputs `zNN` must represent the binary sum of X + Y (carry adder).

Puzzle parts:
- Part 1: Run the circuit as is and obtain the decimal value of all `zNN`.
- Part 2: Detect 8 swapped wires (4 pairs) and correct them so that the circuit is a correct adder.

Approach:
- Parse initial inputs and gates.
- Basic propagation simulation.
- For Part 2, use structural analysis of the Ripple Carry Adder to identify swapped wires.
"""


def parse(text: str):
    """
    Parse the input text into two blocks:
    - Initial signal states (`xNN`, `yNN`) with values 0/1.
    - List of gates `op a b -> out`.

    Args:
        text: Complete content of the input file.
    Returns:
        `initial`: dictionary of initial signal values (0/1).
        `gates`: list of tuples `(op, a, b, out)` describing each gate.
    """
    parts = text.strip().split("\n\n")
    initial = {}
    for line in parts[0].splitlines():
        name, val = line.split(":")
        initial[name.strip()] = int(val.strip())
    gates = []
    for line in parts[1].splitlines():
        left, out = line.split("->")
        out = out.strip()
        a, op, b = [t.strip() for t in left.strip().split()]
        gates.append((op, a, b, out))
    return initial, gates


def simulate(initial, gates):
    """
    Simulate the circuit by propagation until no more changes occur.

    Args:
        initial: dictionary of known input signal values.
        gates: list of gate tuples `(op, a, b, out)`.
    Returns:
        Dictionary `val` with 0/1 values for all resolvable signals.
    """
    val = dict(initial)
    remaining = list(gates)
    changed = True
    while changed and remaining:
        changed = False
        next_remaining = []
        for op, a, b, out in remaining:
            if a in val and b in val:
                if op == "AND":
                    val[out] = val[a] & val[b]
                elif op == "OR":
                    val[out] = val[a] | val[b]
                elif op == "XOR":
                    val[out] = val[a] ^ val[b]
                else:
                    raise ValueError(op)
                changed = True
            else:
                next_remaining.append((op, a, b, out))
        remaining = next_remaining
    return val


def z_value(val):
    """
    Convert the output signals `zNN` into a decimal integer (little-endian: z00 is the least significant bit).

    Args:
        val: dictionary of signal values (0/1).
    Returns:
        Decimal integer result of concatenating the bits `zNN`.
    """
    zs = [(w, v) for w, v in val.items() if w.startswith("z")]

    def idx(w):
        return int(w[1:])

    zs.sort(key=lambda x: idx(x[0]))
    total = 0
    for i, (_, bit) in enumerate(zs):
        total |= (bit & 1) << i
    return total


def solve_part2(gates):
    """
    Identify swapped wires based on Ripple Carry Adder structure rules.

    Rules for a correct Full Adder (for bit i > 0):
    1. z[i] must be produced by an XOR gate (except the last carry bit).
    2. Intermediate XOR gates (inputs x, y) must output to another XOR (sum) and an AND (carry generation).
    3. Intermediate AND gates (inputs x, y) must output to an OR (carry propagation).
    4. Carry OR gates must output to an XOR (next sum) and an AND (next carry generation).

    We can detect swaps by finding gates that violate these structural rules.
    """

    # Helper to check if a wire is an input to an OR gate
    def is_input_to_op(wire, op_target):
        for op, a, b, out in gates:
            if (a == wire or b == wire) and op == op_target:
                return True
        return False

    bad_wires = set()

    # Find max z to identify MSB
    z_wires = [g[3] for g in gates if g[3].startswith("z")]
    max_z = max(z_wires)

    for op, in1, in2, out in gates:
        # Rule 1: If output is z (and not MSB), op must be XOR
        if out.startswith("z") and out != max_z:
            if op != "XOR":
                bad_wires.add(out)

        # Rule 2: If output is NOT z, and inputs are NOT x/y, op should NOT be XOR
        # (Because the only valid XORs are x^y or the ones producing z)
        is_xy_input = (in1.startswith("x") or in1.startswith("y")) and (
            in2.startswith("x") or in2.startswith("y")
        )

        if not out.startswith("z") and not is_xy_input:
            if op == "XOR":
                bad_wires.add(out)

        # Rule 3: If inputs are x/y (and not bit 0), output of XOR must be input to another XOR or AND
        # Rule 4: If inputs are x/y (and not bit 0), output of AND must be input to an OR
        if is_xy_input:
            # Skip bit 0 checks for usage rules as it's special (half adder)
            if "00" not in in1:
                if op == "XOR":
                    # Must be used in XOR or AND (for carry logic)
                    # If used in OR, it's wrong.
                    if is_input_to_op(out, "OR"):
                        bad_wires.add(out)
                elif op == "AND":
                    # Must be used in OR (for carry logic)
                    # If used in XOR or AND (except OR), it's likely wrong.
                    # Actually, checking if it is NOT used in OR is safer.
                    if not is_input_to_op(out, "OR"):
                        bad_wires.add(out)

    return sorted(list(bad_wires))


def main():
    """
    Entry point:
    - Read `day24.txt`, parse and simulate Part 1.
    - Run swap detection for Part 2.
    - Print results.
    """
    input_path = os.path.join(os.path.dirname(__file__), "day24.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    initial, gates = parse(content)

    # Part 1
    val = simulate(initial, gates)
    total = z_value(val)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 24: Crossed Wires")
    print("=" * 70)
    print(f"Part 1 - Decimal output: {total}")
    print("=" * 70)

    # Part 2
    swapped_wires = solve_part2(gates)
    print(f"Part 2 - Swapped wires (sorted): {','.join(swapped_wires)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
