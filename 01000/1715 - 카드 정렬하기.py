__problem__ = 'https://boj.kr/1715', '카드 정렬하기'

import sys
from heapq import heappop, heappush

input = sys.stdin.readline

n = int(input().strip())
N = []

for _ in range(n):
    heappush(N, int(input().strip()))

s = 0
while len(N) > 1:
    t = heappop(N) + heappop(N)
    heappush(N, t)
    s += t

print(s)
