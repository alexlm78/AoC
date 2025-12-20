from collections import deque


def solve():
    try:
        with open("input.txt", "r") as f:
            regex = f.read().strip()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return

    # Parse regex and build map (distances)
    # We can use a stack to handle branching
    # Current position: (0, 0)

    # Map stores shortest distance to each room (x, y) from (0, 0)
    # Actually, we just need to track the distance as we traverse.
    # BFS is implicit in the structure if we explore all paths?
    # No, regex describes paths. We can just follow them.
    # Since we need "shortest path from starting location", we are essentially building a graph
    # and then we can run BFS on it. Or we can compute distances on the fly if the regex doesn't have loops that shorten paths?
    # The problem says "routes that will take you... through every door... mapping out all of these routes will let you build a proper map".
    # And "find the room for which the shortest path to that room would require passing through the most doors".
    # Regex traversal is DFS-like.
    # Let's build the graph (adjacency list) first, then BFS for distances.

    adj = {}  # (x, y) -> set of (nx, ny)

    x, y = 0, 0

    # Previous position tracking isn't enough, we need to track where we are in the regex?
    # Actually, we can just simulate the traversal.
    # Stack stores (x, y) positions before branching.

    # Wait, simple stack of current positions might work?
    # When '(' push current position.
    # When '|' reset to popped position (but don't pop, peek).
    # When ')' pop.

    # Correct logic for regex stack:
    # When we see '(', we save the current position.
    # Inside a group, '|' restores the position to what it was at '('.
    # ')' finishes the group.

    # But wait, nested groups.
    # Stack should store the position at the start of the group.

    curr_x, curr_y = 0, 0
    stack = []

    # We need to handle the regex char by char
    # ^ and $ can be ignored (except for start/end check)

    for char in regex:
        if char == "^":
            continue
        elif char == "$":
            break
        elif char == "N":
            next_x, next_y = curr_x, curr_y - 1
            adj.setdefault((curr_x, curr_y), set()).add((next_x, next_y))
            adj.setdefault((next_x, next_y), set()).add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == "S":
            next_x, next_y = curr_x, curr_y + 1
            adj.setdefault((curr_x, curr_y), set()).add((next_x, next_y))
            adj.setdefault((next_x, next_y), set()).add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == "E":
            next_x, next_y = curr_x + 1, curr_y
            adj.setdefault((curr_x, curr_y), set()).add((next_x, next_y))
            adj.setdefault((next_x, next_y), set()).add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == "W":
            next_x, next_y = curr_x - 1, curr_y
            adj.setdefault((curr_x, curr_y), set()).add((next_x, next_y))
            adj.setdefault((next_x, next_y), set()).add((curr_x, curr_y))
            curr_x, curr_y = next_x, next_y
        elif char == "(":
            stack.append((curr_x, curr_y))
        elif char == "|":
            curr_x, curr_y = stack[-1]
        elif char == ")":
            # End of group.
            # Does ')' reset position? No.
            # If we had (A|B), we end up at end of B.
            # If we had (A|), we end up at start of group (effectively).
            # The stack top is the start of the group. We pop it.
            # BUT, wait.
            # If regex is (N|S), after processing, we could be at N or S?
            # No, the problem implies "branches".
            # The description says: "^N(E|W)N$ ... after going north, you must choose to go either east or west before finishing your route by going north again."
            # This implies that the paths merge back? Or do they?
            # "Sequences of letters like this always match that exact route".
            # "Regardless of which option is taken, the route continues from the position it is left at after taking those steps."
            # Wait, if we have N(E|W)N:
            # Path 1: N -> E -> N
            # Path 2: N -> W -> N
            # This means from the end of E, we go N. From end of W, we go N.
            # This implies the regex describes ALL valid paths.
            # My stack logic:
            # '(': Push current.
            # '|': Reset to stack top (start of group).
            # ')': Pop.
            # This leaves us at the end of the last option.
            # But what about previous options?
            # Example: N(E|W)N
            # Start (0,0). N -> (0,-1).
            # '(': Stack pushes (0,-1).
            # 'E': Move to (1,-1).
            # '|': Reset to (0,-1).
            # 'W': Move to (-1,-1).
            # ')': Pop. Current is (-1,-1).
            # 'N': Move to (-1,-2).
            # So we traced N -> W -> N.
            # But we missed N -> E -> N!
            # The 'N' after the group should apply to ALL endpoints of the group?
            # Or does the puzzle structure imply that all branches end at the same point?
            # "branches... determine where the doors are".
            # Actually, usually in AoC these regexes map out a maze where branches loop back or dead end.
            # If the regex is simple like ^ENWWW(NEEE|SSE(EE|N))$, the branches might not merge.
            # BUT, to build the map, we need to explore ALL branches.
            # So, we need to track a SET of current positions?
            # No, the standard stack approach for this problem (which is common) handles simple branching.
            # However, to correctly handle the continuation after ')' applying to all branches, we would need more complex logic.
            # BUT, let's look at the input.
            # If the input is a tree traversal (DFS), we just need to record the doors.
            # The issue is subsequent characters.
            # If the regex is N(E|W)S, does S connect to both E and W endpoints?
            # If it's a "Regular Map", usually it means we are exploring a consistent grid.
            # If N(E|W)S is valid, then E and W must end up at the same spot? Or S is valid from both?
            # If S is valid from both, then there are doors from E-end to South, and W-end to South.
            # In typical regex, concatenation distributes over alternation: N(E|W)S == NES|NWS.
            # So yes, we need to continue from ALL endpoints.

            # Since this is likely a maze exploration, we can just maintain the graph.
            # And since the regex is a single long string, we can process it.
            # But how to handle the state?
            # If we use recursion or a stack of positions?
            # Since the graph is static, we can traverse it.

            # Let's verify if branches merge.
            # Input snippet: (NNNEESW... | WWWWS...)
            # It seems they explore different areas.
            # If they don't merge, then simple stack with reset is fine, BUT we need to handle the fact that
            # after ')', we might need to continue from multiple points?
            # Actually, in many AoC solutions for this day, it is observed that (A|B)C usually implies A and B end at the same point OR C is empty.
            # OR, we just need to traverse the whole regex to find all doors.
            # Finding the furthest room is BFS on the resulting graph.
            # So the only goal is to build the adjacency list.

            # If I use a recursive function `build_map(regex_part, start_positions)` it might blow up.
            # Better: Iterative approach.
            # `positions` is a set of current possible locations.
            # Initially {(0,0)}.
            # Char 'N': For each pos in positions, move N, add edge, update pos.
            # Char '(': Push current `positions` to stack.
            # Char '|': The group branches. We need to collect endpoints.
            #   We have `start_positions` (from stack top).
            #   We have `current_positions` (end of current branch).
            #   We need to accumulate `end_positions` of the whole group.
            #   When '|', we add `current_positions` to `group_end_positions`, and reset `current_positions` to `start_positions`.
            # Char ')': Add `current_positions` to `group_end_positions`.
            #   Pop `start_positions`.
            #   Set `current_positions` to `group_end_positions`.

            # Let's refine stack logic.
            # Stack stores: (start_positions, group_end_positions)

            stack.pop()  # Remove the tuple

            pass

    # New Logic:
    current_positions = {(0, 0)}
    stack = []  # Stores (starts, ends)

    for char in regex:
        if char == "^":
            continue
        elif char == "$":
            break
        elif char in "NSEW":
            next_positions = set()
            for x, y in current_positions:
                if char == "N":
                    nx, ny = x, y - 1
                elif char == "S":
                    nx, ny = x, y + 1
                elif char == "E":
                    nx, ny = x + 1, y
                elif char == "W":
                    nx, ny = x - 1, y

                adj.setdefault((x, y), set()).add((nx, ny))
                adj.setdefault((nx, ny), set()).add((x, y))
                next_positions.add((nx, ny))
            current_positions = next_positions
        elif char == "(":
            stack.append((current_positions, set()))
        elif char == "|":
            starts, ends = stack[-1]
            ends.update(current_positions)
            current_positions = starts
        elif char == ")":
            starts, ends = stack.pop()
            ends.update(current_positions)
            current_positions = ends

    # BFS for shortest path distances
    distances = {}
    q = deque([(0, 0, 0)])  # x, y, dist
    distances[(0, 0)] = 0

    max_dist = 0

    while q:
        x, y, dist = q.popleft()

        if dist > max_dist:
            max_dist = dist

        for nx, ny in adj.get((x, y), []):
            if (nx, ny) not in distances:
                distances[(nx, ny)] = dist + 1
                q.append((nx, ny, dist + 1))

    print(f"Part 1 Result: {max_dist}")

    # Part 2: Count rooms with distance >= 1000
    count_1000 = sum(1 for d in distances.values() if d >= 1000)
    print(f"Part 2 Result: {count_1000}")


if __name__ == "__main__":
    solve()
