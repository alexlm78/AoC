import re

def parse_input(file_path):
    points = []
    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>', line)
            if match:
                points.append({
                    'x': int(match.group(1)),
                    'y': int(match.group(2)),
                    'vx': int(match.group(3)),
                    'vy': int(match.group(4))
                })
    return points

def get_bounds(points):
    min_x = min(p['x'] for p in points)
    max_x = max(p['x'] for p in points)
    min_y = min(p['y'] for p in points)
    max_y = max(p['y'] for p in points)
    return min_x, max_x, min_y, max_y

def update_points(points):
    for p in points:
        p['x'] += p['vx']
        p['y'] += p['vy']

def solve():
    points = parse_input('input.txt')
    seconds = 0
    min_area = float('inf')
    
    # We expect the message to appear when the points are closest together.
    # We can track the bounding box area. When it starts increasing, the previous step was the minimum.
    
    while True:
        min_x, max_x, min_y, max_y = get_bounds(points)
        width = max_x - min_x
        height = max_y - min_y
        area = width * height
        
        if area < min_area:
            min_area = area
            # Save state in case this is the minimum
            best_points = [{'x': p['x'], 'y': p['y']} for p in points]
            best_seconds = seconds
        else:
            # Area started increasing, so the previous state was the message
            print(f"Message appeared at {best_seconds} seconds.")
            
            # Print the message
            min_x, max_x, min_y, max_y = get_bounds(best_points)
            grid = [[' ' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
            
            for p in best_points:
                grid[p['y'] - min_y][p['x'] - min_x] = '#'
                
            for row in grid:
                print("".join(row))
            
            break
            
        update_points(points)
        seconds += 1

if __name__ == "__main__":
    solve()
