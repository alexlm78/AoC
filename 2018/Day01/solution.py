import itertools


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        changes = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            changes.append(int(line))

        # Part 1
        part1_frequency = sum(changes)
        print(f"Part 1 - Resulting frequency: {part1_frequency}")

        # Part 2
        current_frequency = 0
        seen_frequencies = {0}

        # itertools.cycle repeats the list of changes indefinitely
        for change in itertools.cycle(changes):
            current_frequency += change
            if current_frequency in seen_frequencies:
                print(f"Part 2 - First frequency reached twice: {current_frequency}")
                return
            seen_frequencies.add(current_frequency)

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
