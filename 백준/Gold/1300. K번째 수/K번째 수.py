__problem__ = 'https://boj.kr/1300', 'K번째 수'

import sys

input = sys.stdin.readline

n = int(input())
k = int(input())

def get_k(x):
    ret = 0

    for divisor in range(1, n + 1):
        ret += min(n, x // divisor)     # 작거나 같은 개수를 각 행에 대해 구하기

    return ret

# 어차피 0 <= x <= k 임 항상
# 문제는 B[k] = x를 구하라고 함
i, j = 1, k
result = -1

while i <= j:
    mid = (i + j) // 2
    mid_k = get_k(mid)

    if mid_k < k:
        i = mid + 1
    else:
        result = mid
        j = mid - 1

print(result)
