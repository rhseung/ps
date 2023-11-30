__problem__ = 'https://boj.kr/1463', '1로 만들기'

import sys
from math import inf

input = sys.stdin.readline

n = int(input())

# 10 -> 9 -> 3 -> 1 로 하는 것이 제일 빠르기 때문에 그리디로는 풀 수 없음
dp = {1: 0}

def get(n):
    if n in dp:
        return dp[n]
    if n % 6 == 0:
        dp[n] = min(get(n // 3), get(n // 2)) + 1
    elif n % 3 == 0:
        dp[n] = min(get(n // 3), get(n - 1)) + 1
    elif n % 2 == 0:
        dp[n] = min(get(n // 2), get(n - 1)) + 1
    else:
        dp[n] = get(n - 1) + 1

    return dp[n]

print(get(n))
