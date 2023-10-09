import sys
from collections import deque

problem_url = "https://boj.kr/12789"
problem_name = "도키도키 간식드리미"
input = sys.stdin.readline

n = int(input())
S = []
Q = deque(map(int, input().split()))

# WC. 1 3 2 4 처럼 중간에 스택에서 내보낼 수도 있음

now = 1
while now <= n:
	if S and S[-1] == now:
		S.pop()
		now += 1
	elif Q and Q[0] == now:
		Q.popleft()
		now += 1
	elif S and not Q:   # 위의 두 조건문을 만족하지 않아 라인을 통과할 수 없는데, S는 채워져 있고 Q는 비어 있다면 이건 Sad
		print('Sad')
		break
	elif Q:     # 이미 들어있는 S를 pop 하면서 라인을 통과하는 경우가 연속될 수가 있으니까 else에 넣어줌
		S.append(Q.popleft())
	
if not Q and not S:
	print('Nice')
