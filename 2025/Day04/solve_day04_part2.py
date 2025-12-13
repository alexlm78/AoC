#!/usr/bin/env python3

def count_adjacent_rolls(grid, i, j):
    """
    Count how many of the 8 adjacent positions contain paper rolls.
    """
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    adjacent_count = 0
    
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            if grid[ni][nj] == '@':
                adjacent_count += 1
    
    return adjacent_count

def find_accessible_rolls(grid):
    """
    Find all rolls that are currently accessible (< 4 adjacent rolls).
    """
    accessible = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '@':
                adjacent = count_adjacent_rolls(grid, i, j)
                if adjacent < 4:
                    accessible.append((i, j))
    
    return accessible

def remove_rolls_iteratively(grid):
    """
    Iteratively remove accessible rolls until no more can be removed.
    Returns the total number of rolls removed.
    """
    # Convert grid to mutable list of lists
    grid = [list(row) for row in grid]
    
    total_removed = 0
    iteration = 0
    
    while True:
        # Find all accessible rolls
        accessible = find_accessible_rolls(grid)
        
        if not accessible:
            # No more accessible rolls
            break
        
        iteration += 1
        num_removed = len(accessible)
        total_removed += num_removed
        
        print(f"Iteration {iteration}: Removing {num_removed} rolls")
        
        # Remove all accessible rolls
        for i, j in accessible:
            grid[i][j] = '.'
    
    return total_removed

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE (PART 2)")
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
    
    print("\nInitial grid:")
    for row in grid:
        print(row)
    
    # Count initial rolls
    initial_count = sum(row.count('@') for row in grid)
    print(f"\nInitial paper rolls: {initial_count}")
    
    total_removed = remove_rolls_iteratively(grid)
    
    print(f"\n{'='*70}")
    print(f"Total rolls removed: {total_removed}")
    print(f"Expected: 43")
    print(f"Match: {total_removed == 43}")
    print("="*70 + "\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_04.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE (PART 2)")
    print("="*70 + "\n")
    
    initial_count = sum(row.count('@') for row in grid)
    print(f"Initial paper rolls: {initial_count}")
    
    total_removed = remove_rolls_iteratively(grid)
    
    print(f"\n{'='*70}")
    print(f"ANSWER: {total_removed} rolls can be removed in total")
    print(f"Percentage of initial rolls: {100 * total_removed / initial_count:.1f}%")
    print(f"{'='*70}")
