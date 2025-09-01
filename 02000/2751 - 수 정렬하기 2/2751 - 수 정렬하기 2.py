import sys

problem_url = "https://boj.kr/2751"
problem_name = "수 정렬하기 2"
input = sys.stdin.readline

n = int(input())
A = []

for _ in range(n):
	A.append(int(input()))

def merge_sort(A, s, e):
	if s < e:
		mid = (s + e) // 2
		merge_sort(A, s, mid)
		merge_sort(A, mid + 1, e)
		merge(A, s, mid, e)

def merge(A, s, mid, e):
	L = A[s:mid+1]
	R = A[mid+1:e+1]
	
	i = j = 0
	k = s
	
	while i < len(L) and j < len(R):
		if L[i] < R[j]:
			A[k] = L[i]
			i += 1
		else:
			A[k] = R[j]
			j += 1
		k += 1
	
	while i < len(L):
		A[k] = L[i]
		i += 1
		k += 1
	
	while j < len(R):
		A[k] = R[j]
		j += 1
		k += 1

merge_sort(A, 0, n - 1)
for a in A:
	print(a)
