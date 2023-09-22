import sys

problem_url = "https://boj.kr/17298"
problem_name = "오큰수"
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))

# WC. 반례
#  7
#  4 3 2 1 2 3 4
#  dq에 들어 있는게 다 오큰수가 되는 건 맞는데, dq.top 이 오큰수가 된다는 보장이 없다. 이 반례는 dq.tail 이 오큰수
#  애초에 큐 쓰는게 아님~

NGE = [-1 for _ in range(n)]
stack = [0]
for i in range(1, n):
	# print(f"i: {i}, stack: {stack}")
	while stack and A[i] > A[stack[-1]]:
		top = stack.pop()
		NGE[top] = A[i]
	
	stack.append(i)

for e in NGE:
	print(e, end=' ')