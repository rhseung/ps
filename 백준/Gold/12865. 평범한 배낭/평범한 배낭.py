__problem__ = 'https://boj.kr/12865', '평범한 배낭'

import sys

input = sys.stdin.readline

N, K = map(int, input().split())
W = [0] * (N + 1)
V = [0] * (N + 1)
D = [[0]*(K + 1) for _ in range(N + 1)]

for i in range(1, N + 1):
    W[i], V[i] = map(int, input().split())

for i in range(1, N + 1):
    for j in range(1, K + 1):
        if j < W[i]:
            D[i][j] = D[i - 1][j]
        else:
            D[i][j] = max(D[i - 1][j], D[i - 1][j - W[i]] + V[i])

print(D[N][K])
