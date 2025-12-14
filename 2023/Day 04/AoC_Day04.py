f = open("AoC_Day04.input.txt").read().strip().split('\n')

p1 = 0
dp = [1] * len(f)

for i, x in enumerate(f):
   win, num = x.split(':')[1].strip().split('|')
   win = { s for s in win.split() }
   num = [ s for s in num.split() ]
   matches = len([ s for s in num if s in win ])

   # part 1
   if matches:
      p1 += 2 ** (matches - 1)

   # part 2 (simple dp)
   for j in range(matches):
      dp[i + j + 1] += dp[i]

print(p1)
print(sum(dp))
