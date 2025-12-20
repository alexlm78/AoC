import sys

# Increase recursion depth just in case the tree is deep
sys.setrecursionlimit(10000)


def parse_input(data):
    return list(map(int, data.strip().split()))


def parse_node(data, index):
    # Header: quantity of child nodes, quantity of metadata entries
    num_children = data[index]
    num_metadata = data[index + 1]
    index += 2

    children = []
    for _ in range(num_children):
        child_node, new_index = parse_node(data, index)
        children.append(child_node)
        index = new_index

    metadata = []
    for _ in range(num_metadata):
        metadata.append(data[index])
        index += 1

    return {"children": children, "metadata": metadata}, index


def sum_metadata(node):
    total = sum(node["metadata"])
    for child in node["children"]:
        total += sum_metadata(child)
    return total


def get_node_value(node):
    if not node["children"]:
        return sum(node["metadata"])

    value = 0
    for index in node["metadata"]:
        # Indices are 1-based
        if 1 <= index <= len(node["children"]):
            value += get_node_value(node["children"][index - 1])
    return value


def solve():
    try:
        with open("input.txt", "r") as f:
            content = f.read()

        data = parse_input(content)
        root, _ = parse_node(data, 0)

        # Part 1
        result_p1 = sum_metadata(root)
        print(f"Metadata sum: {result_p1}")

        # Part 2
        result_p2 = get_node_value(root)
        print(f"Root node value: {result_p2}")

    except FileNotFoundError:
        print("Error: input.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    solve()
