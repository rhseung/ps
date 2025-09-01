import sys

problem_url = "https://boj.kr/9935"
problem_name = "문자열 폭발"
input = sys.stdin.readline

query = list(input().strip())
expl = list(input().strip())

n_q = len(query)
n_e = len(expl)

stack = query[:n_e - 1]
for i in range(n_e - 1, n_q):
	stack.append(query[i])
	if len(stack) >= n_e and stack[-n_e:] == expl:
		# WC. stack = stack[:-n_e]
		del stack[-n_e:]    # 이건 폭발 문자열의 길이가 최대 36이라 최대 삭제 수가 36이라서 훨~씬 빠름

print('FRULA' if not stack else ''.join(stack))
