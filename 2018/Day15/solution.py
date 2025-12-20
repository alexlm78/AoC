import sys
from collections import deque


class Unit:
    def __init__(self, x, y, team, attack_power=3):
        self.x = x
        self.y = y
        self.team = team  # 'G' or 'E'
        self.hp = 200
        self.ap = attack_power
        self.id = f"{team}_{y}_{x}"  # Unique ID mainly for debugging

    def __repr__(self):
        return f"{self.team}({self.hp})@{self.x},{self.y}"


class Game:
    def __init__(self, input_file, elf_attack_power=3):
        self.grid = []
        self.units = []
        self.width = 0
        self.height = 0
        self.rounds = 0
        self.elf_attack_power = elf_attack_power
        self.parse_input(input_file)

    def parse_input(self, input_file):
        with open(input_file, "r") as f:
            lines = f.read().splitlines()

        self.height = len(lines)
        self.width = len(lines[0])
        self.grid = [["" for _ in range(self.width)] for _ in range(self.height)]

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char in ["G", "E"]:
                    ap = self.elf_attack_power if char == "E" else 3
                    self.units.append(Unit(x, y, char, ap))
                    self.grid[y][x] = "."  # The unit stands on open ground
                else:
                    self.grid[y][x] = char

    def get_unit_at(self, x, y):
        for u in self.units:
            if u.x == x and u.y == y and u.hp > 0:
                return u
        return None

    def is_occupied(self, x, y):
        if self.grid[y][x] == "#":
            return True
        if self.get_unit_at(x, y):
            return True
        return False

    def get_neighbors(self, x, y):
        # Reading order for neighbors: Up, Left, Right, Down
        # Note: (y, x) -> (y-1, x), (y, x-1), (y, x+1), (y+1, x)
        candidates = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        valid = []
        for cx, cy in candidates:
            if 0 <= cx < self.width and 0 <= cy < self.height:
                valid.append((cx, cy))
        return valid

    def bfs(self, start_pos, targets=None):
        # Generic BFS to find distances to all reachable squares
        # start_pos: (x, y)
        # targets: set of (x, y) we are interested in (optional optimization)

        q = deque([(start_pos, 0)])
        visited = {start_pos: 0}

        while q:
            (cx, cy), dist = q.popleft()

            # Optimization: If we found all targets, maybe stop?
            # But we usually need the full map or specific closest ones.
            # For this problem, we usually want to find the nearest target.

            for nx, ny in self.get_neighbors(cx, cy):
                if not self.is_occupied(nx, ny) and (nx, ny) not in visited:
                    visited[(nx, ny)] = dist + 1
                    q.append(((nx, ny), dist + 1))

        return visited

    def step(self):
        # Sort units by reading order
        self.units.sort(key=lambda u: (u.y, u.x))

        for unit in self.units:
            if unit.hp <= 0:
                continue

            # Check for targets
            targets = [u for u in self.units if u.team != unit.team and u.hp > 0]
            if not targets:
                return False  # Combat ends

            # --- MOVE PHASE ---

            # Check if already in range
            in_range = False
            for t in targets:
                if abs(unit.x - t.x) + abs(unit.y - t.y) == 1:
                    in_range = True
                    break

            if not in_range:
                # Identify open squares in range of targets
                target_squares = set()
                for t in targets:
                    for nx, ny in self.get_neighbors(t.x, t.y):
                        if not self.is_occupied(nx, ny):
                            target_squares.add((nx, ny))

                if target_squares:
                    # BFS from unit to find reachable squares
                    dists = self.bfs((unit.x, unit.y))

                    # Filter reachable target squares
                    reachable = []
                    for tx, ty in target_squares:
                        if (tx, ty) in dists:
                            reachable.append(((tx, ty), dists[(tx, ty)]))

                    if reachable:
                        # Sort by distance, then reading order
                        reachable.sort(
                            key=lambda item: (item[1], item[0][1], item[0][0])
                        )
                        chosen_target = reachable[0][0]

                        # Now choose the step
                        # BFS from chosen_target to unit
                        dists_from_target = self.bfs(chosen_target)

                        # Check neighbors of unit
                        neighbors = self.get_neighbors(unit.x, unit.y)
                        best_step = None
                        min_step_dist = float("inf")

                        for nx, ny in neighbors:
                            if (
                                not self.is_occupied(nx, ny)
                                and (nx, ny) in dists_from_target
                            ):
                                d = dists_from_target[(nx, ny)]
                                if d < min_step_dist:
                                    min_step_dist = d
                                    best_step = (nx, ny)
                                # Tie-breaking is implicit by neighbor order (Up, Left, Right, Down)
                                # if we iterate in reading order?
                                # Wait, get_neighbors returns: Up (y-1), Left (x-1), Right (x+1), Down (y+1).
                                # Reading order is (y, x).
                                # (y-1, x) comes before (y, x-1) ?
                                # y-1 is definitely smaller than y. So yes, Up is first.
                                # Left is (y, x-1), Right is (y, x+1). Left is before Right.
                                # Down is (y+1, x). Last.
                                # So yes, iterating get_neighbors order and taking the first strictly smaller isn't enough.
                                # We need the first one that matches the MIN distance.

                        # Correct loop for best step:
                        best_step = None
                        min_step_dist = float("inf")

                        # Neighbors are already in reading order: Up, Left, Right, Down
                        # If we find a new min, take it.
                        # If we find an equal min, ignore it (since we want the FIRST in reading order).

                        for nx, ny in neighbors:
                            if (
                                not self.is_occupied(nx, ny)
                                and (nx, ny) in dists_from_target
                            ):
                                d = dists_from_target[(nx, ny)]
                                if d < min_step_dist:
                                    min_step_dist = d
                                    best_step = (nx, ny)

                        if best_step:
                            unit.x, unit.y = best_step

            # --- ATTACK PHASE ---
            # Check for adjacent targets (re-evaluate because we might have moved)
            adjacent_targets = []
            for t in targets:
                if abs(unit.x - t.x) + abs(unit.y - t.y) == 1:
                    adjacent_targets.append(t)

            if adjacent_targets:
                # Select target: fewest HP, then reading order
                adjacent_targets.sort(key=lambda t: (t.hp, t.y, t.x))
                target = adjacent_targets[0]

                target.hp -= unit.ap
                if target.hp <= 0:
                    # Unit dies
                    # We don't remove from list immediately to avoid breaking the loop iterator?
                    # The loop iterates over a copy or we handle 'dead' checks.
                    # We check `unit.hp > 0` at start of loop.
                    # But if a unit dies, it shouldn't attack later in this round.
                    pass

        # Cleanup dead units
        self.units = [u for u in self.units if u.hp > 0]
        return True

    def play(self, fail_on_elf_death=False):
        initial_elves = len([u for u in self.units if u.team == "E"])

        while True:
            # We need to detect if a full round completes
            self.units.sort(key=lambda u: (u.y, u.x))
            full_round = True

            for i, unit in enumerate(self.units):
                if unit.hp <= 0:
                    continue

                targets = [u for u in self.units if u.team != unit.team and u.hp > 0]
                if not targets:
                    full_round = False
                    # Combat ends immediately
                    return self.rounds * sum(u.hp for u in self.units if u.hp > 0)

                # ... Move logic ...
                # Move Logic
                in_range = False
                for t in targets:
                    if abs(unit.x - t.x) + abs(unit.y - t.y) == 1:
                        in_range = True
                        break

                if not in_range:
                    target_squares = set()
                    for t in targets:
                        for nx, ny in self.get_neighbors(t.x, t.y):
                            if not self.is_occupied(nx, ny):
                                target_squares.add((nx, ny))

                    if target_squares:
                        dists = self.bfs((unit.x, unit.y))
                        reachable = []
                        for tx, ty in target_squares:
                            if (tx, ty) in dists:
                                reachable.append(((tx, ty), dists[(tx, ty)]))

                        if reachable:
                            reachable.sort(
                                key=lambda item: (item[1], item[0][1], item[0][0])
                            )
                            chosen_target = reachable[0][0]

                            dists_from_target = self.bfs(chosen_target)
                            neighbors = self.get_neighbors(unit.x, unit.y)
                            best_step = None
                            min_step_dist = float("inf")

                            for nx, ny in neighbors:
                                if (
                                    not self.is_occupied(nx, ny)
                                    and (nx, ny) in dists_from_target
                                ):
                                    d = dists_from_target[(nx, ny)]
                                    if d < min_step_dist:
                                        min_step_dist = d
                                        best_step = (nx, ny)

                            if best_step:
                                unit.x, unit.y = best_step

                # Attack Logic
                enemies = [u for u in self.units if u.team != unit.team and u.hp > 0]
                adjacent_targets = []
                for t in enemies:
                    if abs(unit.x - t.x) + abs(unit.y - t.y) == 1:
                        adjacent_targets.append(t)

                if adjacent_targets:
                    adjacent_targets.sort(key=lambda t: (t.hp, t.y, t.x))
                    target = adjacent_targets[0]
                    target.hp -= unit.ap

                    if target.hp <= 0 and target.team == "E" and fail_on_elf_death:
                        return None

            self.units = [u for u in self.units if u.hp > 0]
            if fail_on_elf_death:
                current_elves = len([u for u in self.units if u.team == "E"])
                if current_elves < initial_elves:
                    return None

            if full_round:
                self.rounds += 1
            else:
                break

        return self.rounds * sum(u.hp for u in self.units)


def solve():
    input_file = "input.txt"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    # Part 1
    game = Game(input_file)
    result = game.play()
    print(f"Part 1 Result: {result}")

    # Part 2
    attack_power = 4
    while True:
        game = Game(input_file, elf_attack_power=attack_power)
        outcome = game.play(fail_on_elf_death=True)
        if outcome is not None:
            print(f"Part 2 Result: {outcome} (Attack Power: {attack_power})")
            break
        attack_power += 1


if __name__ == "__main__":
    solve()
