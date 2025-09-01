import sys

problem_url = "https://boj.kr/1427"
problem_name = "소트인사이드"
input = sys.stdin.readline

# 선택 정렬
A = list(input().strip())

for i in range(len(A)):
	max_idx = i
	
	for j in range(max_idx, len(A)):
		if A[max_idx] < A[j]:
			max_idx = j
	
	A[i], A[max_idx] = A[max_idx], A[i]

for a in A:
	print(a, end='')
