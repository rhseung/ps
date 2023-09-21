import sys

problem_url = "https://boj.kr/2750"
problem_name = "수 정렬하기"
input = sys.stdin.readline

arr = []

n = int(input())
for _ in range(n):
	arr.append(int(input()))

# a, b는 call by value로 작동하므로 이 함수가 생각대로 될리가 없음
# def swap(a, b):
# 	"""
# 	swap(arr[j - 1], arr[j])
# 	"""
# 	a, b = b, a

# 이렇게 하면 되겠지
def swap(arr, i, j):
	arr[i], arr[j] = arr[j], arr[i]

def bubble_sort(arr):
	for i in range(len(arr)):
		for j in range(1, len(arr) - i):
			if arr[j - 1] > arr[j]:
				swap(arr, j - 1, j)
				
bubble_sort(arr)
for e in arr:
	print(e)
