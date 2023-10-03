import sys

problem_url = "https://boj.kr/1517"
problem_name = "버블 소트"
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))
swap = 0

def merge_sort(A, start, end):
	if start < end:
		mid = (start + end) // 2
		
		merge_sort(A, start, mid)
		merge_sort(A, mid + 1, end)
		merge(A, start, mid, end)

def merge(A, start, mid, end):
	global swap
	
	L = A[start:mid+1]
	R = A[mid+1:end+1]
	
	i = start
	l = r = 0
	
	# idea. L 대신 R을 A에 넣는 것이 곧 스왑
	#  - L의 l번째 인덱스까지 스왑을 해야 하므로 len(L) - l 이 스왑 횟수
	
	while l < len(L) and r < len(R):
		if L[l] <= R[r]:
			A[i] = L[l]
			l += 1
		else:
			A[i] = R[r]
			swap += len(L) - l
			r += 1
		i += 1
	
	while l < len(L):
		A[i] = L[l]
		l += 1
		i += 1
	
	while r < len(R):
		A[i] = R[r]
		r += 1
		i += 1

merge_sort(A, 0, n - 1)
print(swap)
