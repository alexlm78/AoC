def parse_input(input_data):
    antennas = {}
    lines = input_data.strip().split('\n')
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '.':
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((x, y))
    return antennas, len(lines[0]), len(lines)


def calculate_antinode_positions(antennas, width, height):
    antinodes = set()
    for freq, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                # Check horizontal line
                if y1 == y2:
                    d = abs(x2 - x1)
                    if d % 3 == 0:
                        antinode_x1 = x1 + d // 3
                        antinode_x2 = x1 - d // 3
                        if 0 <= antinode_x1 < width:
                            antinodes.add((antinode_x1, y1))
                        if 0 <= antinode_x2 < width:
                            antinodes.add((antinode_x2, y1))
                # Check vertical line
                if x1 == x2:
                    d = abs(y2 - y1)
                    if d % 3 == 0:
                        antinode_y1 = y1 + d // 3
                        antinode_y2 = y1 - d // 3
                        if 0 <= antinode_y1 < height:
                            antinodes.add((x1, antinode_y1))
                        if 0 <= antinode_y2 < height:
                            antinodes.add((x1, antinode_y2))
                # Check diagonal lines
                if abs(x2 - x1) == abs(y2 - y1):
                    d = abs(x2 - x1)
                    if d % 3 == 0:
                        antinode_x1 = x1 + d // 3
                        antinode_x2 = x1 - d // 3
                        antinode_y1 = y1 + d // 3
                        antinode_y2 = y1 - d // 3
                        if 0 <= antinode_x1 < width and 0 <= antinode_y1 < height:
                            antinodes.add((antinode_x1, antinode_y1))
                        if 0 <= antinode_x2 < width and 0 <= antinode_y2 < height:
                            antinodes.add((antinode_x2, antinode_y2))
    return antinodes


def count_unique_antinode_locations(input_data):
    antennas, width, height = parse_input(input_data)
    antinodes = calculate_antinode_positions(antennas, width, height)
    return len(antinodes)


input_data = open("day08.txt", "r", encoding="utf-8").read()
# Example input
# input_data = """
# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............
# """

# Calculate the unique antinode locations
res = count_unique_antinode_locations(input_data)
print(f"Number of unique antinode locations: {res}")
