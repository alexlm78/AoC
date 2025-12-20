def solve():
    try:
        with open("input.txt", "r") as f:
            input_str = f.read().strip()
            input_val = int(input_str)
            target_seq = [int(d) for d in input_str]
    except FileNotFoundError:
        print("Error: input.txt not found")
        return

    # Part 1
    scoreboard = [3, 7]
    elf1 = 0
    elf2 = 1

    # We need enough recipes for Part 1
    target_length_p1 = input_val + 10

    # For Part 2, we need to search for target_seq
    # We can combine loops or just run until we find it,
    # ensuring we also cover Part 1 length if it's not reached yet.

    # Let's run a loop that checks for Part 2 condition,
    # but we also need to print Part 1 result once we pass that length.

    part1_done = False
    part2_done = False

    seq_len = len(target_seq)

    while not (part1_done and part2_done):
        sum_val = scoreboard[elf1] + scoreboard[elf2]

        digits_added = []
        if sum_val >= 10:
            d1 = sum_val // 10
            d2 = sum_val % 10
            scoreboard.append(d1)
            digits_added.append(d1)
            scoreboard.append(d2)
            digits_added.append(d2)
        else:
            scoreboard.append(sum_val)
            digits_added.append(sum_val)

        elf1 = (elf1 + 1 + scoreboard[elf1]) % len(scoreboard)
        elf2 = (elf2 + 1 + scoreboard[elf2]) % len(scoreboard)

        # Check Part 1
        if not part1_done and len(scoreboard) >= target_length_p1:
            result_p1 = "".join(map(str, scoreboard[input_val : input_val + 10]))
            print(f"Part 1 Result: {result_p1}")
            part1_done = True

        # Check Part 2
        if not part2_done:
            # We added 1 or 2 digits. Check if the sequence matches the end.
            # Only need to check if length is sufficient
            if len(scoreboard) >= seq_len:
                # If we added 1 digit, check last seq_len
                # If we added 2 digits, we might match at end, or end-1

                # Check match at end
                if scoreboard[-seq_len:] == target_seq:
                    print(f"Part 2 Result: {len(scoreboard) - seq_len}")
                    part2_done = True
                    continue

                # If we added 2 digits, check match at end-1
                if (
                    len(digits_added) == 2
                    and scoreboard[-seq_len - 1 : -1] == target_seq
                ):
                    print(f"Part 2 Result: {len(scoreboard) - seq_len - 1}")
                    part2_done = True
                    continue


if __name__ == "__main__":
    solve()
