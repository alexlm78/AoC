# Day 21 Part 1 Analysis
# The program only checks Register 0 at one specific instruction:
# 30: eqrr 5 0 4
# This compares Register 5 with Register 0.
# If they are equal, R4 becomes 1.
# 31: addr 4 1 1 -> Adds R4 (1) to IP (31), so IP becomes 32.
# 32: seti 5 8 1 -> This is outside the program (lines 0-32, wait, line 32 is in input?)
# Input has 33 lines (0 to 32).
# Line 32: seti 5 8 1.
# Wait, if IP becomes 32, it executes line 32.
# Line 32 sets IP to 5. So it loops back to 6.
# Wait, if R5 == R0, then R4=1. IP = 31 + 1 = 32.
# Then line 32 executes: seti 5 8 1 -> IP=5.
# Then IP increments to 6.
# So if R5 == R0, we jump to 6?
# Let's check the logic.
# If R5 != R0, R4=0. IP = 31 + 0 = 31.
# Then IP increments to 32.
# Then line 32 executes: seti 5 8 1 -> IP=5.
# Then IP increments to 6.
# This means regardless of the check, we loop back to 6?
# Wait, let's look at the input again.
# 30: eqrr 5 0 4  (R4 = 1 if R5 == R0 else 0)
# 31: addr 4 1 1  (IP = IP + R4) -> IP is 31.
# If match: IP = 31 + 1 = 32.
# If no match: IP = 31 + 0 = 31.
# Then IP increments (instruction cycle).
# If match: IP becomes 33. -> HALT.
# If no match: IP becomes 32. -> Execute line 32.
# Line 32: seti 5 8 1. IP reg (1) becomes 5.
# Then IP increments to 6. Loop.

# So, to HALT, we need R5 == R0 at instruction 30.
# We need to find the FIRST value of R5 when we hit instruction 30.
# That value is the answer to Part 1.

# Let's simulate the program until we hit instruction 30.
# Since we need the fewest instructions, we just need the first occurrence.


def solve():
    # Optimized logic for Part 2
    # The assembly code implements a hashing-like function.
    # We can replicate it in Python to be much faster.

    seen_values = set()
    last_unique_value = None

    # Initial register values
    r5 = 0

    while True:
        # Instruction 6: bori 5 65536 3
        t = r5 | 65536  # t maps to r3

        # Instruction 7: seti 521363 7 5
        r5 = 521363

        while True:
            # Instruction 8: bani 3 255 4
            r4 = t & 255

            # Instruction 9: addr 5 4 5
            r5 = r5 + r4

            # Instruction 10: bani 5 16777215 5
            r5 = r5 & 16777215

            # Instruction 11: muli 5 65899 5
            r5 = r5 * 65899

            # Instruction 12: bani 5 16777215 5
            r5 = r5 & 16777215

            # Instruction 13: gtir 256 3 4
            if 256 > t:
                # Instruction 28: eqrr 5 0 4 (Check against R0)
                # This is where the program would halt if R5 == R0.
                if len(seen_values) == 0:
                    print(f"Part 1 Result: {r5}")

                if r5 in seen_values:
                    print(f"Part 2 Result: {last_unique_value}")
                    return

                seen_values.add(r5)
                last_unique_value = r5

                # Instruction 30 loops back to Instruction 6
                break
            else:
                # Instructions 17-27: Optimized division loop
                # This block calculates t = t // 256
                t = t // 256
                # Instruction 27 loops back to Instruction 8
                continue


if __name__ == "__main__":
    solve()
