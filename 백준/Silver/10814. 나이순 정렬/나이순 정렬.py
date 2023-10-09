import sys

problem_url = "https://boj.kr/10814"
problem_name = "나이순 정렬"
input = sys.stdin.readline

n = int(input())
A = [input().split() for _ in range(n)]
for i in range(n):
	A[i][0] = int(A[i][0])

def merge_sort(A, s, e):
	if s < e:
		mid = (s + e) // 2
		merge_sort(A, s, mid)
		merge_sort(A, mid + 1, e)
		merge(A, s, mid, e)

def merge(A, s, m, e):
	L = A[s:m+1]
	R = A[m+1:e+1]
	
	n_L = len(L)
	n_R = len(R)
	
	i = s
	l, r = 0, 0
	while l < n_L and r < n_R:
		if L[l][0] <= R[r][0]:  # L, R이 같을 때도 포함해버리면 A에서의 인덱스는 늘 L이 R보다 작으니까 안정 정렬이 됨
			A[i] = L[l]
			l += 1
		else:
			A[i] = R[r]
			r += 1
		i += 1
	
	while l < n_L:
		A[i] = L[l]
		l += 1
		i += 1
	
	while r < n_R:
		A[i] = R[r]
		r += 1
		i += 1

merge_sort(A, 0, n - 1)
for a in A:
	print(*a)