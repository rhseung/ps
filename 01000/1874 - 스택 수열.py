import sys

problem_url = "https://boj.kr/1874"
problem_name = "스택 수열"
input = sys.stdin.readline

n = int(input())
S = []
ans = []

i = 1
for _ in range(1, n + 1):
	query = int(input())
	
	# 비어있는 S
	if not S or query >= i:
		while not S or query > S[-1]:
			S.append(i)
			ans.append('+')
			i += 1
		S.pop()
		ans.append('-')
	else:   # query < i
		val = S.pop()
		ans.append('-')
		if query > val:
			print('NO')
			exit()

for a in ans:
	print(a)
