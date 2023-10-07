import sys
from collections import Counter

problem_url = "https://boj.kr/17299"
problem_name = "오등큰수"
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))

stack = [0]
F = Counter(A)
NGF = [-1 for _ in range(n)]

for i in range(1, n):
	while stack and F[A[stack[-1]]] < F[A[i]]:
		idx = stack.pop()
		NGF[idx] = A[i]
	
	stack.append(i)

for e in NGF:
	print(e, end=' ')
