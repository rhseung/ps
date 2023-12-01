__problem__ = 'https://boj.kr/2193', '이친수'

import sys

input = sys.stdin.readline

n = int(input())
D: list[list[int, int]] = [[0, 0] for _ in range(n + 1)]    # (0의 개수, 1의 개수)

# i
# 0 0 0
# 1 0 1
# 2 1 0
# 3 1 1
# 4 2 1
# 5 3 2
# 피보나치긴 함

D[1] = [0, 1]
for i in range(2, n + 1):
    # 0의 개수 = 전에 1로 끝나면 무조건 + 전에 0으로 끝나도 올 수 있음
    D[i][0] = D[i - 1][1] + D[i - 1][0]
    # 1의 개수 = 전에 0으로 끝난 거만 올 수 있음
    D[i][1] = D[i - 1][0]

print(sum(D[n]))
