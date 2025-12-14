#!/usr/bin/env python3

def find_largest_rectangle(tiles):
    """
    Find the largest rectangle that can be formed using any two red tiles
    as opposite corners.
    """
    n = len(tiles)
    max_area = 0
    best_pair = None
    
    # Try all pairs of tiles as opposite corners
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            
            # Calculate rectangle area
            # The two tiles are opposite corners
            # The rectangle includes both corners, so we add 1 to each dimension
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
                best_pair = (tiles[i], tiles[j])
    
    return max_area, best_pair

def verify_with_example():
    """Verify with the example from the problem."""
    print("="*70)
    print("VERIFYING WITH EXAMPLE")
    print("="*70)
    
    example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    
    tiles = []
    for line in example.strip().split('\n'):
        x, y = map(int, line.split(','))
        tiles.append((x, y))
    
    print(f"\nNumber of red tiles: {len(tiles)}")
    print(f"Red tiles: {tiles}")
    
    max_area, best_pair = find_largest_rectangle(tiles)
    
    print(f"\n{'='*70}")
    print(f"Largest rectangle area: {max_area}")
    if best_pair:
        print(f"Between tiles: {best_pair[0]} and {best_pair[1]}")
        x1, y1 = best_pair[0]
        x2, y2 = best_pair[1]
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        print(f"Width: {width}, Height: {height}")
    print(f"Expected: 50")
    print(f"Match: {max_area == 50}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # Verify with example
    verify_with_example()
    
    # Read actual input
    with open('/mnt/user-data/uploads/input_09.txt', 'r') as f:
        tiles = []
        for line in f:
            x, y = map(int, line.strip().split(','))
            tiles.append((x, y))
    
    # Solve actual puzzle
    print("\n" + "="*70)
    print("SOLVING ACTUAL PUZZLE")
    print("="*70 + "\n")
    
    print(f"Number of red tiles: {len(tiles)}")
    
    # Show a few sample tiles
    print(f"First 5 tiles: {tiles[:5]}")
    print(f"Last 5 tiles: {tiles[-5:]}")
    
    max_area, best_pair = find_largest_rectangle(tiles)
    
    if best_pair:
        x1, y1 = best_pair[0]
        x2, y2 = best_pair[1]
        width = abs(x2 - x1) + 1
        height = abs(y2 - y1) + 1
        
        print(f"\n{'='*70}")
        print(f"Largest rectangle:")
        print(f"  Corner 1: ({x1}, {y1})")
        print(f"  Corner 2: ({x2}, {y2})")
        print(f"  Width: {width:,}")
        print(f"  Height: {height:,}")
        print(f"ANSWER: Area = {max_area:,}")
        print(f"{'='*70}")
