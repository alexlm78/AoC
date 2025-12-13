#!/usr/bin/env python3
import math
from collections import defaultdict

class UnionFind:
    """Union-Find (Disjoint Set Union) data structure for tracking circuits."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_components = n
    
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
        self.num_components -= 1
        return True
    
    def is_single_circuit(self):
        """Check if all elements are in a single circuit."""
        return self.num_components == 1

def distance(p1, p2):
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

def connect_until_single_circuit(positions):
    """
    Connect junction boxes until they all form a single circuit.
    Return the indices and coordinates of the last two boxes connected.
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
    
    # Make connections until single circuit
    connections_made = 0
    last_connection = None
    
    for dist, i, j in edges:
        if uf.union(i, j):
            connections_made += 1
            last_connection = (i, j, dist)
            
            if connections_made <= 10 or connections_made % 100 == 0:
                print(f"Connection {connections_made}: boxes {i} and {j} (distance: {dist:.2f}, circuits remaining: {uf.num_components})")
            
            if uf.is_single_circuit():
                print(f"\nSingle circuit achieved after {connections_made} connections!")
                break
    
    return last_connection, connections_made

def verify_with_example():
    """Verify with the example from the problem."""
    print("="*70)
    print("VERIFYING WITH EXAMPLE (PART 2)")
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
    
    last_connection, total_connections = connect_until_single_circuit(positions)
    
    if last_connection:
        i, j, dist = last_connection
        x1, y1, z1 = positions[i]
        x2, y2, z2 = positions[j]
        
        print(f"\n{'='*70}")
        print(f"Last connection:")
        print(f"  Box {i}: ({x1}, {y1}, {z1})")
        print(f"  Box {j}: ({x2}, {y2}, {z2})")
        print(f"  Distance: {dist:.2f}")
        print(f"  Product of X coordinates: {x1} × {x2} = {x1 * x2}")
        print(f"Expected: 216 × 117 = 25272")
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
    print("SOLVING ACTUAL PUZZLE (PART 2)")
    print("="*70 + "\n")
    
    print(f"Number of junction boxes: {len(positions)}")
    
    last_connection, total_connections = connect_until_single_circuit(positions)
    
    if last_connection:
        i, j, dist = last_connection
        x1, y1, z1 = positions[i]
        x2, y2, z2 = positions[j]
        
        result = x1 * x2
        
        print(f"\n{'='*70}")
        print(f"Total connections made: {total_connections}")
        print(f"Last connection:")
        print(f"  Box {i}: ({x1}, {y1}, {z2})")
        print(f"  Box {j}: ({x2}, {y2}, {z2})")
        print(f"  Distance: {dist:.2f}")
        print(f"ANSWER: Product of X coordinates = {x1} × {x2} = {result:,}")
        print(f"{'='*70}")
