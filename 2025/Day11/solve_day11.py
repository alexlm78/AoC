#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 11: Reactor
Find all possible paths from 'you' to 'out' in a directed graph
"""

from typing import Dict, List, Set
from collections import defaultdict


def parse_input(filename: str) -> Dict[str, List[str]]:
    """
    Parse the input file to build the graph.

    Args:
        filename: Input file name

    Returns:
        Dictionary where each key is a device and the value is the list of connected devices
    """
    graph = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse line: "device: output1 output2 ..."
            parts = line.split(": ")
            if len(parts) != 2:
                continue

            device = parts[0]
            outputs = parts[1].split()

            graph[device] = outputs

    return dict(graph)


def find_all_paths_dfs(
    graph: Dict[str, List[str]], start: str, end: str
) -> List[List[str]]:
    """
    Find all possible paths from start to end using DFS.

    Args:
        graph: Graph represented as an adjacency dictionary
        start: Start node
        end: Target node

    Returns:
        List of all possible paths (each path is a list of nodes)
    """
    all_paths = []

    def dfs(current_node: str, current_path: List[str], visited: Set[str]):
        # If we reach the target, save the path
        if current_node == end:
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

                dfs(next_node, current_path, visited)

                # Backtrack
                current_path.pop()
                visited.remove(next_node)

    # Start DFS from the start node
    if start in graph:
        visited = {start}
        dfs(start, [start], visited)

    return all_paths


def count_paths_optimized(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """
    Count all possible paths in an optimized way using memoization.

    Args:
        graph: Graph represented as an adjacency dictionary
        start: Start node
        end: Target node

    Returns:
        Total number of possible paths
    """
    memo = {}

    def count_paths_from(node: str, visited: Set[str]) -> int:
        # If we reach the target, there is exactly 1 path
        if node == end:
            return 1

        # If the node has no outputs, there are no paths
        if node not in graph:
            return 0

        # Create a memoization key (current node + visited nodes)
        visited_tuple = tuple(sorted(visited))
        memo_key = (node, visited_tuple)

        if memo_key in memo:
            return memo[memo_key]

        total_paths = 0

        # Explore all connected nodes
        for next_node in graph[node]:
            # Avoid cycles
            if next_node not in visited:
                new_visited = visited | {next_node}
                total_paths += count_paths_from(next_node, new_visited)

        memo[memo_key] = total_paths
        return total_paths

    return count_paths_from(start, {start})


def test_example():
    """Test with the example given in the statement"""

    # Create the example graph
    example_graph = {
        "aaa": ["you", "hhh"],
        "you": ["bbb", "ccc"],
        "hhh": ["ccc", "fff", "iii"],
        "bbb": ["ddd", "eee"],
        "ccc": ["ddd", "eee", "fff"],
        "ddd": ["ggg"],
        "eee": ["out"],
        "fff": ["out"],
        "ggg": ["out"],
        "iii": ["out"],
    }

    # Find all paths from 'you' to 'out'
    paths = find_all_paths_dfs(example_graph, "you", "out")

    print("Example - Paths found:")
    for i, path in enumerate(paths, 1):
        print(f"{i}. {' -> '.join(path)}")

    print(f"\nTotal paths in the example: {len(paths)} (expected: 5)")

    # Verify with the optimized method
    count_optimized = count_paths_optimized(example_graph, "you", "out")
    print(f"Optimized count: {count_optimized}")

    return len(paths) == 5


def main():
    """Main function that solves the full puzzle."""

    print("Testing with the example...")
    if not test_example():
        print("❌ The example does not match. Verify the algorithm.")
        return

    print("✅ Example correct! Solving the full puzzle...\n")

    # Load the graph from the input file
    graph = parse_input("Day11/input_11.txt")

    print(f"Graph loaded: {len(graph)} devices")

    # Verify that nodes 'you' and 'out' exist
    if "you" not in graph:
        print("❌ Device 'you' not found in the graph")
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

    print("Counting paths from 'you' to 'out'...")

    # Use the optimized method to count paths
    total_paths = count_paths_optimized(graph, "you", "out")

    print(f"\n🎯 Total different paths from 'you' to 'out': {total_paths}")


if __name__ == "__main__":
    main()
