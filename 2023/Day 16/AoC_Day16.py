from collections import deque

def get_grid(text):
    
    grid = [list(row) for row in text]
    
    return grid

def update_direction(elem, direction):
    
        if elem == ".":

            new_direction = [direction]

        elif elem == "/":

            # left --> right: up 
            if direction == (0,1):
                new_direction = [(-1,0)] 
            # right --> left: down 
            elif direction == (0,-1):
                new_direction = [(1,0)] 
            # up --> down: left 
            elif direction == (1,0):
                new_direction = [(0,-1)]
            # down --> up: right
            else:
                new_direction = [(0,1)]          

        elif elem == "\\":
            
            # left --> right: down 
            if direction == (0,1):
                new_direction = [(1,0)]
            # right --> left: up 
            elif direction == (0,-1):
                new_direction = [(-1,0)] 
            # up --> down: right     
            elif direction == (1,0):
                new_direction = [(0,1)]
            # down --> up: left
            else:
                new_direction = [(0,-1)]


        elif elem == "|":

            if direction[0] in [-1,1]:
                new_direction = [direction]
            else:
                new_direction = [(-1,0), (1,0)]

        elif elem == "-":

            if direction[1] in [-1,1]:
                new_direction = [direction]
            else:
                new_direction = [(0, -1),(0, 1)]
    
        return new_direction

def follow_path(grid, position, direction):

    n_rows = len(grid)
    n_cols = len(grid[0])

    q = deque([(position, direction)])
    tiles = set()
    visited = set()
    
    while q:
        
        position, direction = q.popleft()
        visited.add((position, direction))
        
        new_position = (position[0] + direction[0], position[1] + direction[1])

        if not (0 <= new_position[0] < n_rows and 0 <= new_position[1] < n_cols):
            continue
    
        tiles.add(new_position)
        elem = grid[new_position[0]][new_position[1]]

        new_directions = update_direction(elem, direction)
        
        for new_direction in new_directions:
            if (new_position, new_direction) not in visited:
                q.append((new_position, new_direction))
    return tiles

def get_start_positions(grid):
    
    n_rows = len(grid)
    n_cols = len(grid[0])


    start_positions = []

    for row in range(n_rows):

        start_positions.append([(row,-1),(0,1)])
        start_positions.append([(row,n_cols),(0,-1)])

    for col in range(n_cols):

        start_positions.append([(-1, col),(1,0)])
        start_positions.append([(n_rows,col),(-1,0)])

    return start_positions

def get_path_lengths(grid):
    
    results = []
    start_positions = get_start_positions(grid)
    

    for start, direction in start_positions:

        result = follow_path(grid, start, direction)
        results.append(len(result))

    return results

text = open("input.txt", "r").readlines()
text = [i.split("\n")[0] for i in text]

grid = get_grid(text)

start = (0, -1)
direction = (0, 1)
result = follow_path(grid, start, direction)
print("Part 1: ", len(result))

# Part2
grid = get_grid(text)
results = get_path_lengths(grid)
print("Part 2: ", max(results))
