import sys
from collections import deque

problem_url = "https://boj.kr/11003"
problem_name = "최솟값 찾기"
input = sys.stdin.readline

n, l = map(int, input().split())
A = list(map(int, input().split()))
D = deque()

for i in range(n):
	val = (i, A[i])
	
	while D and D[-1][1] > val[1]:
		D.pop()
	
	while D and D[0][0] <= i - l:
		D.popleft()
	
	D.append(val)
	print(D[0][1], end=' ')
