import sys
from collections import Counter

problem_url = "https://boj.kr/16139"
problem_name = "인간-컴퓨터 상호작용"
input = sys.stdin.readline

query = input().strip()
n = int(input().strip())

counts = {}
for c in 'abcdefghijklmnopqrstuvwxyz':
	counts[c] = [0 if query[0] != c else 1]

for i in range(n):
	alphabet, l, r = input().split()
	l, r = int(l), int(r)
	
	if len(counts[alphabet]) == 1:
		for j in range(1, len(query)):
			counts[alphabet].append(counts[alphabet][j - 1] + (1 if query[j] == alphabet else 0))
	
	count = counts[alphabet][r] - (counts[alphabet][l - 1] if l != 0 else 0)
	print(count)
