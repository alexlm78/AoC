#!/usr/bin/env python3

def count_accessible_rolls(grid):
    """
    Count how many paper rolls (@) have fewer than 4 adjacent paper rolls.
    Adjacent means the 8 surrounding positions (including diagonals).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Directions for 8 adjacent cells (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
        (0, -1),           (0, 1),   # left, right
        (1, -1),  (1, 0),  (1, 1)    # bottom-left, bottom, bottom-right
    ]
    
    accessible_count = 0
    accessible_positions = []
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '@':
                # Count adjacent paper rolls
                adjacent_rolls = 0
                
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    # Check if within bounds
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni][nj] == '@':
                            adjacent_rolls += 1
                
                # Accessible if fewer than 4 adjacent rolls
                if adjacent_rolls < 4:
                    accessible_count += 1
                    accessible_positions.append((i, j, adjacent_rolls))
    
    return accessible_count, accessible_positions

def visualize_accessible(grid, accessible_positions):
    """
    Create a visualization showing which rolls are accessible (x).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Create a copy of the grid
    visual = [list(row) for row in grid]
    
    # Mark accessible positions with 'x'
    accessible_set = {(i, j) for i, j, _ in accessible_positions}
    for i in range(rows):
        for j in range(cols):
            if (i, j) in accessible_set:
                visual[i][j] = 'x'
    
    return [''.join(row) for row in visual]

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE")
    print("="*70)
    
    example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    
    grid = example.strip().split('\n')
    
    print("\nOriginal grid:")
    for row in grid:
        print(row)
    
    accessible_count, accessible_positions = count_accessible_rolls(grid)
    
    print(f"\nAccessible rolls: {accessible_count}")
    print(f"Expected: 13")
    print(f"Match: {accessible_count == 13}")
    
    print("\nVisualization (accessible rolls marked with 'x'):")
    visual = visualize_accessible(grid, accessible_positions)
    for row in visual:
        print(row)
    
    expected_visual = """..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x."""
    
    expected_lines = expected_visual.strip().split('\n')
    match = all(v == e for v, e in zip(visual, expected_lines))
    print(f"\nVisualization matches expected: {match}")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_04.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    total_rolls = sum(row.count('@') for row in grid)
    
    print(f"Grid size: {rows} rows × {cols} columns")
    print(f"Total paper rolls: {total_rolls}")
    
    accessible_count, accessible_positions = count_accessible_rolls(grid)
    
    print(f"\n{'='*70}")
    print(f"ANSWER: {accessible_count} rolls can be accessed by forklifts")
    print(f"{'='*70}")
    
    # Show some statistics
    adjacent_counts = {}
    for _, _, adj_count in accessible_positions:
        adjacent_counts[adj_count] = adjacent_counts.get(adj_count, 0) + 1
    
    print(f"\nBreakdown by adjacent roll count:")
    for count in sorted(adjacent_counts.keys()):
        print(f"  {count} adjacent rolls: {adjacent_counts[count]} accessible rolls")
    
    # Show a few example accessible positions
    print(f"\nFirst 10 accessible roll positions (row, col, adjacent_count):")
    for i, (row, col, adj) in enumerate(accessible_positions[:10], 1):
        print(f"  {i}. Position ({row}, {col}): {adj} adjacent rolls")
