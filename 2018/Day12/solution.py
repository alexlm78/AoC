import re


def parse_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    initial_state_match = re.match(r"initial state: ([#\.]+)", lines[0])
    initial_state_str = initial_state_match.group(1)

    plants = set()
    for i, char in enumerate(initial_state_str):
        if char == "#":
            plants.add(i)

    rules = set()
    for line in lines[1:]:
        match = re.match(r"([#\.]+) => ([#\.])", line)
        if match:
            pattern = match.group(1)
            result = match.group(2)
            if result == "#":
                rules.add(pattern)

    return plants, rules


def get_pattern(plants, center_index):
    pattern = []
    for i in range(center_index - 2, center_index + 3):
        if i in plants:
            pattern.append("#")
        else:
            pattern.append(".")
    return "".join(pattern)


def simulate_generation(plants, rules):
    if not plants:
        return set()

    min_pot = min(plants)
    max_pot = max(plants)

    next_plants = set()

    # Check pots from min-2 to max+2
    for i in range(min_pot - 2, max_pot + 3):
        pattern = get_pattern(plants, i)
        if pattern in rules:
            next_plants.add(i)

    return next_plants


def solve():
    plants, rules = parse_input("input.txt")

    # Part 1: 20 generations
    p1_plants = plants.copy()
    for gen in range(20):
        p1_plants = simulate_generation(p1_plants, rules)
    print(f"Part 1 (20 generations): {sum(p1_plants)}")

    # Part 2: 50 billion generations
    # We look for convergence.
    plants = plants  # Reset to initial
    prev_sum = sum(plants)
    diffs = []
    target_generations = 50000000000

    # Simulate until stable
    for gen in range(1, 2000):  # 2000 should be enough to stabilize
        plants = simulate_generation(plants, rules)
        curr_sum = sum(plants)
        diff = curr_sum - prev_sum
        prev_sum = curr_sum

        diffs.append(diff)

        # Check if diff is stable for a while (e.g., 10 generations)
        if len(diffs) > 10 and all(d == diff for d in diffs[-10:]):
            remaining_gens = target_generations - gen
            final_sum = curr_sum + (remaining_gens * diff)
            print(f"Part 2 (50 billion generations): {final_sum}")
            print(f"Stabilized at generation {gen} with diff {diff}")
            return

    print("Did not stabilize within limit.")


if __name__ == "__main__":
    solve()
