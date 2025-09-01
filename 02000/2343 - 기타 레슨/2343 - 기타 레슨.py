__problem__ = 'https://boj.kr/2343', '기타 레슨'

import sys

input = sys.stdin.readline

n, m = map(int, input().split())
L = list(map(int, input().split()))

# 한 blueray당 capacity를 건네주면 총 blueray 개수를 반환하는 함수
def get_count_of_blueray(L, capacity):
    s = 0   
    count = 1

    for l in L:
        if s + l > capacity:
            count += 1
            s = 0
        s += l

    return count

i, j = max(L), sum(L)
# 블루레이당 최소 capacity는 가장 긴 레슨의 길이(1개 넣었을 때), 최대 capacity는 모든 레슨의 길이 합(다 넣었을 때)

result = -1

while i <= j:
    mid = (i + j) // 2
    count = get_count_of_blueray(L, mid)

    if count > m:
        i = mid + 1
    elif count <= m:
        result = mid
        j = mid - 1

print(result)
