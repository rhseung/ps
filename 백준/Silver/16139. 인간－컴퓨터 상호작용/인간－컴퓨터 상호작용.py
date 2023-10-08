import sys
from collections import Counter

problem_url = "https://boj.kr/16139"
problem_name = "인간-컴퓨터 상호작용"
input = sys.stdin.readline

query = input().strip()
n = int(input().strip())

counters = [Counter(query[0])]
for i in range(1, len(query)):
	c = counters[i - 1].copy()
	c[query[i]] += 1
	counters.append(c)

empty = Counter()
for i in range(n):
	alphabet, l, r = input().split()
	l, r = int(l), int(r)
	
	count = counters[r] - (counters[l - 1] if l != 0 else empty)
	print(count[alphabet])
