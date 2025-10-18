# BOJ 12920 - 평범한 배낭 2
import sys
def input() -> str: return sys.stdin.readline()

n, m = map(int, input().split())

W = [0]
V = [0]

for i in range(1, n + 1):
    w, v, k = map(int, input().split())

    f = 1
    while k > 0:
        W.append(w * min(k, f))
        V.append(v * min(k, f))

        k -= f
        f <<= 1

new_n = len(W) - 1
DP = [[0] * (m + 1) for _ in range(new_n + 1)]

for i in range(1, new_n + 1):
    for j in range(1, m + 1):
        if j >= W[i]:
            DP[i][j] = max(DP[i - 1][j], DP[i - 1][j - W[i]] + V[i])
        else:
            DP[i][j] = DP[i - 1][j]

print(DP[new_n][m])