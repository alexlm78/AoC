class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 0:^, 1:>, 2:v, 3:<
        self.turn_state = 0  # 0:Left, 1:Straight, 2:Right
        self.crashed = False

    def __repr__(self):
        return f"Cart({self.x}, {self.y}, {self.direction})"


def solve():
    with open("input.txt", "r") as f:
        lines = [line.strip("\n") for line in f]

    grid = []
    carts = []

    # Directions: 0:^, 1:>, 2:v, 3:<
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]

    for y, line in enumerate(lines):
        row = []
        for x, char in enumerate(line):
            if char in "^>v<":
                direction = {"^": 0, ">": 1, "v": 2, "<": 3}[char]
                carts.append(Cart(x, y, direction))
                # Replace cart with track
                if char in "^v":
                    row.append("|")
                else:
                    row.append("-")
            else:
                row.append(char)
        grid.append(row)

    tick = 0
    first_crash_reported = False

    while True:
        tick += 1
        # Sort carts by y, then x
        carts.sort(key=lambda c: (c.y, c.x))

        for i, cart in enumerate(carts):
            if cart.crashed:
                continue

            # Move cart
            cart.x += dx[cart.direction]
            cart.y += dy[cart.direction]

            # Check for collision
            for other in carts:
                if (
                    other != cart
                    and not other.crashed
                    and other.x == cart.x
                    and other.y == cart.y
                ):
                    cart.crashed = True
                    other.crashed = True
                    if not first_crash_reported:
                        print(f"Part 1 - First crash: {cart.x},{cart.y}")
                        first_crash_reported = True
                    break

            if cart.crashed:
                continue

            # Update direction based on track
            try:
                track = grid[cart.y][cart.x]
            except IndexError:
                print(f"Error: Cart out of bounds at {cart.x},{cart.y}")
                return

            if track == "+":
                if cart.turn_state == 0:  # Left
                    cart.direction = (cart.direction - 1) % 4
                elif cart.turn_state == 1:  # Straight
                    pass
                elif cart.turn_state == 2:  # Right
                    cart.direction = (cart.direction + 1) % 4
                cart.turn_state = (cart.turn_state + 1) % 3

            elif track == "/":
                if cart.direction == 0:
                    cart.direction = 1
                elif cart.direction == 1:
                    cart.direction = 0
                elif cart.direction == 2:
                    cart.direction = 3
                elif cart.direction == 3:
                    cart.direction = 2

            elif track == "\\":
                if cart.direction == 0:
                    cart.direction = 3
                elif cart.direction == 1:
                    cart.direction = 2
                elif cart.direction == 2:
                    cart.direction = 1
                elif cart.direction == 3:
                    cart.direction = 0

            elif track in "|-":
                pass

            else:
                print(
                    f"Error: Cart went off track at {cart.x},{cart.y} (track: '{track}')"
                )
                return

        # Remove crashed carts
        carts = [c for c in carts if not c.crashed]

        if len(carts) == 1:
            last_cart = carts[0]
            print(f"Part 2 - Last cart position: {last_cart.x},{last_cart.y}")
            return
        elif len(carts) == 0:
            print("All carts crashed!")
            return


if __name__ == "__main__":
    solve()
