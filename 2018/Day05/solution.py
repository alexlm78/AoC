def react(polymer):
    stack = []
    for char in polymer:
        if not stack:
            stack.append(char)
        else:
            last_char = stack[-1]
            # Check if characters are the same type but opposite polarity
            if last_char != char and last_char.lower() == char.lower():
                stack.pop()
            else:
                stack.append(char)
    return stack


def solve():
    try:
        with open("input.txt", "r") as f:
            polymer = f.read().strip()

        # Part 1
        result_stack = react(polymer)
        print(f"Part 1 - Units remaining: {len(result_stack)}")

        # Part 2
        min_length = len(polymer)

        # Get all unique unit types (case-insensitive) present in the polymer
        unique_units = set(polymer.lower())

        for unit in unique_units:
            # Create a new polymer with the current unit type removed
            temp_polymer = polymer.replace(unit, "").replace(unit.upper(), "")

            # React the new polymer
            reacted_polymer = react(temp_polymer)

            # Update minimum length
            if len(reacted_polymer) < min_length:
                min_length = len(reacted_polymer)

        print(f"Part 2 - Shortest polymer length: {min_length}")

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
