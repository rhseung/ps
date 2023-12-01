__problem__ = 'https://boj.kr/14501', '퇴사'

import sys

input = sys.stdin.readline

N = int(input())
T = [0] * N
P = [0] * N
D = [0] * (N + 1)
ans = 0

for i in range(N):
    T[i], P[i] = map(int, input().split())

for i in range(N-1, -1, -1):
    if i + T[i] > N:
        D[i] = D[i + 1]     # 남은 시간이 부족해 상담을 못하는 경우
    else:   # i + T[i] <= N
        D[i] = max(D[i + T[i]] + P[i], D[i + 1])    # 상담을 하는게 이득인지 안 하는게 이득인지

# print(*D, sep=', ')
print(D[0])
