__problem__ = 'https://boj.kr/11726', '2×n 타일링'

import sys

input = sys.stdin.readline

n = int(input())
m = 10007

D = [0] * n
D[0] = 1
if n > 1:
    D[1] = 2    # n = 1일 때 index error 남

for i in range(2, n):
    D[i] = (D[i - 1] + D[i - 2]) % m

print(D[n - 1])
