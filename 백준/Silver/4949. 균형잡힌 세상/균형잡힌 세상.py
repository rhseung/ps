import sys

problem_url = "https://boj.kr/4949"
problem_name = "균형잡힌 세상"
input = sys.stdin.readline

while True:
	query = input()[:-1]
	
	if query == '.':
		break
	
	B = []
	
	for c in query:
		if c == '(':
			B.append(c)
		elif c == ')':
			if B and B[-1] == '(':
				B.pop()
			else:
				B.append(c)
		elif c == '[':
			B.append(c)
		elif c == ']':
			if B and B[-1] == '[':
				B.pop()
			else:
				B.append(c)
	
	print('no' if B or B else 'yes')
