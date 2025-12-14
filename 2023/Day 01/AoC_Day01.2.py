import re

def f(x):
    for i, s in enumerate(['one','two','three','four','five','six','seven','eight','nine']):
        x = x.replace(s, s[0] + str(i+1) + s[-1])
    z = re.findall(r'\d', x)
    return int(z[0] + z[-1])

print(sum(map(f, open('AoC_Day01.txt'))))