import re
from collections import defaultdict


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        # Sort lines chronologically
        lines.sort()

        guards = defaultdict(lambda: defaultdict(int))
        guards_total_sleep = defaultdict(int)

        current_guard = None
        sleep_start = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Parse timestamp and message
            match = re.match(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)", line)
            if not match:
                continue

            minute = int(match.group(5))
            message = match.group(6)

            if "Guard" in message:
                # Guard #10 begins shift
                guard_match = re.search(r"#(\d+)", message)
                if guard_match:
                    current_guard = int(guard_match.group(1))
            elif "falls asleep" in message:
                sleep_start = minute
            elif "wakes up" in message:
                if current_guard is not None and sleep_start is not None:
                    # Record sleep minutes
                    for m in range(sleep_start, minute):
                        guards[current_guard][m] += 1
                        guards_total_sleep[current_guard] += 1
                    sleep_start = None

        # Strategy 1: Find the guard that has the most minutes asleep
        if not guards_total_sleep:
            print("No sleep data found.")
            return

        sleepiest_guard = max(guards_total_sleep, key=guards_total_sleep.get)
        sleepiest_guard_minutes = guards[sleepiest_guard]

        if sleepiest_guard_minutes:
            sleepiest_minute = max(
                sleepiest_guard_minutes, key=sleepiest_guard_minutes.get
            )
            print("Strategy 1:")
            print(f"Sleepiest Guard: {sleepiest_guard}")
            print(f"Sleepiest Minute: {sleepiest_minute}")
            print(f"Result: {sleepiest_guard * sleepiest_minute}")
        else:
            print("Strategy 1: No sleep data for the sleepiest guard.")

        # Strategy 2: Of all guards, which guard is most frequently asleep on the same minute?
        max_frequency = -1
        target_guard = -1
        target_minute = -1

        for guard_id, minutes in guards.items():
            if not minutes:
                continue
            most_frequent_minute = max(minutes, key=minutes.get)
            frequency = minutes[most_frequent_minute]

            if frequency > max_frequency:
                max_frequency = frequency
                target_guard = guard_id
                target_minute = most_frequent_minute

        print("\nStrategy 2:")
        print(f"Guard: {target_guard}")
        print(f"Minute: {target_minute}")
        print(f"Frequency: {max_frequency}")
        print(f"Result: {target_guard * target_minute}")

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
