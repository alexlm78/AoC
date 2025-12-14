"""Custom module with utilities. Consists of functions to handle frequently needed subtasks when dealing with AOC"""

# General purpose
def import_rows(sep: str = "\n") -> list[str]:
    """
    Loads the puzzle input in line-by-line list format from ./input.in file.

    :param sep: Separator to use when splitting the data. Default is \\n
    :type sep: str
    :return: List of strings where each element is exactly one line of the source file
    :rtype: list[str]
    """

    with open("AoC_Day09.input.txt", "r") as input_data:
        return input_data.read().split(sep)

def print_results(first: str | int | None, second: str | int | None) -> None:
    """
    Prints puzzle answers to the console.

    :param first: The final answer to the first part of the puzzle
    :type first: str | int | None
    :param second: The final answer to the second part of the puzzle
    :type second: str | int | None
    :rtype: None
    """

    print("#"*25)
    print("Part 1 answer:", first if first is not None else "N/A")
    print("Part 2 answer:", second if second is not None else "N/A")
    print("#"*25)

# Specific purpose
def get_neighbours(x: int, y: int, field: list, corners: bool = False, as_tuple: bool = False) -> list[tuple[int, int]] | tuple[tuple[int, int]]:
    """
        Returns positions of neighbouring elements of given coordinates in a 2D list

        :param x: Starting x-coordinate
        :type x: int
        :param y: Starting y-coordinate
        :type y: int
        :param field: A list to operate within
        :type field: list
        :param corners: Whether elements sharing just a corner should be treated as neighbours. False by default
        :type corners: bool
        :param as_tuple: Whether the return value should be a tuple instead of a list. False by default
        :type as_tuple: bool
        :return: A list or a tuple of neighbours' positions
        :rtype: list[tuple[int, int]] | tuple[tuple[int, int]]
    """

    possibilities = [[(x, y-1), (x-1, y), (x+1, y), (x, y+1)], [(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]]
    neighbours = []
    for i, j in enumerate(possibilities):
        if i == 0 or (i == 1 and corners):
            for k in j:
                if k[1] >= 0 and k[1] < len(field) and k[0] >= 0 and k[0] < len(field[k[1]]): neighbours.append(k)
    return tuple(neighbours) if as_tuple else neighbours

# Init
data = [[int(j) for j in i.split(" ")] for i in import_rows()]

# Part 1 & Part 2
part_1, part_2 = 0, 0
for k in range(0, 2):
    for row in data:
        if k == 1: row.reverse()
        extrapolated = 0
        diffs = [row]
        diff_source = row
        while True:
            diff = []
            for i in range(0, len(diff_source)-1): diff.append(diff_source[i+1]-diff_source[i])
            if set(diff) == {0}: break
            diff_source = diff
            diffs.append(diff)
        for i in diffs: extrapolated += i[-1]
        if k == 0: part_1 += extrapolated
        else: part_2 += extrapolated

# Results
print_results(part_1, part_2)