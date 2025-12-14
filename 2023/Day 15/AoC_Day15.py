from collections import OrderedDict

def s_hash(s):
    current = 0
    for char in s:
        current += ord(char)
        current = (current*17) % 256
    return current

total1 = 0
boxes = [OrderedDict() for _ in range(256)]
with open('input.txt', 'r') as f:
    for line in f.readlines():
        for s in line.strip().split(','):
            # part 1
            total1 += s_hash(s)
            # part 2
            if '-' in s:
                label = s[:-1]
                box = boxes[s_hash(label)]
                if label in box:
                    box.pop(label)
            else:
                label, focal = s.split('=')
                box = boxes[s_hash(label)]
                box[label] = int(focal)

# part 1
print(total1)

# part 2
total2 = 0
for i, box in enumerate(boxes):
    for j, lens in enumerate(box.items()):
        total2 += ((i+1) * (j+1) * lens[1])
print(total2)
