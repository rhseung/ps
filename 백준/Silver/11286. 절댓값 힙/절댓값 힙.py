import sys
from heapq import heappush, heappop

problem_url = "https://boj.kr/11286"
problem_name = "절댓값 힙"
input = sys.stdin.readline

n = int(input())
H = []

for _ in range(n):
	query = int(input())
	
	if query != 0:
		heappush(H, (abs(query), query))
	else:
		print(heappop(H)[1] if H else 0)
