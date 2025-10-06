# BOJ 2302 - 극장 좌석
import sys
def input() -> str: return sys.stdin.readline()

n = int(input())
m = int(input())
VIP = [int(input()) for _ in range(m)]

W = [n] if m == 0 else [VIP[0] - 1, n - VIP[-1]]
for i in range(1, m):
    W.append(VIP[i] - VIP[i - 1] - 1)

DP = [0] * (max(W) + 1)
DP[0] = 1
if len(DP) > 1:
    DP[1] = 1
if len(DP) > 2:
    DP[2] = 2
for i in range(3, len(DP)):
    DP[i] = DP[i - 1] + DP[i - 2]

ret = 1
for width in W:
    ret *= DP[width]

print(ret)
