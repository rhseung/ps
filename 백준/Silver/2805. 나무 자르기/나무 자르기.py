__problem__ = 'https://boj.kr/2805', '나무 자르기'

import sys

input = sys.stdin.readline

n, key = map(int, input().split())
H = list(map(int, input().split()))

H.sort()

def get_logs(H, height):
    return sum(max(0, h - height) for h in H)

result = 0
i, j = 0, H[-1]

while i <= j:
    mid = (i + j) // 2
    logs = get_logs(H, mid)

    if logs >= key:  # 너무 많이 잘랐으면 높이를 올려야지, 또는 적절히 자른 경우에는 최대 높이를 구해야지
        result = mid
        i = mid + 1
    else:   # 너무 적게 잘랐으면 높이를 내려야지
        j = mid - 1

print(result)
