# BOJ 2748 - 피보나치 수 2
import sys
def input() -> str: return sys.stdin.readline()

n = int(input())

DP = [0] * (n + 1)
if n + 1 > 1:
    DP[1] = 1

for i in range(2, n + 1):
    DP[i] = DP[i - 1] + DP[i - 2]

print(DP[n])