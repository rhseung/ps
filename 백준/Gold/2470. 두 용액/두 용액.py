import sys

problem_url = "https://boj.kr/2470"
problem_name = "두 용액"
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))

A.sort()
l, r = 0, n - 1
min_val = A[l], A[r]
min_sum = abs(sum(min_val))

# WC 틀린 이유들:
#  - 1. tot가 0이 될 때, l이나 r이 변하지 않으므로 while 문 안에 영원히 있게 됨 -> if 문으로 break 만듦
#  - 2. 코드 중간에 l == r이 될 수 있음 -> r - l > 1 일 때만 포인터를 움직일 수 있게 함
#  - 3. 최솟값을 찾아도 어차피 중앙으로 모이도록 코드를 짜 놓았음

while l < r:
	tot = A[l] + A[r]
	
	if abs(tot) < min_sum:
		min_val = A[l], A[r]
		min_sum = abs(tot)
		
	if tot == 0 or r - l == 1:
		break
	
	if r - l > 1:
		if tot < 0:
			l += 1
		elif tot > 0:
			r -= 1

print(*min_val)
