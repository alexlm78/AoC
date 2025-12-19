from collections import deque, defaultdict
import sys
import itertools

# Intcode Computer
def runComputer(data, inputqueue: deque, inputDefault = lambda: -1):
  program = defaultdict(int, { k: v for k, v in enumerate(data) })
  output = None
  i = 0
  relbase = 0

  while True:
    opcode = program[i] % 100

    if opcode == 99: break

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
    elif mode3 == 1: raise ValueError('Immediate mode invalid for param 3')
    elif mode3 == 2: p3 = program[i + 3] + relbase

    if opcode == 1: # addition
      program[p3] = program[p1] + program[p2]
      i += 4
    elif opcode == 2: # multiplication
      program[p3] = program[p1] * program[p2]
      i += 4
    elif opcode == 3: # input
      if len(inputqueue) > 0:
        program[p1] = inputqueue.popleft()
        i += 2
      else:
        # program[p1] = inputDefault()
        # i += 2
        yield "NEED_INPUT"
        continue
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

def send_command(q, cmd):
    # print(f"Sending command: {cmd}")
    for c in cmd:
        q.append(ord(c))
    q.append(10)

def parse_output(output_str):
    lines = output_str.strip().split('\n')
    room_name = ""
    desc = ""
    doors = []
    items = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('== '):
            room_name = line.replace('==', '').strip()
        elif line == "Doors here lead:":
            i += 1
            while i < len(lines) and lines[i].strip().startswith('- '):
                doors.append(lines[i].strip()[2:])
                i += 1
            continue
        elif line == "Items here:":
            i += 1
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(lines[i].strip()[2:])
                i += 1
            continue
        elif line == "Command?":
            pass
        else:
            if line:
                desc += line + "\n"
        i += 1
    return room_name, doors, items, desc

def get_output(vm):
    out_str = ""
    while True:
        try:
            res = next(vm)
            if res == "NEED_INPUT":
                break
            out_str += chr(res)
        except StopIteration:
            break
    return out_str

