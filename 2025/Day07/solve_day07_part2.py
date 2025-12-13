#!/usr/bin/env python3

def count_quantum_timelines(grid):
    """
    Count the number of different timelines a quantum tachyon particle
    ends up on after taking all possible paths through the manifold.
    
    At each splitter, the particle takes BOTH left and right paths,
    creating parallel timelines.
    
    The key insight: we need to count the number of distinct exit points
    (or more precisely, distinct paths through the manifold).
    """
    # Find the starting position 'S'
    start_row, start_col = None, None
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == 'S':
                start_row, start_col = i, j
                break
        if start_row is not None:
            break
    
    if start_row is None:
        return 0
    
    # Use dynamic programming / memoization
    # For each position, count how many ways we can reach the bottom
    memo = {}
    
    def count_paths(row, col):
        """
        Count how many distinct paths exist from this position
        to the bottom of the manifold (or end of path).
        """
        # Check if we've already calculated this
        if (row, col) in memo:
            return memo[(row, col)]
        
        # Base case: if we're at or past the bottom, this is one path
        if row >= len(grid) - 1:
            return 1
        
        # Move down to next row
        next_row = row + 1
        
        # Check what's at the next position
        if grid[next_row][col] == '^':
            # Hit a splitter! Particle takes BOTH paths
            total_paths = 0
            
            # Left path
            left_col = col - 1
            if 0 <= left_col < len(grid[0]):
                total_paths += count_paths(next_row, left_col)
            
            # Right path
            right_col = col + 1
            if 0 <= right_col < len(grid[0]):
                total_paths += count_paths(next_row, right_col)
            
            # If both paths go out of bounds, this path ends
            if total_paths == 0:
                total_paths = 1
        else:
            # Empty space - continue straight down
            total_paths = count_paths(next_row, col)
        
        memo[(row, col)] = total_paths
        return total_paths
    
    return count_paths(start_row, start_col)

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE (PART 2 - QUANTUM)")
    print("="*70)
    
    example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    
    grid = [line for line in example.strip().split('\n')]
    
    print(f"\nGrid size: {len(grid)} rows x {len(grid[0])} columns")
    
    # Count splitters
    splitter_count = sum(row.count('^') for row in grid)
    print(f"Total splitters: {splitter_count}")
    
    timeline_count = count_quantum_timelines(grid)
    
    print(f"\n{'='*70}")
    print(f"Number of timelines: {timeline_count}")
    print(f"Expected: 40")
    print(f"Match: {timeline_count == 40}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_07.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE (PART 2 - QUANTUM)")
    print("="*70 + "\n")
    
    print(f"Grid size: {len(grid)} rows x {len(grid[0])} columns")
    
    # Count splitters
    splitter_count = sum(row.count('^') for row in grid)
    print(f"Total splitters in grid: {splitter_count}")
    
    timeline_count = count_quantum_timelines(grid)
    
    print(f"\n{'='*70}")
    print(f"ANSWER: Number of timelines = {timeline_count:,}")
    print(f"{'='*70}")
