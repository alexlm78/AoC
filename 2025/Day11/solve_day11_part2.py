#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 11: Reactor - Part 2
Find all paths from 'svr' to 'out' that go through 'dac' AND 'fft'
"""

from typing import Dict, List, Set
from solve_day11 import parse_input


def find_paths_through_required_nodes(
    graph: Dict[str, List[str]], start: str, end: str, required_nodes: Set[str]
) -> List[List[str]]:
    """
    Find all paths from start to end that go through ALL required nodes.

    Args:
        graph: Graph represented as an adjacency dictionary
        start: Start node
        end: Target node
        required_nodes: Set of nodes that MUST be in the path

    Returns:
        List of all valid paths
    """
    all_paths = []

    def dfs(
        current_node: str,
        current_path: List[str],
        visited: Set[str],
        required_visited: Set[str],
    ):
        """
        DFS that tracks both visited nodes and visited required nodes
        """
        # If we reach the target, verify all required nodes were visited
        if current_node == end:
            if required_visited == required_nodes:
                all_paths.append(current_path.copy())
            return

        # If the current node has no outputs, end this path
        if current_node not in graph:
            return

        # Explore all connected nodes
        for next_node in graph[current_node]:
            # Avoid infinite cycles
            if next_node not in visited:
                visited.add(next_node)
                current_path.append(next_node)

                # Update the set of visited required nodes
                new_required_visited = required_visited.copy()
                if next_node in required_nodes:
                    new_required_visited.add(next_node)

                dfs(next_node, current_path, visited, new_required_visited)

                # Backtrack
                current_path.pop()
                visited.remove(next_node)

    # Start DFS from the start node
    if start in graph:
        visited = {start}
        initial_required = set()
        if start in required_nodes:
            initial_required.add(start)

        dfs(start, [start], visited, initial_required)

    return all_paths


def count_paths_with_bitmask(
    graph: Dict[str, List[str]], start: str, end: str, required_nodes: Set[str]
) -> int:
    """
    Ultra-efficient approach using a bitmask to track visited required nodes.
    Only tracks the state of required nodes, not all visited nodes.
    """
    # Mapear nodos requeridos a bits
    required_list = list(required_nodes)
    node_to_bit = {node: i for i, node in enumerate(required_list)}
    target_mask = (1 << len(required_nodes)) - 1  # All bits set to 1

    memo = {}

    def count_from(node: str, required_mask: int) -> int:
        # If we reach the target with all required nodes visited
        if node == end:
            return 1 if required_mask == target_mask else 0

        # If there are no outputs from this node
        if node not in graph:
            return 0

        # Memoization using only current node and required mask
        memo_key = (node, required_mask)
        if memo_key in memo:
            return memo[memo_key]

        total = 0
        for next_node in graph[node]:
            new_mask = required_mask
            # If the next node is required, set its bit
            if next_node in node_to_bit:
                new_mask |= 1 << node_to_bit[next_node]

            total += count_from(next_node, new_mask)

        memo[memo_key] = total
        return total

    # Initialize mask
    initial_mask = 0
    if start in node_to_bit:
        initial_mask |= 1 << node_to_bit[start]

    return count_from(start, initial_mask)


def test_example_part2():
    """Test with the example for part 2"""

    # Create the example graph
    example_graph = {
        "svr": ["aaa", "bbb"],
        "aaa": ["fft"],
        "fft": ["ccc"],
        "bbb": ["tty"],
        "tty": ["ccc"],
        "ccc": ["ddd", "eee"],
        "ddd": ["hub"],
        "hub": ["fff"],
        "eee": ["dac"],
        "dac": ["fff"],
        "fff": ["ggg", "hhh"],
        "ggg": ["out"],
        "hhh": ["out"],
    }

    required_nodes = {"dac", "fft"}

    # Find all paths that go through dac AND fft
    paths = find_paths_through_required_nodes(
        example_graph, "svr", "out", required_nodes
    )

    print("Part 2 Example - Paths that go through 'dac' AND 'fft':")
    for i, path in enumerate(paths, 1):
        print(f"{i}. {' -> '.join(path)}")

    print(f"\nTotal valid paths in the example: {len(paths)} (expected: 2)")

    # Verify with the bitmask method
    count_bitmask = count_paths_with_bitmask(
        example_graph, "svr", "out", required_nodes
    )
    print(f"Bitmask count: {count_bitmask}")

    return len(paths) == 2


def main():
    """Main function that solves part 2 of the puzzle."""

    print("Testing with the part 2 example...")
    if not test_example_part2():
        print("❌ The part 2 example does not match. Verify the algorithm.")
        return

    print("✅ Part 2 example correct! Solving the full puzzle...\n")

    # Load the graph from the input file
    graph = parse_input("Day11/input_11.txt")

    print(f"Graph loaded: {len(graph)} devices")

    # Verify that required nodes exist
    required_nodes = {"dac", "fft"}
    missing_nodes = []

    if "svr" not in graph:
        missing_nodes.append("svr")

    for node in required_nodes:
        # Verify the node exists in the graph (as source or destination)
        node_exists = node in graph
        if not node_exists:
            # Check if it appears as a destination
            for device, outputs in graph.items():
                if node in outputs:
                    node_exists = True
                    break
        if not node_exists:
            missing_nodes.append(node)

    if missing_nodes:
        print(f"❌ The following nodes were not found: {missing_nodes}")
        return

    # Check if any device can reach 'out'
    has_out = False
    for device, outputs in graph.items():
        if "out" in outputs:
            has_out = True
            break

    if not has_out:
        print("❌ No device found that connects to 'out'")
        return

    print("Counting paths from 'svr' to 'out' that go through 'dac' AND 'fft'...")

    # Use the bitmask method to count paths
    total_paths = count_paths_with_bitmask(graph, "svr", "out", required_nodes)

    print(
        f"\n🎯 Total paths from 'svr' to 'out' that go through 'dac' AND 'fft': {total_paths}"
    )


if __name__ == "__main__":
    main()
