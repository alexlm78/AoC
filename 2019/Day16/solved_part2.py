from time import time


def solve_part2(data):
    """
    Optimized solution for Part 2.

    Key insight: When the message offset is in the second half of the signal,
    the FFT pattern simplifies dramatically. For positions in the second half,
    the pattern only contains 1s (no 0s or -1s), which means each new digit
    is just the sum of all digits from that position to the end, mod 10.

    This allows us to compute from right to left using cumulative sums.
    """
    # Get the message offset from first 7 digits
    message_offset = int(data[:7])

    # Repeat the input 10000 times
    full_signal = list(map(int, data)) * 10000
    total_length = len(full_signal)

    print(f"Message offset: {message_offset}")
    print(f"Total signal length: {total_length}")
    print(f"Offset is in second half: {message_offset > total_length // 2}")

    # Check if offset is in second half (this is the key optimization)
    if message_offset < total_length // 2:
        print("Warning: Offset is in first half - this will be slow!")
        # For first half, we'd need the full FFT algorithm
        # This is computationally expensive for 10000 repetitions

    # We only need to compute from the offset onwards
    # This is a huge optimization - we don't need the first half of the signal
    signal = full_signal[message_offset:]

    # Run 100 phases
    start = time()
    for phase in range(100):
        if phase % 10 == 0:
            elapsed = time() - start
            print(f"Phase {phase}/100 - Elapsed: {elapsed:.2f}s")

        # For the second half, each position is the sum of all positions
        # from that point to the end, mod 10
        # We can compute this efficiently from right to left
        new_signal = [0] * len(signal)
        cumsum = 0

        for i in range(len(signal) - 1, -1, -1):
            cumsum += signal[i]
            new_signal[i] = cumsum % 10

        signal = new_signal

    elapsed = time() - start
    print(f"Total time: {elapsed:.2f}s")

    # Extract the 8-digit message
    message = "".join(map(str, signal[:8]))
    return message


# Read input
with open("input.txt", "r") as file:
    txt = file.read().strip()

print("Solving Part 2...")
result = solve_part2(txt)
print(f"\nPart 2: {result}")
