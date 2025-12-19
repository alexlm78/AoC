import sys
from collections import defaultdict

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def runComputer(data, input):
    program = defaultdict(int, {k: v for k, v in enumerate(data)})
    output = None
    i = 0
    relbase = 0

    while True:
        opcode = program[i] % 100

        if opcode == 99:
            break

        mode1 = (program[i] - opcode) // 100 % 10
        mode2 = (program[i] - opcode) // 1000 % 10
        mode3 = (program[i] - opcode) // 10000 % 10

        p1, p2, p3 = None, None, None

        if mode1 == 0:
            p1 = program[i + 1]
        elif mode1 == 1:
            p1 = i + 1
        elif mode1 == 2:
            p1 = program[i + 1] + relbase

        if mode2 == 0:
            p2 = program[i + 2]
        elif mode2 == 1:
            p2 = i + 2
        elif mode2 == 2:
            p2 = program[i + 2] + relbase

        if mode3 == 0:
            p3 = program[i + 3]
        elif mode3 == 1:
            raise ValueError("Immediate mode invalid for param 3")
        elif mode3 == 2:
            p3 = program[i + 3] + relbase

        if opcode == 1:  # addition
            program[p3] = program[p1] + program[p2]
            i += 4
        elif opcode == 2:  # multiplication
            program[p3] = program[p1] * program[p2]
            i += 4
        elif opcode == 3:  # input
            if len(input) == 0:
                raise ValueError("No input available")
            program[p1] = input.pop()
            i += 2
        elif opcode == 4:  # output
            yield program[p1]
            i += 2
        elif opcode == 5:  # jump-if-true
            i = program[p2] if program[p1] != 0 else i + 3
        elif opcode == 6:  # jump-if-false
            i = program[p2] if program[p1] == 0 else i + 3
        elif opcode == 7:  # less-than
            program[p3] = 1 if program[p1] < program[p2] else 0
            i += 4
        elif opcode == 8:  # equals
            program[p3] = 1 if program[p1] == program[p2] else 0
            i += 4
        elif opcode == 9:  # relative base adjust
            relbase += program[p1]
            i += 2
        else:
            raise ValueError(f"opcode {opcode} from {program[i]}")


def solve(data, debug=False):
    # Wake up the robot by changing address 0 from 1 to 2
    data[0] = 2

    # Correct path derived from analyze_path.py:
    # Full path: R,8,R,10,R,10,R,4,R,8,R,10,R,12,R,8,R,10,R,10,R,12,R,4,L,12,L,12,
    #            R,8,R,10,R,10,R,4,R,8,R,10,R,12,R,12,R,4,L,12,L,12,R,8,R,10,R,10,
    #            R,4,R,8,R,10,R,12,R,12,R,4,L,12,L,12
    #
    # Breaking it down:
    # A: R,8,R,10,R,10      (13 chars)
    # B: R,4,R,8,R,10,R,12  (17 chars)
    # C: R,12,R,4,L,12,L,12 (18 chars)
    # Main: A,B,A,C,A,B,C,A,B,C (19 chars)

    main_routine = "A,B,A,C,A,B,C,A,B,C"
    func_a = "R,8,R,10,R,10"
    func_b = "R,4,R,8,R,10,R,12"
    func_c = "R,12,R,4,L,12,L,12"
    video_feed = "n"

    # Verify lengths (must be <= 20 characters)
    if debug:
        print(f"Main routine: '{main_routine}' (length: {len(main_routine)})")
        print(f"Function A: '{func_a}' (length: {len(func_a)})")
        print(f"Function B: '{func_b}' (length: {len(func_b)})")
        print(f"Function C: '{func_c}' (length: {len(func_c)})")
        print()

    moves = [main_routine, func_a, func_b, func_c, video_feed]

    # Convert to ASCII codes and add newlines
    inputs = []
    for line in moves:
        for c in line:
            inputs.append(ord(c))
        inputs.append(10)  # newline

    # Reverse because IntCode uses a stack (pop from end)
    inputs = inputs[::-1]

    if debug:
        print(f"Total input characters: {len(inputs)}")

    runner = runComputer(data, inputs)
    dust_collected = 0
    output_buffer = []
    show_output = debug

    try:
        while True:
            status = next(runner, "halt")
            if status == "halt":
                break

            output_buffer.append(status)

            # ASCII printable range
            if status < 256:
                if show_output:
                    print(chr(status), end="")
            else:
                # Large non-ASCII value is the dust collected
                dust_collected = status
                if debug:
                    print(f"\n\nDust collected: {dust_collected}")
                break
    except Exception as e:
        if debug:
            print(f"\nError: {e}")
            print(f"Last outputs: {output_buffer[-20:]}")
        raise

    return dust_collected


# Read input
with open("input.txt", "r") as file:
    raw = list(map(int, file.read().splitlines()[0].split(",")))

# Run with debug to see what's happening
print("Running Part 2...\n")
result = solve(raw.copy(), debug=False)
print(f"Part 2: {result}")
