import sys

problem_url = "https://boj.kr/11659"
problem_name = "구간 합 구하기 4"
input = sys.stdin.readline

n, m = map(int, input().split())
A = list(map(int, input().split()))
C = [0 for _ in range(n + 1)]   # padding

for i in range(1, n + 1):
	C[i] = C[i - 1] + A[i - 1]

for _ in range(m):
	x1, x2 = map(int, input().split())
	print(C[x2] - C[x1 - 1])
