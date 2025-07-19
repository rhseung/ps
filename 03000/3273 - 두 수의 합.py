import sys

problem_url = "https://boj.kr/3273"
problem_name = "두 수의 합"
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))
x = int(input())

A.sort()
l, r = 0, len(A) - 1
cnt = 0

while l < r:
	if x > A[l] + A[r]:
		l += 1
	elif x < A[l] + A[r]:
		r -= 1
	else:
		cnt += 1
		l += 1

print(cnt)
