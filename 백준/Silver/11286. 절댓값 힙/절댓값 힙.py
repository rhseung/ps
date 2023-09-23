import sys
from heapq import heappush, heappop

problem_url = "https://boj.kr/11286"
problem_name = "절댓값 힙"
input = sys.stdin.readline

n = int(input())
prior_q = []

for _ in range(n):
	cmd = int(input())
	
	if cmd != 0:
		# 우선순위 큐에 데이터가 [a, b, c, d, ...] 이런 구조라면, 우선순위 큐는 pop 할 때,
		# a의 오름차순, a가 같으면 b의 오름차순, ... 순서로 정렬한다
		heappush(prior_q, (abs(cmd), cmd))
	else:
		if prior_q:
			print(heappop(prior_q)[1])
		else:
			print(0)
