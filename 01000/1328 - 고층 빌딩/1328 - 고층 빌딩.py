# BOJ 1328 - 고층 빌딩
import sys
def input() -> str: return sys.stdin.readline()

n, l, r = map(int, input().split())

DP = [[[0 for _ in range(r + 1)] for _ in range(l + 1)] for _ in range(n + 1)]
DP[1][1][1] = 1

for n_ in range(1, n + 1):
    for l_ in range(1, l + 1):
        for r_ in range(1, r + 1):
            # 가장 작은 빌딩을 왼쪽에 배치할 경우 -> n과 l이 1 늘어나므로
            DP[n_][l_][r_] += DP[n_ - 1][l_ - 1][r_]
            DP[n_][l_][r_] %= 1_000_000_007

            # 가장 작은 빌딩을 오른쪽에 배치할 경우 -> n과 r이 1 늘어나므로
            DP[n_][l_][r_] += DP[n_ - 1][l_][r_ - 1]
            DP[n_][l_][r_] %= 1_000_000_007

            # 가장 작은 빌딩을 중간에 배치할 경우 -> n만 1 늘어나므로
            DP[n_][l_][r_] += (n_ - 2) * DP[n_ - 1][l_][r_]
            DP[n_][l_][r_] %= 1_000_000_007

print(DP[n][l][r])
