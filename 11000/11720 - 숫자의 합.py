import sys

problem_url = "https://boj.kr/11720"
problem_name = "숫자의 합"
input = sys.stdin.readline

n = int(input())
pile = int(input())

s = 0
while pile > 0:
	s += pile % 10
	pile //= 10
	
print(s)
