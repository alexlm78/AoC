#!/usr/bin/env python3
"""
Advent of Code 2024 - Day 23: Unstable Diffusion

Part1:
- Parse the input text into a graph of edges.
- Count the number of triangles in the graph.

Part2:
- Find the maximum clique of the graph.
- Calculate the password for the maximum clique.
"""

import os
from typing import Dict, Set, List, Tuple


def parse_edges(text: str) -> List[Tuple[str, str]]:
    """
    Parse the input text into a list of edges.

    Args:
        text: Complete content of the input file.
    Returns:
        List of edges as tuples `(a, b)` where `a` and `b` are nodes.
    """
    edges: List[Tuple[str, str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        a, b = line.split("-")
        if a == b:
            continue
        if a > b:
            a, b = b, a
        edges.append((a, b))
    return edges


def build_graph(edges: List[Tuple[str, str]]) -> Dict[str, Set[str]]:
    """
    Build a graph from a list of edges.

    Args:
        edges: List of edges as tuples `(a, b)` where `a` and `b` are nodes.
    Returns:
        Dictionary representing the graph where keys are nodes and values are sets of adjacent nodes.
    """
    g: Dict[str, Set[str]] = {}
    for a, b in edges:
        g.setdefault(a, set()).add(b)
        g.setdefault(b, set()).add(a)
    return g


def count_triangles_with_t(g: Dict[str, Set[str]]) -> int:
    """
    Count the number of triangles in the graph that include at least one 't*' computer.

    Args:
        g: Dictionary representing the graph where keys are nodes and values are sets of adjacent nodes.
    Returns:
        Number of triangles with at least one 't*' computer.
    """
    nodes = sorted(g.keys())
    count = 0
    # Use edge-based iteration to find triangles efficiently
    for u in nodes:
        for v in sorted(g[u]):
            if u >= v:
                continue
            # common neighbors w where w > v to ensure unique triangle u<v<w
            common = g[u].intersection(g[v])
            for w in sorted(common):
                if v >= w:
                    continue
                if u.startswith("t") or v.startswith("t") or w.startswith("t"):
                    count += 1
    return count


def maximum_clique_password(g: Dict[str, Set[str]]) -> str:
    """
    Find the maximum clique of the graph and return the password for that clique.

    Args:
        g: Dictionary representing the graph where keys are nodes and values are sets of adjacent nodes.
    Returns:
        Comma-separated list of nodes in the maximum clique.
    """
    nodes = set(g.keys())
    best: Set[str] = set()

    def bron_kerbosch(R: Set[str], P: Set[str], X: Set[str]):
        nonlocal best
        if not P and not X:
            if len(R) > len(best):
                best = set(R)
            return
        if P or X:
            u = max(P.union(X), key=lambda n: len(g[n]))
            candidates = P - g[u]
        else:
            candidates = set()
        for v in list(candidates):
            bron_kerbosch(R | {v}, P.intersection(g[v]), X.intersection(g[v]))
            P.remove(v)
            X.add(v)

    bron_kerbosch(set(), set(nodes), set())
    return ",".join(sorted(best))


def main():
    input_path = os.path.join(os.path.dirname(__file__), "day23.txt")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
    edges = parse_edges(content)
    g = build_graph(edges)
    total = count_triangles_with_t(g)
    password = maximum_clique_password(g)
    print("=" * 70)
    print("ADVENT OF CODE 2024 - DAY 23: LAN Party")
    print("=" * 70)
    print(f"Part 1 - Triangles with at least one 't*' computer: {total}")
    print(f"Part 2 - LAN party password: {password}")
    print("=" * 70)


if __name__ == "__main__":
    main()
