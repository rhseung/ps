# BOJ 1958 - LCS 3
import sys
def input() -> str: return sys.stdin.readline().rstrip()

s1 = input()
s2 = input()
s3 = input()

l, m, n = len(s1), len(s2), len(s3)

DP = [[[0] * (n + 1) for _ in range(m + 1)] for _ in range(l + 1)]

for i in range(1, l + 1):
    for j in range(1, m + 1):
        for k in range(1, n + 1):
            if s1[i - 1] == s2[j - 1] == s3[k - 1]:
                DP[i][j][k] = DP[i - 1][j - 1][k - 1] + 1
            else:
                DP[i][j][k] = max(DP[i - 1][j][k], DP[i][j - 1][k], DP[i][j][k - 1])

print(DP[l][m][n])