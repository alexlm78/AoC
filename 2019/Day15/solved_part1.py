import sys
from collections import defaultdict, deque

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

with open("input.txt", "r") as file:
    data = list(map(int, file.read().strip().split(",")))


class IntcodeComputer:
    def __init__(self, program):
        self.memory = defaultdict(int, {k: v for k, v in enumerate(program)})
        self.ip = 0
        self.relbase = 0
        self.halted = False

    def get_param(self, offset, mode):
        """Get parameter value based on mode"""
        if mode == 0:  # position mode
            return self.memory[self.memory[self.ip + offset]]
        elif mode == 1:  # immediate mode
            return self.memory[self.ip + offset]
        elif mode == 2:  # relative mode
            return self.memory[self.memory[self.ip + offset] + self.relbase]

    def get_address(self, offset, mode):
        """Get address for writing based on mode"""
        if mode == 0:  # position mode
            return self.memory[self.ip + offset]
        elif mode == 2:  # relative mode
            return self.memory[self.ip + offset] + self.relbase
        else:
            raise ValueError(f"Invalid mode {mode} for address")

    def run(self, input_value):
        """Run until output or halt"""
        while not self.halted:
            opcode = self.memory[self.ip] % 100
            mode1 = (self.memory[self.ip] // 100) % 10
            mode2 = (self.memory[self.ip] // 1000) % 10
            mode3 = (self.memory[self.ip] // 10000) % 10

            if opcode == 99:
                self.halted = True
                return None
            elif opcode == 1:  # add
                a = self.get_param(1, mode1)
                b = self.get_param(2, mode2)
                addr = self.get_address(3, mode3)
                self.memory[addr] = a + b
                self.ip += 4
            elif opcode == 2:  # multiply
                a = self.get_param(1, mode1)
                b = self.get_param(2, mode2)
                addr = self.get_address(3, mode3)
                self.memory[addr] = a * b
                self.ip += 4
            elif opcode == 3:  # input
                addr = self.get_address(1, mode1)
                self.memory[addr] = input_value
                self.ip += 2
            elif opcode == 4:  # output
                output = self.get_param(1, mode1)
                self.ip += 2
                return output
            elif opcode == 5:  # jump-if-true
                a = self.get_param(1, mode1)
                b = self.get_param(2, mode2)
                if a != 0:
                    self.ip = b
                else:
                    self.ip += 3
            elif opcode == 6:  # jump-if-false
                a = self.get_param(1, mode1)
                b = self.get_param(2, mode2)
                if a == 0:
                    self.ip = b
                else:
                    self.ip += 3
            elif opcode == 7:  # less than
                a = self.get_param(1, mode1)
                b = self.get_param(2, mode2)
                addr = self.get_address(3, mode3)
                self.memory[addr] = 1 if a < b else 0
                self.ip += 4
            elif opcode == 8:  # equals
                a = self.get_param(1, mode1)
                b = self.get_param(2, mode2)
                addr = self.get_address(3, mode3)
                self.memory[addr] = 1 if a == b else 0
                self.ip += 4
            elif opcode == 9:  # adjust relative base
                a = self.get_param(1, mode1)
                self.relbase += a
                self.ip += 2
            else:
                raise ValueError(f"Unknown opcode {opcode}")

        return None


# Movement commands
NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4

# Status codes
WALL, MOVED, OXYGEN = 0, 1, 2

# Direction vectors
DIRECTIONS = {NORTH: (0, -1), SOUTH: (0, 1), WEST: (-1, 0), EAST: (1, 0)}

# Opposite directions for backtracking
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}


def explore_maze(program_data):
    """Explore the entire maze using DFS and build a map"""
    computer = IntcodeComputer(program_data)

    maze = {}  # (x, y) -> status (WALL, MOVED, OXYGEN)
    position = (0, 0)
    maze[position] = MOVED

    def dfs(pos):
        """Depth-first search to explore all reachable positions"""
        for direction, (dx, dy) in DIRECTIONS.items():
            new_pos = (pos[0] + dx, pos[1] + dy)

            # Skip if already explored
            if new_pos in maze:
                continue

            # Try to move in this direction
            status = computer.run(direction)

            if status == WALL:
                maze[new_pos] = WALL
            elif status in (MOVED, OXYGEN):
                maze[new_pos] = status
                # Recursively explore from new position
                dfs(new_pos)
                # Backtrack
                computer.run(OPPOSITE[direction])

    dfs(position)
    return maze


def find_shortest_path(maze):
    """Use BFS to find shortest path from (0,0) to oxygen system"""
    start = (0, 0)

    # Find oxygen position
    oxygen_pos = None
    for pos, status in maze.items():
        if status == OXYGEN:
            oxygen_pos = pos
            break

    if oxygen_pos is None:
        return None

    # BFS
    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        pos, dist = queue.popleft()

        if pos == oxygen_pos:
            return dist

        for dx, dy in DIRECTIONS.values():
            new_pos = (pos[0] + dx, pos[1] + dy)

            if new_pos not in visited and maze.get(new_pos) in (MOVED, OXYGEN):
                visited.add(new_pos)
                queue.append((new_pos, dist + 1))

    return None


def visualize_maze(maze):
    """Print the maze for debugging"""
    if not maze:
        return

    min_x = min(pos[0] for pos in maze)
    max_x = max(pos[0] for pos in maze)
    min_y = min(pos[1] for pos in maze)
    max_y = max(pos[1] for pos in maze)

    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            if pos == (0, 0):
                line += "S"
            elif pos not in maze:
                line += " "
            elif maze[pos] == WALL:
                line += "#"
            elif maze[pos] == OXYGEN:
                line += "O"
            else:
                line += "."
        print(line)


# Solve the puzzle
print("Exploring maze...")
maze = explore_maze(data)
print(f"Explored {len(maze)} positions")

print("\nMaze visualization:")
visualize_maze(maze)

distance = find_shortest_path(maze)
print(f"\nShortest path to oxygen system: {distance} steps")
