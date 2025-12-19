from collections import defaultdict

def runComputer(data, input_vals):
    # Copy data to memory
    program = defaultdict(int, {k: v for k, v in enumerate(data)})
    output = None
    i = 0
    relbase = 0
    input_idx = 0

    while True:
        opcode = program[i] % 100

        if opcode == 99:
            break

        mode1 = (program[i] - opcode) // 100 % 10
        mode2 = (program[i] - opcode) // 1000 % 10
        mode3 = (program[i] - opcode) // 10000 % 10

        p1, p2, p3 = None, None, None

        if mode1 == 0: p1 = program[i + 1]
        elif mode1 == 1: p1 = i + 1
        elif mode1 == 2: p1 = program[i + 1] + relbase

        if mode2 == 0: p2 = program[i + 2]
        elif mode2 == 1: p2 = i + 2
        elif mode2 == 2: p2 = program[i + 2] + relbase
      
        if mode3 == 0: p3 = program[i + 3]
        elif mode3 == 1: pass # raise ValueError('Immediate mode invalid for param 3')
        elif mode3 == 2: p3 = program[i + 3] + relbase

        if opcode == 1: # addition
            program[p3] = program[p1] + program[p2]
            i += 4
        elif opcode == 2: # multiplication
            program[p3] = program[p1] * program[p2]
            i += 4
        elif opcode == 3: # input
            if input_idx >= len(input_vals):
                 raise ValueError("Not enough input")
            program[p1] = input_vals[input_idx]
            input_idx += 1
            i += 2
        elif opcode == 4: # output
            yield program[p1]
            i += 2
        elif opcode == 5: # jump-if-true
            i = program[p2] if program[p1] != 0 else i + 3
        elif opcode == 6: # jump-if-false
            i = program[p2] if program[p1] == 0 else i + 3
        elif opcode == 7: # less-than
            program[p3] = 1 if program[p1] < program[p2] else 0
            i += 4
        elif opcode == 8: # equals
            program[p3] = 1 if program[p1] == program[p2] else 0
            i += 4
        elif opcode == 9: # relative base adjust
            relbase += program[p1]
            i += 2
        else:
            raise ValueError(f'opcode {opcode} from {program[i]}')

def check(data, x, y):
    # Inputs are passed as [x, y] but computer reads them in order.
    # The problem says: "The program uses two input instructions to request the X and Y position"
    # Usually this means first input is X, second is Y.
    runner = runComputer(data, [x, y])
    try:
        return next(runner)
    except StopIteration:
        return 0

def solve(data):
    x = 0
    y = 100 # Start a bit down to avoid the tip where beam might be disconnected or weird
    
    # Square size
    S = 100
    
    while True:
        # Check left edge at current row y
        # We assume x is near the left edge from previous row, so we just increment until we hit beam
        while check(data, x, y) == 0:
            x += 1
        
        # At this point (x, y) is the left-most point of the beam at row y.
        # We consider this row 'y' as the BOTTOM row of our candidate square.
        # The square would extend upwards from here.
        # Bottom-Left: (x, y)
        # Top-Left: (x, y - S + 1)
        # Top-Right: (x + S - 1, y - S + 1)
        
        # We need to check if the Top-Right corner fits in the beam.
        
        top_y = y - S + 1
        
        if top_y >= 0:
             # Check if the top-right corner is in the beam
             if check(data, x + S - 1, top_y) == 1:
                 # Found it!
                 # The answer requires the top-left coordinate.
                 # Top-left is (x, top_y)
                 result_x = x
                 result_y = top_y
                 return result_x * 10000 + result_y
        
        y += 1

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        raw = list(map(int, file.read().splitlines()[0].split(",")))
    
    print("Part 2:", solve(raw))
