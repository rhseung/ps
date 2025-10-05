# BOJ 2098 - 외판원 순회
import sys


def input() -> str: return sys.stdin.readline()


inf = float('inf')

n = int(input())
W = [[w if w != 0 else inf for w in map(int, input().split())] for _ in range(n)]

# DP[mask][i] = mask: 지금까지 방문한 도시들의 집합, i: 지금 서 있는 도시
# 다음 도시 j로: next_mask = mask | (1 << j), DP[next_mask][j] = min(DP[next_mask][j], DP[mask][i] + W[i][j])

DP = [[-1] * n for _ in range(1 << n)]


def dp(visited: int, now: int):
    if visited == (1 << n) - 1:  # all visited
        DP[visited][now] = W[now][0]
        return DP[visited][now]

    if DP[visited][now] != -1:
        return DP[visited][now]

    for i in range(1, n):
        if visited & (1 << i):
            continue

        if DP[visited][now] == -1:
            DP[visited][now] = dp(visited | (1 << i), i) + W[now][i]
        else:
            DP[visited][now] = min(DP[visited][now], dp(visited | (1 << i), i) + W[now][i])

    return DP[visited][now]


print(dp(1, 0))
