import sys

problem_url = "https://boj.kr/1546"
problem_name = "평균"
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))
print((sum(A) / len(A)) / max(A) * 100)
