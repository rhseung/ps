from sys import stdin
from sys import setrecursionlimit
from functools import lru_cache as memoization
from collections import Counter
from collections import deque
setrecursionlimit(10 ** 4)
def inputline(): return stdin.readline().strip()

mod = 1_234_567_891
r = 31

n = int(input())
s = inputline()
hash = 0
for i in range(len(s)):
	hash = (hash + (ord(s[i]) - ord('a') + 1) * r**i % mod) % mod

print(hash)