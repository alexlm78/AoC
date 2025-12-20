# Union-Find (Disjoint Set Union) structure
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.num_sets = n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            if self.rank[root_i] == self.rank[root_j]:
                self.rank[root_i] += 1
            self.num_sets -= 1
            return True
        return False


def manhattan_dist(p1, p2):
    return sum(abs(a - b) for a, b in zip(p1, p2))


def solve():
    points = []
    with open("input.txt", "r") as f:
        for line in f:
            if line.strip():
                points.append(tuple(map(int, line.strip().split(","))))

    n = len(points)
    dsu = DSU(n)

    # Brute force O(N^2) comparison since N is small (lines are ~1300 but N points probably similar or less)
    # 1300 points is fine for O(N^2) ~ 1.6M operations.

    for i in range(n):
        for j in range(i + 1, n):
            if manhattan_dist(points[i], points[j]) <= 3:
                dsu.union(i, j)

    print(f"Part 1 Result: {dsu.num_sets}")


if __name__ == "__main__":
    solve()
