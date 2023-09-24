import sys
from collections import deque

problem_url = "https://boj.kr/10989"
problem_name = "수 정렬하기 3"
input = sys.stdin.readline

n = int(input())
buckets = [0 for _ in range(10000)]

for _ in range(n):
	val = int(input())
	buckets[val - 1] += 1

for i in range(len(buckets)):
	for _ in range(buckets[i]):
		print(i + 1)

# WC. 메모리 초과
#  문제 조건에서 1 ≤ n ≤ 10,000,000 라서, 비둘기 집의 원리에 의해 적어도 한 버킷에 최소 1,000,000개의 요소가 들어감
#  - 버킷 개수를 늘려서 요소 개수를 줄인다
#  - 각 요소는 1 ≤ e ≤ 10,000 라서, 버킷을 10000개로 늘리면 최소 1000개
#  - 이렇게 되면 exp를 쓸 필요도, while 구문 자체가 필요가 없음
#  - 더 나아가서 하나의 버킷에 한 종류의 수만 들어가므로, 수를 저장할 필요가 없고, 그냥 개수만 저장하면 됨
#  - 아니 걍 A라는 배열도 필요가 없음

# radix_sort
# def radix_sort(A):
# 	exp = 1
# 	max_val = max(A)
# 	buckets = [deque() for _ in range(10)]
# 	q = deque(A)
#
# 	while exp <= max_val:
# 		while q:
# 			val = q.popleft()
# 			idx = (val // exp) % 10
# 			buckets[idx].append(val)
#
# 		for bucket in buckets:
# 			while bucket:
# 				q.append(bucket.popleft())
#
# 		exp *= 10
#
# 	return list(q)
