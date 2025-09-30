# BOJ 1309 - 동물원
import sys
input = sys.stdin.readline

n = int(input())
m = 9901

# Left, Right, None
L = [0] * n
R = [0] * n
N = [0] * n

L[0] = 1
R[0] = 1
N[0] = 1

for i in range(1, n):
    L[i] = (N[i - 1] + R[i - 1]) % m
    R[i] = (N[i - 1] + L[i - 1]) % m
    N[i] = (L[i - 1] + R[i - 1] + N[i - 1]) % m

print((L[n - 1] + R[n - 1] + N[n - 1]) % m)
