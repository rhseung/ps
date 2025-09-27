# BOJ 2225 - 합분해
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
m = 1_000_000_000
DP = [[0] * (k + 1) for _ in range(n + 1)]

def dp(n: int, k: int) -> int:
    if DP[n][k] != 0:
        return DP[n][k]

    if n == 0:
        DP[n][k] = 1
    if n == 1:
        DP[n][k] = k % m
    elif k == 2:
        DP[n][k] = (n + 1) % m
    elif k == 1:
        DP[n][k] = 1
    else:
        ret = 0
        for i in range(n + 1):
            ret = (ret + dp(n - i, k - 1) % m) % m

        DP[n][k] = ret

    # print(f"DP[{n}][{k}] = {DP[n][k]}")
    return DP[n][k]

print(dp(n, k))
