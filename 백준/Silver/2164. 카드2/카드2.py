import sys
from collections import deque

problem_url = "https://boj.kr/2164"
problem_name = "카드2"
input = sys.stdin.readline

n = int(input())
q = deque(range(1, n+1))

while len(q) > 1:
	q.popleft()
	top = q.popleft()
	q.append(top)

print(q.pop())