def solve():
    with open('input.txt', 'r') as f:
        program = list(map(int, f.read().strip().split(',')))

    q = deque()
    vm = runComputer(program, q)
    
    # BFS/DFS state
    # We need to map the whole ship.
    # Since we can't easily clone the VM state in Python (it's a defaultdict and has internal pointer),
    # we might need to re-run from scratch to reach a state, OR just traverse back and forth.
    # Traversing back and forth (DFS) is easier if the graph is a tree.
    # If it's not a tree, we need to be careful.
    
    # Let's assume we can move around.
    # We will use DFS to explore.
    
    # Path to current node
    path = []
    
    # Known rooms: name -> {doors, items}
    visited = {}
    
    # Reverse direction map
    reverse_dir = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
    
    # Dangerous items to ignore
    blacklist = ['infinite loop', 'giant electromagnet', 'photons', 'escape pod', 'molten lava']
    
    # We need to keep track of where we are.
    # Since we can't clone the VM, we have to drive the single VM instance.
    
    # Initial read
    out = get_output(vm)
    room_name, doors, items, desc = parse_output(out)
    
    print(f"Start at: {room_name}")
    print(f"Doors: {doors}")
    print(f"Items: {items}")
    
    # We'll maintain a stack for DFS: (room_name, iter_doors)
    # Actually, recursion is easier for DFS logic.
    
    collected_items = []
    checkpoint_path = [] # Path from start to Security Checkpoint
    checkpoint_dir = "" # Direction to enter the pressure sensitive floor (not the room itself, but the room BEFORE it)
    
    # We need to find "Security Checkpoint". The pressure floor is usually adjacent to it.
    
    # Let's write a recursive DFS function.
    # It takes the current room info.
    # It iterates over doors.
    # If a door leads to a new room, go there, recurse, then come back.
    
    visited[room_name] = {'doors': doors, 'items': items}
    
    # We need to handle the case where we might loop back to a visited room.
    # But since we don't know the connection graph ahead of time, we have to try moving.
    
    def dfs(current_room):
        nonlocal checkpoint_path, checkpoint_dir
        
        # Pick up safe items
        curr_items = visited[current_room]['items']
        for item in curr_items:
            if item not in blacklist:
                print(f"Taking {item} in {current_room}")
                send_command(q, f"take {item}")
                out = get_output(vm)
                collected_items.append(item)
        
        # Explore neighbors
        curr_doors = visited[current_room]['doors']
        
        for d in curr_doors:
            # We don't know where 'd' leads yet unless we go there.
            # But wait, if we go there and it's visited, we must come back immediately.
            
            # To know if we've visited the room 'd' leads to, we have to move.
            
            send_command(q, d)
            out = get_output(vm)
            
            # Debug: Check where we are
            # print(f"Moved {d}, Output len: {len(out)}")
            
            if "Alert!" in out or "heavier" in out or "lighter" in out:
                 print(f"Found Pressure-Sensitive Floor direction! It's {d} of {current_room}")
                 checkpoint_path = list(path)
                 checkpoint_dir = d
                 # We were bounced back to current_room (or similar)
                 # We treat this as a visited dead-end for now, but we mark the checkpoint.
                 continue

            new_room, new_doors, new_items, new_desc = parse_output(out)
            
            if new_room == "Pressure-Sensitive Floor":
                print(f"Found Pressure-Sensitive Floor! It's {d} of {current_room}")
                # We found it. We should not have entered it unless we are ready.
                # Usually we get ejected if weight is wrong.
                # "A loud, robotic voice says 'Alert! Droids on this ship are...'"
                # And we are back in the previous room.
                
                # Check if we are back in current_room or if we are in the pressure floor (unlikely if weight is wrong).
                if "Alert!" in out or "heavier" in out or "lighter" in out:
                     # We were bounced back.
                     print("Bounced back from Pressure-Sensitive Floor.")
                     checkpoint_path = list(path) # Path to current_room
                     checkpoint_dir = d
                     continue
                else:
                    # We are somehow in the pressure floor (maybe we got lucky with weight 0?)
                    # Or maybe we just entered it.
                    print("Entered Pressure-Sensitive Floor?")
                    # If we are here, we might be stuck or done.
                    # But usually we need items.
                    pass
            
            if new_room not in visited:
                visited[new_room] = {'doors': new_doors, 'items': new_items}
                path.append(d)
                dfs(new_room)
                path.pop()
                
                # Return to current_room
                back_cmd = reverse_dir[d]
                send_command(q, back_cmd)
                get_output(vm) # Consume output
            else:
                # We found a loop or just revisited a room.
                # Go back immediately.
                back_cmd = reverse_dir[d]
                send_command(q, back_cmd)
                get_output(vm)
                
    dfs(room_name)
    
    print("Exploration finished.")
    print(f"Collected items: {collected_items}")
    print(f"Checkpoint is at {checkpoint_path} then {checkpoint_dir}")
    
    # Navigate to Checkpoint
    # We are currently at start (dfs backtracked all the way).
    # Wait, dfs backtracks, so we should be back at start.
    
    # Verify we are at start
    # We can just assume we are if the code is correct.
    
    # Go to Security Checkpoint (the room BEFORE the pressure floor)
    for move in checkpoint_path:
        send_command(q, move)
        get_output(vm)
        
    print("Arrived at Security Checkpoint.")
    
    # Now try combinations
    # We have all collected items.
    # We need to drop some to match the weight.
    # We can try all subsets.
    
    import itertools
    
    # First drop everything to start with 0 weight (or just hold everything and drop subsets)
    # It's easier to drop everything and pick up subsets, OR hold everything and drop subsets.
    # Let's hold everything.
    
    # We need to test entering the floor.
    # If we fail, we are pushed back to Security Checkpoint.
    
    # Try Gray Code or just simple iteration?
    # Simple iteration is fine for 8 items (2^8 = 256 tries).
    
    # We are holding 'collected_items'.
    # We can try dropping some items.
    
    # Current inventory is 'collected_items'.
    
    for r in range(len(collected_items) + 1):
        for keep in itertools.combinations(collected_items, r):
            # We want to keep these items.
            # So we drop the others.
            
            # Current state: we might be holding random stuff from previous iteration.
            # To be safe: drop everything, then take what we need.
            # OR: be smart about diff.
            
            # Let's just synchronize.
            # Drop all currently held, take 'keep'.
            # But we don't know what we are holding if we failed previously?
            # Actually we do, we are holding what we had.
            # But getting ejected doesn't change inventory.
            
            # Let's just track current inventory in a variable.
            current_inv = set(collected_items) # We start holding everything
            
            # Oh wait, the loop logic needs to be cleaner.
            pass

    # Better approach for trying combinations:
    # 1. Drop all items to have empty inventory.
    # 2. Iterate combinations.
    # 3. For each combination:
    #    a. Take items in combination.
    #    b. Try to move.
    #    c. If success, print code and exit.
    #    d. If fail, we are back. Drop items.
    
    # Drop all first
    for item in collected_items:
        send_command(q, f"drop {item}")
        get_output(vm)
        
    print("Dropped all items.")
    
    for r in range(len(collected_items) + 1):
        for attempt in itertools.combinations(collected_items, r):
            # Equip items
            for item in attempt:
                send_command(q, f"take {item}")
                get_output(vm)
            
            # Try to move
            send_command(q, checkpoint_dir)
            res = get_output(vm)
            
            if "Analysis complete! You may proceed." in res or "get in by typing" in res:
                print(f"Success with items: {attempt}")
                print(res)
                return
            
            # If fail, we are back.
            # Unequip items
            for item in attempt:
                send_command(q, f"drop {item}")
                get_output(vm)
                
solve()
