import sys

problem_url = "https://boj.kr/11660"
problem_name = "구간 합 구하기 4"
input = sys.stdin.readline

n, m = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(n)]
C = [[0 for _ in range(n + 1)] for _ in range(n + 1)]   # padding

for i in range(1, n + 1):
	for j in range(1, n + 1):
		C[i][j] = C[i - 1][j] + C[i][j - 1] - C[i - 1][j - 1] + A[i - 1][j - 1]     # A[i][j] 긴 한데, 패딩해서 1씩 밀림

for _ in range(m):
	x1, y1, x2, y2 = map(int, input().split())
	print(C[x2][y2] - C[x2][y1 - 1] - C[x1 - 1][y2] + C[x1 - 1][y1 - 1])
