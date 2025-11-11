# BOJ 9252 - LCS 2
import sys
def input() -> str: return sys.stdin.readline().rstrip()

s1 = input()
s2 = input()

m, n = len(s1), len(s2)

DP = [[0] * (n + 1) for _ in range(m + 1)]

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[i - 1] == s2[j - 1]:
            DP[i][j] = 1 + DP[i - 1][j - 1]
        else:
            DP[i][j] = max(DP[i - 1][j], DP[i][j - 1])

# for dp in DP:
#     print(dp)
print(DP[m][n])

ret = ''
i, j = m, n

while i >= 0 and j >= 0:
    if DP[i][j] == DP[i - 1][j]:
        i -= 1
    elif DP[i][j] == DP[i][j - 1]:
        j -= 1
    elif DP[i][j] == DP[i - 1][j - 1] + 1:
        ret += s1[i - 1]
        i -= 1
        j -= 1
ret = ret[::-1]

print(ret)
