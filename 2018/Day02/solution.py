from collections import Counter


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        # Part 1
        count_twos = 0
        count_threes = 0

        for line in lines:
            counts = Counter(line)

            has_two = False
            has_three = False

            for count in counts.values():
                if count == 2:
                    has_two = True
                elif count == 3:
                    has_three = True

            if has_two:
                count_twos += 1
            if has_three:
                count_threes += 1

        checksum = count_twos * count_threes
        print(f"Part 1 - Checksum: {checksum}")

        # Part 2
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                id1 = lines[i]
                id2 = lines[j]

                # Assume lines have same length
                diff_count = 0
                diff_index = -1

                for k in range(len(id1)):
                    if id1[k] != id2[k]:
                        diff_count += 1
                        diff_index = k
                        if diff_count > 1:
                            break

                if diff_count == 1:
                    common_chars = id1[:diff_index] + id1[diff_index + 1 :]
                    print(f"Part 2 - Common letters: {common_chars}")
                    return

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
