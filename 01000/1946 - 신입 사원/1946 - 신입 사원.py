# BOJ 1946 - 신입 사원
import sys
def input() -> str: return sys.stdin.readline()

t = int(input())
for _ in range(t):
    n = int(input())
    A = [tuple(map(int, input().split())) for _ in range(n)]
    A.sort(key=lambda x: x[1])

    l = 1
    last = A[0][0]
    for i in range(1, n):
        if A[i][0] < last:
            last = A[i][0]
            l += 1

    print(l)