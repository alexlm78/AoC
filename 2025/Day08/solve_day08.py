#!/usr/bin/env python3
import math
from collections import defaultdict

class UnionFind:
    """Union-Find (Disjoint Set Union) data structure for tracking circuits."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        """Find the root of the set containing x (with path compression)."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union the sets containing x and y. Returns True if they were in different sets."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same circuit
        
        # Union by size - attach smaller tree to larger
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True
    
    def get_circuit_sizes(self):
        """Get the size of each circuit."""
        circuit_sizes = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            circuit_sizes[root] = self.size[root]
        return list(circuit_sizes.values())

def distance(p1, p2):
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def solve_junction_boxes(positions, num_connections):
    """
    Connect junction boxes starting with closest pairs.
    Return the product of the three largest circuit sizes after making connections.
    """
    n = len(positions)
    
    # Calculate all pairwise distances
    print(f"Calculating distances between {n} junction boxes...")
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(positions[i], positions[j])
            edges.append((dist, i, j))
    
    # Sort edges by distance
    print(f"Sorting {len(edges)} edges...")
    edges.sort()
    
    # Use union-find to track circuits
    uf = UnionFind(n)
    
    # Make connections - process the requested number of PAIRS (attempts)
    attempts = 0
    connections_made = 0
    for dist, i, j in edges:
        if attempts >= num_connections:
            break
        
        attempts += 1
        if uf.union(i, j):
            connections_made += 1
            if connections_made <= 10 or attempts % 100 == 0:
                print(f"Attempt {attempts}: Connected boxes {i} and {j} (distance: {dist:.2f})")
        else:
            if attempts <= 15:
                print(f"Attempt {attempts}: Boxes {i} and {j} already in same circuit (distance: {dist:.2f})")
    
    print(f"\nTotal pair attempts: {attempts}")
    print(f"Successful connections: {connections_made}")
    print(f"Redundant attempts: {attempts - connections_made}")
    
    # Get circuit sizes
    circuit_sizes = uf.get_circuit_sizes()
    circuit_sizes.sort(reverse=True)
    
    # Get three largest
    top_three = circuit_sizes[:3]
    
    return top_three, circuit_sizes

def verify_with_example():
    """Verify with the example from the problem."""
    print("="*70)
    print("VERIFYING WITH EXAMPLE")
    print("="*70)
    
    example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    
    positions = []
    for line in example.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        positions.append((x, y, z))
    
    print(f"\nNumber of junction boxes: {len(positions)}")
    
    # After 10 connections
    top_three, all_sizes = solve_junction_boxes(positions, 10)
    
    print(f"\n{'='*70}")
    print(f"After 10 connections:")
    print(f"Circuit sizes: {sorted(all_sizes, reverse=True)}")
    print(f"Top three: {top_three}")
    print(f"Product: {top_three[0] * top_three[1] * top_three[2]}")
    print(f"Expected: 40")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # Verify with example
    verify_with_example()
    
    # Read actual input
    with open('/mnt/user-data/uploads/input_08.txt', 'r') as f:
        positions = []
        for line in f:
            x, y, z = map(int, line.strip().split(','))
            positions.append((x, y, z))
    
    # Solve actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    print(f"Number of junction boxes: {len(positions)}")
    
    # Make 1000 connections
    top_three, all_sizes = solve_junction_boxes(positions, 1000)
    
    result = top_three[0] * top_three[1] * top_three[2] if len(top_three) >= 3 else 0
    
    print(f"\n{'='*70}")
    print(f"After 1000 connections:")
    print(f"Number of circuits: {len(all_sizes)}")
    print(f"All circuit sizes (top 10): {all_sizes[:10]}")
    if len(top_three) >= 3:
        print(f"Top three circuit sizes: {top_three}")
        print(f"ANSWER: Product = {result:,}")
    else:
        print(f"Only {len(top_three)} circuits exist!")
        print(f"Circuit sizes: {all_sizes}")
    print(f"{'='*70}")
