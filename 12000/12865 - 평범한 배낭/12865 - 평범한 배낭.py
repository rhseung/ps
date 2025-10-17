# BOJ 12865 - 평범한 배낭
import sys
def input() -> str: return sys.stdin.readline()

n, k = map(int, input().split())

W = [0] * (n + 1)
V = [0] * (n + 1)
DP = [[0] * (k + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    W[i], V[i] = map(int, input().split())

def knapsack(i: int, j: int) -> int:
    if i == 0 or j == 0:
        return 0
    elif DP[i][j] != 0:
        return DP[i][j]

    if j >= W[i]:
        DP[i][j] = max(knapsack(i - 1, j), knapsack(i - 1, j - W[i]) + V[i])
    else:
        DP[i][j] = knapsack(i - 1, j)

    return DP[i][j]

print(knapsack(n, k))
