# BOJ 5582 - 공통 부분 문자열
import sys
def input() -> str: return sys.stdin.readline()

s1 = input().strip()
s2 = input().strip()
n, m = len(s1), len(s2)
DP = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

for i in range(1, n + 1):
    for j in range(1, m + 1):
        if s1[i - 1] == s2[j - 1]:
            DP[i][j] = DP[i - 1][j - 1] + 1
        else:
            DP[i][j] = 0

print(max(map(max, DP)))
