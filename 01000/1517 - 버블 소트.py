import sys

problem_url = "https://boj.kr/1517"
problem_name = "버블 소트"
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))

cnt = 0

def merge_sort(A, s, e):
	if s < e:
		m = (s + e) // 2
		merge_sort(A, s, m)
		merge_sort(A, m + 1, e)
		merge(A, s, m, e)

def merge(A, s, m, e):
	global cnt
	
	L = A[s:m+1]
	R = A[m+1:e+1]
	
	n_L, n_R = len(L), len(R)
	l, r = 0, 0
	i = s
	
	while l < n_L and r < n_R:
		if L[l] <= R[r]:
			A[i] = L[l]
			l += 1
		else:
			A[i] = R[r]
			r += 1
			cnt += n_L - l
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
print(cnt)
