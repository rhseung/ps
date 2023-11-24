__problem__ = 'https://boj.kr/11047', '동전 0'

import sys

input = sys.stdin.readline

n, k = map(int, input().split())
N = [int(input().strip()) for _ in range(n)]

count = 0
for e in reversed(N):
    t = k // e
    count += t
    k -= e * t

    if k == 0:
        print(count)
        exit()
