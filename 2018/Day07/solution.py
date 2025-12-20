import re
from collections import defaultdict
import heapq


def parse_graph(lines):
    adj = defaultdict(list)
    in_degree = defaultdict(int)
    all_steps = set()

    for line in lines:
        match = re.match(
            r"Step (\w) must be finished before step (\w) can begin.", line
        )
        if match:
            u, v = match.groups()
            adj[u].append(v)
            in_degree[v] += 1
            all_steps.add(u)
            all_steps.add(v)
    return adj, in_degree, all_steps


def solve():
    try:
        with open("input.txt", "r") as f:
            lines = f.readlines()

        # Part 1
        adj, in_degree, all_steps = parse_graph(lines)

        queue = []
        for step in all_steps:
            if in_degree[step] == 0:
                heapq.heappush(queue, step)

        result = []

        while queue:
            u = heapq.heappop(queue)
            result.append(u)

            if u in adj:
                for v in adj[u]:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        heapq.heappush(queue, v)

        print(f"Order: {''.join(result)}")

        # Part 2
        adj, in_degree, all_steps = parse_graph(lines)

        queue = []
        for step in all_steps:
            if in_degree[step] == 0:
                heapq.heappush(queue, step)

        workers = [{"step": None, "time_left": 0} for _ in range(5)]
        current_time = 0

        while True:
            # 1. Process completions
            # Check if any worker has finished their task
            for w in workers:
                if w["step"] is not None and w["time_left"] == 0:
                    finished_step = w["step"]
                    w["step"] = None

                    if finished_step in adj:
                        for v in adj[finished_step]:
                            in_degree[v] -= 1
                            if in_degree[v] == 0:
                                heapq.heappush(queue, v)

            # 2. Assign work
            # Try to assign available tasks to idle workers
            for w in workers:
                if w["step"] is None and queue:
                    step = heapq.heappop(queue)
                    duration = 60 + ord(step) - ord("A") + 1
                    w["step"] = step
                    w["time_left"] = duration

            # 3. Check active workers
            active_workers = False
            for w in workers:
                if w["step"] is not None:
                    active_workers = True
                    break

            if not active_workers:
                break

            # 4. Advance time
            # Find the minimum time to the next event
            min_jump = float("inf")
            for w in workers:
                if w["step"] is not None:
                    if w["time_left"] < min_jump:
                        min_jump = w["time_left"]

            current_time += min_jump
            for w in workers:
                if w["step"] is not None:
                    w["time_left"] -= min_jump

        print(f"Total time: {current_time}")

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
