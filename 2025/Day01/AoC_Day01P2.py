#!/usr/bin/env python3

def count_zeros_during_rotation(start_pos, direction, distance):
    """
    Count how many times the dial points at 0 during a rotation.
    This includes the final position if it's 0.
    """
    count = 0
    
    if direction == 'L':
        # Moving left (toward lower numbers)
        # We need to count how many times we cross/land on 0
        for i in range(1, distance + 1):
            pos = (start_pos - i) % 100
            if pos == 0:
                count += 1
    else:  # direction == 'R'
        # Moving right (toward higher numbers)
        # We need to count how many times we cross/land on 0
        for i in range(1, distance + 1):
            pos = (start_pos + i) % 100
            if pos == 0:
                count += 1
    
    return count

def count_zeros_optimized(start_pos, direction, distance):
    """
    Optimized version that calculates zeros mathematically instead of iterating.
    """
    if distance == 0:
        return 0
    
    if direction == 'L':
        # Moving left from start_pos
        # We hit 0 when (start_pos - i) % 100 == 0
        # This means start_pos - i is divisible by 100
        # So i = start_pos, start_pos + 100, start_pos + 200, ...
        
        # First zero is at click number start_pos (if start_pos <= distance)
        # Then every 100 clicks after that
        
        if start_pos == 0:
            # We're already at 0, first hit is at click 100
            first_zero = 100
        else:
            first_zero = start_pos
        
        if distance < first_zero:
            return 0
        
        # Count: first zero + how many more 100-click intervals fit
        return 1 + (distance - first_zero) // 100
    
    else:  # direction == 'R'
        # Moving right from start_pos
        # We hit 0 when (start_pos + i) % 100 == 0
        # This means start_pos + i is divisible by 100
        # So i = (100 - start_pos), (100 - start_pos) + 100, ...
        
        if start_pos == 0:
            # We're already at 0, first hit is at click 100
            first_zero = 100
        else:
            first_zero = 100 - start_pos
        
        if distance < first_zero:
            return 0
        
        # Count: first zero + how many more 100-click intervals fit
        return 1 + (distance - first_zero) // 100

def solve_safe_puzzle_part2(filename):
    """
    Solve part 2: count all times the dial points at 0 during any rotation.
    """
    # Read the input file
    with open(filename, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]
    
    # Start at position 50
    position = 50
    total_zeros = 0
    
    print(f"Starting position: {position}")
    print(f"Total rotations to process: {len(rotations)}\n")
    
    # Process each rotation
    for i, rotation in enumerate(rotations, 1):
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # The number after L or R
        
        # Count zeros during this rotation
        zeros_in_rotation = count_zeros_optimized(position, direction, distance)
        total_zeros += zeros_in_rotation
        
        # Update position
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        
        # Print some examples for verification
        if zeros_in_rotation > 0 and i <= 20:
            print(f"Rotation {i}: {rotation} -> {zeros_in_rotation} zero(s), ends at {position}")
        elif i <= 10:
            print(f"Rotation {i}: {rotation} -> {zeros_in_rotation} zero(s), ends at {position}")
    
    return total_zeros

def verify_with_example():
    """
    Verify with the example from the problem.
    """
    print("="*60)
    print("VERIFYING WITH EXAMPLE")
    print("="*60)
    
    example = [
        "L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"
    ]
    
    position = 50
    total_zeros = 0
    
    for i, rotation in enumerate(example, 1):
        direction = rotation[0]
        distance = int(rotation[1:])
        
        zeros = count_zeros_optimized(position, direction, distance)
        total_zeros += zeros
        
        if direction == 'L':
            new_pos = (position - distance) % 100
        else:
            new_pos = (position + distance) % 100
        
        print(f"{i}. {rotation}: pos {position} -> {new_pos}, zeros during rotation: {zeros}")
        position = new_pos
    
    print(f"\nTotal zeros in example: {total_zeros}")
    print(f"Expected: 6")
    print(f"Match: {total_zeros == 6}")
    print("="*60 + "\n")

if __name__ == "__main__":
    # First verify with the example
    verify_with_example()
    
    # Then solve the actual puzzle
    result = solve_safe_puzzle_part2('/mnt/user-data/uploads/input_day01.txt')
    print(f"\n{'='*60}")
    print(f"ANSWER (Part 2): The dial points at 0 a total of {result} times")
    print(f"{'='*60}")
