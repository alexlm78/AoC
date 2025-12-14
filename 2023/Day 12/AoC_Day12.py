from time import time
from functools import cache
 
 
def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result
 
    return wrap_func
 
 
@cache
def count_groups(string):
    # return an empty list if the input is empty
    if not string:
        return tuple()
    # Initialize an empty list to store the output
    output = []
    # Initialize a variable to store the current group count
    count = 0
    # Loop through each character in the string
    for char in string:
        # Check if the character is '#'
        if char == '#':
            # Increment the count by 1
            count += 1
        # Check if the character is '.'
        elif char == '.':
            # Check if the count is not zero
            if count != 0:
                # Add the count to the output list
                output.append(count)
                # Reset the count to zero
                count = 0
    # Append the last count if the last character was a '#'
    if string[-1] == '#':
        output.append(count)
    # Return the output list as a tuple (tuple for caching)
    return tuple(output)
 
 
@cache
def fcs(s, g):
    if len(s) < sum(g):
        return 0
    if not s:  # if s is empty, check if there are entries left in g
        return g == ()  # return True if g is empty
    if not g:  # if g is empty, check if there are any broken springs left in s
        return '#' not in s
    combos = 0
    if '?' in s:
        i = s.index('?')
    else:
        return count_groups(s) == g
    sbi = s[:i]  # slice before
    sai = s[i+1:]  # slice after
 
    # if the ? is a .
    gb = count_groups(sbi)  # finding the groups before the ?
    gt = g[:len(gb)]  # trimming g to match the len of gb
    if gt == gb:  # if they match, continue searching with the string after the ? and the reduced groups
        combos += fcs(sai, g[len(gb):])
 
    # if the ? is a #
    gb = count_groups(sbi + '#')  # find the group counts with the additional #
    gt = g[:len(gb)]  # trim like before
    if gb[:-1] == gt[:-1]:  # only match all but the last
        if gb[-1] < gt[-1]:  # if the last doesn't match, flip the current ? to a # and continue matching
            combos += fcs(sbi + '#' + sai, g)
        # if the last of the groups match, and sai is not empty or the next character isn't a #
        if gb[-1] == gt[-1] and (not sai or sai[0] != '#'):
            combos += fcs(sai[1:], g[len(gb):])
 
    return combos
 
 
@timer_func
def day12(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]
    combos = 0
    for line in lines:
        records, groups = line.split()
        groups = tuple([int(x) for x in groups.split(',')])
 
        if not part2:
            combos += fcs(records, groups)
        else:
            combo = fcs('?'.join([records for _ in range(5)]), groups * 5)
            combos += combo
 
    return combos
 
 
def main():
    #assert day12('test12') == 21
    print(f"Part 1: {day12('input.txt')}")
 
    #assert day12('test12', True) == 525152
    print(f"Part 2: {day12('input.txt', True)}")

if __name__ == '__main__':
    main()
