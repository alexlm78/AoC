def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return

    ip_reg = int(lines[0].split()[1])
    program = []
    for line in lines[1:]:
        parts = line.split()
        opcode = parts[0]
        a = int(parts[1])
        b = int(parts[2])
        c = int(parts[3])
        program.append((opcode, a, b, c))

    # Part 1
    registers = [0] * 6
    ip = 0

    # We can run the simulation for Part 1 as it's fast enough
    while 0 <= ip < len(program):
        registers[ip_reg] = ip
        opcode, a, b, c = program[ip]

        if opcode == "addr":
            registers[c] = registers[a] + registers[b]
        elif opcode == "addi":
            registers[c] = registers[a] + b
        elif opcode == "mulr":
            registers[c] = registers[a] * registers[b]
        elif opcode == "muli":
            registers[c] = registers[a] * b
        elif opcode == "banr":
            registers[c] = registers[a] & registers[b]
        elif opcode == "bani":
            registers[c] = registers[a] & b
        elif opcode == "borr":
            registers[c] = registers[a] | registers[b]
        elif opcode == "bori":
            registers[c] = registers[a] | b
        elif opcode == "setr":
            registers[c] = registers[a]
        elif opcode == "seti":
            registers[c] = a
        elif opcode == "gtir":
            registers[c] = 1 if a > registers[b] else 0
        elif opcode == "gtri":
            registers[c] = 1 if registers[a] > b else 0
        elif opcode == "gtrr":
            registers[c] = 1 if registers[a] > registers[b] else 0
        elif opcode == "eqir":
            registers[c] = 1 if a == registers[b] else 0
        elif opcode == "eqri":
            registers[c] = 1 if registers[a] == b else 0
        elif opcode == "eqrr":
            registers[c] = 1 if registers[a] == registers[b] else 0

        ip = registers[ip_reg]
        ip += 1

    print(f"Part 1 Result: {registers[0]}")

    # Part 2
    # The program calculates the sum of divisors of a number stored in a register (R5 in this case).
    # We run the initialization until it enters the main loop (usually instruction 1).
    registers = [0] * 6
    registers[0] = 1  # Part 2 start
    ip = 0

    # Run until we hit instruction 1 (the start of the main loop) repeatedly
    # Actually, we just need to run enough cycles to finish initialization.
    # Initialization usually takes ~20-50 instructions.

    cycle_limit = 1000
    for _ in range(cycle_limit):
        registers[ip_reg] = ip
        opcode, a, b, c = program[ip]

        if opcode == "addr":
            registers[c] = registers[a] + registers[b]
        elif opcode == "addi":
            registers[c] = registers[a] + b
        elif opcode == "mulr":
            registers[c] = registers[a] * registers[b]
        elif opcode == "muli":
            registers[c] = registers[a] * b
        elif opcode == "banr":
            registers[c] = registers[a] & registers[b]
        elif opcode == "bani":
            registers[c] = registers[a] & b
        elif opcode == "borr":
            registers[c] = registers[a] | registers[b]
        elif opcode == "bori":
            registers[c] = registers[a] | b
        elif opcode == "setr":
            registers[c] = registers[a]
        elif opcode == "seti":
            registers[c] = a
        elif opcode == "gtir":
            registers[c] = 1 if a > registers[b] else 0
        elif opcode == "gtri":
            registers[c] = 1 if registers[a] > b else 0
        elif opcode == "gtrr":
            registers[c] = 1 if registers[a] > registers[b] else 0
        elif opcode == "eqir":
            registers[c] = 1 if a == registers[b] else 0
        elif opcode == "eqri":
            registers[c] = 1 if registers[a] == b else 0
        elif opcode == "eqrr":
            registers[c] = 1 if registers[a] == registers[b] else 0

        ip = registers[ip_reg]
        ip += 1

        if ip == 1:
            break

    # The target number is in R5 (based on analysis of instructions 1-16 which compare R1*R3 to R5)
    # R5 is the number being factorized.
    target = registers[5]

    total = 0
    for i in range(1, int(target**0.5) + 1):
        if target % i == 0:
            total += i
            if i * i != target:
                total += target // i

    print(f"Part 2 Result: {total}")


if __name__ == "__main__":
    solve()
