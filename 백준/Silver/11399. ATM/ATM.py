import sys

problem_url = "https://boj.kr/11399"
problem_name = "ATM"
input = sys.stdin.readline

n = int(input())
times = list(map(int, input().split()))

# 삽입 정렬
for i in range(1, n):
	for j in range(i - 1, -1, -1):
		if times[j] > times[j + 1]:
			times[j], times[j + 1] = times[j + 1], times[j]

cum = [0 for _ in range(n)]
for i in range(n):
	cum[i] = (0 if i == 0 else cum[i - 1]) + times[i]

print(sum(cum))
