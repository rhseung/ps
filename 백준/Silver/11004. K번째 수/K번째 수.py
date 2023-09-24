import sys

problem_url = "https://boj.kr/11004"
problem_name = "K번째 수"
input = sys.stdin.readline

n, k = map(int, input().split())
A = list(map(int, input().split()))

# quick sort
# WC. quick sort 최적화 엄청 해야해서 이건 그냥 스킵
# def quick_sort(A, s, e):
# 	if s < e:
# 		pivot = partition(A, s, e)
# 		quick_sort(A, s, pivot - 1)
# 		quick_sort(A, pivot + 1, e)
#
# def partition(A, s, e) -> int:
# 	pivot = s
# 	left, right = s + 1, e
#
# 	while left <= right:
# 		while left <= right and A[left] <= A[pivot]:
# 			left += 1
#
# 		while left <= right and A[pivot] <= A[right]:
# 			right -= 1
#
# 		if left < right:
# 			A[left], A[right] = A[right], A[left]
# 			left += 1
# 			right -= 1
#
# 	A[pivot], A[right] = A[right], A[pivot]
#
# 	return right
#
#
# quick_sort(A, 0, n - 1)

A.sort()
print(A[k - 1])
