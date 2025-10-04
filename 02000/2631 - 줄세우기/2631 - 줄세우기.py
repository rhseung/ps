# BOJ 2631 - 줄세우기
import sys
def input() -> str: return sys.stdin.readline()

n = int(input())
A = [int(input()) for _ in range(n)]

DP = [1] * n
for i in range(n):
  for j in range(i):
    if A[j] < A[i]:
      DP[i] = max(DP[j] + 1, DP[i])
      
print(n - max(DP))