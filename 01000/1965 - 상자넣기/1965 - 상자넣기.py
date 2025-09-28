# BOJ 1965 - 상자넣기
import sys
input = sys.stdin.readline

n = int(input())
A = list(map(int, input().split()))
DP = [1] * n

for i in range(n):
    for j in range(i):
        if A[j] < A[i]:
            DP[i] = max(DP[i], DP[j] + 1)

print(max(DP))