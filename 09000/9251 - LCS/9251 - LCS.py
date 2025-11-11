# BOJ 9251 - LCS
import sys
def input() -> str: return sys.stdin.readline().rstrip()

s1 = input()
s2 = input()

m, n = len(s1), len(s2)

# recursion
# def LCS(i: int, j: int):
#     if i == 0 or j == 0:
#         return 0
#     elif s1[i] == s2[j]:
#         return 1 + LCS(i - 1, j - 1)
#     else:
#         return max(LCS(i - 1, j), LCS(i, j - 1))

# memoization
# sys.setrecursionlimit(m * n)
# DP = [[-1] * n for _ in range(m)]   # LCS 값이 0일 수도 있어서 DP를 0으로 초기화하면 중복 계산 발생
# def LCS(i: int, j: int):
#     if i < 0 or j < 0:
#         return 0
#     elif DP[i][j] != -1:
#         return DP[i][j]
#
#     if s1[i] == s2[j]:
#         DP[i][j] = 1 + LCS(i - 1, j - 1)
#     else:
#         DP[i][j] = max(LCS(i - 1, j), LCS(i, j - 1))
#     return DP[i][j]
# print(LCS(m - 1, n - 1))

# tabulation
# DP = [[-1] * n for _ in range(m)]
# for i in range(m):
#     for j in range(n):
#         if s1[i] == s2[j]:
#             # 인덱스가 음수(-1)가 되는 것을 방지하기 위한 똥꼬쇼
#             if i >= 1 and j >= 1:
#                 DP[i][j] = 1 + DP[i - 1][j - 1]
#             else:
#                 DP[i][j] = 1
#         else:
#             # 인덱스가 음수(-1)가 되는 것을 방지하기 위한 똥꼬쇼
#             if i >= 1 and j >= 1:
#                 DP[i][j] = max(DP[i - 1][j], DP[i][j - 1])
#             elif i >= 1:
#                 DP[i][j] = DP[i - 1][j]
#             elif j >= 1:
#                 DP[i][j] = DP[i][j - 1]
#             else:
#                 DP[i][j] = 0
# print(DP[m - 1][n - 1])

# improved tabulation
DP = [[-1] * (n + 1) for _ in range(m + 1)]
# DP를 한 칸씩 민다면?
for i in range(m + 1):
    DP[i][0] = 0
for j in range(n + 1):
    DP[0][j] = 0

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[i - 1] == s2[j - 1]:
            DP[i][j] = DP[i - 1][j - 1] + 1
        else:
            DP[i][j] = max(DP[i - 1][j], DP[i][j - 1])
print(DP[m][n])

# for dp in DP:
#     print(dp)
