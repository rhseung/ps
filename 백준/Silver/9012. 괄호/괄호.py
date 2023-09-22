import sys

problem_url = "https://boj.kr/9012"
problem_name = "괄호"
input = sys.stdin.readline

n = int(input())
for _ in range(n):
	query = input().strip()
	
	stack = []
	for c in query:
		if c == ')' and (stack and stack[-1] == '('):
			stack.pop()
		else:
			stack.append(c)
		# print(stack)
	
	if stack:
		print("NO")
	else:
		print("YES")
