# BOJ 2011 - 암호코드
import sys
input = sys.stdin.readline

P = list(map(int, list(input().strip())))
n = len(P)
DP = [0] * n
m = 1000000

def isalpha(c: int) -> bool:
    return 1 <= c <= 26

def isalpha2(a: int, b: int) -> bool:
    # 08 같은 건 안됨
    return a > 0 and isalpha(a * 10 + b)

DP[0] = 0
if isalpha(P[0]):
    DP[0] += 1

if n > 1:
    DP[1] = 0
    if isalpha2(P[0], P[1]):
        DP[1] += 1
    if isalpha(P[1]):
        DP[1] += 1

for i in range(2, n):
    DP[i] = 0
    if isalpha2(P[i - 1], P[i]):
        DP[i] = (DP[i] + DP[i - 2]) % m
    if isalpha(P[i]):
        DP[i] = (DP[i] + DP[i - 1]) % m

for i in range(n):
    if DP[i] == 0:
        print(0)
        exit()

# print(DP)
print(DP[n - 1] % m)