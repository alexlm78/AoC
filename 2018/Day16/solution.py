import re


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return

    # Parse Input
    samples = []
    program = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith("Before:"):
            before_match = re.match(r"Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]", line)
            before = [int(x) for x in before_match.groups()]

            i += 1
            instr_line = lines[i].strip()
            instr = [int(x) for x in instr_line.split()]

            i += 1
            after_line = lines[i].strip()
            after_match = re.match(
                r"After:\s+\[(\d+), (\d+), (\d+), (\d+)\]", after_line
            )
            after = [int(x) for x in after_match.groups()]

            samples.append({"before": before, "instr": instr, "after": after})
            i += 1
        else:
            # This is part of the test program
            program.append([int(x) for x in line.split()])
            i += 1

    # Define operations
    def addr(regs, a, b, c):
        regs[c] = regs[a] + regs[b]

    def addi(regs, a, b, c):
        regs[c] = regs[a] + b

    def mulr(regs, a, b, c):
        regs[c] = regs[a] * regs[b]

    def muli(regs, a, b, c):
        regs[c] = regs[a] * b

    def banr(regs, a, b, c):
        regs[c] = regs[a] & regs[b]

    def bani(regs, a, b, c):
        regs[c] = regs[a] & b

    def borr(regs, a, b, c):
        regs[c] = regs[a] | regs[b]

    def bori(regs, a, b, c):
        regs[c] = regs[a] | b

    def setr(regs, a, b, c):
        regs[c] = regs[a]

    def seti(regs, a, b, c):
        regs[c] = a

    def gtir(regs, a, b, c):
        regs[c] = 1 if a > regs[b] else 0

    def gtri(regs, a, b, c):
        regs[c] = 1 if regs[a] > b else 0

    def gtrr(regs, a, b, c):
        regs[c] = 1 if regs[a] > regs[b] else 0

    def eqir(regs, a, b, c):
        regs[c] = 1 if a == regs[b] else 0

    def eqri(regs, a, b, c):
        regs[c] = 1 if regs[a] == b else 0

    def eqrr(regs, a, b, c):
        regs[c] = 1 if regs[a] == regs[b] else 0

    ops = [
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr,
    ]

    # Part 1: Count samples behaving like >= 3 opcodes
    count_ge_3 = 0

    # Also for Part 2: Track possible opcodes
    possible_mapping = {i: set(ops) for i in range(16)}

    for s in samples:
        matches = 0
        valid_ops_for_sample = set()

        opcode = s["instr"][0]
        a, b, c = s["instr"][1:]

        for op in ops:
            regs = list(s["before"])
            try:
                op(regs, a, b, c)
                if regs == s["after"]:
                    matches += 1
                    valid_ops_for_sample.add(op)
            except IndexError:
                pass

        if matches >= 3:
            count_ge_3 += 1

        possible_mapping[opcode] &= valid_ops_for_sample

    print(f"Part 1 Result: {count_ge_3}")

    # Part 2: Deduce mapping
    final_mapping = {}

    while len(final_mapping) < 16:
        # Find opcodes with only 1 possibility
        determined = {k: list(v)[0] for k, v in possible_mapping.items() if len(v) == 1}

        if not determined:
            print("Error: Could not determine mapping uniquely")
            break

        for opcode, op in determined.items():
            if opcode in final_mapping:
                continue

            final_mapping[opcode] = op
            # Remove this op from all other sets
            for k in possible_mapping:
                if op in possible_mapping[k]:
                    possible_mapping[k].remove(op)

    # Execute program
    regs = [0, 0, 0, 0]
    for instr in program:
        opcode, a, b, c = instr
        op = final_mapping[opcode]
        op(regs, a, b, c)

    print(f"Part 2 Result: {regs[0]}")


if __name__ == "__main__":
    solve()
