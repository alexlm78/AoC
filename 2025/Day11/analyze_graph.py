#!/usr/bin/env python3
"""
Additional analysis of the Day 11 graph
"""

from solve_day11 import parse_input, count_paths_optimized
from collections import deque


def analyze_graph(graph):
    """Analyze graph properties"""

    print("📊 GRAPH ANALYSIS:")
    print("-" * 40)

    # Basic statistics
    total_devices = len(graph)
    total_connections = sum(len(outputs) for outputs in graph.values())

    print(f"Total devices: {total_devices}")
    print(f"Total connections: {total_connections}")
    print(f"Average connections per device: {total_connections / total_devices:.2f}")

    # Devices that connect directly to 'out'
    direct_to_out = []
    for device, outputs in graph.items():
        if "out" in outputs:
            direct_to_out.append(device)

    print(f"\nDevices that connect directly to 'out': {len(direct_to_out)}")
    print(f"Some examples: {direct_to_out[:10]}")

    # Devices from 'you'
    if "you" in graph:
        you_outputs = graph["you"]
        print(f"\nDevices connected from 'you': {len(you_outputs)}")
        print(f"Connections from 'you': {you_outputs}")

    # Find devices with no outputs (leaves)
    leaves = []
    for device, outputs in graph.items():
        if not outputs:
            leaves.append(device)

    print(f"\nDevices with no outputs (leaves): {len(leaves)}")

    # Most connected devices
    most_connected = sorted(graph.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    print("\nDevices with most connections:")
    for device, outputs in most_connected:
        print(f"  {device}: {len(outputs)} connections")


def find_shortest_path(graph, start, end):
    """Find the shortest path using BFS"""

    if start not in graph:
        return None

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        if current == end:
            return path

        if current in graph:
            for next_node in graph[current]:
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))

    return None


def main():
    """Complete graph analysis"""

    # Load the graph
    graph = parse_input("Day11/input_11.txt")

    # General analysis
    analyze_graph(graph)

    # Shortest path
    shortest = find_shortest_path(graph, "you", "out")
    if shortest:
        print("\n🎯 Shortest path from 'you' to 'out':")
        print(f"   {' -> '.join(shortest)}")
        print(f"   Length: {len(shortest) - 1} hops")

    # Count total paths
    total_paths = count_paths_optimized(graph, "you", "out")
    print(f"\n🎯 Total different paths: {total_paths}")


if __name__ == "__main__":
    main()
