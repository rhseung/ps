# BOJ 11066 - 파일 합치기
import sys
def input() -> str: return sys.stdin.readline().rstrip()

inf = sys.maxsize

def dp(l: int, r: int, DP: list[list[int]], S: list[int]) -> int:
    if l == r:
        return 0
    elif DP[l][r] != -1:
        return DP[l][r]

    DP[l][r] = min((dp(l, k, DP, S) + dp(k + 1, r, DP, S) + S[r] - (S[l - 1] if l >= 1 else 0) for k in range(l, r)), default=inf)
    return DP[l][r]

t = int(input())
for _ in range(t):
    n = int(input())
    A = list(map(int, input().split()))
    S = [0] * n
    S[0] = A[0]
    for i in range(1, n):
        S[i] = S[i - 1] + A[i]

    DP = [[-1] * n for _ in range(n)]
    print(dp(0, n - 1, DP, S))
