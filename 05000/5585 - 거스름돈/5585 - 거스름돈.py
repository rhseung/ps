# BOJ 5585 - 거스름돈
import sys
def input() -> str: return sys.stdin.readline()

m = int(input())
r = 1000 - m

c = 0
M = [500, 100, 50, 10, 5, 1]
i = 0

while r > 0 and i < len(M):
    if r >= M[i]:
        q = r // M[i]
        c += q
        r -= q * M[i]
    i += 1

print(c)
