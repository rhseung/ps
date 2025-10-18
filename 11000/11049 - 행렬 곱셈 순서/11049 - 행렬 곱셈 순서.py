# BOJ 11049 - 행렬 곱셈 순서
import sys
def input() -> str: return sys.stdin.readline()

n = int(input())
P = [0] * (n + 1)

for i in range(n):
    P[i], P[i + 1] = map(int, input().split())

DP = [[0] * n for _ in range(n)]

# l은 체인 길이
for l in range(2, n + 1):
    for i in range(n - l + 1):
        j = i + l - 1
        DP[i][j] = min(DP[i][k] + DP[k + 1][j] + P[i] * P[k + 1] * P[j + 1] for k in range(i, j))

# print(DP)
print(DP[0][n - 1])