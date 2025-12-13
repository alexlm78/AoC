#!/usr/bin/env python3

def simulate_tachyon_beam(grid):
    """
    Simulate a tachyon beam starting from 'S' and moving downward.
    When it hits a splitter ('^'), it stops and creates two new beams
    going left and right from that position.
    Count total number of UNIQUE splitters that get activated.
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
    
    # Track active beams: (row, col)
    # All beams move downward
    beams = [(start_row, start_col)]
    
    # Track which beams have been processed to avoid infinite loops
    processed = set()
    
    # Track which splitters have been activated
    activated_splitters = set()
    
    while beams:
        row, col = beams.pop(0)
        
        # Skip if we've already processed this beam
        state = (row, col)
        if state in processed:
            continue
        processed.add(state)
        
        # Move the beam downward until it hits something or exits
        while True:
            # Move down
            next_row = row + 1
            next_col = col
            
            # Check if beam exits the manifold
            if next_row >= len(grid):
                break  # Exits bottom
            
            row, col = next_row, next_col
            
            # Check what's at this position
            cell = grid[row][col]
            
            if cell == '^':
                # Hit a splitter! Record it and create two new beams
                activated_splitters.add((row, col))
                
                # Create left beam (starts one position to the left of the splitter)
                left_col = col - 1
                if 0 <= left_col < len(grid[0]):
                    left_state = (row, left_col)
                    if left_state not in processed:
                        beams.append(left_state)
                
                # Create right beam (starts one position to the right of the splitter)
                right_col = col + 1
                if 0 <= right_col < len(grid[0]):
                    right_state = (row, right_col)
                    if right_state not in processed:
                        beams.append(right_state)
                
                break  # This beam stops
            
            # Otherwise, beam continues (empty space '.' or 'S')
    
    return len(activated_splitters)

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*70)
    print("VERIFYING WITH EXAMPLE")
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
    
    split_count = simulate_tachyon_beam(grid)
    
    print(f"\n{'='*70}")
    print(f"Beam split count: {split_count}")
    print(f"Expected: 21")
    print(f"Match: {split_count == 21}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Read the actual input
    with open('/mnt/user-data/uploads/input_07.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    
    # Solve the actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    print(f"Grid size: {len(grid)} rows x {len(grid[0])} columns")
    
    # Count splitters
    splitter_count = sum(row.count('^') for row in grid)
    print(f"Total splitters in grid: {splitter_count}")
    
    split_count = simulate_tachyon_beam(grid)
    
    print(f"\n{'='*70}")
    print(f"ANSWER: Beam split count = {split_count}")
    print(f"{'='*70}")
