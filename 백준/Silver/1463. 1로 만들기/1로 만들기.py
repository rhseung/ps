__problem__ = 'https://boj.kr/1463', '1로 만들기'

import sys
from math import inf

input = sys.stdin.readline

n = int(input())

# 10 -> 9 -> 3 -> 1 로 하는 것이 제일 빠르기 때문에 그리디로는 풀 수 없음
dp = [0] * (n + 1)

# note: top-down은 재귀 호출 limit에 걸리게 되는데 setrecursionlimit를 늘리면 메모리가 늘어나서 메모리초과
# def solve(n):
#     if n not in dp:
#         min_way = inf
#
#         if n % 3 == 0:
#             min_way = min(min_way, solve(n // 3) + 1)
#         if n % 2 == 0:
#             min_way = min(min_way, solve(n // 2) + 1)
#         min_way = min(min_way, solve(n - 1) + 1)
#
#         dp[n] = min_way
#
#     return dp[n]

for i in range(2, n+1):
    min_way = inf

    if i % 3 == 0:
        min_way = min(min_way, dp[i // 3] + 1)
    if i % 2 == 0:
        min_way = min(min_way, dp[i // 2] + 1)
    min_way = min(min_way, dp[i - 1] + 1)

    dp[i] = min_way

print(dp[n])
