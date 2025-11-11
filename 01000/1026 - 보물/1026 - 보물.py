# BOJ 1026 - 보물
import sys

def input() -> str: return sys.stdin.readline().rstrip()

n = int(input())

A = list(map(int, input().split()))  # 1 1 1 6 0
B = list(enumerate(map(int, input().split())))  # 2 7 8 3 1

B.sort(key=lambda x: x[1])
A.sort(reverse=True)

print(sum(A[i] * B[i][1] for i in range(n)))
