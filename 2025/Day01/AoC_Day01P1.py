#!/usr/bin/env python3

def solve_safe_puzzle(filename):
    """
    Solve the safe dial puzzle by simulating rotations and counting
    how many times the dial points at 0.
    """
    # Read the input file
    with open(filename, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]
    
    # Start at position 50
    position = 50
    zero_count = 0
    
    print(f"Starting position: {position}")
    
    # Process each rotation
    for i, rotation in enumerate(rotations, 1):
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # The number after L or R
        
        if direction == 'L':
            # Left rotation (toward lower numbers)
            position = (position - distance) % 100
        else:  # direction == 'R'
            # Right rotation (toward higher numbers)
            position = (position + distance) % 100
        
        # Check if we're at 0
        if position == 0:
            zero_count += 1
            print(f"Rotation {i}: {rotation} -> Position {position} (ZERO #{zero_count})")
        
        # Print first few and last few for debugging
        if i <= 10 or i > len(rotations) - 5:
            print(f"Rotation {i}: {rotation} -> Position {position}")
    
    return zero_count

if __name__ == "__main__":
    result = solve_safe_puzzle('/mnt/user-data/uploads/input_day01.txt')
    print(f"\n{'='*50}")
    print(f"ANSWER: The dial points at 0 a total of {result} times")
    print(f"{'='*50}")
