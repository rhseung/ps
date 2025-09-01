import sys

problem_url = "https://boj.kr/11650"
problem_name = "좌표 정렬하기"
input = sys.stdin.readline

n = int(input())
D = [tuple(map(int, input().split())) for _ in range(n)]

def quick_sort(A, s, e):
	if s < e:
		p = partition(A, s, e)
		quick_sort(A, s, p - 1)
		quick_sort(A, p, e)

def partition(A, s, e):
	p = A[(s + e) // 2]
	l, r = s, e
	
	while l <= r:
		while l <= r and (A[l][1] < p[1] if A[l][0] == p[0] else A[l][0] < p[0]):
			l += 1
		while l <= r and (p[1] < A[r][1] if p[0] == A[r][0] else p[0] < A[r][0]):
			r -= 1
		if l <= r:
			A[l], A[r] = A[r], A[l]
			l += 1
			r -= 1
	
	return l

quick_sort(D, 0, len(D) - 1)

for dot in D:
	print(dot[0], dot[1])
