# BOJ 1890 - 점프
import sys
input = sys.stdin.readline

n = int(input())
A = [list(map(int, input().split())) for _ in range(n)]
D = [[0] * n for _ in range(n)]
D[0][0] = 1

def dp(i: int, j: int) -> int:
    if D[i][j] != 0:
        return D[i][j]

    ret = 0
    for u in range(i):
        if A[u][j] == i - u:
            ret += dp(u, j)
    for v in range(j):
        if A[i][v] == j - v:
            ret += dp(i, v)

    D[i][j] = ret

    return ret


print(dp(n - 1, n - 1))