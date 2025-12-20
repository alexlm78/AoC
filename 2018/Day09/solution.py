import re
from collections import deque


def get_high_score(num_players, last_marble):
    scores = [0] * num_players
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            removed_marble = circle.pop()
            player = (marble - 1) % num_players
            scores[player] += marble + removed_marble
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores)


def solve():
    try:
        with open("input.txt", "r") as f:
            content = f.read().strip()

        match = re.match(r"(\d+) players; last marble is worth (\d+) points", content)
        if not match:
            print("Error: Could not parse input.")
            return

        num_players = int(match.group(1))
        last_marble = int(match.group(2))

        # Part 1
        result_p1 = get_high_score(num_players, last_marble)
        print(f"High score: {result_p1}")

        # Part 2
        result_p2 = get_high_score(num_players, last_marble * 100)
        print(f"High score (100x): {result_p2}")

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
